#_*_coding:UTF-8_*_
import argparse
import subprocess
import os

def Aspergillus_verificate(bowtie2_path,index_path,cur_path,samtools_path):

    # bowtie2 align
    cmd = bowtie2_path + " -x " + index_path + " " + " -U " + "/home/pmd/analysis/" + args.batch + "/se_v1/" \
          + args.sample_num + "/map/" + args.sample_num + ".non_human.exclude.fastq.gz" \
          + " --threads 12 --end-to-end --maxins 800 -S " \
          + cur_path + "/" + args.sample_num + ".af.clean.sam " \
          + "2> " + cur_path + "/" + args.sample_num + ".af.clean.sam.log "
    subprocess.check_output(cmd, shell=True)

    # sam2bam
    cmd1 = samtools_path + " view -b  -S " + args.sample_num + ".af.clean.sam > " + args.sample_num + ".af.clean.bam"
    subprocess.check_output(cmd1, shell=True)

    # exclude fasta
    cmd2 = samtools_path + " fasta -F 4 " + args.sample_num + ".af.clean.bam > " + args.sample_num + ".af.clean.fasta"
    subprocess.check_output(cmd2, shell=True)

    # blastn



if __name__ == '__main__':
    parser = argparse.ArgumentParser("Aspergillus verificate")
    parser.add_argument("-b", "--batch", type=str, help="batch")
    parser.add_argument("-s", "--sample_num", type=str, help="sample num")
    args = parser.parse_args()
    bowtie2_path = "/opt/biotools/bowtie2-2.2.9/bowtie2"
    index_path = "/home/pmd/Genome/Genome_bowtie2/Aspergillus_clean/Aspergillus.fa"
    cur_path = os.getcwd()
    samtools_path = "/opt/apps/samtools-1.3/bin/samtools"
    Aspergillus_verificate(bowtie2_path,index_path,cur_path,samtools_path)
