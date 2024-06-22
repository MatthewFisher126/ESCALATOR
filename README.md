# ESCALATOR README

This repo holds the scripts and the singulairty def file of ESCALATOR. To directly download a the ESCALATOR singularity container, or have a general overview of ESCALATOR introduction and its usage, visit [the general repo](https://github.com/menglin44/ESCALATOR) and its [vignette](https://github.com/menglin44/ESCALATOR/blob/main/escalator_container/ESCALATOR_container_readme.pdf).


## If to create a singularity container:

You can download the [escalator.def](escalator.def) file and create the container on https://cloud.sylabs.io/. You will also need singularity installed locally or on your HPC. 

Refer to the vignette above for explanations and examples of how to run the container. Briefly, running the container requires specifying the container name, the wrapper script, and then all of the arguments. Simply run the below:
(Note that here *"escalator-v2.sif"* can be replaced by the container image name you created)
```
singularity exec escalator-v2.sif masterPRS_v4.sh [reformatting script designed (1, 2, or 3)] \
[input directory (where weight file is)] \
[weight input filename] \
[output directory] \
[trait name (trait_PGSxxx)] \
[pfile directory] \
[pfile prefix name - ex: chr22_freeze3_dosages_PAIR.pgen = freeze3_dosages_PAIR] \
[T or F - whether to remove ambiguous variants] \
[NA or filename - frequency file for PLINK to impute missing genotypes, can be NA to skip if sample size >50]
```

You can also run the below to get similar information on running the container:

```
singularity run-help <container_name>.sif
```

## If to use the original scripts by download the repo: 

**Note: You will need to download this repo and edit the masterPRS_v4.sh. Then,** 
- **Unzip the prs_pipeline_bin.tar.gz file in the [bin folder](eureka_cloud_version/bin/prs_pipeline_bin.tar.gz)**
- **Uncomment "script_path" and "bin_path" on lines 13 and 14 to point to the locations of the ESCALATOR scripts as in the [scripts folder](eureka_cloud_version/scripts) and
  unzipped binary software as in the [bin folder](eureka_cloud_version/bin/prs_pipeline_bin.tar.gz), respectively**
- **Comment out the same variables on lines 83 and 84.**


Once the above steps are complete, simply run the wrapper with the required arguments similar to the way above, except for replacing "singularity exec" by "bash". 

```
# Arguments
Bash masterPRS_v4.sh [reformatting script designed (1, 2, or 3)] \
[input directory (where weight file is)] \
[weight input filename] \
[output directory] \
[trait name (trait_PGSxxx)] \
[pfile directory] \
[pfile prefix name - ex: chr22_freeze3_dosages_PAIR.pgen = freeze3_dosages_PAIR]
[path to scripts] \
[path to prs_pipeline_bin (plink and liftover)] \
[whether to remove ambiguous variants] \
[frequency file under the input directory to impute missing genotypes, can be 'NA' if none]
``` 


