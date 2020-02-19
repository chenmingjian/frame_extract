import os
import numpy as np
import json
import cv2
import random
import math
import uuid


def err(info):
    print("\033[1;31m%s\033[0m" % info)


def get_all_file_path(root_path):
    all_file_path = list()
    for root, dirs, files in os.walk(root_path):
        for f in files:
            file_path = os.path.join(root, f)
            all_file_path.append(file_path)

    return all_file_path


def get_names_from_path_list(path_list):
    file_name_list = list()
    for path in path_list:
        file_name_without_suffix = os.path.basename(path).split(".")[0]
        file_name_list.append(file_name_without_suffix)
    return file_name_list


def make_name_to_path_map(name_list, file_path_list):
    name_to_path_map = dict()
    for name in name_list:
        name_to_path_map[name] = ""

    for path in file_path_list:
        file_name_in_file_path = os.path.basename(path).split(".")[0]
        if file_name_in_file_path in name_to_path_map.keys():
            name_to_path_map[file_name_in_file_path] = path

    return name_to_path_map


def parse_txt(txt_path):
    txt_np = np.loadtxt(txt_path)
    positions = txt_np[:, 0]
    actions = txt_np[:, 1]

    section_dict = dict()
    for i in range(8):
        section_dict[str(i + 1)] = list()

    for i in range(len(positions) - 1):
        if i < len(positions) - 2 and actions[i + 1] == actions[i + 2]:
            continue
        section = [positions[i], positions[i + 1]]
        action = actions[i + 1]

        section_dict[str(int(action))].append(section)

    for i in range(8):
        section_dict[str(i + 1)] = np.array(section_dict[str(i + 1)])

    return section_dict


def get_video_info(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    return total_frame_num


def get_overall_frame_numbers(section_np, count):
    section_total_frame_number = np.sum(section_np[:, 1] - section_np[:, 0])
    frame_number_list = list()
    for _ in range(count):
        random_n = random.randint(0, section_total_frame_number)
        for section in section_np:
            begin = section[0]
            end = section[1]

            random_n += begin
            if end > random_n:
                frame_number_list.append(random_n)
                break
            else:
                random_n -= end
    return frame_number_list


def get_segmentation_frame_numbers(section_np, proportion_list, count_list):
    assert len(proportion_list) == len(count_list)

    frame_number_list = list()
    for i in range(len(proportion_list)):
        frame_number_list.append(list())

    for b, section in enumerate(section_np):
        if b == 2:
            break
        section_frame = section[1] - section[0]

        segment_list = list()

        begin = section[0]
        for p in proportion_list:
            end = begin + math.floor(section_frame * p)

            segment_list.append([begin, end])
            begin = end

        for i, segment in enumerate(segment_list):
            for c in range(count_list[i]):
                random_n = random.randint(segment[0], segment[1])
                frame_number_list[i].append(random_n)

    return frame_number_list


def save_img_with_a_random_name(img, k, name):
    uuid_str = uuid.uuid4().hex
    save_path = os.path.join("output_img", k)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_path = os.path.join(save_path, name + "_" + k + "_" + uuid_str + ".jpg")
    cv2.imwrite(save_path, img)


def get_frame_from_video(section_dict, video_path):
    action_num_word_map = ["", '整理着装_整齐报数', '立正-稍息-跨立', '停止间转法', '齐步', '正步', '跑步']

    def parse_json():
        json_dict = json.load(open("config.json", "r"))
        return json_dict

    def get_from_cap(cap, n):
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        _, img = cap.read()
        return img

    config = parse_json()

    name = os.path.basename(video_path)

    if len(name) < 12:
        print(name, "!!!")
        return
    if name[11] == 'Z':
        config = config["正面"]
    elif name[11] == 'C':
        config = config["侧面"]
    else:
        print(video_path[10:12], "???")
        return
    global count__
    count__ += 1
    for k in section_dict.keys():
        if section_dict[k].size == 0 or int(k) > len(action_num_word_map) - 1:
            continue
        config_local = config[action_num_word_map[int(k)]]

        if config_local["图片获取方式"] == "随机":
            count = config_local["图片获取数量"]
            frame_list = get_overall_frame_numbers(section_dict[k], count)
        elif config_local["图片获取方式"] == "分段":
            count_list = config_local["图片获取数量"]
            proportion_list = config_local["分段比例"]
            frame_list = get_segmentation_frame_numbers(section_dict[k], proportion_list, count_list)
        else:
            print("json error")
            return

        cap = cv2.VideoCapture(video_path)

        for f in frame_list:
            if type(f) is list:
                for i in f:
                    img = (get_from_cap(cap, i))
                    save_img_with_a_random_name(img, k, name.split(".")[0])
            else:
                img = get_from_cap(cap, f)
                save_img_with_a_random_name(img, k, name.split(".")[0])


if __name__ == "__main__":
    # txt_root_path = R"output_txt"
    txt_root_path = "/home/chen/tmp/video_label"
    video_root_path = R"/home/chen/workshop/video/2019"

    txt_path_list = get_all_file_path(txt_root_path)
    video_path_list = get_all_file_path(video_root_path)

    all_name_list = get_names_from_path_list(txt_path_list)

    txt_map = make_name_to_path_map(all_name_list, txt_path_list)
    video_map = make_name_to_path_map(all_name_list, video_path_list)
    count__ = 0
    for name in all_name_list:
        txt_path = txt_map[name]
        video_path = video_map[name]

        print(name)
        print(txt_path)
        print(video_path)

        section_dict = parse_txt(txt_path)
        frame_num = get_video_info(video_path)

        for i in range(8):
            section_dict[str(i + 1)] = (section_dict[str(i + 1)] * frame_num).astype(int)

        get_frame_from_video(section_dict, video_path)
        print(count__)
