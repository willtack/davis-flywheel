import flywheel
import datetime

# Create client
fw = flywheel.Client()

# define containers & files
gear = fw.lookup('gears/fmriprep')
project = fw.lookup('davis/presurgicalEpilepsy')
license_file = project.get_file('freesurfer_license.txt')
license_string = 'william.tackett@pennmedicine.upenn.edu\
                39492\
                *Cze83ZRK81rI\
                FSB/TAmun94lg'

# set date for label
x = datetime.datetime.now()
date_str = '%s-%s-%s %s:%s' % (x.month, x.day, x.year, x.hour, x.minute)

# set inputs and config for gear
inputs = {'freesurfer_license': license_file}
config = {'save_outputs': True, 'FREESURFER_LICENSE': license_string, 'fs_no_reconall': True, 'use_aroma': True}

# run gear
session = fw.lookup('davis/presurgicalEpilepsy/P70/ses-01')
analysis_id = gear.run(analysis_label='fmriprep_test', config=config, inputs=inputs, destination=session)


#for ses in project.sessions():
#    analysis_id = gear.run(analysis_label='fmriprep_test', config=config, inputs=inputs, destination=ses)
