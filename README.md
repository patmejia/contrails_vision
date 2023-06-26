#### Title:
# GOES-16 Satellite Contrail Detection using CV/ML

### Optimizing satellite imagery, [GOES-R ABI](https://www.star.nesdis.noaa.gov/goes/index.php), and advanced computer vision/machine learning for accurate detection of contrails


#### Description:

##### Connecting machine learning (ML) and computer vision (CV) techniques to detect contrails in GOES-16 satellite data, providing valuable insights for climate change research. The contrail detection model integrates various features such as darkness, linearity, appearance, size, movement, aging, color, and flight path alignment. Additionally, strategies to mitigate contrail formation, including altitude adjustments, optimized flight paths, schedule modifications, improved efficiency, exploration of alternative fuels, and advanced weather forecasts, are considered. The availability of the OpenContrails dataset and the proposed contrail detection model contribute to advancing contrail research and promoting sustainable practices in the aviation industry.

![network-architecture](documentation/images/network-architecture.png)

> #### Q: Why focus on contrails to curb climate change impacts?
> #### Adam Durant: It’s not just direct engine emissions that matter in terms of aviation’s climate impacts. Non-carbon dioxide sources — like the climate forcing from contrails — make up almost two-thirds of the industry’s impact, which is a surprisingly big number. In fact, it equates to 2% of all human-caused climate change.
![detected-contrails-flights](documentation/images/detected-contrails-flights.png)

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
###### ☛ Adam Duran (Michigan Tech, Q&A with SATAVIA: Climate and Contrails): https://www.mtu.edu/unscripted/2021/06/qa-with-satavia-climate-and-contrails.html
###### ☛ contrails-labeling-guide: https://storage.googleapis.com/goes_contrails_dataset/20230419/Contrail_Detection_Dataset_Instruction.pdf
###### ☛ catalogues of atmospheric optics (rocket plume, contrail shadow): https://atoptics.co.uk/atoptics/shuttle.htm, https://atoptics.co.uk/atoptics/contr1.htm
###### ☛ high-score-example: https://www.kaggle.com/code/egortrushin/gr-icrgw-training-with-4-folds
###### ☛ visualize (input dataset 450.91 GB): https://www.kaggle.com/code/inversion/visualizing-contrails#OpenContrails-dataset-documentation
###### ☛ GOES-16 (Geostationary Operational Environmental Satellite, Launch Date: Nov. 19, 2016): https://eospso.nasa.gov/missions/geostationary-operational-environmental-satellite-16
###### ☛ contrails dataset sample (11.74 GB) train_df.csv, valid_df.csv: https://www.kaggle.com/datasets/shashwatraman/contrails-images-ash-color
