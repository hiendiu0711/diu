import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# Hàm đọc dữ liệu từ file Excel
def read_data():
    file_path = filedialog.askopenfilename(title="Chọn file Excel", filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:  # Kiểm tra nếu người dùng đã chọn file
        df = pd.read_excel(file_path, index_col=0, header=0)
        return df
    else:
        messagebox.showerror("Lỗi", "Không có file nào được chọn.")
        return None

# Hàm hiển thị biểu đồ
def plot_chart(data, title, xlabel, ylabel, chart_type):
    plt.figure(figsize=(10, 6))

    if chart_type == "Biểu đồ cột":
        plt.bar(data.index, data.values, color='skyblue', label=xlabel)
        plt.legend(title="Lớp")
    elif chart_type == "Biểu đồ đường":
        plt.plot(data.index, data.values, marker='o', color='skyblue', label=xlabel)
        plt.legend(title="Lớp")
    elif chart_type == "Biểu đồ tròn":
        # Kiểm tra nếu tổng giá trị của dữ liệu là 0
        if data.sum() == 0 or len(data[data > 0]) == 0:
            messagebox.showerror("Lỗi", "Không có dữ liệu để vẽ biểu đồ tròn.")
            return
        plt.pie(data.values, labels=data.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Đảm bảo hình tròn
        plt.title(title)
        plt.legend(title="Lớp", loc="upper right")  # Thêm legend cho biểu đồ tròn

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Hàm hiển thị biểu đồ theo lựa chọn của người dùng
def show_chart(grade_combobox, chart_combobox):
    selected_grade = grade_combobox.get()  # Lấy giá trị từ combobox loại điểm

    # Thêm "Loại " vào trước tên điểm nếu cần thiết
    if selected_grade in ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F']:
        selected_grade = 'Loại ' + selected_grade

    # Kiểm tra xem cột có tồn tại hay không
    if selected_grade not in df.columns:
        messagebox.showerror("Lỗi", f"Không tìm thấy cột '{selected_grade}' trong dữ liệu.")
        return

    # Tiếp tục phần xử lý khi cột tồn tại
    data = df[selected_grade]

    # Gọi hàm vẽ biểu đồ với loại biểu đồ đã chọn
    plot_chart(data, f"Kết quả {selected_grade}", "Lớp", "Số sinh viên", chart_combobox.get())

# Đọc dữ liệu từ file
df = read_data()
if df is None:
    exit()  # Thoát nếu không có dữ liệu

# Tạo cửa sổ chính của ứng dụng
root = tk.Tk()
root.title("Ứng dụng Thống kê điểm sinh viên")
root.geometry("600x400")

# Tạo các tab
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Tab Phân loại điểm theo các loại điểm (A+, A, B+, B, v.v.)
tab_grades = ttk.Frame(notebook)
notebook.add(tab_grades, text="Phân loại điểm")

# Tab Phân loại bài kiểm tra
tab_tests = ttk.Frame(notebook)
notebook.add(tab_tests, text="Bài kiểm tra")

### Tab 1: Phân loại điểm ###
frame_grade = ttk.LabelFrame(tab_grades, text="Chọn phân loại điểm")
frame_grade.pack(padx=10, pady=10, fill="x")

# Tạo Combobox để lựa chọn loại điểm
grades = ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"]
grade_combobox = ttk.Combobox(frame_grade, values=grades, state="readonly")
grade_combobox.set("A+")  # Thiết lập giá trị mặc định
grade_combobox.pack(padx=10, pady=10, fill="x")

# Tạo Combobox để lựa chọn loại biểu đồ
chart_types = ["Biểu đồ cột", "Biểu đồ đường", "Biểu đồ tròn"]
chart_combobox_grade = ttk.Combobox(frame_grade, values=chart_types, state="readonly")
chart_combobox_grade.set("Biểu đồ cột")  # Thiết lập giá trị mặc định
chart_combobox_grade.pack(padx=10, pady=10, fill="x")

# Nút hiển thị biểu đồ
btn_show_grade = ttk.Button(tab_grades, text="Hiển thị biểu đồ",
                             command=lambda: show_chart(grade_combobox, chart_combobox_grade))
btn_show_grade.pack(pady=20)

### Tab 2: Bài kiểm tra ###
frame_tests = ttk.LabelFrame(tab_tests, text="Chọn bài kiểm tra")
frame_tests.pack(padx=10, pady=10, fill="x")

# Tạo Combobox để lựa chọn bài kiểm tra
tests = ["TX1", "TX2", "Cuối kỳ"]
test_combobox = ttk.Combobox(frame_tests, values=tests, state="readonly")
test_combobox.set("TX1")  # Thiết lập giá trị mặc định
test_combobox.pack(padx=10, pady=10, fill="x")

# Tạo Combobox để lựa chọn loại biểu đồ
chart_combobox_test = ttk.Combobox(frame_tests, values=chart_types, state="readonly")
chart_combobox_test.set("Biểu đồ cột")  # Thiết lập giá trị mặc định
chart_combobox_test.pack(padx=10, pady=10, fill="x")

# Nút hiển thị biểu đồ cho bài kiểm tra
btn_show_test = ttk.Button(tab_tests, text="Hiển thị biểu đồ",
                            command=lambda: show_chart(test_combobox, chart_combobox_test))
btn_show_test.pack(pady=20)

# Chạy ứng dụng
root.mainloop()
