import pyautogui
import pytesseract
import cv2
import time
import keyboard
import numpy as np
import json
import os

pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

sleep_time = 0.3
boxes = []
config_file = "coordinates.json"

def select_region(event, x, y, flags, param):
    global boxes
    if event == cv2.EVENT_LBUTTONDOWN:
        boxes.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        boxes[-1] = boxes[-1] + (x, y)
        cv2.rectangle(img, boxes[-1][:2], boxes[-1][2:], (0, 255, 0), 2)
        cv2.imshow("Select Region", img)

def select_area():
    global img
    img = np.array(pyautogui.screenshot())
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow("Select Region", img)
    cv2.setMouseCallback("Select Region", select_region)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_text(box):
    try:
        x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray, config='--psm 6').strip()
    except Exception as e:
        print(f"Error getting text: {e}")
        return ""

def draw_symbol(symbol: str, target_box: tuple):
    center_x = (target_box[0] + target_box[2]) // 2
    center_y = (target_box[1] + target_box[3]) // 2

    pyautogui.moveTo(center_x, center_y)
    pyautogui.mouseDown()

    if symbol == ">":
        pyautogui.moveTo(center_x + 10, center_y - 10, duration=0)
        pyautogui.moveTo(center_x + 20, center_y, duration=0)
        pyautogui.moveTo(center_x + 10, center_y + 10, duration=0)
    elif symbol == "<":
        pyautogui.moveTo(center_x - 10, center_y - 10, duration=0)
        pyautogui.moveTo(center_x - 20, center_y, duration=0)
        pyautogui.moveTo(center_x - 10, center_y + 10, duration=0)

    pyautogui.mouseUp()

def save_coordinates(coordinates):
    with open(config_file, 'w') as f:
        json.dump(coordinates, f)

def load_coordinates():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return None

# 询问用户是否更新框选区域
update_choice = input("是否要更新框选区域？(y/n): ").strip().lower()

if update_choice == 'y':
    print("请框选第一个数字区域")
    select_area()
    first_number_box = boxes.pop()

    print("请框选第二个数字区域")
    select_area()
    second_number_box = boxes.pop()

    print("请框选作答区域")
    answer_box = boxes.pop()

    print("请框选‘开心收下’区域")
    select_area()
    happy_accept_box = boxes.pop()

    save_coordinates({
        'first': first_number_box,
        'second': second_number_box,
        'answer': answer_box,
        'happy_accept': happy_accept_box
    })
else:
    saved_coordinates = load_coordinates()
    if saved_coordinates:
        first_number_box = saved_coordinates['first']
        second_number_box = saved_coordinates['second']
        answer_box = saved_coordinates['answer']
        happy_accept_box = saved_coordinates['happy_accept']
    else:
        print("没有找到已保存的坐标，请先运行一次并选择区域。")
        exit()

print("半糖脚本启动！")

paused = False  # 初始化暂停状态
while True:
    if keyboard.is_pressed('q'):
        print("退出程序")
        break

    if keyboard.is_pressed('space'):
        paused = not paused  # 切换暂停状态
        print("暂停" if paused else "继续")
        time.sleep(0.5)  # 防止多次触发

    if paused:
        time.sleep(1)  # 暂停时不进行其他操作
        continue

    num1_text = get_text(first_number_box)
    num2_text = get_text(second_number_box)

    print(f"提取的数字: {num1_text}, {num2_text}")

    # 检查是否能比较
    while not (num1_text.isdigit() and num2_text.isdigit()):
        print("等待有效数字...")
        time.sleep(1)  # 暂停一段时间
        num1_text = get_text(first_number_box)
        num2_text = get_text(second_number_box)

    num1 = int(num1_text)
    num2 = int(num2_text)

    answer = ">" if num1 > num2 else "<" if num1 < num2 else None

    if answer:
        draw_symbol(answer, answer_box)

    # 检查是否识别到“开心收下”
    happy_text = get_text(happy_accept_box)
    if happy_text == "开心收下":
        pyautogui.click((happy_accept_box[0] + happy_accept_box[2]) // 2, (happy_accept_box[1] + happy_accept_box[3]) // 2)

    time.sleep(sleep_time)
