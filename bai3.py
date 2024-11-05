import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

# Hàm kiểm tra hợp lệ của các giá trị đầu vào
def validate_inputs(params, shape=None):
    try:
        values = [float(param) for param in params]
        if all(value > 0 for value in values):
            if shape == "Tứ giác" and values[0] == values[2]:
                messagebox.showerror("Lỗi", "Tứ giác không hợp lệ khi cạnh a và c bằng nhau.")
                return None
            return values
        else:
            messagebox.showerror("Lỗi", "Giá trị nhập vào phải là số dương.")
            return None
    except ValueError:
        messagebox.showerror("Lỗi", "Giá trị nhập vào không hợp lệ. Vui lòng nhập số.")
        return None

# Hàm vẽ hình tròn
def draw_circle(radius):
    fig, ax = plt.subplots()
    circle = plt.Circle((0, 0), radius, color='blue', fill=False)
    ax.add_artist(circle)
    ax.set_xlim(-radius - 1, radius + 1)
    ax.set_ylim(-radius - 1, radius + 1)
    ax.set_aspect('equal', 'box')
    plt.title(f"Hình tròn bán kính {radius}")
    plt.show()

# Hàm vẽ tam giác
def draw_triangle(a, b, c):
    fig, ax = plt.subplots()
    x = [0, a, b, 0]
    y = [0, 0, c, 0]
    ax.plot(x, y, 'b-')
    ax.fill(x, y, 'b', alpha=0.3)
    ax.set_aspect('equal', 'box')
    plt.title("Tam giác với ba cạnh a, b, c")
    plt.show()

# Hàm vẽ tứ giác
def draw_quadrilateral(a, b, c, d):
    fig, ax = plt.subplots()
    x = [0, a, a + b, d, 0]
    y = [0, 0, c, c, 0]
    ax.plot(x, y, 'b-')
    ax.fill(x, y, 'b', alpha=0.3)
    ax.set_aspect('equal', 'box')
    plt.title("Tứ giác với bốn cạnh a, b, c, d")
    plt.show()

# Hàm vẽ hình vuông
def draw_square(side):
    fig, ax = plt.subplots()
    x = [0, side, side, 0, 0]
    y = [0, 0, side, side, 0]
    ax.plot(x, y, 'b-')
    ax.fill(x, y, 'b', alpha=0.3)
    ax.set_aspect('equal', 'box')
    plt.title(f"Hình vuông cạnh {side}")
    plt.show()

# Hàm vẽ hình chữ nhật
def draw_rectangle(length, width):
    fig, ax = plt.subplots()
    x = [0, length, length, 0, 0]
    y = [0, 0, width, width, 0]
    ax.plot(x, y, 'b-')
    ax.fill(x, y, 'b', alpha=0.3)
    ax.set_aspect('equal', 'box')
    plt.title(f"Hình chữ nhật với chiều dài {length} và chiều rộng {width}")
    plt.show()

# Hàm vẽ hình trụ
def draw_cylinder(radius, height):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    z = np.linspace(0, height, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid)
    y_grid = radius * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, color='blue', alpha=0.7)
    ax.set_title(f"Hình trụ bán kính {radius} và chiều cao {height}")
    plt.show()

# Hàm vẽ hình cầu
def draw_sphere(radius):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='blue', alpha=0.7)
    ax.set_title(f"Hình cầu bán kính {radius}")
    plt.show()

# Tính chu vi, diện tích cho hình 2D
def calculate_2d(shape, params):
    if shape == "Hình tròn":
        radius = params[0]
        perimeter = 2 * math.pi * radius
        area = math.pi * radius ** 2
        return perimeter, area
    elif shape == "Tứ giác":
        a, b, c, d = params
        perimeter = a + b + c + d
        # Sử dụng công thức Heron cho diện tích tứ giác, giả định b và d là chiều cao
        area = (a + c) / 2 * math.sqrt(b ** 2 - (((a - c) ** 2 + b ** 2 - d ** 2) / (2 * (a - c))) ** 2)
        return perimeter, area
    elif shape == "Tam giác":
        a, b, c = params
        perimeter = a + b + c
        s = perimeter / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return perimeter, area
    elif shape == "Hình vuông":
        side = params[0]
        perimeter = 4 * side
        area = side ** 2
        return perimeter, area
    elif shape == "Hình chữ nhật":
        length, width = params
        perimeter = 2 * (length + width)
        area = length * width
        return perimeter, area

