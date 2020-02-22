#_*_coding:UTF-8_*_

import os
import argparse
import math


"""
分割基因组序列至76bp,含38bp的overlap序列，并生成fastq格式文件
"""

def split_genome(cur_path):
    # 去除序列分行
    with open('%s/%s'%(cur_path,args.input_file)) as in_file:
        with open("%s/.tmp"%(cur_path),"w") as tmp:
            for line in in_file:
                if line.startswith(">"):
                    tmp.write(line)
                else:
                    tmp.write(line.strip())
    in_file.close()
    tmp.close()

    title = ""
    seq = ""
    with open("%s/.tmp"%(cur_path),'r') as tmp1:
            for line01 in tmp1:
                if line01.startswith(">"):
                    title = line01.strip()
                else:
                    seq = line01.strip()
    tmp1.close()

    # 序列分割成含overlap的fastq格式文件
    with open("%s/%s.fastq"%(cur_path,args.input_file), 'w') as outfile:
        outfile.write(title + "\t" + "0" + "\n")
        outfile.write(seq[0:76] + "\n")
        outfile.write("+"  + "\n")
        outfile.write("H" * len(seq[0:76]) + "\n")
        for i in range(1,int(math.ceil(len(seq)/38))):
            outfile.write(title + "\t" + str(i)+ "\n")
            outfile.write(seq[(38*i):38*(i+2)] + "\n")
            outfile.write( "+"  + "\n")
            outfile.write("H" * len(seq[(38*i):38*(i+2)]) + "\n")
    outfile.close()

    # 删除中间文件
    rm_tmp_cmd = "rm %s/.tmp"%cur_path
    os.system(rm_tmp_cmd)

    # 压缩fastq文件
    gzip_fastq_cmd = "gzip %s/%s.fastq"%(cur_path,args.input_file.split["_"][:1])
    os.system(gzip_fastq_cmd)


if __name__ ==  "__main__":
    parser = argparse.ArgumentParser("The genome was splited to the length of 76bp")
    parser.add_argument("-i", "--input_file", type=str, help=".fasta/.fna/.fa")
    args = parser.parse_args()
    cur_path = os.getcwd()
    split_genome(cur_path)
