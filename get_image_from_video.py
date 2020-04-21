# -*- coding: UTF-8 -*-
import cv2
import os
import pdb

count = 0
path_in = r'F:\doing\Pyscript\im_or_videos_transform\total'
path = os.walk(path_in)
path_out = r'F:\doing\Pyscript\im_or_videos_transform\total'
crop_height_start_factor = 0.
crop_height_stop_factor = 0.9
sample_frames = 1
#fps = int(vidcap.get(cv2.CAP_PROP_FPS))
for path,dir_list,file_list in path:
    for ind,file in enumerate(file_list):
        success = True
        vidcap = cv2.VideoCapture(os.path.join(path_in,file))
        while success:
            success,image = vidcap.read()
            if not success:
                break
            image_height = image.shape[0]
            image = image[int(crop_height_start_factor*image_height): int(crop_height_stop_factor*image_height),:,:]
            print('read a new frame:',success)
            path_subfolder = os.path.join(path_out,file.split('.')[0])
            if not os.path.exists(path_subfolder):
                os.makedirs(path_subfolder)
            if count%sample_frames == 0:
                os.chdir(path_subfolder)
                #cv2.imwrite('video'+str(ind+160)+'frame' + '_'+ str(count).zfill(4) + '.jpg',image)
                #cv2.imwrite(str(count).zfill(4) + '_' + str(file.split('.')[0]) + '.jpg', image)
                cv2.imwrite(str(count).zfill(4) + '.jpg', image)
                print('successfully written 25th frame')
            count+=1
        print('finished one video')
        #cv2.destroyAllWindows()
        vidcap.release()
        
