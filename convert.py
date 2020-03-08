# encoding: utf-8
import os
import cv2
import argparse
import threading
import imageio


# 多线程视频分解类
class VideoSplitThread(threading.Thread):
    # 构造函数
    def __init__(self, src_dir, dst_dir, file_names):
        super(VideoSplitThread, self).__init__()
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.file_names = file_names

    # 处理单个视频
    def process(self, file_name):
        file_path = os.path.join(self.src_dir, file_name)
        video = imageio.get_reader(file_path)
        fps = video.get_meta_data()['fps']
        # 检查个时
        ext = file_name[file_name.rfind(".") + 1:]
        if ext != "mp4" and ext != "MP4" and ext != "avi" and ext != "AVI":
            print("The video ext %s is not supported!" % ext)
            return
        root = os.path.join(self.dst_dir, file_name[:file_name.rfind(".")])
        if not os.path.exists(root):
            os.makedirs(root)
        for i, frame in enumerate(video):
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite(os.path.join(root, "%d.jpg" % i), frame)
            print("Save [%s] fame %d......" % (file_name, i))
        print("Video %s is done!" % file_name)

    # 批次处理视频
    def run(self):
        if not os.path.exists(self.dst_dir):
            os.makedirs(self.dst_dir)
        for file_name in self.file_names:
            if file_name[file_name.rfind("."):] != ".mp4":
                continue
            self.process(file_name)


# 多线程视频合并类
class VideoMergeThread(threading.Thread):
    # 构造函数
    def __init__(self, src_dir, dst_dir, subdir_names):
        super(VideoMergeThread, self).__init__()
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.subdir_names = subdir_names

    # 处理单个视频
    def process(self, subdir_name):
        video_name = subdir_name + ".mp4"
        dst_path = os.path.join(self.dst_dir, video_name)
        fps = 30
        video = imageio.get_writer(dst_path, fps=fps)
        subdir = os.path.join(self.src_dir, subdir_name)
        image_names = os.listdir(subdir)
        for i in range(len(image_names)):
            frame = cv2.imread(os.path.join(subdir, "%d.jpg" % i))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video.append_data(frame)
            print("Save [%s] fame %03d......" % (video_name, i))
        print("Video %s is done!" % video_name)

    # 批次处理视频
    def run(self):
        if not os.path.exists(self.dst_dir):
            os.makedirs(self.dst_dir)
        for subdir_name in self.subdir_names:
            if not os.path.isdir(os.path.join(self.src_dir, subdir_name)):
                continue
            self.process(subdir_name)


# 转化
def convert(src_dir, dst_dir, mode, thread_num):
    # 检查参数
    if mode != "video2frames" and mode != "frames2video":
        raise ValueError("Incorrect converting mode!")
    file_names = os.listdir(src_dir)
    if thread_num > len(file_names):
        thread_num = len(file_names)
    # 创建多线程
    threads = list([])
    per_num = len(file_names) / float(thread_num)
    for i in range(thread_num):
        start = int(round(i * per_num))
        end = int(round((i + 1) * per_num))
        # 根据模式创建不同的多线程
        if mode == "video2frames":
            threads.append(VideoSplitThread(src_dir, dst_dir, file_names[start: end]))
        elif mode == "frames2video":
            threads.append(VideoMergeThread(src_dir, dst_dir, file_names[start: end]))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Tasks are all done!")


# 程序入口
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_dir', required=True)
    parser.add_argument('--dst_dir', required=True)
    parser.add_argument('--mode', choices=["video2frames", "frames2video"], required=True)
    FLAGS = parser.parse_args()
    convert(FLAGS.src_dir, FLAGS.dst_dir, FLAGS.mode, 4)
