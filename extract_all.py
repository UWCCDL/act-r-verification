import os
import numpy as np
import pandas as pd
from nilearn import image
from nilearn.image import load_img
from nilearn.masking import apply_mask
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


subjs = [i for i in os.listdir("data") if i.startswith("sub-")]
rois = [i for i in os.listdir("ROIs") if i.endswith("nii.gz")]
roi_masks = [image.load_img(os.path.join("ROIs", roi)) for roi in rois]


def extract_pca_component(img, mask):
    # extract ROI
    data = apply_mask(img, image.index_img(mask, 0))
    # normalized data
    scaler = StandardScaler()
    normalized = scaler.fit_transform(data)
    # pca
    pca = PCA(n_components=1)
    pca.fit(normalized)
    # force eigenvalue to be positive
    if np.all(pca.components_ < 0):
        pca.components_ = -1 * pca.components_
    projected = pca.transform(data)
    # variance 
    var_projected = np.sum(np.var(projected, axis=0))
    var_original = np.sum(np.var(data, axis=0)) 
    return projected, var_projected / var_original


def create_time_series(subj, rois, roi_masks, roi_variance):
    # write dataframe out to csv
    img = image.load_img(os.path.join("data", subj, "func", "swa" + subj + "_task-stroop_bold.nii"))
    rois = [i for i in os.listdir("ROIs") if i.endswith(".nii.gz")]
    data = []
    for idx, roi_mask in enumerate(roi_masks):
        projected, var_percentage = extract_pca_component(img, roi_mask) 
        data.append(projected)
        roi_variance[rois[idx]].append(var_percentage)

    df = pd.DataFrame(np.column_stack(data), columns=rois)
    df.to_csv(subj + ".csv", index=None)


roi_variance = {i:[] for i in rois}
for subj in subjs:
    create_time_series(subj, rois, roi_masks, roi_variance)
new_df = pd.DataFrame(roi_variance)
new_df.to_csv("pca_stats.csv")

