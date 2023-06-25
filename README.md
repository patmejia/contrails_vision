#### Title:
# GOES16 Contrail Detection with Computer Vision

#### Description:

#### Harnessing machine learning and computer vision techniques, this project discerns contrails within GOES-16 satellite data, thereby supplying critical knowledge for climate change studies and global warming countermeasures. It exemplifies the conversion of intricate satellite data into data-driven, impactful environmental solutions.

![network-architecture](documentation/images/network-architecture.png)

> #### Q: Why focus on contrails to curb climate change impacts?
> #### Adam Durant: It’s not just direct engine emissions that matter in terms of aviation’s climate impacts. Non-carbon dioxide sources — like the climate forcing from contrails — make up almost two-thirds of the industry’s impact, which is a surprisingly big number. In fact, it equates to 2% of all human-caused climate change.
![detected-contrails-flights](documentation/images/detected-contrails-flights.png)

## Setup
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

## Run
```bash
conda activate contrails_env
python src/visualize.py --base_dir samples/sample1 --n_records 5 --n_times_before 4
```
#### Stop
```bash
conda deactivate
```
