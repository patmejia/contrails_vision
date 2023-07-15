# Contrail Analysis Roadmap

<center>

"Accurate contrail detection through robust insights."
 <br> - i.e., $\{∃ \text{ data | partition, differentiate : contrails vs. clouds}\}$

</center>

---

- **Data Acquisition and Preparation**
  - Get and organize data.
  - Understand data structure, contents, labels.
  - Explore data: Record count, samples, value range.
  - Check data presence, consistency.
  
- **Data Quality and Integrity**
  - Quality checks: Visual inspection, distributions, label validation, class imbalance, metadata, outliers.
  - Clean data: Missing values, duplicates, errors.
  - Identify patterns.
  - Transform data: One-hot encoding, normalization, feature creation.
  
- **Model Selection, Training, and Evaluation**
  - Select appropriate models.
  - Advanced analysis: Contrail pixel proportion, mean Dice coefficient, summary stats, band correlation, machine learning, performance metrics.
  - Adjust based on evaluation results.
  
- **Data Preservation and Model Deployment**
  - Preserve data.
  - Deploy model, make predictions.

---
- **Keywords**
  - Data Loading, Exploration, Cleaning, Transformation, Storage, Integrity, Class Imbalance, Outliers, One-Hot Encoding, Normalization, Feature Engineering, Correlation Analysis, Machine Learning, Data Leakage, Performance Metrics, Climate Change, Contrails, Satellite Imagery, GOES-16, ABI, NOAA, MIT, Google Research, OpenContrail, Kaggle.
  ---
- **Libraries/Tools**
  - NumPy, Pandas, Matplotlib/Seaborn, Scikit-learn.
  
- **Goal**
  - Boost contrail model accuracy, minimize contrail formation, reduce climate impact.
  
- **Context**
  - Contrails - ice crystal clouds from aircraft exhaust, contribute to global warming. Competition - validate contrail prediction models using satellite imagery, enable reliable contrail avoidance.
  ---
- **Acknowledgments**
  - MIT Laboratory, Google Research, NOAA GOES-16.
  ---
- **Competition Evaluation**
  - Global Dice coefficient - pixel-wise agreement between predicted and ground truth segmentations.
  
- **Submission Format**
  - Run-length encoding - reduce submission file size, header and space-delimited pairs for start position and run length. Empty predictions marked with '-'.
  
- **Dataset**
  - Geostationary images from GOES-16 ABI, 10-minute intervals. Training data - labeled frames, individual/human masks, aggregated ground truth annotations. Validation data - only aggregated ground truth annotations. 
  
- **OpenContrails Dataset - Creation Methodology**
  - Image Collection: GOES-16 ABI - high-resolution images.
  - Labeling: Human labelers - contrail images using brightness temperature difference (BTD) map.
  - Contrail Detection Model: U-Net architecture model - temporal context.
  - Model Training: Model trained on human-labeled images, AUC score of 0.63 on test set.
  - Model Evaluation: Model tested on multiple years of GOES-16 images, confirmed previous findings.
  - Model Output Availability: Outputs available on Google Cloud Storage at gs://goes_contrails_dataset.
  ---
- **Reference**
  - [OpenContrails: Benchmarking Contrail Detection on GOES-16 ABI](https://arxiv.org/abs/2304.02122) - Ng, J. Y.-H., McCloskey, K., Cui, J., Meijer, V., Brand, E., Sarna, A., Goyal, N., Van Arsdale, C., & Geraedts, S. (2023).