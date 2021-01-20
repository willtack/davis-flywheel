import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# structurals
t1w = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_T1w')
t2w = create_key(
     'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_T2w')
t2_2d = create_key(
     'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_acq-2D_T2w')
t2_cor = create_key(
     'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_acq-coronal_T2w')
flair = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_FLAIR')
flair2 = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_acq-3D_FLAIR')
tof1 = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_angio')
tof2 = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_acq-cor_angio')
tof3 = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_acq-sag_angio')

# task fMRI
object_run1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-object_run-01_bold')
object_run2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-object_run-02_bold')
rhyme_run1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-rhyme_run-01_bold')
rhyme_run2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-rhyme_run-02_bold')
scenemem_run1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-scenemem_run-01_bold')
scenemem_run2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-scenemem_run-02_bold')
sentence_run1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-sentence_run-01_bold')
sentence_run2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-sentence_run-02_bold')
wordgen_run1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-wordgen_run-01_bold')
wordgen_run2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-wordgen_run-02_bold')
binder_run1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-binder_run-01_bold')
binder_run2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-binder_run-02_bold')
verbgen_run1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-verbgen_run-01_bold')
verbgen_run2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-verbgen_run-02_bold')
rest_run1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-rest_run-01_bold')
rest_run2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-rest_run-02_bold')

# ASL scans
asl = create_key(
     'sub-{subject}/ses-{session}/perf/sub-{subject}_{session}_asl')
m0 = create_key(
    'sub-{subject}/ses-{session}/perf/sub-{subject}_{session}_m0scan')
mean_perf = create_key(
    'sub-{subject}/ses-{session}/perf/sub-{subject}_{session}_mean-perfusion')

# Diffusion
dwi = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-multiband_dwi')

# Field maps
b0_mag = create_key(
   'sub-{subject}/ses-{session}/fmap/sub-{subject}_{session}_magnitude{item}')
b0_phase = create_key(
   'sub-{subject}/ses-{session}/fmap/sub-{subject}_{session}_phasediff')
pe_rev = create_key(
    'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-multishell_dir-j_epi')
bold_tu = create_key(
    'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-bold_dir-j_epi')


def infotodict(seqinfo):

    last_run = len(seqinfo)

    info = {t1w:[], t2w:[], t2_2d:[], t2_cor:[],flair:[], flair2:[], tof1: [], tof2: [], tof3: [],
            pe_rev: [],dwi:[],object_run1: [], object_run2: [], rhyme_run1: [],
            rhyme_run2: [],scenemem_run1: [], scenemem_run2: [], sentence_run1: [],
            sentence_run2: [],wordgen_run1: [], wordgen_run2: [], binder_run1: [],
            binder_run2:[],verbgen_run1: [], verbgen_run2: [], rest_run1: [], rest_run2: [],
            bold_tu: [],asl: [], m0: [], mean_perf: [], b0_phase: [], b0_mag: []}

# sometimes patients struggle with a task the first time around (or something
# else goes wrong and often some tasks are repeated. This function accomodates
# the variable number of task runs
    def get_both_series(key1, key2, s):
         if len(info[key1]) == 0:
             info[key1].append(s.series_id)
         else:
             info[key2].append(s.series_id)

