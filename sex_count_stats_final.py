#_*_coding:UTF-8_*_
# 修改于20200109
import os
import argparse
import re
import csv
import subprocess

def obtain_sample(cur_path,sample_list):
    with open("%s/%s"%(cur_path,args.sample_list),"r") as in_list:
        for info in in_list:
            info = info.strip().split("\t")
            if re.findall("^[AR]",info[1]):
                sample_list.append(info[1])
            else:
                continue
    return sample_list

def gender_stats(cur_path,sample_list):
    sex_dict = {}
    for sample in sample_list:
        count_cmd = "grep -v '@' %s/se_v1/%s/map/%s.sam |awk -F '\t' '{print$3}' " \
                    "|sort|uniq -c |tail -n 2 > %s/se_v1/Infos_TMP/sex_stats_final/%s.txt"\
                    %(cur_path,sample,sample,cur_path,sample)
        os.system(count_cmd)
        sex_dict[sample] = []
        X_cmd = "grep 'X' %s/se_v1/Infos_TMP/sex_stats_final/%s.txt |awk -F ' ' '{print$1}' >> .tmp"%(cur_path,sample)
        Y_cmd = "grep 'Y' %s/se_v1/Infos_TMP/sex_stats_final/%s.txt |awk -F ' ' '{print$1}' >> .tmp"%(cur_path,sample)
        subprocess.check_output(X_cmd,shell=True)
        subprocess.check_output(Y_cmd,shell=True)
        with open(cur_path + "/.tmp","r") as in_tmp:
            for num in in_tmp:
                sex_dict[sample].append(int(num.rstrip("\n")))

        rm_tmp = "rm %s/.tmp"%cur_path
        subprocess.check_output(rm_tmp,shell=True)

    with open("{}/se_v1/Infos_TMP/sex_stats_final/{}_sex_stats.csv".format(cur_path,args.batch), "w") as write_file:
        col_header = ["sample_num", "X", "Y", "Ratio", "sex"]
        csv_writer = csv.DictWriter(write_file, fieldnames=col_header)
        csv_writer.writeheader()
        for k,v in sex_dict.items():
            if v[0] / v[1] >= 13:
                gender = "F"
            else:
                gender = "M"
            csv_writer.writerow({"sample_num": k, "X":v[0] , "Y": v[1], "Ratio": v[0] / v[1], "sex": gender})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="\npython count_sex_stats.py [-s sample.list] [-b batch]")
    parser.add_argument("-s", "--sample_list",type=str,help="sample.list")
    parser.add_argument("-b", "--batch",type=str, help="batch")
    args = parser.parse_args()
    cur_path = os.getcwd()
    sample_list = []
    obtain_sample(cur_path,sample_list)
    if os.path.exists("{}/se_v1/Infos_TMP/sex_stats_final".format(cur_path)) == True:
        gender_stats(cur_path,sample_list)
    else:
        mkdir_cmd = "mkdir {}/se_v1/Infos_TMP/sex_stats_final".format(cur_path)
        os.system(mkdir_cmd)
        gender_stats(cur_path,sample_list)
