# How to make a submission using the Run-Length Encoding format
import os
import numpy as np
import pandas as pd
import argparse

import matplotlib.pyplot as plt

from pathlib import Path

## Argparse Code
parser = argparse.ArgumentParser(description='Process the given file path')
parser.add_argument('data_path', type=str, help='The data file path')
args = parser.parse_args()
data_path = Path(args.data_path)

## Run-Length Code

# The rest of your code

## Create a naive submission

test_recs = os.listdir(data_path / 'test')
n = 1000
band_08 = np.load(data_path / 'test' / test_recs[0] / 'band_08.npy').sum(axis=2)
preds = np.c_[np.unravel_index(np.argpartition(band_08.ravel(),-n)[-n:],band_08.shape)]
mask = np.zeros((256, 266))
mask[preds[:, 0], preds[:, 1]] = 1

## Convert to RLE
list_to_string(rle_encode(mask))

## Now let's automate a submission
submission = pd.read_csv(data_path / 'sample_submission.csv', index_col='record_id')

for rec in test_recs:
    band_08 = np.load(data_path / 'test' / rec / 'band_08.npy').sum(axis=2)
    preds = np.c_[np.unravel_index(np.argpartition(band_08.ravel(),-n)[-n:],band_08.shape)]
    mask = np.zeros((256, 266))
    mask[preds[:, 0], preds[:, 1]] = 1
    submission.loc[int(rec), 'encoded_pixels'] = list_to_string(rle_encode(mask))

submission.head()
submission.to_csv('submission.csv')
