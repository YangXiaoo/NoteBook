# coding:utf-8
# 2019-1-12
# data factory

import os
import cv2
import numpy as np 


__suffix__ = ["tif", "png"]

__all__ = [
    'create_train_data',
    'load_train_data',
    'create_test_data',
    'load_test_data',
    'mkdir',
]


def mkdir(file_list):
    if isinstance(file_list, list):
        for f in file_list:
            if not os.path.isdir(f):
                os.makedirs(f)
    else:
        if not os.path.isdir(file_list):
            os.makedirs(file_list)
    return None


def get_files(dirpath):
    file = []
    for root, dirs, files in os.walk(dirpath, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            if name.split(".")[-1] in __suffix__:
                file.append(path)
    return file


def normalization(img, img_size=(256, 256)):
    """
    归一化
    """
    # print(img.shape)
    h, w = np.shape(img)[0], np.shape(img)[1]
    if w > h:
        gap = w - h
        fill = np.zeros([1, w], np.uint8)
        for i in range(gap//2):
            img = np.concatenate((img,fill), axis = 0)
        for i in range(gap//2):
            img = np.concatenate((fill, img), axis = 0)
    elif w < h:
        gap = h - w
        fill = np.zeros([h, 1], np.uint8)
        for i in range(gap//2):
            img = np.concatenate((img,fill), axis = 1)
        for i in range(gap//2):
            img = np.concatenate((fill, img), axis = 1)
    else:
        pass

    img_new = cv2.resize(img, img_size, interpolation=cv2.INTER_LINEAR)

    return img_new


def _get_pic_map(pic_files):
    """
    pic_files: [pic_path, ]
    
    return: {pic_id : [file_path,]}
    """
    file_dict = {} 
    for f in pic_files:
        pic_basename = os.path.basename(f)
        file_dict[pic_basename] =  f

    return file_dict


def create_train_data(train_path, 
                    labels_path, 
                    output_train_data,
                    output_labels_data,
                    height, 
                    width):
    """
    创建测试集数据
    """
    print("creating train datasets.")
    train_files = sorted(get_files(train_path))
    labels_files = sorted(get_files(labels_path))

    len_train = len(train_files)
    len_labels = len(labels_files)
    assert len_train == len_labels, "训练集与标签数量不一致"

    label_dict = _get_pic_map(labels_files)
    # print(len(train_files), train_files[0])
    # assert 0 == 1


    img_data = np.ndarray((len_train, height, width, 1), dtype=np.uint8)
    img_labels = np.ndarray((len_labels, height, width, 1), dtype=np.uint8)

    for i in range(len(train_files)):
        # print(i)
        train_basename = os.path.basename(train_files[i])
        # label_basename = os.path.basename(labels_files[i])
        # assert train_basename == label_basename, '训练图片与标签不一致'

        if train_basename not in label_dict:
            continue

        label_pic = label_dict[train_basename]

        img_train = cv2.imread(train_files[i], 0)
        img_label = cv2.imread(label_pic, 0)

        img_train = normalization(img_train, (height, width))
        img_label = normalization(img_label, (height, width))

        img = np.array(img_train)
        # print(img[:,:])
        label = np.array(img_label)

        img_data[i] = np.reshape(img ,(height, width, 1))
        img_labels[i] = np.reshape(label ,(height, width, 1))

        if not i % 10:
            print("processed: %s" % i)

    np.save(output_train_data, img_data)
    np.save(output_labels_data, img_labels)

    print('Finish!')

    return None


def load_train_data(train_data_path, labels_data_path):
    """
    加载训练集数据
    """
    imgs_train = np.load(train_data_path)
    imgs_mask_train = np.load(labels_data_path)
    imgs_train = imgs_train.astype('float32')
    imgs_mask_train = imgs_mask_train.astype('float32')
    imgs_train /= 255
    mean = imgs_train.mean(axis = 0)
    imgs_train -= mean
    imgs_mask_train /= 255
    # 分割对象为1， 背景为0
    imgs_mask_train[imgs_mask_train > 0.5] = 1
    imgs_mask_train[imgs_mask_train <= 0.5] = 0

    print("Data loaded successfully.")

    return imgs_train, imgs_mask_train


def create_test_data(data_path, output_path, height, width):
    """
    创建测试集
    """
    files = get_files(data_path)
    img_data = np.ndarray((len(files), height, width, 1), dtype=np.uint8)

    for i in range(len(files)):
        img_test = cv2.imread(files[i], 0)
        img_test = normalization(img_test, (height, width))
        img = np.array(img_test)
        img_data[i] = np.reshape(img ,(height, width, 1))

        if not i % 10:
            print("processed: %s" % i)

    np.save(output_path, img_data)
    print("Test data created successfully.")


def load_test_data(data_path):
    """
    加载测试数据
    """
    imgs_test = np.load(data_path)
    imgs_test = imgs_test.astype('float32')
    imgs_test /= 255
    mean = imgs_test.mean(axis = 0)
    imgs_test -= mean

    print("Data loaded successfully.")

    return imgs_test


if __name__ == '__main__':
    train_path = r'C:\Study\github\others\Unet-master\Unet-master\images\train\images'
    labels_path = r'C:\Study\github\others\Unet-master\Unet-master\images\train\label'
    output_train_data = r'C:\Study\github\others\Unet-master\Unet-master\imgs_train.npy'
    output_labels_data = r'C:\Study\github\others\Unet-master\Unet-master\imgs_mask_train.npy'

    test_data_path = r'C:\Study\github\others\Unet-master\Unet-master\images\test'
    test_output_path = r'C:\Study\github\others\Unet-master\Unet-master\imgs_test.npy'

    height = 512
    width = 512

    mkdir([os.path.split(output_train_data)[0], 
            os.path.split(output_labels_data)[0], 
            os.path.split(test_output_path)[0]])

    create_train_data(train_path, 
                    labels_path, 
                    output_train_data,
                    output_labels_data,
                    height, 
                    width)

    # ret_train, ret_labels = load_train_data(output_train_data, output_labels_data)

    create_test_data(test_data_path, test_output_path, height, width)

    # ret_test = load_test_data(test_output_path)
