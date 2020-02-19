import os
from ffmpy3 import FFmpeg
import shutil

ROOT_PATH = R"/home/chen/workshop/video/2019"

MOV_PATH = R"/home/chen/workshop/video/mov"


def format_conversion(input_video_path, output_video_path):
    ff = FFmpeg(inputs={input_video_path: '-strict -2'}, outputs={output_video_path: "-vcodec libx264 -strict -2"})
    print(ff.cmd)
    ff.run()


def get_file_path(root_path):
    file_path_list = []
    suffix_set = ["mp4"]
    for root, _, files in os.walk(root_path):
        for f in files:
            if f[-3:] in suffix_set:
                continue
            file_path = os.path.join(root, f)
            file_path_list.append(file_path)
    return file_path_list


if __name__ == "__main__":
    src_file_list = get_file_path(ROOT_PATH)
    print((src_file_list))
    for src_file_path in src_file_list:
        dst_file_path = src_file_path[:-3] + "mp4"
        try:
            format_conversion(src_file_path, dst_file_path)
        except:
            pass
        shutil.move(src_file_path, os.path.join(MOV_PATH, os.path.basename(src_file_path)))
