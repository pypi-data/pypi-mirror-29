Generated from [nbs/python-api.ipynb](https://github.com/kipoi/kipoi/blob/master/nbs/python-api.ipynb)

# Kipoi python API

## Quick start

There are three basic building blocks in kipoi:

- **Source** - provides Models and DataLoaders.
- **Model** - makes the prediction given the numpy arrays. 
- **Dataloader** - loads the data from raw files and transforms them into a form that is directly consumable by the Model

![img](/img/kipoi-workflow.png)

## List of main commands


- `kipoi.list_sources()`
- `kipoi.get_source()`


- `kipoi.list_models()`
- `kipoi.list_dataloaders()`


- `kipoi.get_model()`
- `kipoi.get_dataloader_factory()`



### Source

Available sources are specified in the config file located at: `~/.kipoi/config.yaml`. Here is an example config file:

```yaml
model_sources:
    kipoi: # default
        type: git-lfs # git repository with large file storage (git-lfs)
        remote_url: git@github.com:kipoi/models.git # git remote
        local_path: ~/.kipoi/models/ # local storage path
    gl:
        type: git-lfs  # custom model
        remote_url: https://i12g-gagneurweb.informatik.tu-muenchen.de/gitlab/gagneurlab/model-zoo.git
        local_path: /s/project/model-zoo
```

There are three different model sources possible: 

- **`git-lfs`** - git repository with source files tracked normally by git and all the binary files like model weights (located in `files*` directories) are tracked by [git-lfs](https://git-lfs.github.com). 
  - Requires `git-lfs` to be installed.
- **`git`** - all the files including weights (not recommended)
- **`local`** - local directory containing models defined in subdirectories

For **`git-lfs`** source type, larger files tracked by `git-lfs` will be downloaded into the specified directory `local_path` only after the model has been requested (when invoking `kipoi.get_model()`).

#### Note

A particular model/dataloader is defined by its source (say `kipoi` or `my_git_models`) and the relative path of the desired model directory from the model source root (say `rbp/`).

A directory is considered a model if it contains a `model.yaml` file.


```python
import kipoi
```


```python
import warnings
warnings.filterwarnings('ignore')

import logging
logging.disable(1000)
```


```python
kipoi.list_sources()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>source</th>
      <th>type</th>
      <th>location</th>
      <th>local_size</th>
      <th>n_models</th>
      <th>n_dataloaders</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>kipoi</td>
      <td>git-lfs</td>
      <td>/home/avsec/.kipoi/mo...</td>
      <td>8,6G</td>
      <td>779</td>
      <td>779</td>
    </tr>
  </tbody>
</table>
</div>




```python
s = kipoi.get_source("kipoi")
```


```python
s
```




    GitLFSSource(remote_url='git@github.com:kipoi/models.git', local_path='/home/avsec/.kipoi/models/')




```python
kipoi.list_models()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>source</th>
      <th>model</th>
      <th>version</th>
      <th>authors</th>
      <th>doc</th>
      <th>type</th>
      <th>inputs</th>
      <th>targets</th>
      <th>license</th>
      <th>cite_as</th>
      <th>trained_on</th>
      <th>training_procedure</th>
      <th>tags</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>kipoi</td>
      <td>DeepSEAKeras</td>
      <td>0.1</td>
      <td>[Author(name='Lara Ur...</td>
      <td>This CNN is based on ...</td>
      <td>keras</td>
      <td>seq</td>
      <td>TFBS_DHS_probs</td>
      <td>MIT</td>
      <td>https://doi.org/10.10...</td>
      <td>ENCODE and Roadmap Ep...</td>
      <td>https://www.nature.co...</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>kipoi</td>
      <td>extended_coda</td>
      <td>0.1</td>
      <td>[Author(name='Johnny ...</td>
      <td>Single bp resolution ...</td>
      <td>keras</td>
      <td>[H3K27AC_subsampled]</td>
      <td>[H3K27ac]</td>
      <td>MIT</td>
      <td>https://doi.org/10.10...</td>
      <td>Described in https://...</td>
      <td>Described in https://...</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>kipoi</td>
      <td>DeepCpG_DNA/Hou2016_m...</td>
      <td>1.0.4</td>
      <td>[Author(name='Christo...</td>
      <td>This is the extractio...</td>
      <td>keras</td>
      <td>[dna]</td>
      <td>[cpg/mESC1, cpg/mESC2...</td>
      <td>MIT</td>
      <td>https://doi.org/10.11...</td>
      <td>scBS-seq and scRRBS-s...</td>
      <td>Described in https://...</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>780</th>
      <td>kipoi</td>
      <td>CpGenie/SK_N_SH_ENCSR...</td>
      <td>0.1</td>
      <td>[Author(name='Haoyang...</td>
      <td>Abstract: DNA methyla...</td>
      <td>keras</td>
      <td>seq</td>
      <td>methylation_prob</td>
      <td>Apache License v2</td>
      <td>https://doi.org/10.10...</td>
      <td>RRBS (restricted repr...</td>
      <td>RMSprop</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>781</th>
      <td>kipoi</td>
      <td>CpGenie/SK_N_SH_ENCSR...</td>
      <td>0.1</td>
      <td>[Author(name='Haoyang...</td>
      <td>Abstract: DNA methyla...</td>
      <td>keras</td>
      <td>seq</td>
      <td>methylation_prob</td>
      <td>Apache License v2</td>
      <td>https://doi.org/10.10...</td>
      <td>RRBS (restricted repr...</td>
      <td>RMSprop</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>782</th>
      <td>kipoi</td>
      <td>CpGenie/HEK293_ENCSR0...</td>
      <td>0.1</td>
      <td>[Author(name='Haoyang...</td>
      <td>Abstract: DNA methyla...</td>
      <td>keras</td>
      <td>seq</td>
      <td>methylation_prob</td>
      <td>Apache License v2</td>
      <td>https://doi.org/10.10...</td>
      <td>RRBS (restricted repr...</td>
      <td>RMSprop</td>
      <td>[]</td>
    </tr>
  </tbody>
</table>
<p>779 rows × 13 columns</p>
</div>



## Model

Let's choose to use the `rbp_eclip/UPF1` model from kipoi


```python
# Note. Install all the dependencies for that model using
# kipoi env install 
model = kipoi.get_model("rbp_eclip/UPF1")
```

### Available fields:

#### Model

- type
- args
- info
  - authors
  - name
  - version
  - tags
  - doc
- schema
  - inputs
  - targets
- default_dataloader - loaded dataloader class


- predict_on_batch()
- source
- source_dir
- pipeline
  - predict()
  - predict_example()
  - predict_generator()
  
#### Dataloader

- type
- defined_as
- args
- info (same as for the model)
- output_schema
  - inputs
  - targets
  - metadata


- source
- source_dir
- example_kwargs
- init_example()
- batch_iter()
- batch_train_iter()
- batch_predict_iter()
- load_all()


```python
model
```




    <kipoi.model.KerasModel at 0x7f60ef774dd8>




```python
model.type
```




    'keras'



### Info


```python
model.info
```




    ModelInfo(authors=[Author(name='Ziga Avsec', github='avsecz', email=None)], doc='\'RBP binding model from Avsec et al: "Modeling positional effects of regulatory sequences with spline transformations increases prediction accuracy of deep neural networks". \'
', name=None, version='0.1', license='MIT', tags=[], cite_as='https://doi.org/10.1093/bioinformatics/btx727', trained_on='RBP occupancy peaks measured by eCLIP-seq (Van Nostrand et al., 2016 - https://doi.org/10.1038/nmeth.3810), https://github.com/gagneurlab/Manuscript_Avsec_Bioinformatics_2017
', training_procedure='Single task training with ADAM')




```python
model.info.version
```




    '0.1'



### Schema


```python
dict(model.schema.inputs)
```




    {'dist_exon_intron': ArraySchema(shape=(1, 10), doc='Distance the nearest exon_intron (splice donor) site transformed with B-splines', name='dist_exon_intron', special_type=None, associated_metadata=[], column_labels=None),
     'dist_gene_end': ArraySchema(shape=(1, 10), doc='Distance the nearest gene end transformed with B-splines', name='dist_gene_end', special_type=None, associated_metadata=[], column_labels=None),
     'dist_gene_start': ArraySchema(shape=(1, 10), doc='Distance the nearest gene start transformed with B-splines', name='dist_gene_start', special_type=None, associated_metadata=[], column_labels=None),
     'dist_intron_exon': ArraySchema(shape=(1, 10), doc='Distance the nearest intron_exon (splice acceptor) site transformed with B-splines', name='dist_intron_exon', special_type=None, associated_metadata=[], column_labels=None),
     'dist_polya': ArraySchema(shape=(1, 10), doc='Distance the nearest Poly-A site transformed with B-splines', name='dist_polya', special_type=None, associated_metadata=[], column_labels=None),
     'dist_start_codon': ArraySchema(shape=(1, 10), doc='Distance the nearest start codon transformed with B-splines', name='dist_start_codon', special_type=None, associated_metadata=[], column_labels=None),
     'dist_stop_codon': ArraySchema(shape=(1, 10), doc='Distance the nearest stop codon transformed with B-splines', name='dist_stop_codon', special_type=None, associated_metadata=[], column_labels=None),
     'dist_tss': ArraySchema(shape=(1, 10), doc='Distance the nearest TSS site transformed with B-splines', name='dist_tss', special_type=None, associated_metadata=[], column_labels=None),
     'seq': ArraySchema(shape=(101, 4), doc='One-hot encoded RNA sequence', name='seq', special_type=<ArraySpecialType.DNASeq: 'DNASeq'>, associated_metadata=[], column_labels=None)}




```python
model.schema.targets
```




    ArraySchema(shape=(1,), doc='Predicted binding strength', name=None, special_type=None, associated_metadata=[], column_labels=None)



### Default dataloader

Model already has the default dataloder present. To use it, specify


```python
model.source_dir
```




    '/home/avsec/.kipoi/models/rbp_eclip/UPF1'




```python
model.default_dataloader
```




    dataloader.SeqDistDataset




```python
model.default_dataloader.info
```




    Info(authors=[Author(name='Ziga Avsec', github='avsecz', email=None)], doc='RBP binding prediction for UPF1 protein', name=None, version='0.1', license='MIT', tags=[])



### Predict_on_batch


```python
model.predict_on_batch
```




    <bound method KerasModel.predict_on_batch of <kipoi.model.KerasModel object at 0x7f60ef774dd8>>



### Pipeline

Pipeline object will take the dataloader arguments and run the whole pipeline:

```
dataloader arguments --Dataloader-->  numpy arrays --Model--> prediction
```


```python
#model.pipeline.predict
```


```python
#model.pipeline.predict_generator
```

### Others


```python
# Model source
model.source
```




    GitLFSSource(remote_url='git@github.com:kipoi/models.git', local_path='/home/avsec/.kipoi/models/')




```python
# model location directory
model.source_dir
```




    '/home/avsec/.kipoi/models/rbp_eclip/UPF1'



## DataLoader


```python
DataLoader = kipoi.get_dataloader_factory("rbp_eclip/UPF1")
```


```python
?DataLoader
```


    [0;31mInit signature:[0m [0mDataLoader[0m[0;34m([0m[0mintervals_file[0m[0;34m,[0m [0mfasta_file[0m[0;34m,[0m [0mgtf_file[0m[0;34m,[0m [0mtarget_file[0m[0;34m=[0m[0;32mNone[0m[0;34m,[0m [0muse_linecache[0m[0;34m=[0m[0;32mFalse[0m[0;34m)[0m[0;34m[0m[0m
    [0;31mDocstring:[0m     
    Args:
        intervals_file: file path; tsv file
            Assumes bed-like `chrom start end id score strand` format.
        fasta_file: file path; Genome sequence
        gtf_file: file path; Genome annotation GTF file.
        preproc_transformer: file path; tranformer used for pre-processing.
        target_file: file path; path to the targets
        batch_size: int
    [0;31mType:[0m           type



## Run dataloader on some examples


```python
# each dataloader already provides the example files
DataLoader.example_kwargs
```




    {'fasta_file': 'example_files/hg38_chr22.fa',
     'gtf_file': 'example_files/gencode.v24.annotation_chr22.gtf',
     'intervals_file': 'example_files/intervals.bed',
     'target_file': 'example_files/targets.tsv'}




```python
import os
```


```python
# cd into the source directory 
os.chdir(DataLoader.source_dir)
```


```python
!tree
```

    .
    ├── custom_keras_objects.py -> ../template/custom_keras_objects.py
    ├── dataloader_files
    │   └── position_transformer.pkl
    ├── dataloader.py -> ../template/dataloader.py
    ├── dataloader.yaml -> ../template/dataloader.yaml
    ├── example_files -> ../template/example_files
    ├── model_files
    │   └── model.h5
    ├── model.yaml -> ../template/model.yaml
    └── __pycache__
        ├── custom_keras_objects.cpython-36.pyc
        └── dataloader.cpython-36.pyc
    
    4 directories, 8 files



```python
dl = DataLoader(**DataLoader.example_kwargs)
# could be also done with DataLoader.init_example()
```


```python
# This particular dataloader is of type Dataset
# i.e. it implements the __getitem__ method:
dl[0].keys()
```




    dict_keys(['inputs', 'targets', 'metadata'])




```python
dl[0]["inputs"].keys()
```




    dict_keys(['seq', 'dist_tss', 'dist_polya', 'dist_exon_intron', 'dist_intron_exon', 'dist_start_codon', 'dist_stop_codon', 'dist_gene_start', 'dist_gene_end'])




```python
dl[0]["inputs"]["seq"][:5]
```




    array([[0.25, 0.25, 0.25, 0.25],
           [0.25, 0.25, 0.25, 0.25],
           [0.25, 0.25, 0.25, 0.25],
           [0.25, 0.25, 0.25, 0.25],
           [0.25, 0.25, 0.25, 0.25]], dtype=float32)




```python
len(dl)
```




    14



### Get the whole dataset


```python
whole_data = dl.load_all()
```

    100%|██████████| 1/1 [00:00<00:00,  7.59it/s]



```python
whole_data.keys()
```




    dict_keys(['inputs', 'targets', 'metadata'])




```python
whole_data["inputs"]["seq"].shape
```




    (14, 101, 4)



### Get the iterator to run predictions


```python
it = dl.batch_iter(batch_size=1, shuffle=False, num_workers=0, drop_last=False)
```


```python
next(it)["inputs"]["seq"].shape
```




    (1, 101, 4)




```python
model.predict_on_batch(next(it)["inputs"])
```




    array([[0.0005]], dtype=float32)



### Train the Keras model

Keras model is stored under the `.model` attribute.


```python
model.model.compile("adam", "binary_crossentropy")
```


```python
train_it = dl.batch_train_iter(batch_size=2)
```


```python
# model.model.summary()
```


```python
model.model.fit_generator(train_it, steps_per_epoch=3, epochs=1)
```

    Epoch 1/1
    3/3 [==============================] - 1s 309ms/step - loss: 1.3466





    <keras.callbacks.History at 0x7f6067500240>



## Pipeline: `raw files -[dataloader]-> numpy arrays -[model]-> prediction`


```python
example_kwargs = model.default_dataloader.example_kwargs
```


```python
model.pipeline.predict(example_kwargs)
```




    array([[0.1351],
           [0.0005],
           [0.0005],
           [0.1351],
           [0.1351],
           [0.1351],
           [0.0005],
           [0.1351],
           [0.1351],
           [0.1351],
           [0.1351],
           [0.1351],
           [0.1351],
           [0.1351]], dtype=float32)




```python
next(model.pipeline.predict_generator(example_kwargs, batch_size=2))
```




    array([[0.3588],
           [0.0004]], dtype=float32)
