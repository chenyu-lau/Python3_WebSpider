# -*- coding:utf-8 -*-
"""
Created at 21:27 at Sep 17,2018
@author: Northxw
"""

import os
import requests

from os.path import join as pjoin
from tqdm import tqdm
from colorama import init, Fore

init(autoreset=True)


def save_img(save_dir, hero_num, hero_name, skin_name, cnt):

    save_file_name = pjoin(save_dir, f"{hero_num}-{hero_name}-{skin_name}.jpg")
    skin_url = f"http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{hero_num}/{hero_num}-bigskin-{cnt+1}.jpg"

    if os.path.exists(save_file_name):
        # 跳过已经下载好的图片
        pass
    else:
        
        msg = f"{Fore.GREEN}-- 正在下载：{hero_num}-{hero_name}-{skin_name}.jpg"
        # 修复打印错位
        if cnt == 0:
            print("\n" + msg)
        else:
            print(msg)
        # 获取图片的位数据(二进制流数据)
        response_skin_content = requests.get(skin_url).content
        with open(save_file_name, 'wb') as f:
            f.write(response_skin_content)

def main(path):
    print(f"{Fore.RED} 提示：王者荣耀英雄皮肤图片下载开始！")
    print(f"{Fore.RED} 提示：保存目录：{path} ")

    if not os.path.exists(path):
        os.makedirs(path)

    # 全英雄列表请求链接
    herolist_url = 'https://pvp.qq.com/web201605/js/herolist.json'
    # 获取数据
    response = requests.get(herolist_url).json()

    for i in tqdm(range(len(response)), desc='下载进度', ncols=len(response)):
        # 获取英雄皮肤列表
        skin_names = response[i].get('skin_name')
        if skin_names:
            skin_names = skin_names.split('|')
        else:
            continue

        # 下载当前英雄的所有皮肤
        for cnt in range(len(skin_names)):
            hero_num = response[i]['ename']     # 英雄序号
            hero_name = response[i]['cname']    # 英雄名称
            skin_name = skin_names[cnt]         # 皮肤名称
            save_img(path, hero_num, hero_name, skin_name, cnt)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = pjoin(current_dir, "images")  # 指定下载位置
    main(save_dir)
