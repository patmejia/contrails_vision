## `goes16_data.py`

### **Overview**
- A script to search and count data blobs in NOAA GOES-R weather imagery.
- Specific products, dates, and hours can be targeted.

### **Requirements**
- Python 3.x
- Azure Storage Blob Python SDK

### **Environment Variables**
- `AZURE_ACCOUNT_URL`: URL to Azure Blob Storage (default: https://goeseuwest.blob.core.windows.net/).
- `AZURE_CONTAINER_NAME`: Container name in Azure Blob Storage (default: noaa-goes16).

### **Command-Line Arguments for `get goes16_data.get_index`**
- `product`: Name of GOES-R product (e.g., ABI-L2-CMIPC).
- `year`: Four-digit year (e.g., 2021).
- `day`: Three-digit day-of-year code (e.g., 001).
- `start_hour`: Two-digit start hour (e.g., 08).
- `end_hour`: Two-digit end hour (e.g., 15).

### **Functionality**
- Validates command-line arguments.
- Configures Azure Blob Storage client.
- Searches specified container for blobs with given prefix.
- Prints details of matching blobs and counts them.
- Handles Azure Blob Storage-related errors.

### **Usage**
1. **Preparation**
- **External Dataset**: [NOAA GOES-R weather imagery](https://microsoft.github.io/AIforEarthDataSets/data/goes-r.html)
- **Environment Setup**:
```bash
conda create --name contrail_env python=3.8
conda activate contrail_env
pip install azure-storage-blob
```

2. **Example Run**:
- **Command**:
```bash
python src/goes16_data/get_index.py ABI-L2-CMIPF 2021 001 08 15
```

- **Output**:
```bash
Searching in container: noaa-goes16 with prefix: ABI-L2-CMIPF/2021/001/08/
...
Process completed in 3.10 seconds.
```

- **Note**: The product must be one of the available GOES-R products, date and time must be within valid ranges.

3. **Available Products**:
```python
PRODUCT_LIST = [
"ABI-L2-CMIPC", "ABI-L2-CMIPF", "ABI-L2-CMIPM",
"ABI-L2-FDCC", "ABI-L2-FDCF", "ABI-L2-LSTC",
"ABI-L2-LSTF", "ABI-L2-LSTM", "ABI-L2-MCMIPC",
"ABI-L2-MCMIPF", "ABI-L2-MCMIPM", "ABI-L2-RRQPEF",
"ABI-L2-SSTF", "GLM-L2-LCFA"
]
```

### **Output Details**
- Displays search results for specified parameters.
- Prints total processing time.