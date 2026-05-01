# robot-vision-demo
# robot-vision-demo

基于 OpenCV 的实时颜色目标检测系统，支持对任意图片进行红、绿、蓝、黄四色识别与目标框定，可应用于机器人视觉引导、工业分拣等场景。

---

## 效果展示

| 红色识别 | 蓝色识别 |
|----------|----------|
| ![red](demo/red.png) | ![blue](demo/blue.png) |

| 绿色识别 | 黄色识别 |
|----------|----------|
| ![green](demo/green.png) | ![yellow](demo/yellow.png) |

---

## 功能特性

- 支持选择任意本地图片进行检测（弹窗选择，无需修改代码）
- 支持四种颜色实时切换识别：红 / 绿 / 蓝 / 黄
- 自动框出目标区域并显示像素面积
- 同步显示颜色掩膜（Mask）窗口，便于调试
- 基于 HSV 颜色空间，识别效果稳定，抗光照干扰能力强

---

## 运行环境

| 依赖 | 版本 |
|------|------|
| Python | 3.8 及以上 |
| OpenCV | `pip install opencv-python` |
| NumPy | `pip install numpy` |

---

## 快速开始

```bash
# 安装依赖
pip install opencv-python numpy

# 运行程序
python opencv.py
```

运行后会弹出文件选择窗口，选择任意图片即可开始检测。

---

## 操作说明

| 按键 | 功能 |
|------|------|
| `R` | 切换为红色检测模式 |
| `G` | 切换为绿色检测模式 |
| `B` | 切换为蓝色检测模式 |
| `Y` | 切换为黄色检测模式 |
| `Q` | 退出程序 |

---

## 文件结构

```
robot-vision-demo/
├── opencv.py        # 主程序
├── README.md        # 项目说明
└── demo/            # 效果截图
    ├── red.png
    ├── green.png
    ├── blue.png
    └── yellow.png
```

---

## 技术说明

- 颜色识别基于 **HSV 颜色空间**（相比 RGB 对光照变化更鲁棒）
- 使用形态学操作（`MORPH_CLOSE` + `MORPH_OPEN`）去除噪点、填补空洞
- 自动筛选面积最大的轮廓作为目标，过滤小干扰区域
- 支持带空格和中文的文件路径（使用 `cv2.imdecode` + `np.fromfile`）

---

## 作者

**方博林** · 河海大学 机器人工程专业  
frptp@outlook.com
