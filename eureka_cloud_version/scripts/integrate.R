args = commandArgs(T)
score.list <- read.table(args[1])
output.name <- args[2]


i=0
for(filename in as.character(score.list$V1)){
  #infile <- read.table(paste("chr", i, "_CCPM_trait_snps.sscore", sep=""), colClasses = c("character", "numeric", "numeric", "numeric"))
  i = i+1
  #infile <- read.table(filename, colClasses = c("character", "numeric", "numeric", "numeric"))
  infile <- read.table(filename, colClasses="character", header=T)
  coln <- ncol(infile)
  if(i==1){ # on the first file
    scores <- infile
    scores$ALLELE_CT <- as.numeric(scores$ALLELE_CT)
    scores$NAMED_ALLELE_DOSAGE_SUM <- as.numeric(scores$NAMED_ALLELE_DOSAGE_SUM)
    scores$SCORE <- as.numeric(scores$SCORE)
    if(coln==5){
      # has FID present
      scores$tempID <- paste(scores$FID, scores$IID, sep=':')
    }else if(coln==4){
      # just IID
      next
    }else{
      stop(paste0('Wrong number of columns in the score output for ', filename))
      }
  }else{ # onto the second file and beyond
    if(coln==5){
      infile$tempID <- paste(infile$FID, infile$IID, sep=':')
      temp_ct <- as.numeric(infile$ALLELE_CT[match(scores$tempID, infile$tempID)]) + scores$ALLELE_CT
      scores$ALLELE_CT <- temp_ct # update total allele counts before imputation
      temp_dsum <- as.numeric(infile$NAMED_ALLELE_DOSAGE_SUM[match(scores$tempID, infile$tempID)]) + scores$NAMED_ALLELE_DOSAGE_SUM
      scores$NAMED_ALLELE_DOSAGE_SUM <- temp_dsum # update sum of dosages of the risk alleles before imputation
      temp_score <- as.numeric(infile$SCORE[match(scores$tempID, infile$tempID)]) + scores$SCORE
      scores$SCORE <- as.numeric(temp_score)
    }else if(coln==4){
      temp_ct <- as.numeric(infile$ALLELE_CT[match(scores$IID, infiles$IID)]) + scores$ALLELE_CT
      scores$ALLELE_CT <- temp_ct
      temp_dsum <- as.numeric(infile$NAMED_ALLELE_DOSAGE_SUM[match(scores$IID, infile$IID)]) + scores$NAMED_ALLELE_DOSAGE_SUM
      scores$NAMED_ALLELE_DOSAGE_SUM <- temp_dsum # update sum of dosages of the risk alleles before imputation
      temp_score <- as.numeric(infile$SCORE[match(scores$IID, infile$IID)]) + scores$SCORE
      scores$SCORE <- as.numeric(temp_score)
    }else{
      stop(paste0('Wrong number of columns in the score output for ', filename))
      }
  }
}

if(ncol(scores)==6){ # with FID, and then the extra column of tempID
  scores2 <- scores[,c("FID", "IID", "ALLELE_CT", "NAMED_ALLELE_DOSAGE_SUM", "SCORE")
}else{
  scores2 <- scores
}

write.table(scores2, output.name, col.names=F, row.names=F, quote=F, sep='\t')
