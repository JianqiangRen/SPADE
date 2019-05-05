# coding=utf-8
# summary: 语义图数据增广，对某些区域进行语义变换
# author: rjq
# date:

import os
import glob
import cv2
import numpy as np
import errno
import shutil


input_labels_path = "datasets/xl_landscope/val_label"
output_labels_path = "datasets/xl_landscope/new_val_label"


def create_dir(path):
    """
    Creates a directory
    :param path: string
    :return: nothing
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

def empty_dir(path):
    """
    Delete all files and folders in a directory
    :param path: string, path to directory
    :return: nothing
    """
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Warning: {}'.format(e))
            

def prepare_dir(path, empty=False):
    """
    Creates a directory if it soes not exist
    :param path: string, path to desired directory
    :param empty: boolean, delete all directory content if it exists
    :return: nothing
    """
    if not os.path.exists(path):
        create_dir(path)

    if empty:
        empty_dir(path)


def intersection(list_a, list_b):
    intersect = []
    for i, a in enumerate(list_a):
        for j, b in enumerate(list_b):
            if a == b:
                intersect.append(a)
    return intersect


exchangeable_labels =  {"sea": ["grass", "floor-wood", "snow", "water-other"],
                        "grass": ["snow", "hill", "sea", "water-other"],
                        "clouds": ["sky-other"],
                        "snow": ["grass", "water-other"],
                        "sand": ["snow", "grass"],
                        "floor-wood": ["grass", "sea", "water-other", "snow"],
                        "hill": ["mountain", "tree"],
                        "water-other":["grass", "snow"],
                        "mountain": ["hill", "clouds","sky-other","sky"]
                        }

if __name__ == "__main__":
    label2semantic = {}
    semantic2label = {}
    with open('data_augmentation/cocostuff_labels.txt', 'r') as f:
        for line in f:
            labelsemantic = line.split()
            # print(labelsemantic)
            label2semantic[int(labelsemantic[0].strip())] = labelsemantic[1].strip()
            semantic2label[labelsemantic[1].strip()] = int(labelsemantic[0].strip())

    labels = glob.glob(os.path.join(input_labels_path, "*.png"))
    
    prepare_dir(output_labels_path, True)
    
    for label_map_dir in labels:
        label_map = cv2.imread(label_map_dir, -1)
        cur_labels_id = np.unique(label_map)
        
        for ex_labels in exchangeable_labels.keys():
            if semantic2label[ex_labels] in cur_labels_id:
                for l in exchangeable_labels[ex_labels]:
                        new_label_map = label_map.copy()
                        new_label_map[label_map == semantic2label[ex_labels]] = semantic2label[l]
                        new_name = output_labels_path + "/" + label_map_dir.split('/')[-1].split('.')[0] +"_{}_{}.png".format(ex_labels, l)
                        cv2.imwrite(new_name, new_label_map)
        

