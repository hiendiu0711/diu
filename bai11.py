import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Button, Label, filedialog, Text, Scrollbar, END, Frame, BOTH, RIGHT, Y
from tkinter.messagebox import showinfo

# Hàm đọc và phân tích dữ liệu
def load_file():
    global data
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            data = pd.read_csv(file_path)
            text_output.delete("1.0", END)
            text_output.insert(END, f"File loaded: {file_path}\n\n")
            text_output.insert(END, "Thông tin dữ liệu:\n")
            text_output.insert(END, str(data.info()) + "\n\n")
            text_output.insert(END, "Mô tả thống kê:\n")
            text_output.insert(END, str(data.describe()) + "\n\n")
            showinfo("Thành công", "Dữ liệu đã được tải.")
        except Exception as e:
            showinfo("Lỗi", f"Không thể đọc file. Lỗi: {e}")

# Hàm vẽ biểu đồ phân phối
def plot_distribution():
    if data is None:
        showinfo("Thông báo", "Vui lòng tải dữ liệu trước.")
        return
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        plt.figure(figsize=(8, 5))
        sns.histplot(data[col], kde=True, bins=20)
        plt.title(f"Phân bố của {col}")
        plt.xlabel(col)
        plt.ylabel("Tần suất")
        plt.show()

# Hàm vẽ ma trận tương quan
def plot_correlation():
    if data is None:
        showinfo("Thông báo", "Vui lòng tải dữ liệu trước.")
        return
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
    plt.figure(figsize=(10, 8))
    corr_matrix = data[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Ma trận tương quan")
    plt.show()

# Hàm vẽ các cặp biểu đồ quan hệ
def plot_pairplot():
    if data is None:
        showinfo("Thông báo", "Vui lòng tải dữ liệu trước.")
        return
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
    sns.pairplot(data[numeric_cols])
    plt.show()

# Tạo GUI bằng Tkinter
root = Tk()
root.title("Phân tích dữ liệu sinh viên")

# Khung giao diện
frame = Frame(root)
frame.pack(fill=BOTH, expand=True)

# Nút bấm
btn_load = Button(frame, text="Tải File CSV", command=load_file, width=20)
btn_load.pack(pady=5)

btn_plot_dist = Button(frame, text="Biểu đồ phân phối", command=plot_distribution, width=20)
btn_plot_dist.pack(pady=5)

btn_plot_corr = Button(frame, text="Ma trận tương quan", command=plot_correlation, width=20)
btn_plot_corr.pack(pady=5)

btn_plot_pair = Button(frame, text="Cặp biểu đồ quan hệ", command=plot_pairplot, width=20)
btn_plot_pair.pack(pady=5)

# Text box hiển thị thông tin
text_output = Text(frame, wrap="word", height=15)
scrollbar = Scrollbar(frame, command=text_output.yview)
text_output.configure(yscrollcommand=scrollbar.set)

text_output.pack(side=RIGHT, fill=Y)
scrollbar.pack(side=RIGHT, fill=Y)

# Biến toàn cục lưu dữ liệu
data = None

# Chạy GUI
root.mainloop()