# Tính diện tích, thể tích cho hình 3D
def calculate_3d(shape, params):
    if shape == "Hình cầu":
        radius = params[0]
        area = 4 * math.pi * radius ** 2
        volume = (4 / 3) * math.pi * radius ** 3
        return area, volume
    elif shape == "Hình trụ":
        radius, height = params
        area = 2 * math.pi * radius * (radius + height)
        volume = math.pi * radius ** 2 * height
        return area, volume

# Hàm hiển thị trường nhập liệu cho hình 2D
def show_2d_inputs(event):
    shape = shape_2d_selection.get()
    for widget in frame_inputs.winfo_children():
        widget.destroy()

    if shape == "Hình vuông":
        tk.Label(frame_inputs, text="Cạnh:").grid(row=0, column=0)
        entry_side = tk.Entry(frame_inputs)
        entry_side.grid(row=0, column=1)
        button_calc = tk.Button(frame_inputs, text="Tính và vẽ",
                                command=lambda: handle_2d_calculation("Hình vuông", [entry_side.get()]))
        button_calc.grid(row=1, column=0, columnspan=2)

    elif shape == "Hình chữ nhật":
        tk.Label(frame_inputs, text="Chiều dài:").grid(row=0, column=0)
        entry_length = tk.Entry(frame_inputs)
        entry_length.grid(row=0, column=1)

        tk.Label(frame_inputs, text="Chiều rộng:").grid(row=1, column=0)
        entry_width = tk.Entry(frame_inputs)
        entry_width.grid(row=1, column=1)

        button_calc = tk.Button(frame_inputs, text="Tính và vẽ", command=lambda: handle_2d_calculation("Hình chữ nhật",
                                                                                                       [entry_length.get(),
                                                                                                        entry_width.get()]))
        button_calc.grid(row=2, column=0, columnspan=2)

    elif shape == "Hình tròn":
        tk.Label(frame_inputs, text="Bán kính:").grid(row=0, column=0)
        entry_radius = tk.Entry(frame_inputs)
        entry_radius.grid(row=0, column=1)
        button_calc = tk.Button(frame_inputs, text="Tính và vẽ",
                                command=lambda: handle_2d_calculation("Hình tròn", [entry_radius.get()]))
        button_calc.grid(row=1, column=0, columnspan=2)

    elif shape == "Tứ giác":
        tk.Label(frame_inputs, text="Cạnh a:").grid(row=0, column=0)
        entry_a = tk.Entry(frame_inputs)
        entry_a.grid(row=0, column=1)

        tk.Label(frame_inputs, text="Cạnh b:").grid(row=1, column=0)
        entry_b = tk.Entry(frame_inputs)
        entry_b.grid(row=1, column=1)

        tk.Label(frame_inputs, text="Cạnh c:").grid(row=2, column=0)
        entry_c = tk.Entry(frame_inputs)
        entry_c.grid(row=2, column=1)

        tk.Label(frame_inputs, text="Cạnh d:").grid(row=3, column=0)
        entry_d = tk.Entry(frame_inputs)
        entry_d.grid(row=3, column=1)

        button_calc = tk.Button(frame_inputs, text="Tính và vẽ",
                                command=lambda: handle_2d_calculation("Tứ giác", [entry_a.get(), entry_b.get(), entry_c.get(), entry_d.get()]))
        button_calc.grid(row=4, column=0, columnspan=2)

    elif shape == "Tam giác":
        tk.Label(frame_inputs, text="Cạnh a:").grid(row=0, column=0)
        entry_a = tk.Entry(frame_inputs)
        entry_a.grid(row=0, column=1)

        tk.Label(frame_inputs, text="Cạnh b:").grid(row=1, column=0)
        entry_b = tk.Entry(frame_inputs)
        entry_b.grid(row=1, column=1)

        tk.Label(frame_inputs, text="Cạnh c:").grid(row=2, column=0)
        entry_c = tk.Entry(frame_inputs)
        entry_c.grid(row=2, column=1)

        button_calc = tk.Button(frame_inputs, text="Tính và vẽ",
                                command=lambda: handle_2d_calculation("Tam giác", [entry_a.get(), entry_b.get(), entry_c.get()]))
        button_calc.grid(row=3, column=0, columnspan=2)

