import os
import sys

module = ['visual', 'imaginal', 'manual', 'retrieval', 'procedual', 'goal']
coords = [(60, 26, 17), (51, 22, 47), (60, 44, 52), (60, 68, 37), (46, 62, 25), (42, 60, 45)]

for m, coordinates in zip(module, coords):
    left_cmd = "fslmaths ref.nii -mul 0 -add 1 -roi {} 1 {} 1 {} 1 0 1 {} -odt float".format(coordinates[0], coordinates[1], coordinates[2], m + "_temp")
    os.system(left_cmd)
    if m == 'goal':
        size = '4'
    else:
        size = '8'
    left_cmd = "fslmaths {} -kernel box {} -fmean {} -odt float".format(m + "_temp.nii.gz", size, m)
    os.system(left_cmd)
    # remove temp file
    os.system("rm " + m + "_temp.nii.gz")
    print("{} module done".format(m))
    sys.stdout.flush()

