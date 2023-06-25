Title:
# GOES16 Contrail Detection with Computer Vision

Description:

Harnessing machine learning and computer vision techniques, this project discerns contrails within GOES-16 satellite data, thereby supplying critical knowledge for climate change studies and global warming countermeasures. It exemplifies the conversion of intricate satellite data into data-driven, impactful environmental solutions.


## setup
### environment

```bash
conda create --name contrails_env python=3.8
conda activate contrails_env
pip install -r requirements.txt
```
### download data

```bash
conda activate contrails_env
mkdir ~/.kaggle
mv /path/to/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json  
```
contrails dataset sample [(11.74 GB)](https://www.kaggle.com/shashwatraman/contrails-images-ash-color):
```bash 
kaggle datasets download shashwatraman/contrails-images-ash-color -p /path/to/desired/directory
unzip contrails-images-ash-color.zip -d /path/to/desired/directory
rm contrails-images-ash-color.zip
```
OpenContrails: dataset [(244400 files -
450.91 GB)](https://arxiv.org/pdf/2304.02122.pdf):

```bash
kaggle competitions download -c google-research-identify-contrails-reduce-gobal-warming
unzip google-research-identify-contrails-reduce-gobal-warming.zip
rm google-research-identify-contrails-reduce-gobal-warming.zip
```


## run

```bash
conda activate contrails_env
python src/visualize.py --base_dir samples/sample1 --n_records 5 --n_times_before 4
```

## stop

```bash
conda deactivate
```
