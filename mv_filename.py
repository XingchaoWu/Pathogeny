#_*_coding:UTF-8_*_


import os
import subprocess
import argparse

def mv_filename(cur_path):
    with open(args.inputfile) as in_file:
        for line in in_file:
            line = line.strip().split("\t")

            cmd = "mv " + cur_path + "/"+ line[0] + "_1.fastq.gz " + line[1] + "_1.fastq.gz" 
            subprocess.check_output(cmd,shell=True)
    in_file.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser("change the file name")
    parser.add_argument("-i", "--inputfile",type=str,help="The original name corresponds to the modified name")
    args =parser.parse_args()
    cur_path = os.getcwd()
    mv_filename(cur_path)
