import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Khởi tạo các biến toàn cục
df = None  # Dữ liệu sẽ được tải lên ở đây
model = None
X_train, X_test, y_train, y_test = None, None, None, None


# Hàm để tải lên file dữ liệu
def load_data():
    global df
    filepath = filedialog.askopenfilename(filetypes=[("Tập tin CSV", "*.csv")])
    if filepath:
        df = pd.read_csv(filepath)
        messagebox.showinfo("Tải dữ liệu", "Dữ liệu đã được tải thành công!")
    else:
        messagebox.showwarning("Tải dữ liệu", "Chưa chọn tập tin nào.")


# Hàm huấn luyện mô hình
def train_model():
    global model, X_train, X_test, y_train, y_test

    if df is None:
        messagebox.showerror("Lỗi huấn luyện", "Vui lòng tải dữ liệu trước.")
        return

    # Lấy tập đặc trưng (X) và nhãn (y)
    X = df.iloc[:, :5]  # Lấy cột từ 0 đến 4 làm đặc trưng
    y = df.iloc[:, 5]  # Cột thứ 6 là nhãn (Chỉ số Hiệu suất)

    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    # Lựa chọn thuật toán
    algorithm = selected_algorithm.get()

    if algorithm == "KNN":
        model = KNeighborsRegressor(n_neighbors=3, p=2)
    elif algorithm == "Hồi quy tuyến tính":
        model = LinearRegression()
    elif algorithm == "Cây quyết định":
        model = DecisionTreeRegressor()
    elif algorithm == "SVM":
        model = SVR()

    # Huấn luyện mô hình
    model.fit(X_train, y_train)

    messagebox.showinfo("Huấn luyện", f"Mô hình ({algorithm}) đã được huấn luyện thành công!")


# Hàm kiểm tra và hiển thị sai số, đồ thị
def test_model():
    if model is None or X_test is None or y_test is None:
        messagebox.showerror("Lỗi kiểm tra", "Vui lòng huấn luyện mô hình trước.")
        return

    # Dự đoán trên tập test
    y_predict = model.predict(X_test)

    # Tính toán sai số
    mse = mean_squared_error(y_test, y_predict)
    mae = mean_absolute_error(y_test, y_predict)
    rmse = np.sqrt(mse)

    # Hiển thị sai số
    result_text.set(f"MSE: {mse:.2f}, MAE: {mae:.2f}, RMSE: {rmse:.2f}")

    # Vẽ biểu đồ so sánh
    plt.plot(range(len(y_test)), y_test, 'ro', label='Dữ liệu gốc')
    plt.plot(range(len(y_predict)), y_predict, 'bo', label='Dữ liệu dự đoán')
    for i in range(len(y_test)):
        plt.plot([i, i], [y_test.iloc[i], y_predict[i]], 'g')
    plt.title("Dự đoán so với Thực tế")
    plt.legend()
    plt.show()

    # Biểu đồ thống kê tỷ lệ sai số
    differences = np.abs(y_test - y_predict)

    # Tính toán số lượng và tỷ lệ cho các khoảng sai số
    count_greater_than_2 = np.sum(differences > 2)
    count_between_1_and_2 = np.sum((differences <= 2) & (differences > 1))
    count_less_than_1 = np.sum(differences < 1)

    total_count = len(differences)

    # Tính phần trăm
    greater_than_2_percent = (count_greater_than_2 / total_count) * 100
    between_1_and_2_percent = (count_between_1_and_2 / total_count) * 100
    less_than_1_percent = (count_less_than_1 / total_count) * 100

    # Vẽ biểu đồ phần trăm
    labels = ['Sai số > 2', '1 < Sai số ≤ 2', 'Sai số < 1']
    sizes = [greater_than_2_percent, between_1_and_2_percent, less_than_1_percent]
    colors = ['lightcoral', 'lightblue', 'lightgreen']

    plt.figure()
    plt.bar(labels, sizes, color=colors)
    plt.title('Tỷ lệ sai số của dự đoán')
    plt.ylabel('Phần trăm (%)')
    plt.ylim(0, 100)  # Đặt giới hạn cho trục y
    plt.show()

    # Vẽ biểu đồ cột các chỉ số MSE, MAE, RMSE
    metrics = ['MSE', 'RMSE', 'MAE']
    values = [mse, rmse, mae]

    plt.figure()
    plt.bar(metrics, values, color=['blue', 'orange', 'green'])
    plt.title("Các chỉ số MSE, RMSE và MAE")
    plt.ylabel("Giá trị")
    plt.show()


