import sys

nvar = int(sys.argv[-3])
infile = open(sys.argv[-2])
outfile = open(sys.argv[-1], 'w')

flag_fid = False
for line in infile:
    if line.startswith('#'):
        line = line.replace('#', '').strip().split()
        if 'FID' in line: # optional field depending on the input data
            flag_fid = True
            index_fid = line.index('FID')
        index_iid = line.index('IID')
        index_ct = line.index('ALLELE_CT')
        index_dsum = line.index('NAMED_ALLELE_DOSAGE_SUM')
        index_avg = line.index('SCORE1_AVG')
        if flag_fid:
            outfile.write('FID\tIID\tALLELE_CT\tNAMED_ALLELE_DOSAGE_SUM\tSCORE\n')
        else:
            outfile.write('IID\tALLELE_CT\tNAMED_ALLELE_DOSAGE_SUM\tSCORE\n')
    else:
        line = line.strip().split()
        score_avg = float(line[index_avg])
        score = score_avg * nvar * 2
        if flag_fid:
            outfile.write('%s\n' % '\t'.join([line[index_fid], line[index_iid], line[index_ct], line[index_dsum], str(score)]))
        else:
            outfile.write('%s\n' % '\t'.join([line[index_iid], line[index_ct], line[index_dsum], str(score)]))
outfile.close()
