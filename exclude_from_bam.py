# —*—coding:utf-8_*_
# author: Xingchao Wu

import os
import argparse

def excclude_from_bam(cur_path,samtools_path):
    # sam2bam
    sam2bam_cmd = "%s view -bS %s > %s.bam"%(samtools_path,args.infile,args.outfile)
    exclude_from_bam_cmd = "%s fastq -f 4 %s.bam > %s.non_human.exclude.fastq"%(samtools_path,args.outfile,args.outfile)
    gzip_cmd = "gzip %s.non_human.exclude.fastq"%(args.outfile)
    os.system(sam2bam_cmd)
    os.system(exclude_from_bam_cmd)
    os.system(gzip_cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-in","--infile",type=str,help="input file")
    parser.add_argument("-out", "--outfile",type=str,help="output file")
    args = parser.parse_args()
    cur_path = os.getcwd()
    samtools_path = ""
    excclude_from_bam(cur_path,samtools_path)
