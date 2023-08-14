## goes16_data.py
*•* **Overview**: A script to search and count data blobs in NOAA GOES-R weather imagery for specific products, dates, and hours.
*•* **Requirements**: Azure Storage Blob Python SDK, Python 3.x.
*•* **Environment Variables**:
  *•* `AZURE_ACCOUNT_URL`: URL to the Azure Blob Storage account (default: https://goeseuwest.blob.core.windows.net/).
  *•* `AZURE_CONTAINER_NAME`: Name of the container in Azure Blob Storage (default: noaa-goes16).
*•* **Command-Line Arguments**: 
  *•* `product`: Name of the GOES-R product (e.g., ABI-L2-CMIPC).
  *•* `year`: Four-digit year (e.g., 2021).
  *•* `day`: Three-digit day-of-year code (e.g., 001).
  *•* `start_hour`: Two-digit start hour (e.g., 08).
  *•* `end_hour`: Two-digit end hour (e.g., 15).
*•* **Functionality**:
  *•* Validates command-line arguments for correctness.
  *•* Configures Azure Blob Storage client.
  *•* Searches the specified container for blobs with the given prefix.
  *•* Prints the details of matching blobs and counts them.
  *•* Handles errors related to Azure Blob Storage.
*•* **Usage Example**:
  ```
 python src/goes16_data/get_index.py ABI-L2-CMIPF 2021 001 08 15
  ```
*•* **Output**: Displays the search results for the specified parameters and prints the total processing time.
*•* **Note**: The product must be one of the available GOES-R products, and the date and time must be within valid ranges:
```python
# List of available products
PRODUCT_LIST = [
    "ABI-L2-CMIPC", "ABI-L2-CMIPF", "ABI-L2-CMIPM",
    "ABI-L2-FDCC", "ABI-L2-FDCF", "ABI-L2-LSTC",
    "ABI-L2-LSTF", "ABI-L2-LSTM", "ABI-L2-MCMIPC",
    "ABI-L2-MCMIPF", "ABI-L2-MCMIPM", "ABI-L2-RRQPEF",
    "ABI-L2-SSTF", "GLM-L2-LCFA"
]
```
