import sys
import gzip
import os

builddict = {
    "grch38": "hg38",
    "hg38": "hg38",
    "hg19": "hg19",
    "grch37": "hg19",
    "grch36": "hg18",
    "hg18": "hg18",
    "ncbi36": "hg18",
    "ncbi35": "hg17",
    "hg17": "hg17",
}

build_field_dict = { # catalog version : build header
    "1": "Original Genome Build",
    "2": "genome_build",
    "3":"HmPOS_build",
    "NA": "Original Genome Build"
}

filename = sys.argv[-1]
version = sys.argv[-2]  # pgs catalog format version, 1, 2, or 3(their harmonized)
dbsnp = sys.argv[-3] # where bed_chr_*.bed.gz are located

## pre-defined path
#dbsnp = "gs://hdchpcprodtis1-staging/Reference/dbSNP"
dbsnp = dbsnp.rstrip() # dbsnp bed files to use only to fill in chr and bp positions if missing, but rsIDs are present. Missing allelic code info will not be determined in this script as dbSNP can have multiple alleles for one rsID variant
#momentarily retired: pipeline does not covert dbsnp IDs to chromosome and bp anymore, due to large size of dbsnp bed files.

## assert params
if not version in ["1", "2", "3"]:
    print(
        "Unrecognized params for format version. Will momentarily assume as version2 and confirm by searching the headers."
    )
    version = "NA"


if filename.endswith(".gz"):
    infile = gzip.open(filename, mode='rt')
else:
    infile = open(filename)

pastheader = False
nheader = 0
build = "buildNA"
build_field = build_field_dict.get(version,'genome_build')
for ii, line in enumerate(infile):
    if pastheader:
        if ii == nheader + 1:
            outfile = filename.replace(".gz", "").replace(
                ".txt", "_" + build + "_reformated.txt"
            )
            outfile = open(outfile, "w")
            if flag_dbsnp:
                rs2otherfields = (
                    {}
                )  # prepare a dict of input file with rsID:effectA_refA_weight
        # assuming file is tab delimited, to simplify situations of blank fields
        line = line.strip("\n").split("\t")
        # fixing missing/blank fields
        for i, field in enumerate(line):
            if field == "":
                line[i] = "NA"
        if flag_dbsnp:  # no chr or bp, but rsID
            info = [line[i] for i in index]
            rs2otherfields[info[0]] = "_".join(info[1:])
            original_snps.append(info[0])
        elif flag_field:  # all fields present
            info = [line[i] for i in index]
            outfile.write("%s\n" % "\t".join(info))
        else:  # no rsID
            info = [line[i] for i in index]
            snp = ":".join(line[0:])
            outfile.write("%s\t%s\n" % (snp, "\t".join(info)))
    elif (not line.startswith("#")) and ("effect_allele" in line):
        pastheader = True
        nheader = ii
        # if 'hg38' in line.lower() or 'grch38' in line.lower():
        #    build = 'hg38'
        line = line.strip().split()
        if version == "1":
            print(
                "Formatting the input weight file: assuming the format version is in PGS catalog v1.0"
            )
            rs_field = "rsID"
            oa_field = "reference_allele"
            chr_field = "chr_name"
            pos_field = "chr_position"
        elif version == "2":
            print(
                "Formatting the input weight file: assuming the format version is in PGS catalog v2.0"
            )
            rs_field = "rsID"
            oa_field = "other_allele"
            chr_field = "chr_name"
            pos_field = "chr_position"
        else:
            print(
                "Formatting the input weight file: assuming the format version is in PGS catalog v3.0"
            )
            rs_field = "hm_rsID"
            oa_field = "other_allele"
            chr_field = "hm_chr"
            pos_field = "hm_pos"
        minimum = [rs_field, "effect_allele", oa_field, "effect_weight"]
        required = [
            chr_field,
            pos_field,
            "effect_allele",
            oa_field,
            "effect_weight",
        ]
        stringent = [
            rs_field,
            chr_field,
            pos_field,
            "effect_allele",
            oa_field,
            "effect_weight",
        ]  # some file might not have the field 'rsID'
        if set(stringent).issubset(set(line)):  # ideally, all wanted fields present
            index = [line.index(field) for field in stringent]
            flag_field = True
            flag_dbsnp = False
        elif set(required).issubset(set(line)):  # less ideally, no rsID field present
            # assert set(required).issubset(set(line)), "Some required fields of / chr_position, effect_allele, reference_allele, effect_weight/ are not present."
            index = [line.index(field) for field in required]
            flag_field = False
            flag_dbsnp = False
        else:  # see if at least rsID is present, can update chr and bp info
            assert set(minimum).issubset(
                set(line)
            ), "Error: Requiring fields of effect_allele, reference_allele/other_allele, effect_weight, and either chr + bp or rsID."
            print(
                "The input file has snpID, but no chr and bp columns (both). Will update position info with dbSNP."
            )
            build = "hg38"
            index = [line.index(field) for field in minimum]
            flag_dbsnp = True
            original_snps = []  # a list to preserve the orignal order of snps
    elif build_field in line:
        build = builddict.get(line.strip().split("=")[1].strip().lower(), "buildNA")       
    elif version == "NA" and "format_version=2.0" in line:
        version = "2"

# in case file formatting that never recognized the last header line
if not pastheader:
    print("File format error. Check the column names etc. for the input weight file.")

# below is momentarily retired. dbsnp is not provided in the container.
# if no rs or bp, but rsID, then need to update the position info from dbSNP hg38
if flag_dbsnp:
    snp2pos = {}  # a dict of rsID:chr_bp
    for chr in range(1, 23):
        # os.system("gsutil -q cp gs://hdchpcprodtis1-staging/mlin/dbSNP/bed_chr_" + str(chr) + ".bed.gz .")
        #os.system("gsutil -mq cp " + dbsnp + "/bed_chr_" + str(chr) + ".bed.gz .")
        for line in gzip.open(dbsnp + "/bed_chr_" + str(chr) + ".bed.gz"):
            line = line.strip().split()
            if line[3] in rs2otherfields:
                snp2pos[line[3]] = "_".join([line[0].replace("chr", ""), line[2]])
        os.system("rm bed_chr_" + str(chr) + ".bed.gz")
    for snp in original_snps:
        outfile.write(
            "%s\t%s\n"
            % (
                snp,
                "\t".join(
                    snp2pos.get(snp, "NA_NA").split("_")
                    + rs2otherfields.get(snp, "NA_NA_NA").split("_")
                ),
            )
        )


outfile.close()