# this doesn't need to be a function but using it anyway for aesthetic symmetry
# with above function
    def get_series(key, s):
            info[key].append(s.series_id)

    for s in seqinfo:
        protocol = s.protocol_name.lower()
        if any(id in protocol for id in ["t1w", "t1", "mprage_t"]):
            get_series(t1w,s)
        elif "t2w_spc" in protocol:
            get_series(t2w,s)
        elif "t2_2d" in protocol:
            get_series(t2_2d, s)
        elif "t2_tse_coronal" in protocol:
            get_series(t2_cor, s)
        elif "tra_flair" in protocol:
            get_series(flair,s)
        elif "flair" in protocol and "3d" in protocol:
            get_series(flair2,s)

        elif "tof" in protocol:
            if "COR" in s.series_description:
                get_series(tof2,s)
            elif "SAG" in s.series_description:
                get_series(tof3,s)
            else:
                get_series(tof1,s)

        elif "topup" in protocol and "BOLD" not in s.series_description:
            get_series(pe_rev, s)
        elif "multishell" in protocol and not s.is_derived:
            get_series(dwi, s)

        elif "object" in protocol:
            get_both_series(object_run1,object_run2,s)
        elif "rhyming" in protocol:
            get_both_series(rhyme_run1,rhyme_run2,s)
        elif "scenemem" in protocol:
            get_both_series(scenemem_run1,scenemem_run2,s)
        elif "sentence" in protocol:
            get_both_series(sentence_run1, sentence_run2, s)
        elif "wordgen" in protocol:
            get_both_series(wordgen_run1,wordgen_run2,s)
        elif "binder" in protocol:
            get_both_series(binder_run1, binder_run2,s)
        elif "verbgen" in protocol:
            get_both_series(verbgen_run1, verbgen_run2,s)
        elif "restBOLD" in s.series_description and "asl" not in protocol:
            get_both_series(rest_run1, rest_run2, s)
        elif "topup" in protocol and "MULTISHELL" not in s.series_description:
            get_series(bold_tu, s)

        elif "spiral" in protocol:
            if s.series_description.endswith("_ASL"):
                get_series(asl,s)
            elif s.series_description.endswith("_M0"):
                get_series(m0,s)
            elif s.series_description.endswith("_MeanPerf"):
                get_series(mean_perf,s)

        elif "b0map" in protocol:
                if "P" in s.image_type:
                    get_series(b0_phase,s)
                elif "M" in s.image_type:
                    get_series(b0_mag,s)

    return info


def AttachToSession():

    NUM_VOLUMES=18
    data = ['label', 'control'] * NUM_VOLUMES
    data = '\n'.join(data)
    data = 'volume_type\n' + data # the data is now a string; perfect!

    asl_context = {
      'name': 'sub-{subject}/{session}/perf/sub-{subject}_{session}_aslcontext.tsv',
      'data': data,
      'type': 'text/tab-separated-values'
    }

    return asl_context

