import os
import sys

module = ['visual', 'imaginal', 'manual', 'retrieval']
coords = [((60, 17), 26, 17), ((51, 27), 22, 47), ((60, 18), 44, 52), ((60, 17), 68, 37)]

for m, coordinates in zip(module, coords):
    left_cmd = "fslmaths ref.nii -mul 0 -add 1 -roi {} 1 {} 1 {} 1 0 1 {} -odt float".format(coordinates[0][0], coordinates[1], coordinates[2], "left_" + m + "_temp")
    os.system(left_cmd)
    left_cmd = "fslmaths {} -kernel box 8 -fmean {} -odt float".format("left_" + m + "_temp.nii.gz", "left_" + m)
    os.system(left_cmd)
    right_cmd = "fslmaths ref.nii -mul 0 -add 1 -roi {} 1 {} 1 {} 1 0 1 {} -odt float".format(coordinates[0][1], coordinates[1], coordinates[2], "right_" + m + "_temp")
    os.system(right_cmd)
    right_cmd = "fslmaths {} -kernel box 8 -fmean {} -odt float".format("right_" + m + "_temp.nii.gz", "right_" + m)
    os.system(right_cmd)
    # remove temp file
    os.system("rm left_" + m + "_temp.nii.gz")
    os.system("rm right_" + m + "_temp.nii.gz")
    print("{} module done".format(m))
    sys.stdout.flush()


