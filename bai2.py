import tkinter as tk
from tkinter import ttk, messagebox
from sympy import symbols, diff, integrate, sin, cos, tan, cot, limit, Eq, solve, Sum, oo
from sympy.plotting import plot3d
import matplotlib.pyplot as plt
import numpy as np

# Tạo ứng dụng chính
root = tk.Tk()
root.title("Ứng dụng hỗ trợ học môn Giải tích")

# Biến toàn cục
x, y = symbols('x y')

# Hàm xử lý tính toán
def calculate():
    expression = entry_expression.get()

    try:
        # Đánh giá biểu thức với các hàm lượng giác từ sympy
        expr = eval(expression, {"x": x, "y": y, "sin": sin, "cos": cos, "tan": tan, "cot": cot})

        selected_option = combobox.get()

        if selected_option == "Đạo hàm":
            result = diff(expr, x)
            result_label.config(text=f"Kết quả: {result}")

        elif selected_option == "Tích phân":
            result = integrate(expr, x)
            result_label.config(text=f"Kết quả: {result}")

        elif selected_option == "Giới hạn":
            result = limit(expr, x, 0)
            result_label.config(text=f"Kết quả: {result}")

        elif selected_option == "Giải phương trình":
            result = solve(Eq(expr, 0), x)
            result_label.config(text=f"Nghiệm: {result}")

        elif selected_option == "Tính tổng":
            n = symbols('n')
            result = Sum(expr, (x, 1, oo)).doit()
            result_label.config(text=f"Tổng: {result}")

        elif selected_option == "Đạo hàm cấp cao":
            n = int(entry_order.get())
            result = diff(expr, x, n)
            result_label.config(text=f"Kết quả: {result}")

        elif selected_option == "Vẽ đồ thị":
            plot_graph(expr)

        elif selected_option == "Vẽ đồ thị 3D":
            plot_graph_3d(expr)

    except Exception as e:
        messagebox.showerror("Lỗi cú pháp", f"Biểu thức không hợp lệ: {e}")


# Hàm vẽ đồ thị
def plot_graph(expr):
    x_vals = np.linspace(-10, 10, 400)
    y_vals = [expr.subs(x, val) for val in x_vals]

    plt.figure(figsize=(6, 4))
    plt.plot(x_vals, y_vals, label=f"y = {expr}")
    plt.title(f"Đồ thị của hàm số")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()

# Hàm vẽ đồ thị 3D
def plot_graph_3d(expr):
    plot3d(expr)


# Giao diện
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Nhập hàm số
tk.Label(frame, text="Nhập hàm số (vd: 2*sin(x), cos(x), tan(x)):").grid(row=0, column=0, padx=5, pady=5)
entry_expression = tk.Entry(frame, width=30)
entry_expression.grid(row=0, column=1, padx=5, pady=5)

# Nhập cấp đạo hàm
tk.Label(frame, text="Nhập cấp đạo hàm (nếu cần):").grid(row=1, column=0, padx=5, pady=5)
entry_order = tk.Entry(frame, width=10)
entry_order.grid(row=1, column=1, padx=5, pady=5)

# Tạo Combobox để chọn loại tính toán
tk.Label(frame, text="Chọn loại tính toán:").grid(row=2, column=0, padx=5, pady=5)
combobox = ttk.Combobox(frame, values=[
    "Đạo hàm",
    "Tích phân",
    "Giới hạn",
    "Giải phương trình",
    # "Tính tổng",
    "Đạo hàm cấp cao",
    "Vẽ đồ thị",
    # "Vẽ đồ thị 3D"
])
combobox.grid(row=2, column=1, padx=5, pady=5)
combobox.current(0)  # Mặc định chọn "Đạo hàm"

# Nút Tính toán
calculate_button = tk.Button(frame, text="Tính toán", command=calculate)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Nhãn kết quả
result_label = tk.Label(frame, text="Kết quả: ")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Khởi động vòng lặp chính
root.mainloop()
