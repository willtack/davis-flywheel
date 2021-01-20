# General script for performing a batch job for an analysis
#
# Inputs: config.json, subject list
#
#

import flywheel
import json
import argparse
import datetime
import os
import re
from shutil import copy

# Create client, define project
fw = flywheel.Client()
project = fw.lookup('davis/presurgicalEpilepsy')

# Argument parsing
parser = argparse.ArgumentParser(
        description="Conduct a batch analysis with a gear on Flywheel")

parser.add_argument(
        "--config",
        help="path to config json",
        required=True
        )
parser.add_argument(
        "--subs",
        help="path to text file containing list of subjects",
        required=True
        )
parser.add_argument(
        "--label",
        help="label to attach to analysis container",
        required=False
)

args = parser.parse_args()
config = args.config
subject_list = args.subs
analysis_label = args.label

# set date for label
x = datetime.datetime.now()
date_str = '%s-%s-%s' % (x.year, x.month, x.day)

# For provenance tracking
analysis_ids = []
fails = []
logdir = os.path.join('logs',date_str)
os.makedirs(logdir, exist_ok=True)

# Define containers & files
xcpgear = fw.lookup('gears/xcpengine-fw')
fmriprepgear = fw.lookup('gears/fmriprep-fwheudiconv/0.3.4_20.0.5')
linguagear = fw.lookup('gears/presurg')
license_file = project.get_file('freesurfer_license.txt')
design_file = project.get_file('fc-36p_spkreg_sb.dsn') #TODO: make this an option

# Load in data
with open(config) as f:
    config_dict = json.load(f)

slabel_list = [line.rstrip('\n').split()[0] for line in open(subject_list)]

if "<date>" in analysis_label:
    analysis_label = re.sub('<date>', date_str, analysis_label)

def run_xcp(configuration):
    if analysis_label is None:
        label='xcp ' + date_str
    else:
        label = analysis_label
    for sub in slabel_list:
        print('Trying subject %s' % (sub))
        subject_container = fw.lookup('davis/presurgicalEpilepsy/%s' % (sub))
        for session in subject_container.sessions():
            # session var : <class 'flywheel.models.session.Session'>
            # ses var : <class 'flywheel.models.container_session_output.ContainerSessionOutput'>
            ses = fw.get(session.id)
            for a in ses.analyses:
                if a.files and 'SB_fmriprep' in a.label:
                    fprep_output = [f for f in a.files if 'fmriprep' in f.name]
            # set inputs and config for gear
            inputs = {'designfile': design_file, 'fmriprepdir': fprep_output[0]}
            try:
                analysis_id = xcpgear.run(analysis_label=label, config=configuration, inputs=inputs, destination=ses)
                analysis_ids.append(analysis_id)
            except:
                print(e)
                fails.append(ses)
            inputs_to_save = {'designfile': design_file.name, 'fmriprepdir': a.label}
    return inputs_to_save

def run_fmriprep(configuration):
    if analysis_label is None:
        label='fmriprep ' + date_str
    else:
        label = analysis_label
    for sub in slabel_list:
        print('Trying subject %s' % (sub))
        subject_container = fw.lookup('davis/presurgicalEpilepsy/%s' % (sub))
        for session in subject_container.sessions():
            # session var : <class 'flywheel.models.session.Session'>
            # ses var : <class 'flywheel.models.container_session_output.ContainerSessionOutput'>
            ses = fw.get(session.id)

            # set inputs and config for gear
            inputs = {'freesurfer_license': license_file}
            try:
                analysis_id = fmriprepgear.run(analysis_label=label, config=configuration, inputs=inputs, destination=ses)
                analysis_ids.append(analysis_id)
            except Exception as e:
                print(e)
                fails.append(ses)

def run_lingua_map(configuration):
    if analysis_label is None:
        label='lingua-map ' + date_str
    else:
        label = analysis_label
    for sub in slabel_list:
        print('Trying subject %s' % (sub))
        subject_container = fw.lookup('davis/presurgicalEpilepsy/%s' % (sub))
        for session in subject_container.sessions():
            # session var : <class 'flywheel.models.session.Session'>
            # ses var : <class 'flywheel.models.container_session_output.ContainerSessionOutput'>
            ses = fw.get(session.id)

            # Check if there is task-fMRI data
            bold_img = None
            for acq in ses.acquisitions():
                # if 'BOLD_Sentence' in acq.label or 'BOLD_Wordgen' in acq.label or 'BOLD_SceneMem' in acq.label:
                if 'BOLD_SceneMem' in acq.label:
                    bold_container=fw.get(acq.id)
                    for file in bold_container.files:
                        if '.nii.gz' in file.name:
                            bold_img=file
            if bold_img is None:
                print("  %s: No task-fMRI data." % (sub))

            # Get the fmriprep analysis and check if already been run successfully
            fprep = None
            try:
                for analysis in ses.analyses:
                    if analysis.files and "034" in analysis.label:
                        fprep = fw.get(analysis.id)
                print("   Using %s" % (fprep.label))

                for file in fprep.files:
                    if "fmriprep_sub" in file.name:
                        fmriprepdir = file
            except Exception as e:
                print(e)
                print("Probably unable to find any analyses for this session.")

            # Run gear
            if fprep is not None and bold_img is not None:
                print('   Running analysis for %s' % (sub))
                inputs = {'fmriprepdir': fmriprepdir}
                try:
                    analysis_id = linguagear.run(analysis_label=label, config=configuration, inputs=inputs, destination=ses)
                    analysis_ids.append(analysis_id)
                except Exception as e:
                    print(e)
                    fails.append(ses)
                inputs_to_save = {'fmriprepdir': fprep.label}
    return inputs_to_save

gear = None
if "xcp" in config:
    inputs = run_xcp(config_dict)
    gear = xcpgear
elif "fmriprep" in config:
    run_fmriprep(config_dict)
    gear = fmriprepgear
elif "lingua" in config:
    inputs = run_lingua_map(config_dict)
    gear = linguagear
print("Done!")

# For provenance
with open(os.path.join(logdir,'{}_{}_{}_analysisIDS.txt'.format(gear.gear.name,gear.gear.version,date_str)), 'w') as f:
    for id in analysis_ids:
        f.write("%s\n" % id)
with open(os.path.join(logdir,'{}_{}_{}_failSES.txt'.format(gear.gear.name,gear.gear.version,date_str)), 'w') as a:
    for ses in fails:
        a.write("%s\n" % ses)

if gear is linguagear or gear is xcpgear:
    with open(os.path.join(logdir,'{}_{}_{}_inputs.json'.format(gear.gear.name,gear.gear.version,date_str)), 'w') as fp:
        json.dump(inputs, fp)

copy(config, os.path.join(logdir,'{}_{}_{}_config.json'.format(gear.gear.name, gear.gear.version, date_str)))
if gear is xcpgear: # download the XCP design file
    project.download_file(design_file, os.path.join(logdir, '{}_{}_{}_{}'.format(gear.gear.name, gear.gear.version, date_str, design_file)) )
