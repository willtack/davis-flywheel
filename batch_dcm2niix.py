import flywheel

# Create client
fw = flywheel.Client()

gear = fw.lookup('gears/dcm2niix')
project = fw.lookup('davis/presurgicalEpilepsy')

for ses in project.sessions():
    # Find matching acquisitions, using regular expression match on label
    asl_acquisitions = ses.acquisitions.find('label=~ASL')

    # Propose the batch, set merge2d to no to convert both mag images
    proposal = gear.propose_batch(asl_acquisitions)

    # Run the batch job
    jobs = proposal.run()