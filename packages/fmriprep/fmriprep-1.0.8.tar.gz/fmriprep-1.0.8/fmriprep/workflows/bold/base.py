# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Orchestrating the BOLD-preprocessing workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: init_func_preproc_wf
.. autofunction:: init_func_reports_wf
.. autofunction:: init_func_derivatives_wf

"""

import os

import nibabel as nb
from niworkflows.nipype import logging

from niworkflows.nipype.interfaces.fsl import Split as FSLSplit
from niworkflows.nipype.pipeline import engine as pe
from niworkflows.nipype.interfaces import utility as niu

from ...interfaces import (
    DerivativesDataSink,
    GiftiNameSource
)

from ...interfaces.reports import FunctionalSummary

# Fieldmap workflows
from ..fieldmap import (
    init_pepolar_unwarp_wf,
    init_nonlinear_sdc_wf,
    init_fmap_unwarp_report_wf
)

# BOLD workflows
from .confounds import init_bold_confs_wf
from .hmc import init_bold_hmc_wf
from .stc import init_bold_stc_wf
from .t2s import init_bold_t2s_wf
from .registration import init_bold_reg_wf
from .resampling import (
    init_bold_surf_wf,
    init_bold_mni_trans_wf,
    init_bold_preproc_trans_wf,
    init_bold_preproc_report_wf,
)
from .util import init_bold_reference_wf

DEFAULT_MEMORY_MIN_GB = 0.01
LOGGER = logging.getLogger('workflow')


def init_func_preproc_wf(bold_file, ignore, freesurfer,
                         use_bbr, t2s_coreg, bold2t1w_dof, reportlets_dir,
                         output_spaces, template, output_dir, omp_nthreads,
                         fmap_bspline, fmap_demean, use_syn, force_syn,
                         use_aroma, ignore_aroma_err, medial_surface_nan,
                         debug, low_mem, output_grid_ref, layout=None):
    """
    This workflow controls the functional preprocessing stages of FMRIPREP.

    .. workflow::
        :graph2use: orig
        :simple_form: yes

        from fmriprep.workflows.bold import init_func_preproc_wf
        wf = init_func_preproc_wf('/completely/made/up/path/sub-01_task-nback_bold.nii.gz',
                                  omp_nthreads=1,
                                  ignore=[],
                                  freesurfer=True,
                                  reportlets_dir='.',
                                  output_dir='.',
                                  template='MNI152NLin2009cAsym',
                                  output_spaces=['T1w', 'fsnative',
                                                 'template', 'fsaverage5'],
                                  debug=False,
                                  use_bbr=True,
                                  t2s_coreg=False,
                                  bold2t1w_dof=9,
                                  fmap_bspline=True,
                                  fmap_demean=True,
                                  use_syn=True,
                                  force_syn=True,
                                  low_mem=False,
                                  output_grid_ref=None,
                                  medial_surface_nan=False,
                                  use_aroma=False,
                                  ignore_aroma_err=False)

    **Parameters**

        bold_file : str
            BOLD series NIfTI file
        ignore : list
            Preprocessing steps to skip (may include "slicetiming", "fieldmaps")
        freesurfer : bool
            Enable FreeSurfer functional registration (bbregister) and resampling
            BOLD series to FreeSurfer surface meshes.
        use_bbr : bool or None
            Enable/disable boundary-based registration refinement.
            If ``None``, test BBR result for distortion before accepting.
        t2s_coreg : bool
            Use multiple BOLD echos to create T2*-map for T2*-driven coregistration
        bold2t1w_dof : 6, 9 or 12
            Degrees-of-freedom for BOLD-T1w registration
        reportlets_dir : str
            Directory in which to save reportlets
        output_spaces : list
            List of output spaces functional images are to be resampled to.
            Some parts of pipeline will only be instantiated for some output spaces.

            Valid spaces:

                - T1w
                - template
                - fsnative
                - fsaverage (or other pre-existing FreeSurfer templates)
        template : str
            Name of template targeted by `'template'` output space
        output_dir : str
            Directory in which to save derivatives
        omp_nthreads : int
            Maximum number of threads an individual process may use
        fmap_bspline : bool
            **Experimental**: Fit B-Spline field using least-squares
        fmap_demean : bool
            Demean voxel-shift map during unwarp
        use_syn : bool
            **Experimental**: Enable ANTs SyN-based susceptibility distortion correction (SDC).
            If fieldmaps are present and enabled, this is not run, by default.
        force_syn : bool
            **Temporary**: Always run SyN-based SDC
        use_aroma : bool
            Perform ICA-AROMA on MNI-resampled functional series
        ignore_aroma_err : bool
            Do not fail on ICA-AROMA errors
        medial_surface_nan : bool
            Replace medial wall values with NaNs on functional GIFTI files
        debug : bool
            Enable debugging outputs
        low_mem : bool
            Write uncompressed .nii files in some cases to reduce memory usage
        output_grid_ref : str or None
            Path of custom reference image for normalization
        layout : BIDSLayout
            BIDSLayout structure to enable metadata retrieval

    **Inputs**

        bold_file
            BOLD series NIfTI file
        t1_preproc
            Bias-corrected structural template image
        t1_brain
            Skull-stripped ``t1_preproc``
        t1_mask
            Mask of the skull-stripped template image
        t1_seg
            Segmentation of preprocessed structural image, including
            gray-matter (GM), white-matter (WM) and cerebrospinal fluid (CSF)
        t1_tpms
            List of tissue probability maps in T1w space
        t1_2_mni_forward_transform
            ANTs-compatible affine-and-warp transform file
        t1_2_mni_reverse_transform
            ANTs-compatible affine-and-warp transform file (inverse)
        subjects_dir
            FreeSurfer SUBJECTS_DIR
        subject_id
            FreeSurfer subject ID
        t1_2_fsnative_forward_transform
            LTA-style affine matrix translating from T1w to FreeSurfer-conformed subject space
        t1_2_fsnative_reverse_transform
            LTA-style affine matrix translating from FreeSurfer-conformed subject space to T1w


    **Outputs**

        bold_t1
            BOLD series, resampled to T1w space
        bold_mask_t1
            BOLD series mask in T1w space
        bold_mni
            BOLD series, resampled to template space
        bold_mask_mni
            BOLD series mask in template space
        confounds
            TSV of confounds
        surfaces
            BOLD series, resampled to FreeSurfer surfaces
        aroma_noise_ics
            Noise components identified by ICA-AROMA
        melodic_mix
            FSL MELODIC mixing matrix


    **Subworkflows**

        * :py:func:`~fmriprep.workflows.bold.util.init_bold_reference_wf`
        * :py:func:`~fmriprep.workflows.bold.stc.init_bold_stc_wf`
        * :py:func:`~fmriprep.workflows.bold.hmc.init_bold_hmc_wf`
        * :py:func:`~fmriprep.workflows.bold.t2s.init_bold_t2s_wf`
        * :py:func:`~fmriprep.workflows.bold.registration.init_bold_reg_wf`
        * :py:func:`~fmriprep.workflows.bold.confounds.init_bold_confounds_wf`
        * :py:func:`~fmriprep.workflows.bold.confounds.init_ica_aroma_wf`
        * :py:func:`~fmriprep.workflows.bold.resampling.init_bold_mni_trans_wf`
        * :py:func:`~fmriprep.workflows.bold.resampling.init_bold_preproc_trans_wf`
        * :py:func:`~fmriprep.workflows.bold.resampling.init_bold_surf_wf`
        * :py:func:`~fmriprep.workflows.fieldmap.pepolar.init_pepolar_unwarp_wf`
        * :py:func:`~fmriprep.workflows.fieldmap.init_fmap_estimator_wf`
        * :py:func:`~fmriprep.workflows.fieldmap.init_sdc_unwarp_wf`
        * :py:func:`~fmriprep.workflows.fieldmap.init_nonlinear_sdc_wf`

    """

    if bold_file == '/completely/made/up/path/sub-01_task-nback_bold.nii.gz':
        mem_gb = {'filesize': 1, 'resampled': 1, 'largemem': 1}
        bold_tlen = 10
        ref_file = bold_file
    else:
        if isinstance(bold_file, list):  # if multi-echo data
            ref_file = bold_file[0]
        else:
            ref_file = bold_file

        bold_tlen, mem_gb = _create_mem_gb(ref_file)

    wf_name = _get_wf_name(ref_file)
    LOGGER.log(25, ('Creating bold processing workflow for "%s" (%.2f GB / %d TRs). '
                    'Memory resampled/largemem=%.2f/%.2f GB.'),
               ref_file, mem_gb['filesize'], bold_tlen, mem_gb['resampled'], mem_gb['largemem'])

    # For doc building purposes
    if layout is None or bold_file == 'bold_preprocesing':

        LOGGER.log(25, 'No valid layout: building empty workflow.')
        metadata = {"RepetitionTime": 2.0,
                    "SliceTiming": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}
        fmaps = [{
            'type': 'phasediff',
            'phasediff': 'sub-03/ses-2/fmap/sub-03_ses-2_run-1_phasediff.nii.gz',
            'magnitude1': 'sub-03/ses-2/fmap/sub-03_ses-2_run-1_magnitude1.nii.gz',
            'magnitude2': 'sub-03/ses-2/fmap/sub-03_ses-2_run-1_magnitude2.nii.gz'
        }]
        run_stc = True
        bold_pe = 'j'
    else:
        if isinstance(bold_file, list):  # For multiecho data, grab TEs
            tes = [layout.get_metadata(echo)['EchoTime'] for echo in bold_file]
        # Since all other metadata is constant
        metadata = layout.get_metadata(ref_file)

        # Find fieldmaps. Options: (phase1|phase2|phasediff|epi|fieldmap)
        fmaps = layout.get_fieldmap(bold_file, return_list=True) \
            if 'fieldmaps' not in ignore else []

        # Short circuits: (True and True and (False or 'TooShort')) == 'TooShort'
        run_stc = ("SliceTiming" in metadata and
                   'slicetiming' not in ignore and
                   (_get_series_len(bold_file) > 4 or "TooShort"))
        bold_pe = metadata.get("PhaseEncodingDirection")

    # TODO: To be removed (supported fieldmaps):
    if not set([fmap['type'] for fmap in fmaps]).intersection(['phasediff', 'fieldmap', 'epi']):
        fmaps = None

    # Run SyN if forced or in the absence of fieldmap correction
    use_syn = force_syn or (use_syn and not fmaps)

    # Build workflow
    workflow = pe.Workflow(name=wf_name)
    inputnode = pe.Node(niu.IdentityInterface(
        fields=['bold_file', 'subjects_dir', 'subject_id',
                't1_preproc', 't1_brain', 't1_mask', 't1_seg', 't1_tpms',
                't1_aseg', 't1_aparc',
                't1_2_mni_forward_transform', 't1_2_mni_reverse_transform',
                't1_2_fsnative_forward_transform', 't1_2_fsnative_reverse_transform']),
        name='inputnode')

    if isinstance(bold_file, list):
        inputnode.inputs.iterables = ("bold_file", bold_file)
    else:
        inputnode.inputs.bold_file = bold_file

    outputnode = pe.Node(niu.IdentityInterface(
        fields=['bold_t1', 'bold_mask_t1', 'bold_aseg_t1', 'bold_aparc_t1',
                'bold_mni', 'bold_mask_mni', 'confounds', 'surfaces',
                't2s_map', 'aroma_noise_ics', 'melodic_mix', 'nonaggr_denoised_file']),
        name='outputnode')

    # BOLD buffer: an identity used as a pointer to either the original BOLD
    # or the STC'ed one for further use.
    boldbuffer = pe.Node(niu.IdentityInterface(fields=['bold_file']), name='boldbuffer')

    summary = pe.Node(
        FunctionalSummary(output_spaces=output_spaces,
                          slice_timing=run_stc,
                          registration='FreeSurfer' if freesurfer else 'FSL',
                          registration_dof=bold2t1w_dof,
                          pe_direction=bold_pe),
        name='summary', mem_gb=DEFAULT_MEMORY_MIN_GB, run_without_submitting=True)

    func_reports_wf = init_func_reports_wf(reportlets_dir=reportlets_dir,
                                           freesurfer=freesurfer,
                                           use_aroma=use_aroma,
                                           use_syn=use_syn)

    func_derivatives_wf = init_func_derivatives_wf(output_dir=output_dir,
                                                   output_spaces=output_spaces,
                                                   template=template,
                                                   freesurfer=freesurfer,
                                                   use_aroma=use_aroma)

    workflow.connect([
        (inputnode, func_reports_wf, [('bold_file', 'inputnode.source_file')]),
        (inputnode, func_derivatives_wf, [('bold_file', 'inputnode.source_file')]),
        (outputnode, func_derivatives_wf, [
            ('bold_t1', 'inputnode.bold_t1'),
            ('bold_aseg_t1', 'inputnode.bold_aseg_t1'),
            ('bold_aparc_t1', 'inputnode.bold_aparc_t1'),
            ('bold_mask_t1', 'inputnode.bold_mask_t1'),
            ('bold_mni', 'inputnode.bold_mni'),
            ('bold_mask_mni', 'inputnode.bold_mask_mni'),
            ('confounds', 'inputnode.confounds'),
            ('surfaces', 'inputnode.surfaces'),
            ('aroma_noise_ics', 'inputnode.aroma_noise_ics'),
            ('melodic_mix', 'inputnode.melodic_mix'),
            ('nonaggr_denoised_file', 'inputnode.nonaggr_denoised_file'),
        ]),
    ])

    # The first reference uses T2 contrast enhancement
    bold_reference_wf = init_bold_reference_wf(
        omp_nthreads=omp_nthreads, enhance_t2=True)

    # Top-level BOLD splitter
    bold_split = pe.Node(FSLSplit(dimension='t'), name='bold_split',
                         mem_gb=mem_gb['filesize'] * 3)

    # HMC on the BOLD
    bold_hmc_wf = init_bold_hmc_wf(name='bold_hmc_wf',
                                   mem_gb=mem_gb['filesize'],
                                   omp_nthreads=omp_nthreads)

    # if doing T2*-driven coregistration, create T2* map
    if t2s_coreg is True:
        bold_t2s_wf = init_bold_t2s_wf(echo_times=tes,
                                       name='bold_t2s_wf',
                                       mem_gb=mem_gb['filesize'],
                                       omp_nthreads=omp_nthreads)

    # mean BOLD registration to T1w
    bold_reg_wf = init_bold_reg_wf(name='bold_reg_wf',
                                   freesurfer=freesurfer,
                                   use_bbr=use_bbr,
                                   bold2t1w_dof=bold2t1w_dof,
                                   mem_gb=mem_gb['resampled'],
                                   omp_nthreads=omp_nthreads,
                                   use_compression=False,
                                   use_fieldwarp=(fmaps is not None or use_syn))

    # get confounds
    bold_confounds_wf = init_bold_confs_wf(
        mem_gb=mem_gb['largemem'],
        metadata=metadata,
        name='bold_confounds_wf')
    bold_confounds_wf.get_node('inputnode').inputs.t1_transform_flags = [False]

    # Apply transforms in 1 shot
    # Only use uncompressed output if AROMA is to be run
    bold_bold_trans_wf = init_bold_preproc_trans_wf(
        mem_gb=mem_gb['resampled'],
        omp_nthreads=omp_nthreads,
        use_compression=not low_mem,
        use_fieldwarp=(fmaps is not None or use_syn),
        name='bold_bold_trans_wf'
    )

    # SLICE-TIME CORRECTION (or bypass) #############################################
    if run_stc is True:  # bool('TooShort') == True, so check True explicitly
        bold_stc_wf = init_bold_stc_wf(name='bold_stc_wf', metadata=metadata)
        workflow.connect([
            (bold_stc_wf, boldbuffer, [('outputnode.stc_file', 'bold_file')]),
            (bold_reference_wf, bold_stc_wf, [('outputnode.bold_file', 'inputnode.bold_file'),
                                              ('outputnode.skip_vols', 'inputnode.skip_vols')]),
        ])
    else:  # bypass STC from original BOLD to the splitter through boldbuffer
        workflow.connect([
            (bold_reference_wf, boldbuffer, [
                ('outputnode.bold_file', 'bold_file')]),
        ])

    # MAIN WORKFLOW STRUCTURE #######################################################
    workflow.connect([
        # BOLD buffer has slice-time corrected if it was run, original otherwise
        (boldbuffer, bold_split, [('bold_file', 'in_file')]),
        # Generate early reference
        (inputnode, bold_reference_wf, [('bold_file', 'inputnode.bold_file')]),
        (bold_reference_wf, bold_hmc_wf, [
            ('outputnode.raw_ref_image', 'inputnode.raw_ref_image'),
            ('outputnode.bold_file', 'inputnode.bold_file')]),
        (bold_reference_wf, func_reports_wf, [
            ('outputnode.validation_report', 'inputnode.validation_report')]),
        # EPI-T1 registration workflow
        (inputnode, bold_reg_wf, [
            ('bold_file', 'inputnode.name_source'),
            ('t1_preproc', 'inputnode.t1_preproc'),
            ('t1_brain', 'inputnode.t1_brain'),
            ('t1_mask', 'inputnode.t1_mask'),
            ('t1_seg', 'inputnode.t1_seg'),
            ('t1_aseg', 'inputnode.t1_aseg'),
            ('t1_aparc', 'inputnode.t1_aparc'),
            # Undefined if --no-freesurfer, but this is safe
            ('subjects_dir', 'inputnode.subjects_dir'),
            ('subject_id', 'inputnode.subject_id'),
            ('t1_2_fsnative_reverse_transform', 'inputnode.t1_2_fsnative_reverse_transform')]),
        (bold_split, bold_reg_wf, [('out_files', 'inputnode.bold_split')]),
        (bold_hmc_wf, bold_reg_wf, [('outputnode.xforms', 'inputnode.hmc_xforms')]),
        (bold_reg_wf, func_reports_wf, [
            ('outputnode.out_report', 'inputnode.bold_reg_report'),
            ('outputnode.fallback', 'inputnode.bold_reg_fallback'),
        ]),
        (bold_reg_wf, outputnode, [('outputnode.bold_t1', 'bold_t1'),
                                   ('outputnode.bold_aseg_t1', 'bold_aseg_t1'),
                                   ('outputnode.bold_aparc_t1', 'bold_aparc_t1')]),
        (bold_reg_wf, summary, [('outputnode.fallback', 'fallback')]),
        # Connect bold_confounds_wf
        (inputnode, bold_confounds_wf, [('t1_tpms', 'inputnode.t1_tpms'),
                                        ('t1_mask', 'inputnode.t1_mask')]),
        (bold_hmc_wf, bold_confounds_wf, [
            ('outputnode.movpar_file', 'inputnode.movpar_file')]),
        (bold_reg_wf, bold_confounds_wf, [
            ('outputnode.itk_t1_to_bold', 'inputnode.t1_bold_xform')]),
        (bold_confounds_wf, func_reports_wf, [
            ('outputnode.rois_report', 'inputnode.bold_rois_report')]),
        (bold_confounds_wf, outputnode, [
            ('outputnode.confounds_file', 'confounds'),
        ]),
        # Connect bold_bold_trans_wf
        (inputnode, bold_bold_trans_wf, [
            ('bold_file', 'inputnode.name_source')]),
        (bold_split, bold_bold_trans_wf, [
            ('out_files', 'inputnode.bold_split')]),
        (bold_hmc_wf, bold_bold_trans_wf, [
            ('outputnode.xforms', 'inputnode.hmc_xforms')]),
        (bold_bold_trans_wf, bold_confounds_wf, [
            ('outputnode.bold', 'inputnode.bold'),
            ('outputnode.bold_mask', 'inputnode.bold_mask')]),
        # Summary
        (outputnode, summary, [('confounds', 'confounds_file')]),
        (summary, func_reports_wf, [('out_report', 'inputnode.summary_report')]),
    ])

    # FIELDMAPS ################################################################
    # Table of behavior is now found under workflows/fieldmap/base.py

    # Predefine to pacify the lintian checks about
    # "could be used before defined" - logic was tested to be sound
    nonlinear_sdc_wf = sdc_unwarp_wf = None

    if fmaps:
        # In case there are multiple fieldmaps prefer EPI
        fmaps.sort(key=lambda fmap: {'epi': 0, 'fieldmap': 1, 'phasediff': 2}[fmap['type']])
        fmap = fmaps[0]

        LOGGER.log(25, 'Fieldmap estimation: type "%s" found', fmap['type'])
        summary.inputs.distortion_correction = fmap['type']

        if fmap['type'] == 'epi':
            epi_fmaps = [fmap_['epi'] for fmap_ in fmaps if fmap_['type'] == 'epi']
            sdc_unwarp_wf = init_pepolar_unwarp_wf(fmaps=epi_fmaps,
                                                   layout=layout,
                                                   bold_file=bold_file,
                                                   omp_nthreads=omp_nthreads,
                                                   name='pepolar_unwarp_wf')
        else:
            # Import specific workflows here, so we don't brake everything with one
            # unused workflow.
            from ..fieldmap import init_fmap_estimator_wf, init_sdc_unwarp_wf
            fmap_estimator_wf = init_fmap_estimator_wf(fmap_bids=fmap,
                                                       reportlets_dir=reportlets_dir,
                                                       omp_nthreads=omp_nthreads,
                                                       fmap_bspline=fmap_bspline)
            sdc_unwarp_wf = init_sdc_unwarp_wf(reportlets_dir=reportlets_dir,
                                               omp_nthreads=omp_nthreads,
                                               fmap_bspline=fmap_bspline,
                                               fmap_demean=fmap_demean,
                                               debug=debug,
                                               name='sdc_unwarp_wf')
            workflow.connect([
                (fmap_estimator_wf, sdc_unwarp_wf, [
                    ('outputnode.fmap', 'inputnode.fmap'),
                    ('outputnode.fmap_ref', 'inputnode.fmap_ref'),
                    ('outputnode.fmap_mask', 'inputnode.fmap_mask')]),
            ])

        # Connections and workflows common for all types of fieldmaps
        workflow.connect([
            (inputnode, sdc_unwarp_wf, [('bold_file', 'inputnode.name_source')]),
            (bold_reference_wf, sdc_unwarp_wf, [
                ('outputnode.ref_image', 'inputnode.in_reference'),
                ('outputnode.ref_image_brain', 'inputnode.in_reference_brain'),
                ('outputnode.bold_mask', 'inputnode.in_mask')]),
            (sdc_unwarp_wf, bold_reg_wf, [
                ('outputnode.out_warp', 'inputnode.fieldwarp'),
                ('outputnode.out_reference_brain', 'inputnode.ref_bold_brain'),
                ('outputnode.out_mask', 'inputnode.ref_bold_mask')]),
        ])

        # Report on BOLD correction
        fmap_unwarp_report_wf = init_fmap_unwarp_report_wf(reportlets_dir=reportlets_dir,
                                                           name='fmap_unwarp_report_wf')
        workflow.connect([
            (inputnode, fmap_unwarp_report_wf, [
                ('t1_seg', 'inputnode.in_seg'),
                ('bold_file', 'inputnode.name_source')]),
            (bold_reference_wf, fmap_unwarp_report_wf, [
                ('outputnode.ref_image', 'inputnode.in_pre')]),
            (sdc_unwarp_wf, fmap_unwarp_report_wf, [
                ('outputnode.out_reference', 'inputnode.in_post')]),
            (bold_reg_wf, fmap_unwarp_report_wf, [
                ('outputnode.itk_t1_to_bold', 'inputnode.in_xfm')]),
        ])
    elif not use_syn:
        if t2s_coreg is True:
            workflow.connect([
                (bold_split, bold_t2s_wf, [
                    ('outfiles', 'inputnode.echo_split')]),
                (bold_hmc_wf, bold_t2s_wf, [
                    ('outputnode.xforms', 'inputnode.xforms')]),
                (bold_t2s_wf, bold_reg_wf, [
                    ('outputnode.t2s_map', 'inputnode.ref_bold_brain'),
                    ('outputnode.t2s_mask', 'inputnode.ref_bold_mask')])
            ])
        else:
            LOGGER.warning('No fieldmaps found or they were ignored, building base workflow '
                           'for dataset %s.', ref_file)
            summary.inputs.distortion_correction = 'None'

            workflow.connect([
                (bold_reference_wf, bold_reg_wf, [
                    ('outputnode.ref_image_brain', 'inputnode.ref_bold_brain'),
                    ('outputnode.bold_mask', 'inputnode.ref_bold_mask')]),
            ])

    if use_syn:
        nonlinear_sdc_wf = init_nonlinear_sdc_wf(
            bold_file=bold_file, bold_pe=bold_pe, freesurfer=freesurfer, bold2t1w_dof=bold2t1w_dof,
            template=template, omp_nthreads=omp_nthreads)

        workflow.connect([
            (inputnode, nonlinear_sdc_wf, [
                ('t1_brain', 'inputnode.t1_brain'),
                ('t1_seg', 'inputnode.t1_seg'),
                ('t1_2_mni_reverse_transform', 'inputnode.t1_2_mni_reverse_transform')]),
            (bold_reference_wf, nonlinear_sdc_wf, [
                ('outputnode.ref_image_brain', 'inputnode.bold_ref')]),
            (nonlinear_sdc_wf, func_reports_wf, [
                ('outputnode.out_warp_report', 'inputnode.syn_sdc_report')]),
        ])

        # XXX Eliminate branch when forcing isn't an option
        if not fmaps:
            LOGGER.warning(
                'Susceptibility distortion correction (SDC): no fieldmaps found or they '
                'were ignored. Using EXPERIMENTAL "fieldmap-less" correction for dataset %s.',
                ref_file)
            summary.inputs.distortion_correction = 'SyN'
            workflow.connect([
                (nonlinear_sdc_wf, bold_reg_wf, [
                    ('outputnode.out_warp', 'inputnode.fieldwarp'),
                    ('outputnode.out_reference_brain', 'inputnode.ref_bold_brain'),
                    ('outputnode.out_mask', 'inputnode.ref_bold_mask')]),
            ])

    # BOLD in native BOLD space
    if fmaps:
        workflow.connect([
            (sdc_unwarp_wf, bold_bold_trans_wf, [
                ('outputnode.out_warp', 'inputnode.fieldwarp'),
                ('outputnode.out_mask', 'inputnode.bold_mask')]),
        ])
    elif use_syn:
        workflow.connect([
            (nonlinear_sdc_wf, bold_bold_trans_wf, [
                ('outputnode.out_warp', 'inputnode.fieldwarp'),
                ('outputnode.out_mask', 'inputnode.bold_mask')]),
        ])
    else:
        workflow.connect([
            (bold_reference_wf, bold_bold_trans_wf, [
                ('outputnode.bold_mask', 'inputnode.bold_mask')]),
        ])

    # Map final BOLD mask into T1w space (if required)
    if 'T1w' in output_spaces:
        from niworkflows.interfaces.fixes import (
            FixHeaderApplyTransforms as ApplyTransforms
        )

        boldmask_to_t1w = pe.Node(
            ApplyTransforms(interpolation='MultiLabel', float=True),
            name='boldmask_to_t1w', mem_gb=0.1
        )
        workflow.connect([
            (bold_bold_trans_wf, boldmask_to_t1w, [
                ('outputnode.bold_mask', 'input_image')]),
            (bold_reg_wf, boldmask_to_t1w, [
                ('outputnode.bold_mask_t1', 'reference_image'),
                ('outputnode.itk_bold_to_t1', 'transforms')]),
            (boldmask_to_t1w, outputnode, [
                ('output_image', 'bold_mask_t1')]),
        ])

    if 'template' in output_spaces:
        # Apply transforms in 1 shot
        # Only use uncompressed output if AROMA is to be run
        bold_mni_trans_wf = init_bold_mni_trans_wf(
            template=template,
            mem_gb=mem_gb['resampled'],
            omp_nthreads=omp_nthreads,
            output_grid_ref=output_grid_ref,
            use_compression=not (low_mem and use_aroma),
            use_fieldwarp=(fmaps is not None or use_syn),
            name='bold_mni_trans_wf'
        )

        workflow.connect([
            (inputnode, bold_mni_trans_wf, [
                ('bold_file', 'inputnode.name_source'),
                ('t1_2_mni_forward_transform', 'inputnode.t1_2_mni_forward_transform')]),
            (bold_split, bold_mni_trans_wf, [
                ('out_files', 'inputnode.bold_split')]),
            (bold_hmc_wf, bold_mni_trans_wf, [
                ('outputnode.xforms', 'inputnode.hmc_xforms')]),
            (bold_reg_wf, bold_mni_trans_wf, [
                ('outputnode.itk_bold_to_t1', 'inputnode.itk_bold_to_t1')]),
            (bold_bold_trans_wf, bold_mni_trans_wf, [
                ('outputnode.bold_mask', 'inputnode.bold_mask')]),
            (bold_mni_trans_wf, outputnode, [('outputnode.bold_mni', 'bold_mni'),
                                             ('outputnode.bold_mask_mni', 'bold_mask_mni')]),
        ])

        if fmaps:
            workflow.connect([
                (sdc_unwarp_wf, bold_mni_trans_wf, [
                    ('outputnode.out_warp', 'inputnode.fieldwarp')]),
            ])
        elif use_syn:
            workflow.connect([
                (nonlinear_sdc_wf, bold_mni_trans_wf, [
                    ('outputnode.out_warp', 'inputnode.fieldwarp')]),
            ])

        if use_aroma:  # ICA-AROMA workflow
            """
            ica_aroma_report
                Reportlet visualizing MELODIC ICs, with ICA-AROMA signal/noise labels
            aroma_noise_ics
                CSV of noise components identified by ICA-AROMA
            melodic_mix
                FSL MELODIC mixing matrix
            nonaggr_denoised_file
                BOLD series with non-aggressive ICA-AROMA denoising applied

            """
            from .confounds import init_ica_aroma_wf
            from ...interfaces import JoinTSVColumns
            ica_aroma_wf = init_ica_aroma_wf(name='ica_aroma_wf',
                                             ignore_aroma_err=ignore_aroma_err)
            join = pe.Node(JoinTSVColumns(), name='aroma_confounds')

            workflow.disconnect([
                (bold_confounds_wf, outputnode, [
                    ('outputnode.confounds_file', 'confounds'),
                ]),
            ])
            workflow.connect([
                (bold_hmc_wf, ica_aroma_wf, [
                    ('outputnode.movpar_file', 'inputnode.movpar_file')]),
                (bold_mni_trans_wf, ica_aroma_wf, [
                    ('outputnode.bold_mask_mni', 'inputnode.bold_mask_mni'),
                    ('outputnode.bold_mni', 'inputnode.bold_mni')]),
                (bold_confounds_wf, join, [
                    ('outputnode.confounds_file', 'in_file')]),
                (ica_aroma_wf, join,
                    [('outputnode.aroma_confounds', 'join_file')]),
                (ica_aroma_wf, outputnode,
                    [('outputnode.aroma_noise_ics', 'aroma_noise_ics'),
                     ('outputnode.melodic_mix', 'melodic_mix'),
                     ('outputnode.nonaggr_denoised_file', 'nonaggr_denoised_file')]),
                (join, outputnode, [('out_file', 'confounds')]),
                (ica_aroma_wf, func_reports_wf, [
                    ('outputnode.out_report', 'inputnode.ica_aroma_report')]),
            ])

    # SURFACES ##################################################################################
    if freesurfer and any(space.startswith('fs') for space in output_spaces):
        LOGGER.log(25, 'Creating BOLD surface-sampling workflow.')
        bold_surf_wf = init_bold_surf_wf(mem_gb=mem_gb['resampled'],
                                         output_spaces=output_spaces,
                                         medial_surface_nan=medial_surface_nan,
                                         name='bold_surf_wf')
        workflow.connect([
            (inputnode, bold_surf_wf, [
                ('t1_preproc', 'inputnode.t1_preproc'),
                ('subjects_dir', 'inputnode.subjects_dir'),
                ('subject_id', 'inputnode.subject_id'),
                ('t1_2_fsnative_forward_transform', 'inputnode.t1_2_fsnative_forward_transform')]),
            (bold_reg_wf, bold_surf_wf, [('outputnode.bold_t1', 'inputnode.source_file')]),
            (bold_surf_wf, outputnode, [('outputnode.surfaces', 'surfaces')]),
        ])

    # REPORTING ############################################################
    bold_bold_report_wf = init_bold_preproc_report_wf(
        mem_gb=mem_gb['resampled'],
        reportlets_dir=reportlets_dir
    )

    workflow.connect([
        (inputnode, bold_bold_report_wf, [
            ('bold_file', 'inputnode.name_source'),
            ('bold_file', 'inputnode.in_pre')]),  # This should be after STC
        (bold_bold_trans_wf, bold_bold_report_wf, [
            ('outputnode.bold', 'inputnode.in_post')]),
    ])

    return workflow


def init_func_reports_wf(reportlets_dir, freesurfer, use_aroma, use_syn, name='func_reports_wf'):
    """
    Set up a battery of datasinks to store reports in the right location
    """
    workflow = pe.Workflow(name=name)

    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=['source_file', 'summary_report', 'validation_report',
                    'bold_reg_report', 'bold_reg_fallback', 'bold_rois_report',
                    'syn_sdc_report', 'ica_aroma_report']),
        name='inputnode')

    ds_summary_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='summary'),
        name='ds_summary_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_validation_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='validation'),
        name='ds_validation_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_bold_rois_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='rois'),
        name='ds_bold_rois_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_syn_sdc_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='syn_sdc'),
        name='ds_syn_sdc_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    def _bold_reg_suffix(fallback, freesurfer):
        if fallback:
            return 'coreg' if freesurfer else 'flirt'
        return 'bbr' if freesurfer else 'flt_bbr'

    ds_bold_reg_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir),
        name='ds_bold_reg_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_ica_aroma_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='ica_aroma'),
        name='ds_ica_aroma_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    workflow.connect([
        (inputnode, ds_summary_report, [('source_file', 'source_file'),
                                        ('summary_report', 'in_file')]),
        (inputnode, ds_validation_report, [('source_file', 'source_file'),
                                           ('validation_report', 'in_file')]),
        (inputnode, ds_bold_rois_report, [('source_file', 'source_file'),
                                          ('bold_rois_report', 'in_file')]),
        (inputnode, ds_bold_reg_report, [
            ('source_file', 'source_file'),
            ('bold_reg_report', 'in_file'),
            (('bold_reg_fallback', _bold_reg_suffix, freesurfer), 'suffix')]),
    ])

    if use_aroma:
        workflow.connect([
            (inputnode, ds_ica_aroma_report, [('source_file', 'source_file'),
                                              ('ica_aroma_report', 'in_file')]),
        ])

    if use_syn:
        workflow.connect([
            (inputnode, ds_syn_sdc_report, [('source_file', 'source_file'),
                                            ('syn_sdc_report', 'in_file')]),
        ])

    return workflow


def init_func_derivatives_wf(output_dir, output_spaces, template, freesurfer,
                             use_aroma, name='func_derivatives_wf'):
    """
    Set up a battery of datasinks to store derivatives in the right location
    """
    workflow = pe.Workflow(name=name)

    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=['source_file', 'bold_t1', 'bold_mask_t1', 'bold_mni', 'bold_mask_mni',
                    'bold_aseg_t1', 'bold_aparc_t1',
                    'confounds', 'surfaces', 'aroma_noise_ics', 'melodic_mix',
                    'nonaggr_denoised_file']),
        name='inputnode')

    suffix_fmt = 'space-{}_{}'.format
    variant_suffix_fmt = 'space-{}_variant-{}_{}'.format

    ds_confounds = pe.Node(DerivativesDataSink(
        base_directory=output_dir, suffix='confounds'),
        name="ds_confounds", run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)
    workflow.connect([
        (inputnode, ds_confounds, [('source_file', 'source_file'),
                                   ('confounds', 'in_file')]),
    ])

    # Resample to T1w space
    if 'T1w' in output_spaces:
        ds_bold_t1 = pe.Node(DerivativesDataSink(
            base_directory=output_dir, suffix=suffix_fmt('T1w', 'preproc')),
            name='ds_bold_t1', run_without_submitting=True,
            mem_gb=DEFAULT_MEMORY_MIN_GB)

        ds_bold_mask_t1 = pe.Node(DerivativesDataSink(
            base_directory=output_dir, suffix=suffix_fmt('T1w', 'brainmask')),
            name='ds_bold_mask_t1', run_without_submitting=True,
            mem_gb=DEFAULT_MEMORY_MIN_GB)
        workflow.connect([
            (inputnode, ds_bold_t1, [('source_file', 'source_file'),
                                     ('bold_t1', 'in_file')]),
            (inputnode, ds_bold_mask_t1, [('source_file', 'source_file'),
                                          ('bold_mask_t1', 'in_file')]),
        ])

    # Resample to template (default: MNI)
    if 'template' in output_spaces:
        ds_bold_mni = pe.Node(DerivativesDataSink(
            base_directory=output_dir, suffix=suffix_fmt(template, 'preproc')),
            name='ds_bold_mni', run_without_submitting=True,
            mem_gb=DEFAULT_MEMORY_MIN_GB)
        ds_bold_mask_mni = pe.Node(DerivativesDataSink(
            base_directory=output_dir, suffix=suffix_fmt(template, 'brainmask')),
            name='ds_bold_mask_mni', run_without_submitting=True,
            mem_gb=DEFAULT_MEMORY_MIN_GB)
        workflow.connect([
            (inputnode, ds_bold_mni, [('source_file', 'source_file'),
                                      ('bold_mni', 'in_file')]),
            (inputnode, ds_bold_mask_mni, [('source_file', 'source_file'),
                                           ('bold_mask_mni', 'in_file')]),
        ])

    if freesurfer:
        ds_bold_aseg_t1 = pe.Node(DerivativesDataSink(
            base_directory=output_dir, suffix='space-T1w_label-aseg_roi'),
            name='ds_bold_aseg_t1', run_without_submitting=True,
            mem_gb=DEFAULT_MEMORY_MIN_GB)
        ds_bold_aparc_t1 = pe.Node(DerivativesDataSink(
            base_directory=output_dir, suffix='space-T1w_label-aparcaseg_roi'),
            name='ds_bold_aparc_t1', run_without_submitting=True,
            mem_gb=DEFAULT_MEMORY_MIN_GB)
        workflow.connect([
            (inputnode, ds_bold_aseg_t1, [('source_file', 'source_file'),
                                          ('bold_aseg_t1', 'in_file')]),
            (inputnode, ds_bold_aparc_t1, [('source_file', 'source_file'),
                                           ('bold_aparc_t1', 'in_file')]),
        ])

    # fsaverage space
    if freesurfer and any(space.startswith('fs') for space in output_spaces):
        name_surfs = pe.MapNode(GiftiNameSource(
            pattern=r'(?P<LR>[lr])h.(?P<space>\w+).gii', template='space-{space}.{LR}.func'),
            iterfield='in_file', name='name_surfs', mem_gb=DEFAULT_MEMORY_MIN_GB,
            run_without_submitting=True)
        ds_bold_surfs = pe.MapNode(DerivativesDataSink(base_directory=output_dir),
                                   iterfield=['in_file', 'suffix'], name='ds_bold_surfs',
                                   run_without_submitting=True,
                                   mem_gb=DEFAULT_MEMORY_MIN_GB)
        workflow.connect([
            (inputnode, name_surfs, [('surfaces', 'in_file')]),
            (inputnode, ds_bold_surfs, [('source_file', 'source_file'),
                                        ('surfaces', 'in_file')]),
            (name_surfs, ds_bold_surfs, [('out_name', 'suffix')]),
        ])

    if use_aroma:
        ds_aroma_noise_ics = pe.Node(DerivativesDataSink(
            base_directory=output_dir, suffix='AROMAnoiseICs'),
            name="ds_aroma_noise_ics", run_without_submitting=True,
            mem_gb=DEFAULT_MEMORY_MIN_GB)
        ds_melodic_mix = pe.Node(DerivativesDataSink(
            base_directory=output_dir, suffix='MELODICmix'),
            name="ds_melodic_mix", run_without_submitting=True,
            mem_gb=DEFAULT_MEMORY_MIN_GB)
        ds_aroma_mni = pe.Node(DerivativesDataSink(
            base_directory=output_dir, suffix=variant_suffix_fmt(
                template, 'smoothAROMAnonaggr', 'preproc')),
            name='ds_aroma_mni', run_without_submitting=True,
            mem_gb=DEFAULT_MEMORY_MIN_GB)

        workflow.connect([
            (inputnode, ds_aroma_noise_ics, [('source_file', 'source_file'),
                                             ('aroma_noise_ics', 'in_file')]),
            (inputnode, ds_melodic_mix, [('source_file', 'source_file'),
                                         ('melodic_mix', 'in_file')]),
            (inputnode, ds_aroma_mni, [('source_file', 'source_file'),
                                       ('nonaggr_denoised_file', 'in_file')]),
        ])

    return workflow


def _get_series_len(bold_fname):
    from niworkflows.interfaces.registration import _get_vols_to_discard
    img = nb.load(bold_fname)
    if len(img.shape) < 4:
        return 1

    skip_vols = _get_vols_to_discard(img)

    return img.shape[3] - skip_vols


def _create_mem_gb(bold_fname):
    bold_size_gb = os.path.getsize(bold_fname) / (1024**3)
    bold_tlen = nb.load(bold_fname).shape[-1]
    mem_gb = {
        'filesize': bold_size_gb,
        'resampled': bold_size_gb * 4,
        'largemem': bold_size_gb * (max(bold_tlen / 100, 1.0) + 4),
    }

    return bold_tlen, mem_gb


def _get_wf_name(bold_fname):
    """
    Derives the workflow name for supplied BOLD file.

    >>> _get_wf_name('/completely/made/up/path/sub-01_task-nback_bold.nii.gz')
    'func_preproc_task_nback_wf'
    >>> _get_wf_name('/completely/made/up/path/sub-01_task-nback_run-01_echo-1_bold.nii.gz')
    'func_preproc_task_nback_run_01_echo_1_wf'
    """
    from niworkflows.nipype.utils.filemanip import split_filename
    fname = split_filename(bold_fname)[1]
    fname_nosub = '_'.join(fname.split("_")[1:])
    # if 'echo' in fname_nosub:
    #     fname_nosub = '_'.join(fname_nosub.split("_echo-")[:1]) + "_bold"
    name = "func_preproc_" + fname_nosub.replace(
        ".", "_").replace(" ", "").replace("-", "_").replace("_bold", "_wf")

    return name
