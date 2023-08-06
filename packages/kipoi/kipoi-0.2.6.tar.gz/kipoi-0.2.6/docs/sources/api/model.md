## Model

- [ ] describe the attributes of a model
- [ ] How do the model arguments relate to the yaml

## Available models

<span style="float:right;">[[source]](https://github.com/kipoi/kipoi/blob/master/kipoi/model.py#L413)</span>
### SklearnModel

```python
kipoi.model.SklearnModel(pkl_file)
```

Loads the serialized scikit learn model

__Arguments__

- __pkl_file__: File path to the dumped sklearn file in the pickle format.

__model.yml entry__


```
- __Model__:
  - __type__: sklearn
  - __args__:
	- __pkl_file__: asd.pkl
```

----

<span style="float:right;">[[source]](https://github.com/kipoi/kipoi/blob/master/kipoi/model.py#L159)</span>
### KerasModel

```python
kipoi.model.KerasModel(weights, arch=None, custom_objects=None, backend=None)
```

Loads the serialized Keras model

__Arguments__

- __weights__: File path to the hdf5 weights or the hdf5 Keras model
- __arhc__: Architecture json model. If None, `weights` is
assumed to speficy the whole model
- __custom_objects__: Python file defining the custom Keras objects
in a `OBJECTS` dictionary
- __backend__: Keras backend to use ('tensorflow', 'theano', ...)


__`model.yml` entry__


```
- __Model__:
  - __type__: Keras
  - __args__:
	- __weights__: model.h5
	- __arch__: model.json
	- __custom_objects__: custom_keras_objects.py
```

----

<span style="float:right;">[[source]](https://github.com/kipoi/kipoi/blob/master/kipoi/model.py#L285)</span>
### PyTorchModel

```python
kipoi.model.PyTorchModel(file=None, build_fn=None, weights=None, auto_use_cuda=True)
```

Loads a pytorch model. 


----

<span style="float:right;">[[source]](https://github.com/kipoi/kipoi/blob/master/kipoi/model.py#L463)</span>
### TensorFlowModel

```python
kipoi.model.TensorFlowModel(input_nodes, target_nodes, checkpoint_path, const_feed_dict_pkl=None)
```

----

### get_model


```python
get_model(model, source='kipoi', with_dataloader=True)
```


Load the `model` from `source`, as well as the
default dataloder to model.default_dataloder.

- __Args__:
  model, str:  model name
  source, str:  source name
  with_dataloader, bool: if True, the default dataloader is
loaded to model.default_dataloadera and the pipeline at model.pipeline enabled.

