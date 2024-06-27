import ddddocr
import os
from PIL import Image
import numpy as np
import os
import cv2

"""
by lingdanqing

https://github.com/lingdanqing
"""
# 去除白边的函数
def remove_white_borders(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    thresh = cv2.bitwise_not(thresh)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cropped_image = image[y:y + h, x:x + w]
        return cropped_image
    return image


# 分割图片
def split_image(image, rows, cols, save_path, image_name):
    height, width, _ = image.shape
    tile_height = height // rows
    tile_width = width // cols
    tiles = []
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for row in range(rows):
        for col in range(cols):
            tile = image[row * tile_height:(row + 1) * tile_height, col * tile_width:(col + 1) * tile_width]
            tile = remove_white_borders(tile)  # 去除白边
            tile = cv2.resize(tile, (tile_width, tile_height))
            tiles.append(tile)

            # 保存切割图
            # tile_image = Image.fromarray(tile)
            # tile_image.save(os.path.join(save_path, f"{image_name}_tile_{row}_{col}.png"))
    return tiles


# 计算相邻块边缘差异
def calculate_edge_difference(tiles, rows, cols):
    total_diff = 0
    for row in range(rows):
        for col in range(cols - 1):
            right_edge = tiles[row * cols + col][:, -1, :]
            left_edge = tiles[row * cols + col + 1][:, 0, :]
            total_diff += np.sum((right_edge - left_edge) ** 2)
    for col in range(cols):
        for row in range(rows - 1):
            bottom_edge = tiles[row * cols + col][-1, :, :]
            top_edge = tiles[(row + 1) * cols + col][0, :, :]
            total_diff += np.sum((bottom_edge - top_edge) ** 2)
    return total_diff


def process_images_in_folder2(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    edge_diffs = []
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)

        image_np = np.array(image)
        tiles = split_image(image_np, 4, 4, 'out', image_file.split('.')[0])
        edge_diff = calculate_edge_difference(tiles, 4, 4)
        edge_diffs.append((image_file, edge_diff))

    # 找出边缘差异最小的图片
    edge_diffs.sort(key=lambda x: x[1])
    return edge_diffs[0][0].split(".")[0]


def process_images_in_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    edge_diffs = []
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)

        image_np = np.array(image)
        tiles = split_image(image_np, 4, 4, 'out', image_file.split('.')[0])
        edge_diff = calculate_edge_difference(tiles, 4, 4)
        edge_diffs.append((image_file, edge_diff))

    # 找出边缘差异最小的图片
    edge_diffs.sort(key=lambda x: x[1])
    return edge_diffs[0][0].split(".")[0]


def run():
    folder_path = './temp'
    correct_image = process_images_in_folder(folder_path)
    return correct_image

    # ocr = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False, import_onnx_path="models/pikpak4.0.onnx",
    #                       charsets_path="models/charsets.json")
    #
    # ima_path = 'temp/'
    # for file in os.listdir(ima_path):
    #     with open(f"{ima_path}/{file}", 'rb') as f:
    #         image_bytes = f.read()
    #         if ocr.classification(image_bytes) == 'correct':
    #             # print(f'{file.split(".")[0]}')
    #             return file.split(".")[0]
    #     return 1


if __name__ == '__main__':
    run()
