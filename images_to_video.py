# -*- coding: UTF-8 -*-
import os
import cv2
import time

from tqdm import tqdm

def pic_video(path, size):
    for roots,dirs,files in os.walk(path):
        for dir in dirs:
            path_video = os.path.join(path,dir)
            filelist = os.listdir(path_video)
            fps = 30
            file_path =path_video + ".mp4"
            fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
            video = cv2.VideoWriter(file_path, fourcc, fps, size)
            count = 0
            for item in filelist:
                all_file = len(os.listdir(path_video))
                count += 1
                if count % 1 == 0:
                    print("进度:","{}/{}".format(count, all_file))
                if item.endswith('.jpg'):
                    item = path_video + '/' + item
                    img = cv2.imread(item)
                    video.write(img)
            print(dir,"转换完成")
            video.release()

if __name__ == "__main__":
    print(f"===star===")
    try :
        pic_video(r'F://doing//Pyscript//im_or_videos_transform//total/', (3840, 1944))
    except:
        pass
    print(f"===done===")
    #'''ps.文件路径和图片名都不要出现中文，否则视频可能合成错误。'''

