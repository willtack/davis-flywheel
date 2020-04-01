import flywheel
import os

fw = flywheel.Client()

subject_list = 'subs/lastctrls.txt'
slabel_list = [line.rstrip('\n').split()[0] for line in open(subject_list)]
data_dir = '/media/will/Data/epilepsy-asl/Nifti/'


for sub in slabel_list:
    ses = fw.lookup('davis/presurgicalEpilepsy/{}/ses-01'.format(sub))
    for acq in ses.acquisitions():
        if "SPIRAL" in acq.label and "ASL" in acq.label:
            print("{}: {}".format(sub, acq.label))
            file = [f for f in acq.files if ".nii.gz" in f.name]
            shortname = sub[0] + sub[2:]
            ASL_dir = os.path.join(data_dir, shortname, 'ASL_01')
            os.makedirs(ASL_dir)
            acq.download_file(file[0].name, ASL_dir + '/ASL.nii.gz')
            os.system('gunzip {}'.format(ASL_dir + '/ASL.nii.gz'))
        if "SPIRAL" in acq.label and "M0" in acq.label:
            print("{}: {}".format(sub, acq.label))
            file = [f for f in acq.files if ".nii.gz" in f.name]
            shortname = sub[0] + sub[2:]
            M0_dir = os.path.join(data_dir, shortname, 'M0_01')
            os.makedirs(M0_dir)
            acq.download_file(file[0].name, M0_dir + '/M0.nii.gz')
            os.system('gunzip {}'.format(M0_dir + '/M0.nii.gz'))
        if "T1w" in acq.label:
            print("{}: {}".format(sub, acq.label))
            file = [f for f in acq.files if ".nii.gz" in f.name]
            shortname = sub[0] + sub[2:]
            MPRAGE_dir = os.path.join(data_dir, shortname, 'MPRAGE')
            os.makedirs(MPRAGE_dir)
            acq.download_file(file[0].name, MPRAGE_dir + '/MPRAGE.nii.gz')
            os.system('gunzip {}'.format(MPRAGE_dir + '/MPRAGE.nii.gz'))
