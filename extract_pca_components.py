import os
import numpy as np
import pandas as pd
from nilearn import image
from nilearn.image import load_img
from nilearn.masking import apply_mask
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def extract_pca_component(img, mask):
    # extract ROI
    data = apply_mask(img, image.index_img(mask, 0))
    # normalized data
    scaler = StandardScaler()
    normalized = scaler.fit_transform(data)
    # pca
    pca = PCA(n_components=1)
    pca.fit(normalized)
    projected = pca.transform(data)
    return projected


def create_time_series():
    # write dataframe out to csv
    rois = [i for i in os.listdir("ROIs") if i.endswith(".nii.gz")]
    data = []
    for roi in rois:
        mask = image.load_img(os.path.join("ROIs", roi)) 
        data.append(extract_pca_component(img, mask))

    rois = [i[:-7] for i in os.listdir("ROIs") if i.endswith(".nii.gz")]
    df = pd.DataFrame(np.column_stack(data), columns=rois)
    df.to_csv("testing.csv", index=None)


if __name__ == '__main__':
    # for subj in ['001', '002', '003', '004', '005']:
    subj = '001'
    img = load_img("data/sub-{}/func/swasub-{}_task-stroop_bold.nii".format(subj, subj))
    print("###")
    print("subject {}".format(subj))
    create_time_series()
        
            