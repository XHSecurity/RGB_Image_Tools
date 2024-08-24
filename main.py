import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

import cv2 as cv
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# 创建 log 文件夹，如果不存在
log_folder = 'log'

for folder in [log_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 日志记录函数
def log_action(action):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_filename = "operations_log.txt"
    log_filepath = os.path.join(log_folder, log_filename)
    with open(log_filepath, 'a') as log_file:
        log_file.write(f"Action: {action}, Time: {current_time}\n")

# 读取图像
def read_image():
    global image, blue_channel, green_channel, red_channel
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    image = cv.imread(file_path, cv.IMREAD_COLOR)

    if image is None:
        messagebox.showerror("错误", "无法读取图像文件，请检查文件路径是否正确")
        return

    blue_channel, green_channel, red_channel = cv.split(image)
    messagebox.showinfo("信息", "图像读取成功")
    show_image(image)
    reset_button_colors()
    read_button.config(bg='lightgreen')
    log_action("read_image")

# 处理并保存
def process_and_save():
    if image is None:
        messagebox.showerror("错误", "请先读取图像")
        return

    save_path = filedialog.askdirectory()
    if not save_path:
        return

    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

    # 原始图像
    plt.figure()
    plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    original_output_name = os.path.join(save_path, f'original_{current_time}.png')
    plt.savefig(original_output_name)
    plt.close()

    # 蓝色通道
    plt.figure()
    plt.imshow(blue_channel, cmap='Blues')
    plt.title('Blue Channel')
    plt.axis('off')
    blue_output_name = os.path.join(save_path, f'blue_{current_time}.png')
    plt.savefig(blue_output_name)
    plt.close()

    # 绿色通道
    plt.figure()
    plt.imshow(green_channel, cmap='Greens')
    plt.title('Green Channel')
    plt.axis('off')
    green_output_name = os.path.join(save_path, f'green_{current_time}.png')
    plt.savefig(green_output_name)
    plt.close()

    # 红色通道
    plt.figure()
    plt.imshow(red_channel, cmap='Reds')
    plt.title('Red Channel')
    plt.axis('off')
    red_output_name = os.path.join(save_path, f'red_{current_time}.png')
    plt.savefig(red_output_name)
    plt.close()

    messagebox.showinfo("信息", f'原始图像已保存为 {original_output_name}\n'
                                f'蓝色通道图像已保存为 {blue_output_name}\n'
                                f'绿色通道图像已保存为 {green_output_name}\n'
                                f'红色通道图像已保存为 {red_output_name}')
    reset_button_colors()
    process_button.config(bg='lightgreen')
    log_action("process_and_save")

# 显示图像
def show_image(img):
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    label_img.config(image=img_tk)
    label_img.image = img_tk

# 显示蓝色通道
def show_blue_channel():
    if blue_channel is not None:
        plt.figure()
        plt.imshow(blue_channel, cmap='Blues')
        plt.title('Blue Channel')
        plt.axis('off')
        plt.show()
        reset_button_colors()
        blue_button.config(bg='lightgreen')
        log_action("show_blue_channel")

# 显示绿色通道
def show_green_channel():
    if green_channel is not None:
        plt.figure()
        plt.imshow(green_channel, cmap='Greens')
        plt.title('Green Channel')
        plt.axis('off')
        plt.show()
        reset_button_colors()
        green_button.config(bg='lightgreen')
        log_action("show_green_channel")

# 显示红色通道
def show_red_channel():
    if red_channel is not None:
        plt.figure()
        plt.imshow(red_channel, cmap='Reds')
        plt.title('Red Channel')
        plt.axis('off')
        plt.show()
        reset_button_colors()
        red_button.config(bg='lightgreen')
        log_action("show_red_channel")

# 重置所有按钮的背景颜色
def reset_button_colors():
    read_button.config(bg='SystemButtonFace')
    process_button.config(bg='SystemButtonFace')
    blue_button.config(bg='SystemButtonFace')
    green_button.config(bg='SystemButtonFace')
    red_button.config(bg='SystemButtonFace')

# 窗口居中
def center_window(root):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = screen_width // 2 - size[0] // 2
    y = screen_height // 2 - size[1] // 2
    root.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

# GUI界面
root = tk.Tk()
root.title("RGB彩色图像处理工具")

# 设置窗口大小，便于居中显示
root.geometry("800x600")

image = None  # 全局变量
blue_channel = None
green_channel = None
red_channel = None

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

read_button = tk.Button(frame, text="读取图像", command=read_image)  # 添加读取按钮
read_button.pack(side=tk.LEFT, padx=5)

process_button = tk.Button(frame, text="处理并保存", command=process_and_save)  # 添加处理并保存按钮
process_button.pack(side=tk.LEFT, padx=5)

blue_button = tk.Button(frame, text="显示蓝色通道", command=show_blue_channel)  # 添加蓝色通道按钮
blue_button.pack(side=tk.LEFT, padx=5)

green_button = tk.Button(frame, text="显示绿色通道", command=show_green_channel)  # 添加绿色通道按钮
green_button.pack(side=tk.LEFT, padx=5)

red_button = tk.Button(frame, text="显示红色通道", command=show_red_channel)  # 添加红色通道按钮
red_button.pack(side=tk.LEFT, padx=5)

label_img = tk.Label(root)
label_img.pack(padx=10, pady=10)

center_window(root)
root.mainloop()
