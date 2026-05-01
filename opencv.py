import cv2
import numpy as np
import sys

# 颜色配置
COLORS = {
    'r': {
        'name': 'Red',
        'ranges': [
            (np.array([0, 80, 80]), np.array([10, 255, 255])),
            (np.array([160, 80, 80]), np.array([180, 255, 255]))
        ],
        'bgr': (0, 0, 255)
    },
    'g': {
        'name': 'Green',
        'ranges': [
            (np.array([35, 80, 80]), np.array([85, 255, 255]))
        ],
        'bgr': (0, 255, 0)
    },
    'b': {
        'name': 'Blue',
        'ranges': [
            (np.array([85, 100, 100]), np.array([115, 255, 255]))
        ],
        'bgr': (255, 0, 0)
    },
    'y': {
        'name': 'Yellow',
        'ranges': [
            (np.array([20, 150, 150]), np.array([35, 255, 255]))
        ],
        'bgr': (0, 255, 255)
    },
}

def detect_color(image, color_key):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    config = COLORS[color_key]

    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for lower, upper in config['ranges']:
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))

    kernel = np.ones((15, 15), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = image.copy()

    if contours:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 500:
            x, y, w, h = cv2.boundingRect(largest)
            color = config['bgr']
            cv2.rectangle(result, (x, y), (x+w, y+h), color, 3)
            label = f"{config['name']}  Area: {int(cv2.contourArea(largest))}px"
            cv2.putText(result, label, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.putText(result, f"Mode: {config['name']}  [R/G/B/Y]  Q: quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 2)

    return result, mask

import tkinter as tk
from tkinter import filedialog

# 弹出文件选择窗口
root = tk.Tk()
root.withdraw()  # 隐藏主窗口
img_path = filedialog.askopenfilename(
    title='选择图片',
    filetypes=[('图片文件', '*.jpg *.jpeg *.png *.bmp')]
)

if not img_path:
    print('未选择图片')
    sys.exit()

image = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)

if image is None:
    print(f'无法读取图片：{img_path}')
    sys.exit()

print(f'已加载图片：{img_path}')
print('按 R/G/B/Y 切换检测颜色，按 Q 退出')

current_color = 'r'

while True:
    result, mask = detect_color(image, current_color)
    cv2.imshow('Color Detector', result)
    cv2.imshow('Mask', mask)

    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        current_color = 'r'
    elif key == ord('g'):
        current_color = 'g'
    elif key == ord('b'):
        current_color = 'b'
    elif key == ord('y'):
        current_color = 'y'

cv2.destroyAllWindows()