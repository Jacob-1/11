# -*- coding: UTF-8 -*-
"""
@version: v1.5
@author: jiangjiepeng
@software: PyCharm
@time: 2020/04/20 20:22
"""
import os
import cv2
from tqdm import tqdm
import time
def pic_video(path,fps):
    for roots,dirs,files in os.walk(path):
        for dir in dirs:
            print('\n', dir, "开始转换...")
            path_video = os.path.join(path,dir)
            filelist = os.listdir(path_video)
            #filelist.sort(key=lambda x: int(x.split('.')[0]))
            filelist.sort(key=lambda x: int(x[:-8]))     #文件名乱序的时候用，例：1、11、12...2、20、21..,防止视频合成乱帧
            pic_path = path_video + '/'+ filelist[0]
            img_pick = cv2.imread(pic_path)
            s,p =img_pick.shape[0:2]
            size = (p,s)  #获取图片尺寸
            file_path =path_video + ".mp4"
            # fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video = cv2.VideoWriter(file_path, fourcc, fps, size)

            pbar = tqdm(filelist)
            pbar.set_description("Processing %s"  % dir)
            for item in pbar:
                if item.endswith('.jpg'):
                    item = path_video + '/' + item
                    img = cv2.imread(item)
                    video.write(img)
                    # pbar.update(len(filelist))
                # if count % 20 == 0:
                #     print("进度:", "%.f" % (count*100 / all_file), '%')
            video.release()
            # pbar.close()
        time.sleep(0.5)
        print( '\n',"完成!")

if __name__ == "__main__":
    fps = 30
    path = r'F:\doing\Pyscript\im_or_videos_transform\total'
    print(f"=star=")
    try :
        pic_video(path,fps)
    except:
        pass
    print(f"=done=")
    #'''ps.文件路径和图片名都不要出现中文，否则视频可能合成错误。'''

