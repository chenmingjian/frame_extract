import os
import numpy as np
import json

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
    print(txt_np)
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

    return section_dict


def parse_json():
    action_num_word_map = ["", '整理着装_整齐报数', '立正-稍息-跨立', '停止间转法', '齐步', '正步', '跑步']
    json_dict = json.load(open("config.json", "r"))
    return json_dict

if __name__ == "__main__":

    # txt_root_path = R""
    # video_root_path = R""
    #
    # txt_path_list = get_all_file_path(txt_root_path)
    # video_path_list = get_all_file_path(video_root_path)
    #
    # all_name_list = get_names_from_path_list(txt_path_list)
    #
    # txt_map = make_name_to_path_map(all_name_list, txt_path_list)
    # video_map = make_name_to_path_map(all_name_list, video_path_list)

    # tmp = parse_txt("output_txt/52001301F2QC1S.txt")
    # for i in tmp.keys():
    #     print(tmp[i])