def AttachToProject():
    import pandas as pd
    object_data = {'onset': [0, 18, 36, 54, 72, 90, 108, 126, 144, 162, 180, 198, 16, 234, 252, 270],
                   'duration': [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18],
                   'weight': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                   'trial_type':
                  ['baseline',
                   'stimulus',
                   'baseline',
                   'stimulus',
                   'baseline',
                   'stimulus',
                   'baseline',
                   'stimulus',
                   'baseline',
                   'stimulus',
                   'baseline',
                   'stimulus',
                   'baseline',
                   'stimulus',
                   'baseline',
                   'stimulus']}
    o_df = pd.DataFrame(object_data, columns = ['onset', 'duration','trial_type'])
    object1 = {
        'name': 'task-object_events.tsv',
        'data': o_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }

    rhyme_data ={'onset': [0, 30, 60, 90, 120, 150, 180, 210, 240, 270],
                'duration': [30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
                'weight': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                'trial_type':
                ['baseline',
                 'stimulus',
                 'baseline',
                 'stimulus',
                 'baseline',
                 'stimulus',
                 'baseline',
                 'stimulus',
                 'baseline',
                 'stimulus']}
    r_df = pd.DataFrame(rhyme_data, columns = ['onset', 'duration','trial_type'])
    rhyme = {
        'name': 'task-rhyme_events.tsv',
        'data': r_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }

    scenemem_data = {'onset': [0, 36, 72, 108, 144, 180, 216, 252, 288, 324, 360, 396],
                     'duration': [36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36],
                     'weight': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                     'trial_type':
                     ['baseline',
                      'stimulus',
                      'baseline',
                      'stimulus',
                      'baseline',
                      'stimulus',
                      'baseline',
                      'stimulus',
                      'baseline',
                      'stimulus',
                      'baseline',
                      'stimulus']}
    sm_df = pd.DataFrame(scenemem_data, columns = ['onset', 'duration','trial_type'])
    scenemem = {
        'name': 'task-scenemem_events.tsv',
        'data': sm_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }

    sentence_data = {'onset': [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240],
                     'duration': [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
                     'weight': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                     'trial_type':
                     ['baseline',
                      'stimulus',
                      'baseline',
                      'stimulus',
                      'baseline',
                      'stimulus',
                      'baseline',
                      'stimulus',
                      'baseline',
                      'stimulus',
                      'baseline',
                      'stimulus',
                      'baseline']}
    s_df = pd.DataFrame(sentence_data, columns = ['onset', 'duration','trial_type'])
    sentence = {
        'name': 'task-sentence_events.tsv',
        'data': s_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }

    wordgen_data = {'onset': [0, 30, 60, 90, 120, 150, 180, 210, 240, 270],
                    'duration': [30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
                    'weight': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                    'trial_type':
                   ['baseline',
                    'stimulus',
                    'baseline',
                    'stimulus',
                    'baseline',
                    'stimulus',
                    'baseline',
                    'stimulus',
                    'baseline',
                    'stimulus']}
    w_df = pd.DataFrame(wordgen_data, columns = ['onset', 'duration','trial_type'])
    wordgen = {
        'name': 'task-wordgen_events.tsv',
        'data': w_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }

    return [object1, rhyme, scenemem, sentence, wordgen]


MetadataExtras = {
   b0_phase: {
       "EchoTime1": 0.00507,
       "EchoTime2": 0.00753
   },
   asl: {
   "PulseSequenceType": "3D_SPIRAL",
       "PulseSequenceDetails" : "WIP" ,
       "RepetitionTime":4.2,
       "LabelingType": "PCASL",
       "LabelingDuration": 1.8,
       "PostLabelingDelay": 1.8,
       "BackgroundSuppression": True,
       "BackgroundSuppressionNumberPulses": 2,
       "M0scale":10,
       "LabelingOrientation":"transversal",
       "LabelingDistance":105,
       "LabelingPulseAverageGradient": 10,
       "LabelingPulseMaximumGradient": 80,
       "VascularCrushing": False,
       "PulseDuration": 0.0005,
       "LabelingPulseInterval": 0.00038,
       "PCASLType":"unbalanced",
       "LabelingEfficiency":0.72},
     binder_run1: {
     "FullTaskName": "Binder Semantic Decision"},
     binder_run2: {
     "FullTaskName": "Binder Semantic Decision"},
     object_run1: {
     "FullTaskName": "Object Naming"},
     object_run2: {
     "FullTaskName": "Object Naming"},
     rhyme_run1: {
     "FullTaskName": "Rhyme Matching"},
     rhyme_run2: {
     "FullTaskName": "Rhyme Matching"},
     scenemem_run1: {
     "FullTaskName": "Scene Memory"},
     scenemem_run2: {
     "FullTaskName": "Scene Memory"},
     sentence_run1: {
     "FullTaskName": "Sentence Completion"},
     sentence_run2: {
     "FullTaskName": "Sentence Completion"},
     verbgen_run1: {
     "FullTaskName": "Verb Generation"},
     verbgen_run2: {
     "FullTaskName": "Verb Generation"},
     wordgen_run1: {
     "FullTaskName": "Word Generation"},
     wordgen_run2: {
     "FullTaskName": "Word Generation"},
}

IntendedFor = {
    b0_phase: [
    '{session}/func/sub-{subject}_{session}_task-object_run-01_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-object_run-02_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-rhyme_run-01_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-rhyme_run-02_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-scenemem_run-01_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-scenemem_run-02_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-sentence_run-01_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-sentence_run-02_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-wordgen_run-01_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-wordgen_run-02_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-binder_run-01_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-binder_run-02_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-verbgen_run-01_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-verbgen_run-02_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-rest_run-01_bold.nii.gz',
    '{session}/func/sub-{subject}_{session}_task-rest_run-02_bold.nii.gz'],

    m0: ['{session}/perf/sub-{subject}_{session}_asl.nii.gz'],

    pe_rev: ['{session}/fmap/sub-{subject}_{session}_acq-multishell_dir-j_epi.nii.gz']
}
