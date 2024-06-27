import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


# 导入原始图像
def read_img(path):
    img = cv2.imread(path)
    # 获取图像基本信息
    height, width, channel = img.shape
    return img, height, width


# 图像切割
def cut_img(img, height, width, matrix):
    # 切割图像
    img_list = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix[0]))]
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            # 纵向切割
            img_list[j][i] = img[i * height // len(matrix[0]): (i + 1) * height // len(matrix[0]),
                             j * width // len(matrix[0]): (j + 1) * width // len(matrix[0])]
    return img_list


# 图像重组
def re_img(img_list, height, width, matrix):
    new_img_list = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix[0]))]
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            k, l = matrix[i][j].split(',')
            new_img_list[i][j] = img_list[int(k)][int(l)]
    # 图像拼接
    img = np.zeros((height, width, 3), np.uint8)
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            img[i * height // len(matrix[0]): (i + 1) * height // len(matrix[0]),
            j * width // len(matrix[0]): (j + 1) * width // len(matrix[0])] = new_img_list[i][j]
    return img


# 图像展示
def show_img_list(img_list):
    n = len(img_list)
    for i in range(n):
        for j in range(n):
            plt.subplot(n, n, i * n + j + 1)
            plt.imshow(img_list[i][j])
            plt.axis('off')
    plt.show()


def show_img(img):
    plt.imshow(img)
    plt.axis('off')
    plt.show()


# 保存图像
def save_img(img, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    cv2.imwrite(path, img)


# 删除缓存图像
def delete_img():
    for file in os.listdir('temp/'):
        os.remove(f'temp/{file}')
    # print('删除缓存图片成功')


def run(img_path, frames):
    iamge, height, width = read_img(img_path)
    img_list = cut_img(iamge, height, width, frames[0]['matrix'])
    for i in range(len(frames)):
        matrix = frames[i]['matrix']
        temp_img = re_img(img_list, height, width, matrix)
        save_img(temp_img, f'temp/{i}.png')
