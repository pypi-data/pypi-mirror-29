Generated from [nbs/tf_binding_models.ipynb](https://github.com/kipoi/kipoi/blob/master/nbs/tf_binding_models.ipynb)

# Model benchmarking with Kipoi

This tutorial will show to to easily benchmark tf-binding models in Kipoi. By providing a unified access to models, it takes the same effort to run a simple PWM scanning model then to run a more complicated model (DeepBind in this example).

## Load software tools
Let's start by loading software for this tutorial: the kipoi model zoo, 


```python
import kipoi
import numpy as np
from sklearn.metrics import roc_auc_score
```

## Prepare data files
Next, we introduce a labeled BED-format interval file and a genome fasta file


```python
intervals_file = 'example_data/chr22.101bp.2000_intervals.JUND.HepG2.tsv'
fasta_file  = 'example_data/hg19_chr22.fa'
dl_kwargs = {'intervals_file': intervals_file, 'fasta_file': fasta_file}
```

Let's look at the first few lines in the intervals file


```python
!head $intervals_file
```

    chr22	20208963	20209064	0
    chr22	29673572	29673673	0
    chr22	28193720	28193821	0
    chr22	43864274	43864375	0
    chr22	18261550	18261651	0
    chr22	7869409	7869510	0
    chr22	49798024	49798125	0
    chr22	43088594	43088695	0
    chr22	35147671	35147772	0
    chr22	49486843	49486944	0


The four columns in this file contain chromosomes, interval start coordinate, interval end coordinate, and the label. This file contains 2000 examples, 1000 positives and 1000 negatives.

Let's load the labels from the last column: 


```python
labels = np.loadtxt(intervals_file, usecols=(3,))
```

Next, to evaluate the DeepBind model for JUND, we will 1) install software requirements to run the model, 2) load the model, and 3) get model predictions using our intervals and fasta file.

## Install DeepBind model software requirements


```python
deepbind_model_name = "DeepBind/D00776.005"
kipoi.pipeline.install_model_requirements(deepbind_model_name)
# Use `$ kipoi env install DeepBind/D00776.005 --gpu` from the command-line to install the gpu version of the dependencies
```

    Conda dependencies to be installed:
    ['python=2.7', 'h5py']
    Fetching package metadata ...........
    Solving package specifications: .
    
    # All requested packages already installed.
    # packages in environment at /users/jisraeli/local/anaconda/envs/kipoi:
    #
    h5py                      2.7.1            py27h2697762_0  
    pip dependencies to be installed:
    ['tensorflow==1.4', 'keras==2.1.4']
    Requirement already satisfied: tensorflow==1.4 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages
    Collecting keras==2.1.4
      Using cached Keras-2.1.4-py2.py3-none-any.whl
    Requirement already satisfied: enum34>=1.1.6 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow==1.4)
    Requirement already satisfied: backports.weakref>=1.0rc1 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow==1.4)
    Requirement already satisfied: wheel in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow==1.4)
    Requirement already satisfied: mock>=2.0.0 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow==1.4)
    Requirement already satisfied: tensorflow-tensorboard<0.5.0,>=0.4.0rc1 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow==1.4)
    Requirement already satisfied: numpy>=1.12.1 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow==1.4)
    Requirement already satisfied: protobuf>=3.3.0 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow==1.4)
    Requirement already satisfied: six>=1.10.0 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow==1.4)
    Requirement already satisfied: pyyaml in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from keras==2.1.4)
    Requirement already satisfied: scipy>=0.14 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from keras==2.1.4)
    Requirement already satisfied: funcsigs>=1; python_version < "3.3" in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from mock>=2.0.0->tensorflow==1.4)
    Requirement already satisfied: pbr>=0.11 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from mock>=2.0.0->tensorflow==1.4)
    Requirement already satisfied: bleach==1.5.0 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow==1.4)
    Requirement already satisfied: futures>=3.1.1; python_version < "3.2" in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow==1.4)
    Requirement already satisfied: markdown>=2.6.8 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow==1.4)
    Requirement already satisfied: werkzeug>=0.11.10 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow==1.4)
    Requirement already satisfied: html5lib==0.9999999 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow==1.4)
    Requirement already satisfied: setuptools in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from protobuf>=3.3.0->tensorflow==1.4)
    Installing collected packages: keras
      Found existing installation: Keras 2.0.4
        Uninstalling Keras-2.0.4:
          Successfully uninstalled Keras-2.0.4
    Successfully installed keras-2.1.4


