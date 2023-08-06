Generated from [nbs/variant_effect_prediction.ipynb](https://github.com/kipoi/kipoi/blob/master/nbs/variant_effect_prediction.ipynb)

# Variant effect prediction
This notebook will explain how to run a variant effect prediction (ISM) on a model.

This is automated functionality to predict the variant effects starting from a VCF file. At the moment only SNPs (no indels) are supported. There are a few basic requirements to the model and the dataloader in order to make use of this functionality:

## The procedure (ISM)
The basic procedure is that a VCF is loaded and the genomic position of variants is extracted. From this a bed file is created that is then used to run the dataloader together with the other input arguments. The generated model input is then in-silico mutated yielding 4 sets of prediction data (forward reference, forward alternative, reverse-complement reference, reverse-complement alternative). The individual precitions are then compared and the effect is returned.


## Model and dataloader requirements

* Model predicts (at least partly) based on DNA sequence input
* Dataloader has a bed file argument defining the genomic region for which a data sample is generated
* Dataloader outputs metadata with the DNA sequence that descibes the genomic position (chr, start, end) of the generated sequence


## Setting up the _.yaml_ files
First it is important to tell the variant effect prediction module that your model supports variant effect prediction. Thereor the postprocessing category has to be present in the model.yaml and in the dataloader.yaml in the following ways:

I will assume here a model in which a DNA sequence input called `seq` is present. In model.yaml the following lines tell the variant effect predictor that the model input "seq" is the DNA sequence input that should be modified for an ISM analysis. 

*`model.yaml:`*
```YAML
...
postprocessing:
    - type: var_effect_prediction
      args:
          seq_input:
            - seq
```

You can have multiple DNA sequence model inputs that should be modified, just add them one after the other in the `seq_input` category. Please consider that in the `dataloader.yaml` all those `seq` fields have to be linked to exactly one ranges metadata-element each. Reminder: See `dataloader.yaml > output_schema > inputs > seq > associated_metadata`.

Additionally in order to enable the dataloader for variant effect prediction you will have to tell the variant effect predictor which dataloader argument is used to define the genomic ranges. At the moment only bed files are supported:

*`dataloader.yaml:`*
```YAML
...
postprocessing:
    - type: var_effect_prediction
      args:
          bed_input:
            - intervals_file
```

In this case the `dataloader.yaml > args` defines an argument `intervals_file` that expects a bed file as input and that tells the dataloader for which genomic region the datapoints should be generated. The `rbp`example model is set up in the way mentioned above. We will use that model in order to show how to run variant effect prediction. First we will need to load the required modules:


```python
import kipoi
from kipoi.postprocessing.variant_effects import predict_snvs
from kipoi.pipeline import install_model_requirements
import warnings
from kipoi.utils import cd
warnings.filterwarnings('ignore')
```


```python
model_dir = kipoi.__path__[0] + "/../examples/rbp/"
```

We might decide to install the requirements defined by the model:


```python
install_model_requirements(model_dir, "dir", and_dataloaders=True)
```

Now let's get the model and dataloader factory


```python
model = kipoi.get_model(model_dir, source="dir")
Dataloader = kipoi.get_dataloader_factory(model_dir, source="dir")
```

We will now need to define which input files should be used for predicting. For simplicity we will just use the sample input files delivered with the model:


```python
dataloader_arguments = {
    "fasta_file": "example_files/hg38_chr22.fa",
    "preproc_transformer": "dataloader_files/encodeSplines.pkl",
    "gtf_file": "example_files/gencode_v25_chr22.gtf.pkl.gz",
 }
```

You will have noticed that the `intervals_file` argument was not defined as this will be used by the variant effect predictor function. Reminder: This is an excerpt of the `dataloader.yaml`:

```YAML
args:
    intervals_file:
        ...
    fasta_file:
        ...
    gtf_file:
        ...
    preproc_transformer:
        ...
    target_file:
        ...
        optional: True
...
postprocessing:
    - type: var_effect_prediction
      args:
          bed_input:
            - intervals_file

```

Now it is time to actually add in the vcf file we want to use:


```python
vcf_fpath = "example_files/variants.vcf"
out_vcf_fpath = "variants_pred.vcf"
```

## Prediction
After loading the model, the dataloader and defining which input files should be used, we need to add in a few more arguments:

* The batch size for prediction - this will be limited by the available memory
* Additional parameters for the evaluation function - here ISM is used (the only one which is supported at the moment), which can calculate the effect based on the difference (`"diff"`) or based on log odds ratios of predictions (`"log_odds"`).


```python
with cd(model.source_dir):
    res = predict_snvs(model, vcf_fpath, dataloader_args=dataloader_arguments,
                       dataloader=Dataloader, batch_size=32,
                       evaluation_function_kwargs={"diff_type": "diff"},
                       out_vcf_fpath=out_vcf_fpath)
```

This will return a dictionary with the predictions from the model given the query VCF. At the moment only SNVs are predicted and no indels. If an output VCF path is given the results will be integrated into the input VCF-file in the `INFO` tag.
