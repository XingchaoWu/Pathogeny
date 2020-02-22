# —*—coding:utf-8_*_
# author: Xingchao Wu

import os
import argparse
import gzip

def trim2_76bp(cur_path):
    with gzip.open("%s/%s"%(cur_path,args.inputfile),"r") as in_file:
        with open("%s/%s_76_1.fastq"%(cur_path,args.inputfile.split("_")[0]),"w") as out_file:
            for line in in_file:
                if len(line.strip()) <= 75:
                    out_file.write(line)
                else:
                    out_file.write(line.strip()[:76] + "\n")
    in_file.close()
    out_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("The sequence is trimmed to 76bp")
    parser.add_argument("-i", "--inputfile", type=str, help=".fastq")
    args = parser.parse_args()
    cur_path = os.getcwd()
    trim2_76bp(cur_path)
    gzip_file_cmd = "gzip *fastq"
    os.system(gzip_file_cmd)
    