## Load DeepBind model


```python
deepbind_model = kipoi.get_model(deepbind_model_name)
```

    /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages/h5py/__init__.py:36: FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. In future, it will be treated as `np.float64 == np.dtype(float).type`.
      from ._conv import register_converters as _register_converters
    Using TensorFlow backend.


## Get DeepBind predictions


```python
deepbind_predictions = deepbind_model.pipeline.predict(dl_kwargs, batch_size=1000)
```

## Evaluate DeepBind predictions
Let's check the auROC of deepbind predictions:


```python
roc_auc_score(labels, deepbind_predictions)
```




    0.808138



## Load, run, and evaluate a HOCOMOCO PWM model


```python
pwm_model_name = "pwm_HOCOMOCO/human/JUND"
kipoi.pipeline.install_model_requirements(pwm_model_name)
# Use `$ kipoi env install pwm_HOCOMOCO/human/JUND --gpu` from the command-line to install the gpu version of the dependencies
pwm_model = kipoi.get_model(pwm_model_name)
pwm_predictions = pwm_model.pipeline.predict(dl_kwargs, batch_size=1000)
print("PWM auROC:")
roc_auc_score(labels, pwm_predictions)
```

    Conda dependencies to be installed:
    ['python=3.5', 'h5py']
    Fetching package metadata ...........
    Solving package specifications: .
    
    # All requested packages already installed.
    # packages in environment at /users/jisraeli/local/anaconda/envs/kipoi:
    #
    h5py                      2.7.1            py27h2697762_0  
    pip dependencies to be installed:
    ['tensorflow', 'keras==2.0.4']
    Requirement already satisfied: tensorflow in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages
    Collecting keras==2.0.4
    Requirement already satisfied: enum34>=1.1.6 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow)
    Requirement already satisfied: backports.weakref>=1.0rc1 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow)
    Requirement already satisfied: wheel in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow)
    Requirement already satisfied: mock>=2.0.0 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow)
    Requirement already satisfied: tensorflow-tensorboard<0.5.0,>=0.4.0rc1 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow)
    Requirement already satisfied: numpy>=1.12.1 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow)
    Requirement already satisfied: protobuf>=3.3.0 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow)
    Requirement already satisfied: six>=1.10.0 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow)
    Requirement already satisfied: theano in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages/Theano-1.0.1-py2.7.egg (from keras==2.0.4)
    Requirement already satisfied: pyyaml in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from keras==2.0.4)
    Requirement already satisfied: funcsigs>=1; python_version < "3.3" in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from mock>=2.0.0->tensorflow)
    Requirement already satisfied: pbr>=0.11 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from mock>=2.0.0->tensorflow)
    Requirement already satisfied: bleach==1.5.0 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow)
    Requirement already satisfied: futures>=3.1.1; python_version < "3.2" in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow)
    Requirement already satisfied: markdown>=2.6.8 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow)
    Requirement already satisfied: werkzeug>=0.11.10 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow)
    Requirement already satisfied: html5lib==0.9999999 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow)
    Requirement already satisfied: setuptools in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from protobuf>=3.3.0->tensorflow)
    Requirement already satisfied: scipy>=0.14 in /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages (from theano->keras==2.0.4)
    Installing collected packages: keras
      Found existing installation: Keras 2.1.4
        Uninstalling Keras-2.1.4:
          Successfully uninstalled Keras-2.1.4
    Successfully installed keras-2.0.4


    /users/jisraeli/local/anaconda/envs/kipoi/lib/python2.7/site-packages/keras/models.py:255: UserWarning: No training configuration found in save file: the model was *not* compiled. Compile it manually.
      custom_objects=custom_objects)


    PWM auROC:





    0.6431155



In this example, DeepBind's auROC of 80.8% outperforms the HOCOMOCO PWM auROC of 64.3%
