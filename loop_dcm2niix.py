import flywheel

# Create client
fw = flywheel.Client()

gear = fw.lookup('gears/dcm2niix')
project = fw.lookup('epsteinlab/brainSLAM')

for ses in project.sessions():
    # Find matching acquisitions, using regular expression match on label
    b0_acquisitions = ses.acquisitions.find('label=~^B0map_*')

    # Propose the batch, set merge2d to no to convert both mag images
    proposal = gear.propose_batch(b0_acquisitions, config={'merge2d': 'n'})

    # Run the batch job
    jobs = proposal.run()