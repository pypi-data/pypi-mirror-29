Generated from [nbs/contributing_models.ipynb](https://github.com/kipoi/kipoi/blob/master/nbs/contributing_models.ipynb)

# Contributing a model to the Kipoi model repository

This notebook will show you how to contribute a model to the [Kipoi model repository](https://github.com/kipoi/models). For a simple 'model contribution checklist' see also <http://kipoi.org/docs/contributing/01_Getting_started/>.

## Kipoi basics

Contributing a model to Kipoi means writing a sub-folder with all the required files to the [Kipoi model repository](https://github.com/kipoi/models) via pull request.

Two main components of the model repository are **model** and **dataloader**.

![img](/img/kipoi-workflow.png)

### Model

Model takes as input numpy arrays and outputs numpy arrays. In practice, a model needs to implement the `predict_on_batch(x)` method, where `x` is dictionary/list of numpy arrays. The model contributor needs to provide one of the following:

- Serialized Keras model
- Serialized Sklearn model
- Custom model inheriting from `keras.model.BaseModel`.
  - all the required files, i.e. weights need to be loaded in the `__init__`
  
See <http://kipoi.org/docs/contributing/02_Writing_model.yaml/> and <http://kipoi.org/docs/contributing/05_Writing_model.py/> for more info.

### Dataloader

Dataloader takes raw file paths or other parameters as argument and outputs modelling-ready numpy arrays. The dataloading can be done through a generator---batch-by-batch, sample-by-sample---or by just returning the whole dataset. The goal is to work really with raw files (say fasta, bed, vcf, etc in bioinformatics), as this allows to make model predictions on new datasets without going through the burden of running custom pre-processing scripts. The model contributor needs to implement one of the following:

- PreloadedDataset
- Dataset
- BatchDataset
- SampleIterator
- BatchIterator
- SampleGenerator
- BatchGenerator

See <http://kipoi.org/docs/contributing/04_Writing_dataloader.py/> for more info.

### Folder layout

Here is an example folder structure of a Kipoi model:

```
├── dataloader.py     # implements the dataloader
├── dataloader.yaml   # describes the dataloader
├── dataloader_files/      #/ files required by the dataloader
│   ├── x_transfomer.pkl
│   └── y_transfomer.pkl
├── model.yaml        # describes the model
├── model_files/           #/ files required by the model
│   ├── model.json
│   └── weights.h5
└── example_files/         #/ small example files
    ├── features.csv
    └── targets.csv
```    

Two most important files are `model.yaml` and `dataloader.yaml`. They provide a complete description about the model, the dataloader and the files they depend on.

## Contributing a simple Iris-classifier

Details about the individual files will be revealed throught the tutorial bellow. A simple Keras model will be trained to predict the Iris plant class from the well-known [Iris](archive.ics.uci.edu/ml/datasets/Iris) dataset.



### Outline

1. Train the model
2. Generate `dataloader_files/`
3. Generate `model_files/`
4. Generate `example_files/`
5. Write `model.yaml`
6. Write `dataloader.yaml`
7. Write `dataloader.py`
8. Test with the model with `$ kipoi test .`

### 1. Train the model

#### Load and pre-process the data


```python
import pandas as pd
import os
from sklearn.preprocessing import LabelBinarizer, StandardScaler

from sklearn import datasets
iris = datasets.load_iris()
```


```python
# view more info about the dataset
# print(iris["DESCR"])
```


```python
# Data pre-processing
y_transformer = LabelBinarizer().fit(iris["target"])
x_transformer = StandardScaler().fit(iris["data"])
```


```python
x = x_transformer.transform(iris["data"])
y = y_transformer.transform(iris["target"])
```


```python
x[:3]
```




    array([[-0.9007,  1.0321, -1.3413, -1.313 ],
           [-1.143 , -0.125 , -1.3413, -1.313 ],
           [-1.3854,  0.3378, -1.3981, -1.313 ]])




```python
y[:3]
```




    array([[1, 0, 0],
           [1, 0, 0],
           [1, 0, 0]])



#### Train an example model

Let's train a simple linear-regression model using Keras.


```python
from keras.models import Model
import keras.layers as kl

inp = kl.Input(shape=(4, ), name="features")
out = kl.Dense(units=3)(inp)
model = Model(inp, out)
model.compile("adam", "categorical_crossentropy")

model.fit(x, y, verbose=0)
```

    Using TensorFlow backend.





    <keras.callbacks.History at 0x7f5c537f2d68>



### 2. Generate `dataloader_files/`

Now that we have everything we need, let's start writing the files to model's directory (here `model_template/`). 

In reality, you would need to 

1. Fork the [kipoi/models repository](https://github.com/kipoi/models)
2. Clone your repository fork, ignoring all the git-lfs files
    - `$ git lfs clone git@github.com:<your_username>/models.git '-I /'`
3. Create a new folder `<mynewmodel>` containing all the model files in the repostiory root
    - put all the non-code files (serialized models, test data) into a `*files/` directory, where `*` can be anything. These will namely be tracked by `git-lfs` instead of `git`.
      - Examples: `model_files/`, `dataloader_files/`
4. Test your repository locally:
    - `$ kipoi test <mynewmodel_folder>`
5. Commit, push to your forked remote and submit a pull request to [github.com/kipoi/models](https://github.com/kipoi/models)

Dataloader can use some trained transformer (here the `LabelBinarizer` and `StandardScaler` transformers form sklearn). These should be written to `dataloader_files/`.


```python
cd ../examples/iris_model_template
```

    /data/nasif12/home_if12/avsec/projects-work/kipoi/examples/iris_model_template



```python
os.makedirs("dataloader_files", exist_ok=True)
```


```python
ls
```

    [0m[38;5;27mdataloader_files[0m/  dataloader.yaml  [38;5;27mmodel_files[0m/  [38;5;27m__pycache__[0m/
    dataloader.py      [38;5;27mexample_files[0m/   model.yaml



```python
import pickle
```


```python
with open("dataloader_files/y_transformer.pkl", "wb") as f:
    pickle.dump(y_transformer, f)

with open("dataloader_files/x_transformer.pkl", "wb") as f:
    pickle.dump(x_transformer, f)
```


```python
ls dataloader_files
```

    x_transformer.pkl  y_transformer.pkl


### 3. Generate `model_files/`

The serialized model weights and architecture go to `model_files/`.


```python
os.makedirs("model_files", exist_ok=True)
```


```python
# Architecture
with open("model_files/model.json", "w") as f:
    f.write(model.to_json())
```


```python
# Weights
model.save_weights("model_files/weights.h5")
```


```python
# Alternatively, for the scikit-learn model we would save the pickle file
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
lr = OneVsRestClassifier(LogisticRegression())
lr.fit(x, y)

with open("model_files/sklearn_model.pkl", "wb") as f:
    pickle.dump(lr, f)
```

### 4. Generate `example_files/`

`example_files/` should contain a small subset of the raw files the dataloader will read.

#### Numpy arrays -> pd.DataFrame


```python
iris.keys()
```




    dict_keys(['target_names', 'feature_names', 'data', 'DESCR', 'target'])




```python
X = pd.DataFrame(iris["data"][:20], columns=iris["feature_names"])
```


```python
X.head()
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
      <th>sepal length (cm)</th>
      <th>sepal width (cm)</th>
      <th>petal length (cm)</th>
      <th>petal width (cm)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5.1</td>
      <td>3.5</td>
      <td>1.4</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4.9</td>
      <td>3.0</td>
      <td>1.4</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4.7</td>
      <td>3.2</td>
      <td>1.3</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4.6</td>
      <td>3.1</td>
      <td>1.5</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.0</td>
      <td>3.6</td>
      <td>1.4</td>
      <td>0.2</td>
    </tr>
  </tbody>
</table>
</div>




```python
y = pd.DataFrame({"class": iris["target"][:20]})
```


```python
y.head()
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
      <th>class</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



#### Save example files


```python
os.makedirs("example_files", exist_ok=True)
```


```python
X.to_csv("example_files/features.csv", index=False)
```


```python
y.to_csv("example_files/targets.csv", index=False)
```


```python
!head -n 2 example_files/targets.csv
```

    class
    0



```python
!head -n 2 example_files/features.csv
```

    sepal length (cm),sepal width (cm),petal length (cm),petal width (cm)
    5.1,3.5,1.4,0.2


### 5. Write `model.yaml`

The `model.yaml` for this model should look like this:

```yaml
type: keras  # use `kipoi.model.KerasModel`
args:  # arguments of `kipoi.model.KerasModel`
    arch: model_files/model.json
    weights: model_files/weights.h5
default_dataloader: . # path to the dataloader directory. Here it's defined in the same directory
info: # General information about the model
    authors: 
        - name: Your Name
          github: your_github_username
          email: your_email@host.org
    doc: Model predicting the Iris species
    version: 0.1  # optional 
    cite_as: https://doi.org:/... # preferably a doi url to the paper
    trained_on: Iris species dataset (http://archive.ics.uci.edu/ml/datasets/Iris) # short dataset description
    license: MIT # Software License - defaults to MIT
dependencies:
    conda: # install via conda
      - python=3.5
      - h5py
      # - soumith::pytorch  # specify packages from other channels via <channel>::<package>      
    pip:   # install via pip
      - keras>=2.0.4
      - tensorflow>=1.0
schema:  # Model schema
    inputs:
        features:
            shape: (4,)  # array shape of a single sample (omitting the batch dimension)
            doc: "Features in cm: sepal length, sepal width, petal length, petal width."
    targets:
        shape: (3,)
        doc: "One-hot encoded array of classes: setosa, versicolor, virginica."
```

All file paths are relative relative to `model.yaml`.

### 6. Write `dataloader.yaml`

```yaml
type: Dataset
defined_as: dataloader.py::MyDataset  # We need to implement MyDataset class inheriting from kipoi.data.Dataset in dataloader.py
args:
    features_file:
        # descr: > allows multi-line fields
        doc: >
          Csv file of the Iris Plants Database from
          http://archive.ics.uci.edu/ml/datasets/Iris features.
        type: str
        example: example_files/features.csv  # example files
    targets_file:
        doc: >
          Csv file of the Iris Plants Database targets.
          Not required for making the prediction.
        type: str
        example: example_files/targets.csv
        optional: True  # if not present, the `targets` field will not be present in the dataloader output
info:
    authors: 
        - name: Your Name
          github: your_github_account
          email: your_email@host.org
    version: 0.1
    doc: Model predicting the Iris species
dependencies:
    conda:
      - python=3.5
      - pandas
      - numpy
      - sklearn
output_schema:
    inputs:
        features:
            shape: (4,)
            doc: Features in cm: sepal length, sepal width, petal length, petal width.
    targets:
        shape: (3, )
        doc: One-hot encoded array of classes: setosa, versicolor, virginica.
    metadata:  # field providing additional information to the samples (not directly required by the model)
        example_row_number:
            shape: int
            doc: Just an example metadata column
```

### 7. Write `dataloader.py`

Finally, let's implement MyDataset. We need to implement two methods: `__len__` and `__getitem__`. 

`__getitem__` will return one item of the dataset. In our case, this is a dictionary with `output_schema` described in `dataloader.yaml`.

For more information about writing such dataloaders, see the [Data Loading and Processing Tutorial from pytorch](http://pytorch.org/tutorials/beginner/data_loading_tutorial.html).


```python
import pickle
from kipoi.data import Dataset
import pandas as pd
import numpy as np

def read_pickle(f):
    with open(f, "rb") as f:
        return pickle.load(f)

class MyDataset(Dataset):

    def __init__(self, features_file, targets_file=None):
        self.features_file = features_file
        self.targets_file = targets_file

        self.y_transformer = read_pickle("dataloader_files/y_transformer.pkl")
        self.x_transformer = read_pickle("dataloader_files/x_transformer.pkl")

        self.features = pd.read_csv(features_file)
        if targets_file is not None:
            self.targets = pd.read_csv(targets_file)
            assert len(self.targets) == len(self.features)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        x_features = np.ravel(self.x_transformer.transform(self.features.iloc[idx].values[np.newaxis]))
        if self.targets_file is None:
            y_class = {}
        else:
            y_class = np.ravel(self.y_transformer.transform(self.targets.iloc[idx].values[np.newaxis]))
        return {
            "inputs": {
                "features": x_features
            },
            "targets": y_class,
            "metadata": {
                "example_row_number": idx
            }
        }
```

#### Example usage of the dataset


```python
ds = MyDataset("example_files/features.csv", "example_files/targets.csv")
```


```python
# call __getitem__
ds[5]
```




    {'inputs': {'features': array([-0.5372,  1.9577, -1.1707, -1.05  ])},
     'metadata': {'example_row_number': 5},
     'targets': array([1, 0, 0])}



Since MyDatset inherits from `kipoi.data.Dataset`, it has some additional nice feature. See [python-sdk.ipynb](python-sdk.ipynb) for more information.


```python
# batch-iterator
it = ds.batch_iter(batch_size=3, shuffle=False, num_workers=2)
next(it)
```




    {'inputs': {'features': array([[-0.9007,  1.0321, -1.3413, -1.313 ],
             [-1.143 , -0.125 , -1.3413, -1.313 ],
             [-1.3854,  0.3378, -1.3981, -1.313 ]])},
     'metadata': {'example_row_number': array([0, 1, 2])},
     'targets': array([[1, 0, 0],
            [1, 0, 0],
            [1, 0, 0]])}




```python
# ds.load_all()  # load the whole dataset into memory
```

### 8. Test with the model with `$ kipoi test .`

Before we contribute the model to the repository, let's run the test:


```python
!kipoi test .
```

    [32mINFO[0m [44m[kipoi.data][0m successfully loaded the dataloader from dataloader.py::MyDataset[0m
    Using TensorFlow backend.
    2017-11-29 17:26:21.755321: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.1 instructions, but these are available on your machine and could speed up CPU computations.
    2017-11-29 17:26:21.755368: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.2 instructions, but these are available on your machine and could speed up CPU computations.
    2017-11-29 17:26:21.755385: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX instructions, but these are available on your machine and could speed up CPU computations.
    2017-11-29 17:26:21.755399: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX2 instructions, but these are available on your machine and could speed up CPU computations.
    2017-11-29 17:26:21.755414: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use FMA instructions, but these are available on your machine and could speed up CPU computations.
    [32mINFO[0m [44m[kipoi.model][0m successfully loaded model architecture from <_io.TextIOWrapper name='model_files/model.json' mode='r' encoding='UTF-8'>[0m
    [32mINFO[0m [44m[kipoi.model][0m successfully loaded model weights from model_files/weights.h5[0m
    [32mINFO[0m [44m[kipoi.pipeline][0m dataloader.output_schema is compatible with model.schema[0m
    [32mINFO[0m [44m[kipoi.pipeline][0m Initialized data generator. Running batches...[0m
    /opt/modules/i12g/anaconda/3-4.1.1/lib/python3.5/site-packages/sklearn/base.py:315: UserWarning: Trying to unpickle estimator LabelBinarizer from version 0.19.1 when using version 0.18.1. This might lead to breaking code or invalid results. Use at your own risk.
      UserWarning)
    /opt/modules/i12g/anaconda/3-4.1.1/lib/python3.5/site-packages/sklearn/base.py:315: UserWarning: Trying to unpickle estimator StandardScaler from version 0.19.1 when using version 0.18.1. This might lead to breaking code or invalid results. Use at your own risk.
      UserWarning)
    [32mINFO[0m [44m[kipoi.pipeline][0m Returned data schema correct[0m
    100%|█████████████████████████████████████████████| 1/1 [00:00<00:00, 89.45it/s]
    [32mINFO[0m [44m[kipoi.pipeline][0m predict_example done![0m
    [32mINFO[0m [44m[kipoi.pipeline][0m Successfully ran test_predict[0m
    [0m

This command did the following:

- validated if `output_schema` defined in `dataloader.yaml` matches the shapes of the returned arrays
- validated that model and dataloader are compatible in `inputs` and `targets`
- executed the model pipeline for the example 

## Accessing the model through kipoi 


```python
import kipoi
```


```python
reload(kipoi)
```




    <module 'kipoi' from '/data/nasif12/home_if12/avsec/projects-work/kipoi/kipoi/__init__.py'>




```python
m = kipoi.get_model(".", source="dir")  # See also python-sdk.ipynb
```

    Using TensorFlow backend.



```python
m.pipeline.predict({"features_file": "example_files/features.csv", "targets_file": "example_files/targets.csv" })[:5]
```




    array([[ 1.5356, -0.8118, -0.2712],
           [ 0.4649, -0.22  , -1.1491],
           [ 0.6735, -0.1923, -0.8083],
           [ 0.3958,  0.0178, -0.9159],
           [ 1.6362, -0.79  , -0.0849]], dtype=float32)




```python
m.info
```




    Info(authors=[Author(name='Your Name', github='your_github_username', email=None)], doc='Model predicting the Iris species', name=None, version='0.1', tags=[])




```python
m.default_dataloader
```




    dataloader.MyDataset




```python
m.model
```




    <keras.engine.training.Model at 0x7f0dbe68f8d0>




```python
m.predict_on_batch
```




    <bound method KerasModel.predict_on_batch of <kipoi.model.KerasModel object at 0x7f0dc19cf400>>



## Recap

Congrats! You made it through the tutorial! Feel free to use this model for your model template. Alternatively, you can use `kipoi init` to setup a model directory. Make sure you have read the [getting started guide](http://kipoi.org/docs/contributing/01_Getting_started/) for contributing models.
