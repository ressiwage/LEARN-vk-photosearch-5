import requests as r
import asyncio
import aiohttp  # pip install aiohttp aiodns
import shutil
import time
import json
import os
from db import *
from os import listdir
from config import token, interactive
from mark_image import Marker
from os.path import isfile, join
from datetime import datetime as d
from download_urls import download_links
from download_photos import download_all
from distutils.dir_util import copy_tree
from find_image import save as save_vectors
if interactive:
    from pick import pick
else:
    from pick_substitution import pick

U_D_PATH = 'user data/'
T_D_PATH = 'images/'

if __name__ == "__main__":
    title = "Select option (arrows im cmd, J/K in vs code, if doesn't work then you are on cyrillic)"
    options = ["Скачать ссылки на фото", "Скачать фото", "Разметить фото", "Проиндексировать фото", "Поиск по описанию", "Помощь"]
    option, index = pick(options, title, indicator="=>", default_index=0)
    if index == 0:
        asyncio_result = asyncio.run(download_links())
        for i in asyncio_result:
            save_link(i)
    elif index == 1:
        if os.path.exists(T_D_PATH):
            shutil.rmtree(T_D_PATH)
        os.makedirs(T_D_PATH)
        urls = []
        for url in get_links():
            urls.append(url[0])
        asyncio.run(download_all(urls, list(range(len(urls))), T_D_PATH),)
    elif index == 2:
        new_dir = U_D_PATH+input("input name of a directory for saving photos: ").strip() + "/"

        # trunc_descs()
        while os.path.exists(new_dir):
            new_dir = (
                U_D_PATH+input(
                    "this directory exists. \ninput name of a directory for saving photos: "
                ).strip()
                + "/"
            )
        os.makedirs(new_dir)

        marker = Marker()
        onlyfiles = [f for f in listdir(T_D_PATH) if isfile(join(T_D_PATH, f))]
        offset = min(int(input("enter offset (0 default)")), len(onlyfiles))
        descibed_files = [i[1] for i in get_descs()]
        result = []
        copy_tree(T_D_PATH, new_dir)
        start = time.time()
        skip = True
        for ind, fname in enumerate(onlyfiles):
            old_fname = T_D_PATH + fname
            new_fname = new_dir + fname.split("/")[-1]
            if ind < offset or new_fname in descibed_files:
                continue
            try:
                description = marker.process(new_fname)
            except:
                print("error describing ", new_fname)
                description = "ERROR"
            # print(fname, description, ind, sep="|")
            result.append({"desc": description, "fname": new_fname})
            if (ind % 100 == 0 or ind == len(onlyfiles) - 1) and ind != 0:
                save_desc(result)
                result = []
                print(
                    f"{d.now()}:{round(ind* 100/len(onlyfiles), 2) }%...\nestimated time: {int( ((time.time()-start)*len(onlyfiles)/ind - (time.time()-start))/60 ) } min\ntime passed: {round((time.time()-start)/60, 2)}\n"
                )
        print(result)
    elif index == 3:
        save_vectors()
