# —*—coding:utf-8_*_
# author: Xingchao Wu

"""
分割基因组序列至76bp,含38bp的overlap序列，并生成fastq格式文件
仅适用于完整基因组序列文件
"""
import os
import argparse

def split_genome(cur_path):
    title = ""
    seq = ""
    # 取消序列分行,将序列拼接成一个长的字符串
    with open('%s/%s'%(cur_path,args.input_file),"r") as in_file:
        for line in in_file:
            if line.startswith(">"):
                title = line.strip()
            else:
                seq += line.strip()
    in_file.close()
    # 序列分割成含overlap的fastq格式文件
    with open("%s/%s_%s.fastq"%(cur_path,args.input_file.split("_")[0],args.input_file.split("_")[1]), 'w') as outfile:
        outfile.write(title.replace(">","@") + "\t" + "0" + "\n")
        outfile.write(seq[0:76] + "\n")
        outfile.write("+" + "\n")
        outfile.write("H" * len(seq[0:76]) + "\n")
        for i in range(1,len(seq)-75):
            outfile.write(title.replace(">","@") + "\t" + str(i)+ "\n")
            outfile.write(seq[i:(75+i)] + "\n")
            outfile.write("+" + "\n")
            outfile.write("H" * len(seq[i:(75+i)]) + "\n")
    outfile.close()

    # 压缩
    gzip_cmd = "gzip %s_%s.fastq"%(args.input_file.split("_")[0],args.input_file.split("_")[1])
    os.system(gzip_cmd)

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser("The sequence is trimmed to 76bp")
    parser.add_argument("-i", "--input_file", type=str, help=".fasta|.fna|.fa")
    args = parser.parse_args()
    cur_path = os.getcwd()
    split_genome(cur_path)

