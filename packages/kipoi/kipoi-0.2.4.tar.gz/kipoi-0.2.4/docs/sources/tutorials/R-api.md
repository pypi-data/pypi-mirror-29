Generated from [nbs/R-api.ipynb](https://github.com/kipoi/kipoi/blob/master/nbs/R-api.ipynb)

# Using Kipoi from R

Thanks to the [reticulate](https://github.com/rstudio/reticulate) R package from RStudio, it is possible to easily call python functions from R. Hence one can use kipoi python API from R. This tutorial will show how to do that.

## Install and load `reticulate`

Make sure you have the reticulate R package installed


```R
# install.packages("reticulate")
```


```R
library(reticulate)
```

## Setup the python environment

With `reticulate::py_config()` you can check if the python configuration used by reticulate is correct. You can can also choose to use a different conda environment with `use_condaenv(...)`. This comes handy when using different models depending on different conda environments.


```R
reticulate::py_config()
```


    python:         /opt/modules/i12g/anaconda/3-4.1.1/bin/python
    libpython:      /opt/modules/i12g/anaconda/3-4.1.1/lib/libpython3.5m.so
    pythonhome:     /opt/modules/i12g/anaconda/3-4.1.1:/opt/modules/i12g/anaconda/3-4.1.1
    version:        3.5.2 |Anaconda custom (64-bit)| (default, Jul  2 2016, 17:53:06)  [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)]
    numpy:          /opt/modules/i12g/anaconda/3-4.1.1/lib/python3.5/site-packages/numpy
    numpy_version:  1.13.3
    
    python versions found: 
     /opt/modules/i12g/anaconda/3-4.1.1/bin/python
     /usr/bin/python



```R
# reticulate::conda_list()
```


```R
# reticulate::use_condaenv(...)
```

## Load kipoi


```R
kipoi <- import("kipoi")
```

### List models


```R
kipoi$list_models()$head()
```


      source                      model version  \
    0  kipoi                 MaxEntScan     0.1   
    1  kipoi              extended_coda     0.1   
    2  kipoi                    DeepSEA     0.1   
    3  kipoi                        HAL     0.1   
    4  kipoi  CpGenie/MCF_7_ENCSR943EFS     0.1   
    
                                                 authors  \
    0  [Author(name='Jun Cheng', github='s6juncheng',...   
    1  [Author(name='Johnny Israeli', github='jisrael...   
    2  [Author(name='Lara Urban', github='LaraUrban',...   
    3  [Author(name='Jun Cheng', github='s6juncheng',...   
    4  [Author(name='Haoyang Zeng', github='haoyangz'...   
    
                                                     doc    type  \
    0                              MaxEnt Splicing Model  custom   
    1            Single bp resolution ChIP-seq denoising   keras   
    2  This CNN is based on the DeepSEA model from Zh...   keras   
    3                      Model from Rosenberg ... TODO  custom   
    4  Abstract: DNA methylation plays a crucial role...   keras   
    
                     inputs           targets tags  
    0                 [seq]             [psi]   []  
    1  [H3K27AC_subsampled]         [H3K27ac]   []  
    2                   seq        epigen_mod   []  
    3                 [seq]             [psi]   []  
    4                   seq  methylation_prob   []  


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
<thead><tr><th scope=col>source</th><th scope=col>model</th><th scope=col>version</th><th scope=col>authors</th><th scope=col>doc</th><th scope=col>type</th><th scope=col>inputs</th><th scope=col>targets</th><th scope=col>tags</th></tr></thead>
<tbody>
	<tr><td>kipoi                                                      </td><td>MaxEntScan                                                 </td><td>0.1                                                        </td><td>[Author(name='Jun Cheng', github='s6juncheng', email=None)]</td><td>MaxEnt Splicing Model                                      </td><td>custom                                                     </td><td>seq                                                        </td><td>psi                                                        </td><td>&lt;environment: 0x2b762e8&gt;                             </td></tr>
	<tr><td>kipoi                                                         </td><td>extended_coda                                                 </td><td>0.1                                                           </td><td>[Author(name='Johnny Israeli', github='jisraeli', email=None)]</td><td>Single bp resolution ChIP-seq denoising                       </td><td>keras                                                         </td><td>H3K27AC_subsampled                                            </td><td>H3K27ac                                                       </td><td>&lt;environment: 0x2b03270&gt;                                </td></tr>
</tbody>
</table>



### Get the kipoi model and make a prediction for the example files


```R
model <- kipoi$get_model("rbp_eclip/CSTF2")
```


```R
predictions <- model$pipeline$predict_example()
```


```R
predictions
```


<table>
<tbody>
	<tr><td>0.27158695</td></tr>
	<tr><td>0.09449492</td></tr>
	<tr><td>0.09449492</td></tr>
	<tr><td>0.27158695</td></tr>
	<tr><td>0.27158695</td></tr>
	<tr><td>0.27158695</td></tr>
	<tr><td>0.09449492</td></tr>
	<tr><td>0.27158695</td></tr>
	<tr><td>0.27158695</td></tr>
	<tr><td>0.27158695</td></tr>
	<tr><td>0.27158695</td></tr>
	<tr><td>0.27158695</td></tr>
	<tr><td>0.27158695</td></tr>
	<tr><td>0.27158695</td></tr>
</tbody>
</table>




```R
class(predictions)
```


'matrix'
