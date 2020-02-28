# -*- coding: utf-8 -*-

import os,sys
import json
import os
import traceback
import os.path
from PIL import Image

def json_to_dict(json_filename):
    json_file = open(json_filename, 'r')
    all_pic_dic = json.load(json_file)
    all_item_list = []
    for one_pic_item in all_pic_dic['frames']:
        one_json_item = all_pic_dic['frames'][one_pic_item]
        one_item = {}
        one_name = one_pic_item.strip().lstrip().rstrip(',')
        if one_name.find('/')>=0:
            o_dir =''
            d_list =one_name.split('/')
            for each in d_list:
                if each.find('.')>=0:
                    one_item['name'] = each
                else:
                    o_dir =o_dir+'/'+each
            one_item['dir'] = o_dir
        else:
            one_item['name'] = one_pic_item.strip().lstrip().rstrip(',')
            one_item['dir'] = ''
        one_item['x'] = one_json_item['frame']['x']
        one_item['y'] = one_json_item['frame']['y']
        one_item['w'] = one_json_item['frame']['w']
        one_item['h'] = one_json_item['frame']['h']
        all_item_list.append(one_item)

    return all_item_list
       
   

def gen_png_from_json(folder_name, json_filename, png_filename):
    big_image = Image.open(png_filename)
    all_item_list = json_to_dict(json_filename)

    print 'gen_png_from_json:' + folder_name

    #清理掉原目录
    if not os.path.isdir(folder_name):
        #os.removedirs(folder_name)
        os.mkdir(folder_name)

    for i, one_item_data in enumerate(all_item_list):
        file_name = one_item_data['name']
        dir_name = one_item_data['dir']
        x = one_item_data['x']
        y = one_item_data['y']
        w = one_item_data['w']
        h = one_item_data['h']

        #设置图像裁剪区域 (x左上，y左上，x右下,y右下)
        image_box = [x, y, x + w , y + h ]
        one_pic = big_image.crop(image_box)
        if one_item_data['dir'] == '':
            one_pic.save(folder_name + "/" + file_name) # 存储裁剪得到的图像
        else:
            d_list = dir_name.split('/')
            o_dir = '/'
            for each in d_list:
                if each=='':
                    o_dir =o_dir+''
                else:
                    o_dir =o_dir+'/'+ each
                    p = folder_name + o_dir
                    if not os.path.isdir(p):
                        os.mkdir(p)

            one_pic.save(p + "/" + file_name) # 存储裁剪得到的图像
        
        
        #print one_item_data

if __name__ == '__main__':

    rootdir = sys.argv[1]
    #'E:/_github/Python/TexturePacker'

    file_name_set = set()
    if os.path.exists(rootdir):
        list_file = os.listdir(rootdir)
        for i in range(0,len(list_file)):
            one_file_name = list_file[i]
            path = os.path.join(rootdir, one_file_name)
            if os.path.isfile(path):
                file_name_set.add(os.path.splitext(one_file_name)[0])

    for file_name in file_name_set:
        json_filename = os.path.join(rootdir, file_name) + '.atlas'
        png_filename = os.path.join(rootdir, file_name) + '.png'
        jpg_filename = os.path.join(rootdir, file_name) + '.jpg'
    
        if os.path.exists(json_filename):
            if os.path.exists(png_filename):
                try:
                    gen_png_from_json(os.path.join(rootdir, file_name), json_filename, png_filename )
                except Exception:
                    print '!!!!!!!!!!!!!!!!!!!!' + json_filename + ' json error !!!!!!!!!!!!!!!!!!!!!'
                    print(traceback.format_exc())
            elif os.path.exists(jpg_filename):
                try:
                    gen_png_from_json(os.path.join(rootdir, file_name), json_filename, jpg_filename )
                except Exception:
                    print '!!!!!!!!!!!!!!!!!!!!' + json_filename + ' json error !!!!!!!!!!!!!!!!!!!!!'
                

   
