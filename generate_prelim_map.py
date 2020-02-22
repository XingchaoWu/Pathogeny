#_*_coding:UTF-8_*_

import os
import argparse
import time

# >CU329670.1|kraken:taxid|4896
def generate_prelim_map(cur_path):
    # out_txt = open("%s/prelim_map.txt"%odir,"w")
    with open("%s/%s"%(cur_path,args.inputfile)) as in_fa:
        with open("%s/prelim_map.txt"%args.outdir,"w") as out_txt:
            for line in in_fa:
                if line.startswith(">"):
                    # print("TAXID\ttmp.%s\t%s\n"%(line.strip()[1:],line.strip().split("|")[-1]), file=out_txt)
                    out_txt.write("TAXID\ttmp.%s\t%s\n"%(line.strip()[1:],line.strip().split("|")[-1]))
    in_fa.close()
    out_txt.close()
    print(time.asctime(time.localtime(time.time())) +"\tgenerate prelim_map has completed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser("generate prelim_map.txt",usage="python generate_prelim_map.py [optional] -r [.fa]")
    required = parser.add_argument_group("必选项")
    optional = parser.add_argument_group("可选项")
    required.add_argument("-r", "--inputfile", type=str, help="input .fa to generate prelim_map.txt",required=True)
    optional.add_argument("-o", "--outdir", type=str, help="output path[default ./]",required=True)
    args = parser.parse_args()
    cur_path = os.getcwd()
    generate_prelim_map(cur_path)
