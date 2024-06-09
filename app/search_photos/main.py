import requests as r
import asyncio
import aiohttp 
import shutil
import time
import json
import os
from .db import *
from PIL import Image
from os import listdir
from os.path import isfile, join
from datetime import datetime as d
from ._imports import config
from .mark_image import chosen_marker
from .download_urls import download_links
from .download_photos import download_all
from distutils.dir_util import copy_tree
from .find_image import save as save_vectors, find as find_image
if config.interactive:
    from pick import pick
else:
    from pick_substitution import pick

U_D_PATH = 'app/search_photos/user data/'
T_D_PATH = 'app/search_photos/images/'

if __name__ == "__main__":
    title = "Select option (arrows im cmd, J/K in vs code, if doesn't work then you are on cyrillic)"
    options = ["Скачать ссылки на фото", "Скачать фото", "Разметить фото", "Проиндексировать фото", "Поиск по описанию", "Удалить пользовательские файлы", "Помощь"]
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

        marker = chosen_marker
         
        onlyfiles = [f for f in listdir(T_D_PATH) if isfile(join(T_D_PATH, f))]
        offset = min(int(input("enter offset (0 default)")), len(onlyfiles))
        descibed_files = [i[1] for i in get_descs()]
        result = []
        print("copying photos...")
        copy_tree(T_D_PATH, new_dir)
        print("done")
        start = time.time()
        skip = True
        for ind, fname in enumerate(onlyfiles):
            old_fname = T_D_PATH + fname
            new_fname = new_dir + fname.split("/")[-1]
            if ind < offset or new_fname in descibed_files:
                continue
            try:
                description = marker.process(new_fname)
            except Exception as e:
                print(e)
                print("error describing ", new_fname)
                description = "ERROR"
            # print(fname, description, ind, sep="|")
            result.append({"desc": description, "fname": new_fname})
            if ind>=len(onlyfiles)-1 or (len(onlyfiles) >50 and (ind % (len(onlyfiles) // 50) == 0 or ind == len(onlyfiles) - 1) and ind != 0):
                save_desc(result)
                result = []
                print(
                    f"{d.now()}:\n{round(ind* 100/len(onlyfiles), 2) }%...\nestimated time: {int( ((time.time()-start)*len(onlyfiles)/ind - (time.time()-start))/60 ) } min\ntime passed: {round((time.time()-start)/60, 2)}min\n"
                )
        print(f"time passed: {int(time.time()-start)/60}min")
    elif index == 3:
        save_vectors()
    elif index==4:
        for i in find_image(input('enter your description '), int(input('enter amount of returned photos '))):
            image = Image.open(i[0])
            image.show()
            print('fpath: ', '"'+os.getcwd() + '/' +  i[0]+'"', 'description: ', i[1], sep='\n')
    elif index==5:
        if input('Данная опция удалит ВСЕ пользовательский файлы. для того, чтобы продолжить, введите фразу: "Я хОчУ уДаЛиТь ВсЕ ПоЛьЗоВаТеЛьСкИе ФаЙлЫ" с сохранением регистра')=='Я хОчУ уДаЛиТь ВсЕ ПоЛьЗоВаТеЛьСкИе ФаЙлЫ ':
            for p in [T_D_PATH, 'vectors/', U_D_PATH]:
                if os.path.exists(p):
                    shutil.rmtree(p)
                os.makedirs(p)
            create()
            trunc_descs()
    else:
        pass
