import argparse
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def rle_encode(image, foreground_value=1):
    dots = np.where(image.T.flatten() == foreground_value)[0]
    run_lengths = []
    prev = -2
    for dot in dots:
        if (dot > prev + 1): run_lengths.extend((dot + 1, 0))
        run_lengths[-1] += 1
        prev = dot
    return run_lengths

def rle_to_string(rle):
    return '-'.join(map(str, rle)) if rle else '-'

def create_mask(data_path, record, num_pixels, shape=(256, 256)):
    band_08 = np.load(data_path / 'test' / record / 'band_08.npy').sum(axis=2)
    preds = np.c_[np.unravel_index(np.argpartition(band_08.ravel(), -num_pixels)[-num_pixels:], band_08.shape)]
    mask = np.zeros(shape)
    mask[preds[:, 0], preds[:, 1]] = 1
    return mask

def visualize_mask(mask, output_dir, record):
    plt.imshow(mask, cmap='Greys')
    plt.title("Obviously Not Contrails")
    plt.savefig(output_dir / f'{record}.png')

def prepare_submission(submission, record, mask):
    rle_mask = rle_encode(mask)
    submission.loc[int(record), 'encoded_pixels'] = rle_to_string(rle_mask)

def main(data_path, num_plots):
    data_path = Path(data_path)
    test_records = [entry.name for entry in data_path.glob('test/*') if entry.is_dir()]
    print(f'Found {len(test_records)} test records with IDs: {", ".join(test_records)}')
    num_pixels = 1000
    submission_file = Path('output') / 'submission.csv'
    if submission_file.exists():
        submission_file.unlink()
    submission = pd.DataFrame(columns=['record_id', 'encoded_pixels'])
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    submission.to_csv(output_dir / 'submission.csv', index=False)
    for i, record in enumerate(test_records):
        mask = create_mask(data_path, record, num_pixels)
        if i < num_plots:
            visualize_mask(mask, Path('output'), record)
        prepare_submission(submission, record, mask)
    submission.to_csv(Path('output') / 'submission.csv', index=False)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('data_path', type=str,
						help='Path to data directory')
	parser.add_argument('num_plots', type=int,
						help='Number of plots to visualize')
	args = parser.parse_args()
	main(args.data_path,args.num_plots)
 
# Usage: `python src/utils/rle_encoding_submission.py samples/kaggle_competition_mini_sample 2``
