Generated from [nbs/R-api.ipynb](https://github.com/kipoi/kipoi/blob/master/nbs/R-api.ipynb)

# Using Kipoi from R

Thanks to the [reticulate](https://github.com/rstudio/reticulate) R package from RStudio, it is possible to easily call python functions from R. Hence one can use kipoi python API from R. This tutorial will show how to do that.

Make sure you have git-lfs and Kipoi correctly installed: 

1. Install git-lfs
    - `conda install -c conda-forge git-lfs` (alternatively see <https://git-lfs.github.com/>)
2. Install kipoi
    - `pip install kipoi`
    
    
Please read [docs/using/getting started](http://kipoi.org/docs/using/01_Getting_started/) before going through this notebook.

## Install and load `reticulate`

Make sure you have the reticulate R package installed


```R
# install.packages("reticulate")
```


```R
library(reticulate)
```

## Reticulate quick intro


In general, using Kipoi from R is almost the same as using it from Python: instead of using `object.method()` or `object.attribute` as in python, use `$`: `object$method()`, `object$attribute`. 


```R
# short reticulate example 
os <- import("os")
os$chdir("/tmp")
os$getcwd()
```


'/tmp'


### Type mapping R <-> python

Reticulate translates objects between R and python in the following way:

| R                      | Python            | Examples                                    |
|------------------------|-------------------|---------------------------------------------|
| Single-element vector  | Scalar            | `1`, `1L`, `TRUE`, `"foo"`                  |
| Multi-element vector   | List              | `c(1.0, 2.0, 3.0)`, `c(1L, 2L, 3L)`         |
| List of multiple types | Tuple             | `list(1L, TRUE, "foo")`                     |
| Named list             | Dict              | `list(a = 1L, b = 2.0)`, `dict(x = x_data)` |
| Matrix/Array           | NumPy ndarray     | `matrix(c(1,2,3,4), nrow = 2, ncol = 2)`    |
| Function               | Python function   | `function(x) x + 1`                         |
| NULL, TRUE, FALSE      | None, True, False | `NULL`, `TRUE`, `FALSE`                     |


For more info on reticulate, please visit https://github.com/rstudio/reticulate/.

## Setup the python environment

With `reticulate::py_config()` you can check if the python configuration used by reticulate is correct. You can can also choose to use a different conda environment with `use_condaenv(...)`. This comes handy when using different models depending on different conda environments.


```R
reticulate::py_config()
```


    python:         /home/avsec/bin/anaconda3/bin/python
    libpython:      /home/avsec/bin/anaconda3/lib/libpython3.6m.so
    pythonhome:     /home/avsec/bin/anaconda3:/home/avsec/bin/anaconda3
    version:        3.6.3 |Anaconda custom (64-bit)| (default, Oct 13 2017, 12:02:49)  [GCC 7.2.0]
    numpy:          /home/avsec/bin/anaconda3/lib/python3.6/site-packages/numpy
    numpy_version:  1.14.0
    os:             /home/avsec/bin/anaconda3/lib/python3.6/os.py
    
    python versions found: 
     /home/avsec/bin/anaconda3/bin/python
     /usr/bin/python
     /usr/bin/python3


List all conda environments:

```R
reticulate::conda_list()
```

Create a new conda environment for the model:

```
$ kipoi env create HAL
```

Use that environment in R:

```R
reticulate::use_condaenv("kipoi-HAL')
```

## Load kipoi


```R
kipoi <- import("kipoi")
```

### List models


```R
kipoi$list_models()$head()
```


      source                             model version  \
    0  kipoi                      DeepSEAKeras     0.1   
    1  kipoi                     extended_coda     0.1   
    2  kipoi      DeepCpG_DNA/Hou2016_mESC_dna   1.0.4   
    3  kipoi  DeepCpG_DNA/Smallwood2014_2i_dna   1.0.4   
    4  kipoi     DeepCpG_DNA/Hou2016_HepG2_dna   1.0.4   
    
                                                 authors  \
    0  [Author(name='Jian Zhou', github=None, email=N...   
    1  [Author(name='Pang Wei Koh', github='kohpangwe...   
    2  [Author(name='Christof Angermueller', github='...   
    3  [Author(name='Christof Angermueller', github='...   
    4  [Author(name='Christof Angermueller', github='...   
    
                                            contributors  \
    0  [Author(name='Lara Urban', github='LaraUrban',...   
    1  [Author(name='Johnny Israeli', github='jisrael...   
    2  [Author(name='Roman Kreuzhuber', github='krrom...   
    3  [Author(name='Roman Kreuzhuber', github='krrom...   
    4  [Author(name='Roman Kreuzhuber', github='krrom...   
    
                                                     doc   type  \
    0  This CNN is based on the DeepSEA model from Zh...  keras   
    1  Single bp resolution ChIP-seq denoising - http...  keras   
    2  This is the extraction of the DNA-part of the ...  keras   
    3  This is the extraction of the DNA-part of the ...  keras   
    4  This is the extraction of the DNA-part of the ...  keras   
    
                     inputs                                            targets  \
    0                   seq                                     TFBS_DHS_probs   
    1  [H3K27AC_subsampled]                                          [H3K27ac]   
    2                 [dna]  [cpg/mESC1, cpg/mESC2, cpg/mESC3, cpg/mESC4, c...   
    3                 [dna]  [cpg/BS24_1_2I, cpg/BS24_2_2I, cpg/BS24_4_2I, ...   
    4                 [dna]  [cpg/HepG21, cpg/HepG22, cpg/HepG23, cpg/HepG2...   
    
       postproc_score_variants license  \
    0                     True     MIT   
    1                    False     MIT   
    2                     True     MIT   
    3                     True     MIT   
    4                     True     MIT   
    
                                                 cite_as  \
    0                 https://doi.org/10.1038/nmeth.3547   
    1      https://doi.org/10.1093/bioinformatics/btx243   
    2  https://doi.org/10.1186/s13059-017-1189-z, htt...   
    3  https://doi.org/10.1186/s13059-017-1189-z, htt...   
    4  https://doi.org/10.1186/s13059-017-1189-z, htt...   
    
                                              trained_on  \
    0  ENCODE and Roadmap Epigenomics chromatin profi...   
    1  Described in https://academic.oup.com/bioinfor...   
    2  scBS-seq and scRRBS-seq datasets, https://geno...   
    3  scBS-seq and scRRBS-seq datasets, https://geno...   
    4  scBS-seq and scRRBS-seq datasets, https://geno...   
    
                                      training_procedure  \
    0  https://www.nature.com/articles/nmeth.3547#met...   
    1  Described in https://academic.oup.com/bioinfor...   
    2  Described in https://genomebiology.biomedcentr...   
    3  Described in https://genomebiology.biomedcentr...   
    4  Described in https://genomebiology.biomedcentr...   
    
                                                    tags  
    0  [Histone modification, DNA binding, DNA access...  
    1                             [Histone modification]  
    2                                  [DNA methylation]  
    3                                  [DNA methylation]  
    4                                  [DNA methylation]  


`reticulate` currently doesn't support direct convertion from `pandas.DataFrame` to R's `data.frame`. Let's make a convenience function to create an R dataframe via matrix conversion.


```R
#' List models as an R data.frame
kipoi_list_models <- function() {
    df_models <- kipoi$list_models()
    df <- data.frame(df_models$as_matrix())
    colnames(df) = df_models$columns$tolist()
    return(df)
   
}
```


```R
df <- kipoi_list_models()
```


```R
head(df, 2)
```


<table>
<thead><tr><th scope=col>source</th><th scope=col>model</th><th scope=col>version</th><th scope=col>authors</th><th scope=col>contributors</th><th scope=col>doc</th><th scope=col>type</th><th scope=col>inputs</th><th scope=col>targets</th><th scope=col>postproc_score_variants</th><th scope=col>license</th><th scope=col>cite_as</th><th scope=col>trained_on</th><th scope=col>training_procedure</th><th scope=col>tags</th></tr></thead>
<tbody>
	<tr><td>kipoi                                                                                                                                                                                                                                                                                                                                                                                                                                                                              </td><td>DeepSEAKeras                                                                                                                                                                                                                                                                                                                                                                                                                                                                       </td><td>0.1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                </td><td>&lt;environment: 0x556afc757e38&gt;                                                                                                                                                                                                                                                                                                                                                                                                                                                </td><td>&lt;environment: 0x556afbb0d538&gt;                                                                                                                                                                                                                                                                                                                                                                                                                                                </td><td>This CNN is based on the DeepSEA model from Zhou and Troyanskaya (2015). It categorically predicts 918 cell type-specific epigenetic features from DNA sequence. The model is trained on publicly available ENCODE and Roadmap Epigenomics data and on DNA sequences of size 1000bp. The input of the tensor has to be (N, 1000, 4) for N samples, 1000bp window size and 4 nucleotides. Per sample, 918 probabilities of showing a specific epigentic feature will be predicted.
</td><td>keras                                                                                                                                                                                                                                                                                                                                                                                                                                                                              </td><td>seq                                                                                                                                                                                                                                                                                                                                                                                                                                                                                </td><td>TFBS_DHS_probs                                                                                                                                                                                                                                                                                                                                                                                                                                                                     </td><td>TRUE                                                                                                                                                                                                                                                                                                                                                                                                                                                                               </td><td>MIT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                </td><td>https://doi.org/10.1038/nmeth.3547                                                                                                                                                                                                                                                                                                                                                                                                                                                 </td><td>ENCODE and Roadmap Epigenomics chromatin profiles https://www.nature.com/articles/nmeth.3547#methods                                                                                                                                                                                                                                                                                                                                                                               </td><td>https://www.nature.com/articles/nmeth.3547#methods                                                                                                                                                                                                                                                                                                                                                                                                                                 </td><td>&lt;environment: 0x556afcddfd50&gt;                                                                                                                                                                                                                                                                                                                                                                                                                                                </td></tr>
	<tr><td>kipoi                                                                                    </td><td>extended_coda                                                                            </td><td>0.1                                                                                      </td><td>&lt;environment: 0x556afc764260&gt;                                                      </td><td>&lt;environment: 0x556afbaff708&gt;                                                      </td><td>Single bp resolution ChIP-seq denoising - https://github.com/kundajelab/coda             </td><td>keras                                                                                    </td><td>H3K27AC_subsampled                                                                       </td><td>H3K27ac                                                                                  </td><td>FALSE                                                                                    </td><td>MIT                                                                                      </td><td>https://doi.org/10.1093/bioinformatics/btx243                                            </td><td>Described in https://academic.oup.com/bioinformatics/article/33/14/i225/3953958#100805343</td><td>Described in https://academic.oup.com/bioinformatics/article/33/14/i225/3953958#100805343</td><td>&lt;environment: 0x556afcde7f60&gt;                                                      </td></tr>
</tbody>
</table>



### Get the kipoi model and make a prediction for the example files

To run the following example, make sure you have all the dependencies installed. Run:

```R
kipoi$install_model_requirements("MaxEntScan/3prime")

kipoi$install_dataloader_requirements("MaxEntScan/3prime")
```
from R or
```bash
kipoi env install MaxEntScan/3prime
```
from the command-line. This will install all the required dependencies for both, the model and the dataloader.


```R
model <- kipoi$get_model("MaxEntScan/3prime")
```


```R
predictions <- model$pipeline$predict_example()
```


```R
head(predictions)
```


<ol class=list-inline>
	<li>6.72899227874919</li>
	<li>6.15729433240656</li>
	<li>7.14095214875511</li>
	<li>2.13760519765451</li>
	<li>-9.52033554891735</li>
	<li>9.54342300799607</li>
</ol>



### Use the model and dataloader independently


```R
# Get the dataloader
setwd('~/.kipoi/models/MaxEntScan/3prime')

dl <- model$default_dataloader(gtf_file='example_files/hg19.chr22.gtf', fasta_file='example_files/hg19.chr22.fa')
```


```R
# get a batch iterator
it <- dl$batch_iter(batch_size=4)
```


```R
it
```


    DataLoaderIter



```R
# Retrieve a batch of data
batch <- iter_next(it)
```


```R
str(batch)
```

    List of 2
     $ inputs  : chr [1:4(1d)] "TCTTCTCTCCCCAATCTCAGCCT" "ATTCTCAGTTGTCTTTACAGTTT" "CCTTAGTTTTATTTTTTCAGAGT" "ATTTTTGTTTTTAGACATAGGAT"
     $ metadata:List of 5
      ..$ geneID      : chr [1:4(1d)] "ENSG00000233866" "ENSG00000223875" "ENSG00000223875" "ENSG00000223875"
      ..$ transcriptID: chr [1:4(1d)] "ENST00000424770" "ENST00000420638" "ENST00000420638" "ENST00000420638"
      ..$ biotype     : chr [1:4(1d)] "lincRNA" "pseudogene" "pseudogene" "pseudogene"
      ..$ order       : num [1:4(1d)] 0 0 1 2
      ..$ ranges      :List of 5
      .. ..$ chr   : chr [1:4(1d)] "22" "22" "22" "22"
      .. ..$ start : num [1:4(1d)] 16062790 16118910 16101471 16100645
      .. ..$ end   : num [1:4(1d)] 16062813 16118933 16101494 16100668
      .. ..$ id    : chr [1:4(1d)] "ENSG00000233866" "ENSG00000223875" "ENSG00000223875" "ENSG00000223875"
      .. ..$ strand: chr [1:4(1d)] "+" "-" "-" "-"



```R
# make the prediction with a model
model$predict_on_batch(batch$inputs)
```


<ol class=list-inline>
	<li>6.72899227874919</li>
	<li>6.15729433240656</li>
	<li>7.14095214875511</li>
	<li>2.13760519765451</li>
</ol>



## Troubleshooting

Since Kipoi is not natively implemented in R, the error messages are cryptic and hence debugging can be a bit of a pain. 

### Run the same code in python or CLI

When you encounter an error, try to run the analogous code snippet from the command line or python. A good starting point is to first run

```
$ kipoi test MaxEntScan/3prime --source=kipoi
```

from the command-line first. 

### Dependency issues

It's very likely that the error will be due to missing dependencies. Also note that some models will work only with python 3 or python 2. To install all the required dependencies for the model, run:

```
$ kipoi env install MaxEntScan/3prime
```

This will install the dependencies into your current conda environment. If you wish to create a new environment with all the dependencies installed, run

```
$ kipoi env create MaxEntScan/3prime
```

To use that environment in R, run:

```R
use_condaenv("kipoi-MaxEntScan__3prime")
```

Make sure you run that code snippet right after importing the `reticulate` library (i.e. make sure you run it before `kipoi <- import('kipoi')`)

### Float/Double type issues

When using a pytorch model: `DeepSEA/predict`


```R
# Get the dataloader
setwd('~/.kipoi/models/DeepSEA/predict')
model <- kipoi$get_model("DeepSEA/predict")
dl <- model$default_dataloader(intervals_file='example_files/intervals.bed', fasta_file='example_files/hg38_chr22.fa')
# get a batch iterator
it <- dl$batch_iter(batch_size=4)
# predict for a batch
batch <- iter_next(it)
```


```R
# model$predict_on_batch(batch$inputs)
```

We get an error:

```
Error in py_call_impl(callable, dots$args, dots$keywords): RuntimeError: Input type (CUDADoubleTensor) and weight type (CUDAFloatTensor) should be the same
```

This means that the feeded array is Double instead of Float.

R arrays are by default converted to float64 numpy dtype:


```R
np <- import("numpy", convert=FALSE)
np$array(0.1)$dtype
```


    float64



```R
np$array(batch$inputs)$dtype
```


    float64


To fix this, we need to explicitly convert them to `float32` before passing the batch to the model:


```R
model$predict_on_batch(np$array(batch$inputs, dtype='float32'))
```


<table>
<tbody>
	<tr><td>0.003497796 </td><td>0.003443634 </td><td>0.00475722  </td><td>0.006346597 </td><td>0.01217456  </td><td>0.008442441 </td><td>0.005778539 </td><td>0.007471715 </td><td>0.005652952 </td><td>0.009384833 </td><td>⋯           </td><td>0.0003717453</td><td>0.001310135 </td><td>0.01009644  </td><td>0.008201431 </td><td>0.0004381537</td><td>0.007473897 </td><td>0.009021533 </td><td>0.003500142 </td><td>0.003842842 </td><td>0.0003947651</td></tr>
	<tr><td>0.003497796 </td><td>0.003443634 </td><td>0.00475722  </td><td>0.006346597 </td><td>0.01217456  </td><td>0.008442441 </td><td>0.005778539 </td><td>0.007471715 </td><td>0.005652952 </td><td>0.009384833 </td><td>⋯           </td><td>0.0003717453</td><td>0.001310135 </td><td>0.01009644  </td><td>0.008201431 </td><td>0.0004381537</td><td>0.007473897 </td><td>0.009021533 </td><td>0.003500142 </td><td>0.003842842 </td><td>0.0003947651</td></tr>
	<tr><td>0.003497796 </td><td>0.003443634 </td><td>0.00475722  </td><td>0.006346597 </td><td>0.01217456  </td><td>0.008442441 </td><td>0.005778539 </td><td>0.007471715 </td><td>0.005652952 </td><td>0.009384833 </td><td>⋯           </td><td>0.0003717453</td><td>0.001310135 </td><td>0.01009644  </td><td>0.008201431 </td><td>0.0004381537</td><td>0.007473897 </td><td>0.009021533 </td><td>0.003500142 </td><td>0.003842842 </td><td>0.0003947651</td></tr>
	<tr><td>0.003497796 </td><td>0.003443634 </td><td>0.00475722  </td><td>0.006346597 </td><td>0.01217456  </td><td>0.008442441 </td><td>0.005778539 </td><td>0.007471715 </td><td>0.005652952 </td><td>0.009384833 </td><td>⋯           </td><td>0.0003717453</td><td>0.001310135 </td><td>0.01009644  </td><td>0.008201431 </td><td>0.0004381537</td><td>0.007473897 </td><td>0.009021533 </td><td>0.003500142 </td><td>0.003842842 </td><td>0.0003947651</td></tr>
</tbody>
</table>
