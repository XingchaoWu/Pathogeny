#_*_coding:UTF-8_*_

import os
import argparse
import subprocess
import re

def formate_vfdb(cur_path):
    with open(cur_path + "/" + args.fasta ,"r") as in_fasta:
        with open(cur_path + "/" + args.fasta.split(".")[:-1] + "_formate.fasta" ,"w") as out_fasta:
            for line in in_fasta:
                line = line.strip()[1:]
                pattern = re.compile(r'[(](.*?)[)]', re.S)
                num = re.findall(pattern, line)[-1]
                if line.startswith(">"):
                    gene_num = line.strip()[1:].split(" ")[0]
                    out_fasta.write(gene_num + " | " + num + "\n")
                else:
                    out_fasta.write(line)
    in_fasta.close()
    out_fasta.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Format the sequence file, retaining only the virulence gene number "
                                     "and obtaining the virulence_gene_number to virulence_factor_number mapping")
    parser.add_argument("-f", "--fasta", type=str, help="VFDB fasta file")
    parser.add_argument("-x", "--xls", type=str, help="VFs description file")
    parser.add_argument("-o", "--outfile", type=str, help="output file")
    parser.add_argument("-v", "--vfdb", type=str, help="only run formate_vfdb.py")
    args = parser.parse_args()
    parser.add_argument()
    cur_path = os.getcwd()
    formate_vfdb(cur_path)
