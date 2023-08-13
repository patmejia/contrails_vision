import sys
import time
import os
from azure.storage.blob import BlobServiceClient

# Read environment variables
ACCOUNT_URL = os.getenv('AZURE_ACCOUNT_URL', "https://goeseuwest.blob.core.windows.net/")
CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME', "noaa-goes16")

# Create BlobServiceClient instance
def configure_blob_service_client():
    return BlobServiceClient(account_url=ACCOUNT_URL)

# Validate command-line arguments
def validate_arguments():
    if len(sys.argv) != 6:
        print(f"Usage: python {sys.argv[0]} product year day start_hour end_hour")
        sys.exit(1)

    product = sys.argv[1]
    year = int(sys.argv[2])
    day = int(sys.argv[3])
    start_hour = int(sys.argv[4])
    end_hour = int(sys.argv[5])

    if product not in PRODUCT_LIST:
        print(f"Invalid product: {product}")
        sys.exit(1)

    if year < 1970 or day < 1 or day > 366 or start_hour < 0 or start_hour > 23 or end_hour < 0 or end_hour > 23:
        print("Invalid date or time range.")
        sys.exit(1)

# Print blob names and count
def print_blobs(container_client, prefix):
    blobs = container_client.list_blobs(name_starts_with=prefix)
    return sum(1 for blob in blobs)

# Search blobs and print details
def find_data(blob_service_client, product, year, day, start_hour, end_hour):
    try:
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_count = 0
        for hour in range(start_hour, end_hour + 1):
            prefix = f"{product}/{year}/{day:03d}/{hour:02d}/"
            print(f"Searching in container: {CONTAINER_NAME} with prefix: {prefix}")
            blob_count += print_blobs(container_client, prefix)

        if blob_count == 0:
            print("No matching blobs found.")

        return blob_count
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

# List of available products
PRODUCT_LIST = [
    "ABI-L2-CMIPC", "ABI-L2-CMIPF", "ABI-L2-CMIPM",
    "ABI-L2-FDCC", "ABI-L2-FDCF", "ABI-L2-LSTC",
    "ABI-L2-LSTF", "ABI-L2-LSTM", "ABI-L2-MCMIPC",
    "ABI-L2-MCMIPF", "ABI-L2-MCMIPM", "ABI-L2-RRQPEF",
    "ABI-L2-SSTF", "GLM-L2-LCFA"
]

# Main function
if __name__ == "__main__":
    validate_arguments()
    product, year, day, start_hour, end_hour = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    start_time = time.time()
    blob_service_client = configure_blob_service_client()

    find_data(blob_service_client, product, year, day, start_hour, end_hour)

    print(f"Process completed in {time.time() - start_time:.2f} seconds.")
