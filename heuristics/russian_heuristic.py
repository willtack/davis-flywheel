import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# structurals
t1w = create_key(
    'sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')
flair = create_key(
    'sub-{subject}/{session}/anat/sub-{subject}_{session}_flair')

# task fMRI
object = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-object_bold')
rhyme = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rhyme_bold')
rhyme_russian = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rhymerussian_bold')
scenemem = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-scenemem_bold')
sentence = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-sentence_bold')
sentence_russian = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-sentencerussian_bold')
wordgen = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-wordgen_bold')
wordgen_russian = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-wordgenrussian_bold')
binder = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-binder_bold')
rest = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_bold')

# ASL scans
asl = create_key(
'sub-{subject}/{session}/asl/sub-{subject}_{session}_asl')
m0 = create_key(
'sub-{subject}/{session}/asl/sub-{subject}_{session}_MZeroScan')
mean_perf = create_key(
'sub-{subject}/{session}/asl/sub-{subject}_{session}_CBF')

# Field maps
b0_mag = create_key(
   'sub-{subject}/{session}/fmap/sub-{subject}_{session}_magnitude{item}')
b0_phase = create_key(
   'sub-{subject}/{session}/fmap/sub-{subject}_{session}_phasediff')

def infotodict(seqinfo):

    last_run = len(seqinfo)

    info = {t1w:[], flair:[], object: [], rhyme: [], rhyme_russian: [],
            scenemem: [], sentence: [], sentence_russian: [], wordgen: [],
            wordgen_russian: [], binder: [], rest: [], asl: [], m0: [], mean_perf: [],
            b0_phase: [], b0_mag: []}

    def get_latest_series(key, s):
        if len(info[key]) == 0:
            info[key].append(s.series_id)
        else:
            info[key] = [s.series_id]

    for s in seqinfo:
        protocol = s.protocol_name.lower()
        if "t1w" in protocol:
            get_latest_series(t1w,s)
        elif "flair" in protocol:
            get_latest_series(flair,s)
        elif "object" in protocol:
            get_latest_series(object,s)
        elif "rhyming" in protocol:
            if "russian" in protocol:
                get_latest_series(rhyme_russian,s)
            get_latest_series(rhyme,s)
        elif "scenemem" in protocol:
            get_latest_series(scenemem,s)
        elif "sentence" in protocol:
            if "russian" in protocol:
                get_latest_series(sentence_russian,s)
            get_latest_series(sentence,s)
        elif "wordgen" in protocol:
            if "russian" in protocol:
                get_latest_series(wordgen_russian,s)
            get_latest_series(wordgen,s)
        elif "binder" in protocol:
            get_latest_series(binder,s)
        elif "rest" in protocol:
            get_latest_series(rest,s)
        elif "spiral" in protocol:
            if s.dim3==612:
                get_latest_series(asl,s)
            elif s.dim3==68:
                get_latest_series(m0,s)
        elif "b0map" in protocol:
                if "P" in s.image_type:
                    get_latest_series(b0_phase,s)
                elif "M" in s.image_type:
                    get_latest_series(b0_mag,s)

    return info

MetadataExtras = {
   b0_phase: {
       "EchoTime1": 0.00507,
       "EchoTime2": 0.00753
   }
}
