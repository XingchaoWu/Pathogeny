# —*—coding:utf-8_*_
# author: Xingchao Wu

import os
import argparse
import time

def trim(cur_path):
    # 数据质控去除低质碱基
    trimmomatic_path = "/home/qiime2/miniconda/envs/wgs/bin/trimmomatic"
    ILLUMINACLIP_path = "/home/qiime2/miniconda/envs/wgs/share/trimmomatic/adapters"
    trim_cmd = "jar %s SE -threads %d -phred33 -trimlog " \
               "%s/%s/%s/trim/%s.trim.log " \
               "%s/fastq/%s_1.fastq.gz " \
               "%s/%s/%s/trim/%s.clean.fastq.gz " \
               "ILLUMINACLIP:%s:2:20:10:1:true LEADING:15 TRAILING:15 SLIDINGWINDOW:5:20 MINLEN:36 AVGQUAL:20"\
               %(trimmomatic_path,args.core_thread,cur_path,args.version,args.sample,args.sample,cur_path,
                 args.sample,cur_path,args.version,args.sample,args.sample,ILLUMINACLIP_path)
    os.system(trim_cmd)
def mpg(cur_path):
    GRCH38_index_path = ""
    bowtie2_path = "/home/qiime2/miniconda/envs/wgs/bin/bowtie2"
    samtools_path = "home/qiime2/miniconda/envs/wgs/bin/samtools"
    GRCH38_align_cmd = "%s -x %s -U %s/%s/%s/trim/%s.clean.fastq.gz --threads 32 --maxins 800 --end-to-end " \
                       "-S %s/%s/%s/map/%s.nohuman.sam 2> %s/%s/%s/map/%s.nohuman.sam.log"\
                       %(bowtie2_path,GRCH38_index_path,cur_path,args.version,args.sample,args.sample,
                         cur_path,args.version,args.sample,args.sample,cur_path,args.version,args.sample,args.sample)
    os.system(GRCH38_align_cmd)
    # exclude unmapped from bam (GRCH38)
    os.system("python excclude_from_bam.py -in %s/%s/%s/map/%s.nohuman.sam -out %s/%s/%s/map/%s.non_human.exclude"
              %(cur_path,args.version,args.sample,args.sample,cur_path,args.version,args.sample,args.sample))
    # remove nt human seq
    nt_human_index = ""
    nt_human_align_cmd = "%s -x %s -U %s/%s/%s/map/%s.non_human.exclude.fastq.gz --threads 32 --maxins 800 --end-to-end " \
                         "-S %s/%s/%s/map/%s.nt_humman.sam 2> %s/%s/%s/map/%s.nt_humman.sam.log"\
                         %(bowtie2_path,nt_human_index,cur_path,args.version,args.sample,args.sample,
                           cur_path,args.version,args.sample,args.sample,cur_path,args.version,args.sample,args.sample)
    os.system(nt_human_align_cmd)
    # exclude unmapped from bam (nt_human)
    os.system("python excclude_from_bam.py -in %s/%s/%s/map/%s.nt_humman.sam -out %s/%s/%s/map/%s.non.nt_humman.exclude"
              %(cur_path,args.version,args.sample,args.sample,cur_path,args.version,args.sample,args.sample))
    # remove plasmid seq
    plasmid_index = ""
    plasmid_align_cmd = "%s -x %s -U %s/%s/%s/map/%s.non.nt_human.exclude.fastq.gz --threads 32 --maxins 800 --end-to-end " \
                         "-S %s/%s/%s/map/%s.plasmid.sam 2> %s/%s/%s/map/%s.plasmid.sam.log"\
                         %(bowtie2_path,plasmid_index,cur_path,args.version,args.sample,args.sample,
                           cur_path,args.version,args.sample,args.sample,cur_path,args.version,args.sample,args.sample)
    os.system(plasmid_align_cmd)
    # exclude unmapped from bam (pplasmid)
    os.system("python excclude_from_bam.py -in %s/%s/%s/map/%s.plasmid.sam -out %s/%s/%s/map/%s.exclude"
              % (cur_path, args.version, args.sample, args.sample, cur_path, args.version, args.sample, args.sample))

    # remove dup

def mpm(cur_path):
    # kraken鉴定
    kraken_path = "/home/qiime2/biosoft/kraken2/kraken2/kraken2"
    kraken_db_path = ""
    kraken_cmd = "%s --db %s --threads 15 --gzip-compressed --report-zero-counts --confidence 0.65 " \
                 "--report %s/%s/%s/bracken/%s.kraken.report.txt " \
                 "--classified-out %s/%s/%s/bracken/%s.fastq " \
                 "--use-names %s/%s/%s/map/%s.exclude.fastq.gz > %s/%s/%s/map/%s.kraken.output.txt"\
                 %(kraken_path,kraken_db_path,cur_path, args.version, args.sample, args.sample,
                   cur_path, args.version, args.sample, args.sample,
                   cur_path, args.version, args.sample, args.sample,cur_path, args.version, args.sample, args.sample)
    os.system(kraken_cmd)
    # 丰度计算
    """
    python /home/pmd/soft/Bracken-2.2/src//est_abundance.py 
    -k /home/pmd/genome/index_0206/DEC2020/index/bracken/FBVP_hs37d5.KMER75_DISTR.TXT 
    -t 1 -l S 
    -i /home/pmd/analysis/PM20040/se_v2/A200213PCRN015/bracken/A200213PCRN015.kraken.report.txt 
    -o /home/pmd/analysis/PM20040/se_v2/A200213PCRN015/bracken/A200213PCRN015.bracken.species.txt
    """
    bracken_path = "/home/qiime2/biosoft/Bracken/src/est_abundance.py"
    bracken_kmer_path = ""
    for i in ["S", "G"]:
        if i == "S":
            est_abundance_cmd = "python %s -k %s -t 1 -l %s " \
                                "-i %s/%s/%s/bracken/%s.kraken.report.txt " \
                                "-o %s/%s/%s/bracken/%s.bracken.species.txt"\
                                %(bracken_path,bracken_kmer_path,i,cur_path, args.version, args.sample, args.sample,
                                  cur_path, args.version, args.sample, args.sample)
            os.system(est_abundance_cmd)
        else:
            est_abundance_cmd = "python %s -k %s -t 1 -l %s " \
                                "-i %s/%s/%s/bracken/%s.kraken.report.txt " \
                                "-o %s/%s/%s/bracken/%s.bracken.genus.txt"\
                                %(bracken_path,bracken_kmer_path,i,cur_path, args.version, args.sample, args.sample,
                                  cur_path, args.version, args.sample, args.sample)
            os.system(est_abundance_cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("")
    parser.add_argument("-v","--version",type=str,help="version number")
    parser.add_argument("-s","--sample",type=str,help="sample info")
    parser.add_argument("-core","--core_thread",type=int,help="threads")
    parser.add_argument("trim",type=str,help="the step of trimmomatic")
    parser.add_argument("mpg",type=str,help="the step of aligning to human genome")
    parser.add_argument("mpm",type=str,help="the step of aligning to microbe")
    args = parser.parse_args()
    cur_path = os.getcwd()
    print("start : %s"%time.asctime(time.localtime(time.time())))
    for odir in ["trim","map","bracken"]:
        mkdir_cmd = "mkdir -p %s/%s/%s"%(cur_path,args.version,odir)
        os.system(mkdir_cmd)
    if args.trim == "-trim":
        trim(cur_path)
    elif args.mpg == "-mpg":
        mpg(cur_path)
    elif args.mpm == "-mpm":
        mpm(cur_path)
    print("End : %s"%time.asctime(time.localtime(time.time())))

