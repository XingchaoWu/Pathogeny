# —*—coding:utf-8_*_
# author: Xingchao Wu
# date：20200220

import os
import argparse
import time

def generate_prelim_map(cur_path):
    with open("%s/%s"%(cur_path,args.inputfile)) as in_fa:
        with open("%s/prelim_map.txt"%args.outdir,"w") as out_txt:
            for line in in_fa:
                if line.startswith(">"):
                    out_txt.write("TAXID\ttmp.%s\t%s\n"%(line.strip()[1:],line.strip().split("|")[-1]))
    in_fa.close()
    out_txt.close()
    print(time.asctime(time.localtime(time.time())) +"\tgenerate prelim_map has completed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser("generate prelim_map.txt",usage="python generate_prelim_map.py -r [.fa] -o [dir]")
    required = parser.add_argument_group("required")
    required.add_argument("-r", "--inputfile", type=str, help="input .fa to generate prelim_map.txt",required=True)
    required.add_argument("-o", "--outdir", type=str, help="output path[default ./]",required=True)
    args = parser.parse_args()
    cur_path = os.getcwd()
    generate_prelim_map(cur_path)