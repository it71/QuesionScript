# 小猿口算自动答题脚本

## 项目介绍
本项目是小白编写的练手项目，旨在优化题目解答速度。该脚本专为一年级学生设计，适用于20以内的数字比较。它利用图像处理和OCR技术，自动从屏幕截图中提取数字并判断其大小关系，帮助学生快速练习数字比较。

## 功能与实现原理
- **自动截取指定区域的数字**：使用 `pyautogui` 库截取用户自定义的数字和答题区域。
- **OCR技术提取数字**：通过 `pytesseract` 库对截图进行文字识别，将图像中的数字转换为文本。
- **数字比较与符号绘制**：比较提取的数字，并利用 `pyautogui` 在屏幕上绘制相应的“大于”或“小于”符号。

## 安装说明
1. 确保已安装 Python 3.x。
2. 使用以下命令安装所需库：
   ```bash
   pip install pyautogui pytesseract opencv-python keyboard numpy

## 更新说明
基于 [QuesionScript](https://github.com/maile456/QuesionScript) 修改，新增区域框选功能。框选功能通过鼠标事件和OpenCV实现，具体步骤如下：

### 鼠标回调函数
- 使用 `cv2.setMouseCallback` 设置 `select_region` 函数处理鼠标点击事件。
- 左键按下时 (`EVENT_LBUTTONDOWN`)，记录起始点坐标。
- 左键释放时 (`EVENT_LBUTTONUP`)，记录终点坐标，并绘制矩形框表示所选区域。

### 选择区域函数
- 在 `select_area` 函数中截取屏幕截图并转换为OpenCV格式。
- 使用 `cv2.imshow` 显示截图，调用 `select_region` 处理鼠标事件，等待用户选择完成后关闭窗口。

### 坐标保存与加载
- 所选区域坐标（矩形框的起止坐标）存储在列表中，并可以保存到JSON文件中以便下次使用。
- 使用 `json` 库将坐标保存至 `coordinates.json` 文件，脚本启动时检查文件是否存在，若存在则加载，若不存在则进行区域选择。
- 在首次运行后，用户选择的区域将被保存，后续运行时可直接加载，无需再次框选。
