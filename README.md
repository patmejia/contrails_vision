#### Title:
# GOES-16 Satellite Contrail Detection using CV/ML

### Optimizing satellite imagery, [GOES-R ABI](https://www.star.nesdis.noaa.gov/goes/index.php), and advanced computer vision/machine learning for accurate detection of contrails

#### Absract:

##### The "OpenContrails: Benchmarking Contrail Detection" paper proposes a new contrail detection model, enhancing the study of climate change. The model, leveraging multiple frames for temporal context, improves detection performance and focuses on young, linear contrails. It utilizes the OpenContrails dataset, containing human-labeled contrail detections from the GOES-16 satellite, and confirms prior contrail research. The authors present the OpenContrails dataset and model as public benchmarks, promoting advances in contrail research. This work involves contributors from Google's Research Department and MIT's Laboratory for Aviation and the Environment.

![network-architecture](documentation/images/network-architecture.png)

> #### Q: Why focus on contrails to curb climate change impacts?
> #### Adam Durant: It’s not just direct engine emissions that matter in terms of aviation’s climate impacts. Non-carbon dioxide sources — like the climate forcing from contrails — make up almost two-thirds of the industry’s impact, which is a surprisingly big number. In fact, it equates to 2% of all human-caused climate change.
![detected-contrails-flights](documentation/images/detected-contrails-flights.png)

#### Name of dataset:
##### OpenContrails

##### The dataset contains 244,400 images of contrails and 244,400 images of non-contrails. The images are collected from the GOES-16 satellite over the United States from 2017 to 2019. The dataset is split into 195,520 training images, 24,440 validation images, and 24,440 test images. The dataset is available in TFRecord format and can be downloaded from the [Google Cloud Storage](https://console.cloud.google.com/storage/browser/goes_contrails_dataset) bucket. The dataset is also available on [Kaggle](https://www.kaggle.com/datasets/shashwatraman/contrails-images-ash-color) in JPEG format.

## ➲ Setup
```bash
conda create --name contrails_env python=3.8
conda activate contrails_env
pip install -r requirements.txt
```
---
### Kaggle api key (optional)
```bash
pip install kaggle
mkdir ~/.kaggle
mv /path/to/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
kaggle competitions list
```
##### ☛ Install the Kaggle CLI
##### ☛ Create a Kaggle account and go to your account settings page.
##### ☛ Click "Create New API Token" to download the `kaggle.json` file 
##### ☛  Move the downloaded file to `~/.kaggle/kaggle.json`
##### ☛ Set permissions for the API key file
##### ☛ Confirm the setup: Run kaggle competitions list to verify the API key works
---
### Download data (optional)
##### ☛ sample-dataset ▸ ash-color [22.4k files - 11.74 GB](https://www.kaggle.com/shashwatraman/contrails-images-ash-color)
```bash 
kaggle datasets download shashwatraman/contrails-images-ash-color -p /path/to/desired/directory
unzip contrails-images-ash-color.zip -d /path/to/desired/directory
rm contrails-images-ash-color.zip
```
##### ☛ full-dataset  ▸  OpenContrails [244.4k files - 450.91 GB](https://arxiv.org/pdf/2304.02122.pdf)

```bash
kaggle competitions download -c google-research-identify-contrails-reduce-gobal-warming
unzip google-research-identify-contrails-reduce-gobal-warming.zip
rm google-research-identify-contrails-reduce-gobal-warming.zip
```
---

## ➲ Run
```bash
conda activate contrails_env
python src/visualize.py --base_dir samples/sample_mini/contrails --n_records 5 --n_times_before 4
```
#### Stop
```bash
conda deactivate
```
---
### Acknowledgements:

###### 📌 arxiv: https://arxiv.org/abs/2304.02122
###### 📌 challenge-guide: https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming
###### ☛ contrails-labeling-guide: https://storage.googleapis.com/goes_contrails_dataset/20230419/Contrail_Detection_Dataset_Instruction.pdf
###### ☛ contrails dataset sample (11.74 GB) train_df.csv, valid_df.csv: https://www.kaggle.com/datasets/shashwatraman/contrails-images-ash-color
###### ☛ visualize (input dataset 450.91 GB): https://www.kaggle.com/code/inversion/visualizing-contrails#OpenContrails-dataset-documentation
###### ☛ high-score-example: https://www.kaggle.com/code/egortrushin/gr-icrgw-training-with-4-folds
###### ☛ Beginner's Guide to GOES-R Series Data: https://www.goes-r.gov/downloads/resources/documents/Beginners_Guide_to_GOES-R_Series_Data.pdf
###### ☛ GOES-R Series Product Definition and users' guide: [Level 2+ Algorithm Products, page 43](https://www.goes-r.gov/products/docs/PUG-L2+-vol5.pdf)

###### ☛ GOES-16 (Geostationary Operational Environmental Satellite, Launch Date: Nov. 19, 2016): https://eospso.nasa.gov/missions/geostationary-operational-environmental-satellite-16
###### ☛ GOES-16 Band Reference Guide: https://www.weather.gov/media/crp/GOES_16_Guides_FINALBIS.pdf
###### ☛ Using Python to Explore GOES-16 Data: https://edc.occ-data.org/goes16/python/
###### ☛ Adam Duran (Michigan Tech, Q&A with SATAVIA: Climate and Contrails): https://www.mtu.edu/unscripted/2021/06/qa-with-satavia-climate-and-contrails.html
###### ☛ catalogues of atmospheric optics (rocket plume, contrail shadow): https://atoptics.co.uk/atoptics/shuttle.htm, https://atoptics.co.uk/atoptics/contr1.htm
###### ☛  U-Net: Convolutional Networks for Biomedical Image Segmentation: https://arxiv.org/abs/1505.04597
###### ☛ Using U-Net to Predict Segmentation Masks in Python & Keras: https://www.kaggle.com/keegil/keras-u-net-starter-lb-0-277