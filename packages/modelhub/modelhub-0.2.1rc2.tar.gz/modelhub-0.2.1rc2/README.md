# Modelhub 

A CLI tool to manage your models.

## Commands

It takes a TensorFlow SaveModel file, uploads it with version and meta info, and checkouts it to local.

\- info model_name[@version_number]

\- create model_name -m "comment"

\- submit model_name -m "comment" [–batching_config=batching_config.txt] model_path

\- checkout model_name[@version_number]

\- deploy model_name[@version_number] [CPU/GPU] [online/offline] [instance-number] [offline]


## NTF models

ModelHub ogirinally supports uploading only TensorFlow-based models. From 0.0.8, it supports NTF models.

To prepare NTF models, you need create a new folder containing two subfolders: variables and assets

1. varibles: storing trained models
2. assets: storing any other data files, for example, feature dictionaries.


## Python API
pass
get model path by model name [and version]

checkout model