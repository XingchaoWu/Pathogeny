# —*—coding:utf-8_*_
# author: Xingchao Wu
# date: 20200209

"""
注释：
    包含assembly_summary.txt的url地址列表
    bacteria,archaea,fungi,viral,protozoa四类genbank和refseq assembly summary file
"""

import subprocess
import argparse

def taxonomy():
    taxdump_url = ["ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz"]
    taxonomy_urls = ["ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz",
                     "ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/nucl_wgs.accession2taxid.gz"]
    cmd0 = "mkdir taxonomy"
    subprocess.check_output(cmd0, shell=True)
    cmd1 = "cd taxonomy && wget %s"%taxdump_url[0]
    cmd2 = "cd taxonomy &&  tar -zxvf %s"%taxdump_url[0].split("/")[5]
    subprocess.check_output(cmd1, shell=True)
    subprocess.check_output(cmd2, shell=True)
    for url in taxonomy_urls:
        cmd3 = "cd taxonomy && wget %s"%url
        cmd4 = "cd taxonomy && gunzip %s"%url.split("/")[6]
        subprocess.check_output(cmd3, shell=True)
        subprocess.check_output(cmd4, shell=True)

def download_assembly():
    # refseq genomes info download
    # bacteria/archaea/fungi/viral/protozoa
    refseq_url = ["ftp://ftp.ncbi.nih.gov/genomes/refseq/assembly_summary_refseq.txt"]
    refseq_url_list = ["ftp://ftp.ncbi.nih.gov/genomes/refseq/bacteria/assembly_summary.txt",
                       "ftp://ftp.ncbi.nih.gov/genomes/refseq/archaea/assembly_summary.txt",
                       "ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/assembly_summary.txt",
                       "ftp://ftp.ncbi.nih.gov/genomes/refseq/viral/assembly_summary.txt",
                       "ftp://ftp.ncbi.nih.gov/genomes/refseq/protozoa/assembly_summary.txt"]
    # genbank genomes info download
    # bacteria/archaea/fungi/viral/protozoa
    genbank_url = ["ftp://ftp.ncbi.nih.gov/genomes/genbank/assembly_summary_genbank.txt"]
    genbank_url_list = ["ftp://ftp.ncbi.nih.gov/genomes/genbank/bacteria/assembly_summary.txt",
                        "ftp://ftp.ncbi.nih.gov/genomes/genbank/archaea/assembly_summary.txt",
                        "ftp://ftp.ncbi.nih.gov/genomes/genbank/fungi/assembly_summary.txt",
                        "ftp://ftp.ncbi.nih.gov/genomes/genbank/viral/assembly_summary.txt",
                        "ftp://ftp.ncbi.nih.gov/genomes/genbank/protozoa/assembly_summary.txt"]
    # options "refseq"
    if args.input_type == "refseq":
        cmd = "wget -O %s_%s %s"%(refseq_url[0].split("/")[4],refseq_url[0].split("/")[5],refseq_url[0])
        subprocess.check_output(cmd, shell=True)
        for ref_url in refseq_url_list:
            cmd1 = "wget -O %s_%s_%s %s"%(ref_url.split("/")[4],ref_url.split("/")[5],ref_url.split("/")[6],ref_url)
            subprocess.check_output(cmd1, shell=True)
    # options "genbank"
    elif args.input_type == "genbank":
        cmd = "wget -O %s_%s %s"%(genbank_url[0].split("/")[4],genbank_url[0].split("/")[5],genbank_url[0])
        subprocess.check_output(cmd, shell=True)
        for genbank_url in genbank_url_list:
            cmd1 = "wget -O %s_%s_%s %s"%(genbank_url.split("/")[4],genbank_url.split("/")[5],genbank_url.split("/")[6],genbank_url)
            subprocess.check_output(cmd1, shell=True)
    # options "all"
    elif args.input_type == "all":
        # total info
        merger_url = []
        merger_url.append(refseq_url[0])
        merger_url.append(genbank_url[0])
        # split info
        merger_url_list = []
        for i in refseq_url_list:
            merger_url_list.append(i)
        for j in genbank_url_list:
            merger_url_list.append(j)
        for url in merger_url:
            cmd = "wget -O %s_%s %s"%(url.split("/")[4],url.split("/")[5],url)
            subprocess.check_output(cmd, shell=True)
        for url1 in merger_url_list:
            cmd1 = "wget -O %s_%s_%s %s"%(url1.split("/")[4],url1.split("/")[5],url1.split("/")[6],url1)
            subprocess.check_output(cmd1, shell=True)
    else:
        print("ERROR: CHECK THE TYPE")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download assembly summary from genbank or refseq", usage="download_genbank_assembly.py [-type] INPUT_TYPE [-tax] TAXONOMY")
    parser.add_argument('-tax', "--taxonomy", type=str, help= "GenBank taxonomy files")
    parser.add_argument('-type',"--input_type",type=str, help="input the download directory such as 'refseq', 'genbank' or 'all'")
    args = parser.parse_args()
    if args.taxonomy == "taxonomy":
        taxonomy()
    elif args.input_type == "refseq" or args.input_type == "genbank" or args.input_type == "all":
        download_assembly()
    else:
        print("usage: download_genbank_assembly.py [-h] [-type INPUT_TYPE] [-tax TAXONOMY]")