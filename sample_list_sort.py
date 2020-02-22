#_*_coding:UTF-8_*_

import argparse
import os
import re


def sort_ntc(cur_path):
    with open(cur_path + "/" + args.sample_list, "r") as in_list:
        with open(cur_path + "/sample_sort_1.list", "w") as out_list_1:
            with open(cur_path + "/sample_sort_2.list", "w") as out_list_2:

                for line in in_list:
                    line = line.strip().split("\t")
                    if re.findall("^NTC",line[1]) or re.findall("[A-C].$",line[1]):
                        out_list_1.write(line[0] + "\t" + line[1] + "\t" + line[2] + "\n")
                    else:
                        out_list_2.write(line[0] + "\t" + line[1] + "\t" + line[2] + "\n")

    merge_cmd = "cat sample_sort_?.list > sample_sort.list"
    rm_cmd = "rm sample_sort_?.list"
    rename_cmd = "mv sample_sort.list sample.list"
    os.system(merge_cmd)
    os.system(rm_cmd)
    os.system(rename_cmd)

    in_list.close()
    out_list_1.close()
    out_list_2.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage= "\npython sample_list_sort.py [-s sample.list]")
    parser.add_argument("-s","--sample_list",type=str,help="sample.list")
    args = parser.parse_args()
    cur_path = os.getcwd()
    sort_ntc(cur_path)


