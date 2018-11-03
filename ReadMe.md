# Data-Driven Verification of ACT-R

## ROIs used
See `ROI_voxels.txt` for the voxel locations used (in FSL). The command to create the ROIs is:
```
fslmaths avg152T1.nii.gz -mul 0 -add 1 -roi [x_coor] 1 [y_coor] 1 [z_coor] 1 0 1 [output_name] -odt float
fslmaths [output_name] -kernel box [mm size] -fmean [output_name] -odt float
```


