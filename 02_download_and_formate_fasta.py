# _*_coding:UTF-8_*_
# author Xingchao Wu
# date 2020-02-17

import os
import argparse
import time

def screenGenomeInfo(merge_dict):
    assembly_dict = {}
    with open("%s"%args.path,"r",encoding="UTF-8") as in_file:
        for line in in_file:
            if not line.startswith("#"):
                line = line.strip().split("\t")
                assembly_dict[line[0]] = [line[4],line[5],line[6],line[11],line[17],line[19]]
    in_file.close()

    # 1.按照组装级别筛选信息
    # 分别筛选出组装级别是Complete Genome、Chromosome的accession信息以及组装级别为Scaffold、Contig的accession信息
    assembly_level_top_dict = {}
    assembly_level_down_dict = {}
    assembly_level_top_list = []
    for ac,ac_value in assembly_dict.items():
        if ac_value[3] in ["Complete Genome","Chromosome"] and ac_value[1] != ac_value[2]:
            assembly_level_top_list.append(ac_value[2])
            assembly_level_top_dict[ac] = ac_value
            merge_dict[ac] = ac_value
        else:
            assembly_level_down_dict[ac] = ac_value
    print("the assembly accession number of 'complete genome' or 'chromosome' : %s"%len(assembly_level_top_dict))
    print("the assembly accession number of 'scaffold' or 'contig' : %s"%len(assembly_level_down_dict))

    # 2.组装级别为scaffold、contig的accession信息中筛选出wgs_master为representative genome、reference genome的信息
    assembly_level_down_ref_dict = {}
    assembly_level_down_na_dict = {}
    for ac_down,ac_value_down in assembly_level_down_dict.items():
        if ac_value_down[0] in ["representative genome","reference genome"] and ac_value_down[3] == ["Scaffold","Contig"]:
            assembly_level_top_list.append(ac_value_down[2])
            assembly_level_down_ref_dict[ac_down] = ac_value_down
            merge_dict[ac_down] = ac_value_down
        else:
            assembly_level_down_na_dict[ac_down] = ac_value_down
    print("the assembly accession number of 'representative genome' or 'reference genome' in the assembly level "
          "is 'scaffold' or 'contig' : %s"%len(assembly_level_down_ref_dict))
    print("the assembly accession number of na in the assembly level 'scaffold' or 'contig' : %s"
          %len(assembly_level_down_na_dict))

    # 2.在scaffold或contigs的信息中挑出补充的species_taxid信息
    assembly_level_top_list = list(set(assembly_level_top_list))
    assembly_level_supplyment_dict = {}
    for k,v in assembly_level_down_na_dict.items():
        if v[2] not in assembly_level_top_list:
            assembly_level_supplyment_dict[k] = v
            merge_dict[k] = v
        else:
            continue
    refresh_dict = {}
    for m_key,m_value in merge_dict.items():
        if m_value[1] == m_value[2] and m_value[0] == "na":
            continue
        elif m_value[1] == m_value[2] and m_value[0] in ["representative genome","reference genome"]:
            refresh_dict[m_key] = m_value
        else:
            refresh_dict[m_key] = m_value
    with open("%s/%s/%s_genbank_assembly_summary_screen.log"%(cur_path,args.taxonomy,args.taxonomy),"w") as out_log:
        out_log.write("##assembly_accession\trefseq_category\ttaxid\tspecies_taxid\tgbrs_paired_asm\tftp\n")
        for merge_key,merge_value in refresh_dict.items():
            out_log.write(merge_key+"\t"+merge_value[0]+"\t"+merge_value[1]+"\t"+merge_value[2]+"\t"+merge_value[3]+"\t"+merge_value[4]+"\t"+merge_value[5]+"\n")
    out_log.close()
    print("the total assembly accession number : %s"%len(refresh_dict))

def downloadGenome(merge_dict,cur_path):
    # download and formate genome
    for value in merge_dict.values():
        # download genome
        wget_cmd = "wget -P %s/%s %s/%s_genomic.fna.gz"%(cur_path,args.taxonomy,value[5],value[5].split("/")[-1])
        os.system(wget_cmd)
        # gunzip
        gunzip_cmd = "gunzip %s/%s/%s_genomic.fna.gz"%(cur_path,args.taxonomy,value[5].split("/")[-1])
        os.system(gunzip_cmd)
        print(time.asctime(time.localtime(time.time())) + "  gunzip completed")
        # formate for kraken ()
        with open("%s/%s/%s_genomic.fna"%(cur_path,args.taxonomy,value[5].split("/")[-1]),"r") as in_fna:
            with open("%s/%s/%s_genomic_tmp.fna"%(cur_path,args.taxonomy,value[5].split("/")[-1]),"w") as out_fna:
                for line in in_fna:
                    if line.startswith(">"):
                        out_fna.write("%s|kraken:taxid|%s\n"%(line.strip().split(" ")[0],value[1]))
                    else:
                        out_fna.write(line)
        print(time.asctime(time.localtime(time.time())) + "  Genome formatting complete")
        in_fna.close()
        out_fna.close()
        # rename
        os.rename("%s/%s/%s_genomic_tmp.fna"%(cur_path,args.taxonomy,value[5].split("/")[-1]),
                  "%s/%s/%s_genomic.fna"%(cur_path,args.taxonomy,value[5].split("/")[-1]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Screening genomic information and download genome")
    parser.add_argument("-p","--path",type=str,help="the path of genbank assembly summary txt  or refseq assembly summary txt")
    parser.add_argument("-t","--taxonomy",type=str,help="the info of taxonomy")
    args = parser.parse_args()
    cur_path = os.getcwd()
    merge_dict = {}
    if  os.path.exists("%s/%s"%(cur_path,args.path)) == True:
        os.remove("%s/%s"%(cur_path,args.path))
        mkdir_cmd = "mkdir %s" % args.taxonomy
        os.system(mkdir_cmd)
        screenGenomeInfo(merge_dict)
        downloadGenome(merge_dict,cur_path)
    else:
        mkdir_cmd = "mkdir %s"%args.taxonomy
        os.system(mkdir_cmd)
        screenGenomeInfo(merge_dict)
        downloadGenome(merge_dict, cur_path)

