import flywheel
import datetime

# Create client
fw = flywheel.Client()

# define important containers/files
gear = fw.lookup('gears/fw-heudiconv')
project = fw.lookup('davis/presurgicalEpilepsy')
heuristic = project.get_file('heuristic.py')

# set date for label
x = datetime.datetime.now()
date_str = '%s-%s-%s %s:%s' % (x.month, x.day, x.year, x.hour, x.minute)

# set inputs and config for gear
inputs = {'heuristic': heuristic}
config = {'action': 'Curate', 'do_whole_project': False, 'dry_run': False, 'extended_bids': True}

for ses in project.sessions():
    analysis_id = gear.run(analysis_label='heudiconv ' + date_str, config=config, inputs=inputs, destination=ses)