# Hàm hiển thị trường nhập liệu cho hình 3D
def show_3d_inputs(event):
    shape = shape_3d_selection.get()
    for widget in frame_inputs.winfo_children():
        widget.destroy()

    if shape == "Hình cầu":
        tk.Label(frame_inputs, text="Bán kính:").grid(row=0, column=0)
        entry_radius = tk.Entry(frame_inputs)
        entry_radius.grid(row=0, column=1)
        button_calc = tk.Button(frame_inputs, text="Tính và vẽ",
                                command=lambda: handle_3d_calculation("Hình cầu", [entry_radius.get()]))
        button_calc.grid(row=1, column=0, columnspan=2)

    elif shape == "Hình trụ":
        tk.Label(frame_inputs, text="Bán kính:").grid(row=0, column=0)
        entry_radius = tk.Entry(frame_inputs)
        entry_radius.grid(row=0, column=1)

        tk.Label(frame_inputs, text="Chiều cao:").grid(row=1, column=0)
        entry_height = tk.Entry(frame_inputs)
        entry_height.grid(row=1, column=1)

        button_calc = tk.Button(frame_inputs, text="Tính và vẽ", command=lambda: handle_3d_calculation("Hình trụ",
                                                                                                        [entry_radius.get(), entry_height.get()]))
        button_calc.grid(row=2, column=0, columnspan=2)

# Hàm xử lý tính toán và vẽ cho hình 2D
def handle_2d_calculation(shape, params):
    params = validate_inputs(params, shape)
    if params:
        perimeter, area = calculate_2d(shape, params)
        messagebox.showinfo("Kết quả", f"{shape}:\nChu vi: {perimeter:.2f}\nDiện tích: {area:.2f}")
        if shape == "Hình tròn":
            draw_circle(params[0])
        elif shape == "Tam giác":
            draw_triangle(params[0], params[1], params[2])
        elif shape == "Tứ giác":
            draw_quadrilateral(params[0], params[1], params[2], params[3])
        elif shape == "Hình vuông":
            draw_square(params[0])
        elif shape == "Hình chữ nhật":
            draw_rectangle(params[0], params[1])

# Hàm xử lý tính toán và vẽ cho hình 3D
def handle_3d_calculation(shape, params):
    params = validate_inputs(params)
    if params:
        area, volume = calculate_3d(shape, params)
        messagebox.showinfo("Kết quả", f"{shape}:\nDiện tích bề mặt: {area:.2f}\nThể tích: {volume:.2f}")
        if shape == "Hình cầu":
            draw_sphere(params[0])
        elif shape == "Hình trụ":
            draw_cylinder(params[0], params[1])

# Khởi tạo giao diện Tkinter
root = tk.Tk()
root.title("Chọn Hình Học")

frame_inputs = tk.Frame(root)
frame_inputs.pack()

# Combobox chọn hình 2D
shape_2d_selection = ttk.Combobox(root, values=["Hình tròn", "Tam giác", "Tứ giác", "Hình vuông", "Hình chữ nhật"])
shape_2d_selection.set("Chọn hình 2D")
shape_2d_selection.pack()
shape_2d_selection.bind("<<ComboboxSelected>>", show_2d_inputs)

# Combobox chọn hình 3D
shape_3d_selection = ttk.Combobox(root, values=["Hình cầu", "Hình trụ"])
shape_3d_selection.set("Chọn hình 3D")
shape_3d_selection.pack()
shape_3d_selection.bind("<<ComboboxSelected>>", show_3d_inputs)

root.mainloop()
