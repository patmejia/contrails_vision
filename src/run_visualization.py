import os
import argparse
import subprocess
import random

def main():
    parser = argparse.ArgumentParser(description='Run contrails visualization for random records')
    parser.add_argument('--base_dir', type=str, required=True, help='Base directory for the data')
    parser.add_argument('--n_records', type=int, default=5, help='Number of records to display')
    parser.add_argument('--n_times_before', type=int, default=4, help='Number of images before the labeled frame')
    args = parser.parse_args()

    contrails_dir = os.path.join(args.base_dir, 'contrails')
    record_ids = [f[:-4] for f in os.listdir(contrails_dir) if f.endswith('.npy')]  # Extract record IDs from .npy files
    print(f'Found {len(record_ids)} records')

    # Check if n_records is greater than the total number of records
    if args.n_records > len(record_ids):
        args.n_records = len(record_ids)

    # Pick n_records random record_ids
    random_record_ids = random.sample(record_ids, args.n_records)

    for record_id in random_record_ids:
        print(f'Displaying record_id: {record_id}')
        subprocess.run(['python', 'src/visualizing_contrails.py', '--base_dir', args.base_dir, '--n_times_before', str(args.n_times_before), '--record_id', record_id])

if __name__ == '__main__':
    main()
