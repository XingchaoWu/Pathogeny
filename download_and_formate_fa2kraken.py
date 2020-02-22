#_*_coding:UTF-8_*_

import os
import subprocess
import argparse

def obtain_download_formate_ftp(ftp_dict,cur_path):
    # exclude ftp
    with open(args.assembly_genbank,"r") as gene_bank:
        for line in gene_bank:
            if not line.startswith("#"):
                line = line.strip().split("\t")
                ftp_dict[line[0]] = [line[5],line[19]]
    for k in ftp_dict.keys():
        if k == args.accession:
            ftp = ftp_dict[k][1]

            # download genome
            download_genome = "wget %s/%s_genomic.fna.gz"%(ftp,ftp.split("/")[-1])
            subprocess.check_output(download_genome, shell=True)

            # gunzip genome
            gunzip_file = "gunzip %s_genomic.fna.gz"%(ftp.split("/")[-1])
            subprocess.check_output(gunzip_file,shell=True)

            # formate_fa
            with open("%s/%s_genomic.fna"%(cur_path,ftp.split("/")[-1]), "r") as in_fa:
                with open("%s/%s_genomic_kraken.fna"%(cur_path,ftp.split("/")[-1]), "w") as out_fa:
                    for line in in_fa:
                        if line.startswith(">"):
                            out_fa.write("%s|kraken:taxid|%s\n"%(line.strip().split(" ")[0],ftp_dict[k][0]))
                        else:
                            out_fa.write(line)
            # file rename
            os.rename("%s/%s_genomic_kraken.fna"%(cur_path,ftp.split("/")[-1]),"%s/%s_genomic.fna"%(cur_path,ftp.split("/")[-1]))
            # rename_cmd = "mv %s/%s_genomic_kraken.fna %s/%s_genomic.fna"%(cur_path,ftp.split("/")[-1],cur_path,ftp.split("/")[-1])
            # subprocess.check_output(rename_cmd,shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Accession to download the genome and format as kraken",
                                     usage="\npython download_and_formate_fa2kraken.py -ac [accession] -as [assembly_summarry.txt]")
    parser.add_argument("-ac","--accession",type=str,help="accession num")
    parser.add_argument("-as","--assembly_genbank", type=str,help="assembly_summary_genbank.txt")
    args = parser.parse_args()
    ftp_dict = {}
    cur_path = os.getcwd()
    obtain_download_formate_ftp(ftp_dict,cur_path)