# Hàm dự đoán dữ liệu mới
def predict_new():
    try:
        if model is None:
            messagebox.showerror("Lỗi Dự đoán", "Vui lòng huấn luyện mô hình trước.")
            return

        # Lấy dữ liệu nhập từ giao diện
        hours_studied = float(entry_hours_studied.get())
        previous_scores = float(entry_previous_scores.get())
        extracurricular_activities = float(entry_extracurricular_activities.get())
        sleep_hours = float(entry_sleep_hours.get())
        sample_question_papers_practiced = float(entry_sample_question_papers_practiced.get())

        # Kiểm tra giá trị âm
        if hours_studied < 0 or previous_scores < 0 or extracurricular_activities < 0 or sleep_hours < 0 or sample_question_papers_practiced < 0:
            raise ValueError("Giá trị đầu vào không được âm.")

        # Chuẩn bị dữ liệu đầu vào
        new_student_data = pd.DataFrame([[hours_studied, previous_scores, extracurricular_activities, sleep_hours,
                                          sample_question_papers_practiced]],
                                        columns=['Giờ học', 'Điểm số trước', 'Hoạt động ngoại khóa',
                                                 'Giờ ngủ', 'Số đề ôn tập đã làm'])

        # Dự đoán kết quả
        predicted_performance = model.predict(new_student_data)

        messagebox.showinfo("Dự đoán", f"Chỉ số Hiệu suất Dự đoán: {predicted_performance[0]:.2f}")

    except ValueError as ve:
        messagebox.showerror("Lỗi Nhập liệu", f"Lỗi: {ve}")


# Tạo giao diện với tkinter
root = tk.Tk()
root.title("Dự đoán Hiệu suất Học sinh")

# Tạo các nút và giao diện cho các phần khác nhau
tk.Button(root, text="Tải dữ liệu", command=load_data).grid(row=0, column=0)

# Tùy chọn thuật toán
selected_algorithm = tk.StringVar(value="KNN")
tk.Label(root, text="Chọn Thuật toán:").grid(row=1, column=0)
tk.Radiobutton(root, text="KNN", variable=selected_algorithm, value="KNN").grid(row=1, column=1)
tk.Radiobutton(root, text="Hồi quy tuyến tính", variable=selected_algorithm, value="Hồi quy tuyến tính").grid(row=1,
                                                                                                            column=2)
tk.Radiobutton(root, text="Cây quyết định", variable=selected_algorithm, value="Cây quyết định").grid(row=1, column=3)
tk.Radiobutton(root, text="SVM", variable=selected_algorithm, value="SVM").grid(row=1, column=4)

# Nút để huấn luyện mô hình
tk.Button(root, text="Huấn luyện", command=train_model).grid(row=2, column=0)

# Nút kiểm tra và hiển thị sai số, đồ thị
tk.Button(root, text="Kiểm tra", command=test_model).grid(row=3, column=0)

# Hiển thị sai số sau khi test
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text).grid(row=4, column=0, columnspan=3)

# Nhập liệu mới cho việc dự đoán
tk.Label(root, text="Giờ học:").grid(row=5, column=0)
entry_hours_studied = tk.Entry(root)
entry_hours_studied.grid(row=5, column=1)

tk.Label(root, text="Điểm số trước:").grid(row=6, column=0)
entry_previous_scores = tk.Entry(root)
entry_previous_scores.grid(row=6, column=1)

tk.Label(root, text="Hoạt động ngoại khóa:").grid(row=7, column=0)
entry_extracurricular_activities = tk.Entry(root)
entry_extracurricular_activities.grid(row=7, column=1)

tk.Label(root, text="Giờ ngủ:").grid(row=8, column=0)
entry_sleep_hours = tk.Entry(root)
entry_sleep_hours.grid(row=8, column=1)

tk.Label(root, text="Số đề ôn tập đã làm:").grid(row=9, column=0)
entry_sample_question_papers_practiced = tk.Entry(root)
entry_sample_question_papers_practiced.grid(row=9, column=1)

# Nút để dự đoán dữ liệu mới
tk.Button(root, text="Dự đoán Mới", command=predict_new).grid(row=10, column=0)

# Bắt đầu giao diện
root.mainloop()
