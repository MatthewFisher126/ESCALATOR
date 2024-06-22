# ESCALATOR README

Feel free to download ESCALATOR itself from this github page or you can make it into a container. The tool/container will work in a SLURM environment or locally but it is recommended to use in a SLURM environment if your data set is large.  

## Using the singularity container:

You can download the escalator.def file and create the container on https://cloud.sylabs.io/. You will also need singularity installed locally or on your HPC. 

Running the container is almost the same as above but you will specify the container name, the wrapper script, and then all of the arguments. Simply run the below:

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

## Using the original scripts by download: 

**Note: You will need to download this repo and edit the masterPRS_v4.sh. Then,** 
- **unzip the prs_pipeline_bin.tar.gz file in the [bin folder](eureka_cloud_version/bin/prs_pipeline_bin.tar.gz)**
- **Uncomment "script_path" and "bin_path" on lines 13 and 14 to point to the locations of the ESCALATOR scripts as in the [scripts folder](eureka_cloud_version/scripts) and
  unzipped binary software as in the [bin folder](eureka_cloud_version/bin/prs_pipeline_bin.tar.gz), respectively**
- **Comment out the same variables on lines 83 and 84.**


Once the above steps are complete, simply run the wrapper with the required arguments. 

An example is below:
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

# Example
bash masterPRS_format_v2_freeze3.sh 2 \
./test_escalator/ \
non_hla_escalator_input.txt \
./out_escalator/ \
GRS2_non_hla \
./freeze3_w_dosages \
freeze3_dosages_PAIR \
./ESCALATOR/eureka_cloud_version/scripts/ \
./ESCALATOR/eureka_cloud_version/bin/prs_pipeline_bin/ \
T \
NA
``` 


