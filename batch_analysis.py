# General script for performing a batch job for an analysis
#
# Inputs: config.json, subject list
#
#

import flywheel
import json
import argparse

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

args = parser.parse_args()
config = args.config
subject_list = args.subs



# Define containers & files
xcpgear = fw.lookup('gears/xcpengine-fw')
fmriprepgear = fw.lookup('gears/fmriprep-fwheudiconv')
linguagear = fw.lookup('gears/presurg')
license_file = project.get_file('freesurfer_license.txt')
design_file = project.get_file('fc-36p_spkreg_sb.dsn') #TODO: make this an option

# Load in data
with open(config) as f:
    config_dict = json.load(f)

slabel_list = [line.rstrip('\n').split()[0] for line in open(subject_list)]

def run_xcp(configuration):
    for sub in slabel_list:
        print('Trying subject %s' % (sub))
        subject_container = fw.lookup('davis/presurgicalEpilepsy/%s' % (sub))
        for ses in subject_container.sessions():
            for a in ses.analyses:
                if a.files and 'SB_fmriprep' in a.label:
                    fprep_output = [f for f in a.files if 'fmriprep' in f.name]
            # set inputs and config for gear
            inputs = {'designfile': design_file, 'fmriprepdir': fprep_output[0]}
            analysis_id = xcpgear.run(analysis_label='WT_xcp', config=configuration, inputs=inputs, destination=ses)

def run_fmriprep(configuration):
    for sub in slabel_list:
        print('Trying subject %s' % (sub))
        subject_container = fw.lookup('davis/presurgicalEpilepsy/%s' % (sub))
        for ses in subject_container.sessions():
            # set inputs and config for gear
            inputs = {'freesurfer_license': license_file}
            analysis_id = fmriprepgear.run(analysis_label='WT_fmriprep', config=configuration, inputs=inputs, destination=ses)

def run_lingua_map(configuration):
    for sub in slabel_list:
        print('Running analysis for subject %s' % (sub))
        subject_container = fw.lookup('davis/presurgicalEpilepsy/%s' % (sub))
        for ses in subject_container.sessions():
            # Check if there is task-fMRI data
            bold_img = None
            for acq in ses.acquisitions():
                if 'BOLD_Sentence' in acq.label or 'BOLD_Wordgen' in acq.label or 'BOLD_SceneMem' in acq.label:
                    bold_container=fw.get(acq.id)
                    for file in bold_container.files:
                        if '.nii.gz' in file.name:
                            bold_img=file
            if bold_img is None:
                print("  %s: No task-fMRI data." % (sub))

            # Get the fmriprep analysis and check if already been run successfully
            for analysis in ses.analyses:
                if analysis.files and "fmriprep" in analysis.label:
                    fprep = fw.get(analysis.id)
                    print(analysis.label)
            print("Using %s" % (fprep.label))

            for file in fprep.files:
                if "fmriprep" in file.name:
                    fmriprepdir = file

            # Run gear
            if fprep is not None and bold_img is not None and not alreadydone:
                print(' Running analysis for %s' % (sub))
                inputs = {'fmriprepdir': fmriprepdir }
                #analysis_id = linguagear.run(analysis_label='lingua-map', config=configuration, inputs=inputs, destination=ses)

if "xcp" in config:
    run_xcp(config_dict)
elif "fmriprep" in config:
    run_fmriprep(config_dict)
elif "lingua" in config:
    run_lingua_map(config_dict)

print("Done!")
