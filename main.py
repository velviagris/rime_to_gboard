# -*- coding: utf-8 -*-
# author: cgcel

import re
import zipfile
from datetime import datetime

import opencc
from tqdm import tqdm

from flypy_utils import pinyin_to_flypy


# 获取 rime userdb.txt 用户词典
def read_file(rime_userdb_path: str):
    userdb_data = []
    with open(rime_userdb_path, encoding="utf-8") as f:
        for line in tqdm(f, total=sum(1 for _ in open(rime_userdb_path, "r", encoding="utf-8")), desc="读取 userdb.txt 文件"):
            userdb_data.append(line)
    return userdb_data

# 判断输入方案
def get_scheme(userdb_data: list):
    scheme_type = ""
    if "pinyin" in userdb_data[1]:
        scheme_type = "pinyin"
    elif "flypy" in userdb_data[1]:
        scheme_type = "flypy"
    return scheme_type

# 通过 opencc 繁体转简体
def trans_to_simp(input_data: list):
    output_data = []
    converter = opencc.OpenCC('t2s.json')
    for item in tqdm(input_data, desc="opencc 繁体转简体"):
        output_data.append(converter.convert(item))
    return output_data

# 通过 opencc 简体转繁体
def simp_to_trans(input_data: list):
    output_data = []
    converter = opencc.OpenCC('s2t.json')
    for item in tqdm(input_data, desc="opencc 简体转繁体"):
        output_data.append(converter.convert(item))
    return output_data


# 通过正则匹配自定义短语
def find_words(scheme_type: str, input_data: list):
    result = []

    if scheme_type == "pinyin":
        pattern = re.compile(r'(.*?)\t(.*?)\t')
        for line in tqdm(input_data, desc="正则匹配短语"):
            res = pattern.findall(line)
            result.append(res)
    elif scheme_type == "flypy":
        pattern = re.compile(r'(.*?)\t(.*?)\t')
        for line in tqdm(input_data, desc="正则匹配短语"):
            res = pattern.findall(line)
            new_res = ()
            if len(res) == 1:
                res_list = list(res)
                new_key = res_list[0][0].replace('\x7fenc\x1f', '')
                new_res = [(new_key, res_list[0][1])]
            else:
                new_res = res
            result.append(new_res)
    
    return result


# 新建列表存储短语
def generate_gboard_format_data(output_scheme_type: str, words_list: list):
    new_words_list = []
    for word in tqdm(words_list, desc="创建转换格式短语列表"):
        if word != []:
            if output_scheme_type == "1":
                new_word = '{}\t{}\tzh-CN\n'.format(pinyin_to_flypy(word[0][0]), word[0][1])
            else:
                new_word = '{}\t{}\tzh-CN\n'.format(word[0][0], word[0][1])
            new_words_list.append(new_word)
    return new_words_list


# 生成 gboard 格式词典
def generate_gboardDic(words_list: list):
    with open("dictionary.txt", "w+", encoding="utf-8") as f:  # 覆盖写入
        f.write("# Gboard Dictionary version:1\n")
        for word in tqdm(words_list, desc="写入 dictionary.txt"):
            f.write(word)

    zf = zipfile.ZipFile("PersonalDictionary-{}.zip".format(datetime.now().strftime("%Y%m%d%H%M%S")),
                         mode="w",
                         compression=zipfile.ZIP_DEFLATED)
    zf.write("dictionary.txt")
    zf.close()


def main():
    rime_userdb_path = input("输入 rime_userdb_path: ")

    # 获取 rime userdb.txt 用户词典
    userdb_data = read_file(rime_userdb_path)

    # 判断输入方案
    scheme_type = get_scheme(userdb_data=userdb_data)
    if scheme_type != "":
        scheme_result = input("识别为 {} 词库, 输入 0 -- 正确, 1 -- 错误 以继续: ".format(scheme_type))
    if scheme_type == "" or scheme_result == 1:
        input_scheme_type = input("输入 Rime userdb.txt 方案类型 (0 -- pinyin, 1 -- flypy): ")
        if input_scheme_type == '0':
            scheme_type = "pinyin"
        elif input_scheme_type == '1':
            scheme_type = "flypy"


    while True:
        input_format = ["0", "1"]
        userdb_type = input("输入 Rime userdb.txt 简繁类型 (0 -- 简体, 1 -- 繁体): ")
        if userdb_type not in input_format:
            userdb_type = print("参数格式错误, 重新输入")
            continue
        gboard_type = input("输入 GboardDictionary.zip 简繁类型 (0 -- 简体, 1 -- 繁体): ")
        output_scheme_type = input("输入 Gboard 词库方案类型 (0 -- pinyin, 1 -- flypy): ")
        
        if gboard_type not in input_format:
            gboard_type = print("参数格式错误, 重新输入")
            continue
        else:
            break

    # 将简体字的 userdb.txt 内容转成繁体字
    if (userdb_type == "0" and gboard_type == "1"):
        userdb_data = simp_to_trans(userdb_data)

    # 将繁体字的 userdb.txt 内容转成简体字
    if (userdb_type == "1" and gboard_type == "0"):
        userdb_data = trans_to_simp(userdb_data)

    # 匹配自定义短语
    words_list = find_words(scheme_type, userdb_data)

    # 新建列表存储短语
    new_words_list = generate_gboard_format_data(output_scheme_type, words_list)

    # 生成 gboard 个人词典
    generate_gboardDic(words_list=new_words_list)

    input("转换完成, 回车退出.")

if __name__ == '__main__':
    main()
