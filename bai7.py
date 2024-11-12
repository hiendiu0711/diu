import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import numpy as np

# Biến toàn cục để lưu mô hình và scaler
model = None
scaler = None


# Hàm để huấn luyện lại mô hình
def train_model(file_path):
    global model, scaler

    # Bước 1: Tải và xử lý dữ liệu từ file CSV
    data = pd.read_csv(file_path)
    data = data.dropna()  # Xóa các hàng có giá trị thiếu

    # Phân chia dữ liệu
    X = data.drop('Potability', axis=1)
    y = data['Potability']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Bước 2: Xây dựng mô hình KNN
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)

    # Đánh giá mô hình
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Tính các chỉ số MSE, MRE và R²
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mre = np.mean(np.abs((y_test - y_pred) / y_test))

    # Hiển thị các chỉ số
    messagebox.showinfo("Huấn luyện thành công",
                        f"Độ chính xác của mô hình: {accuracy * 100:.2f}%\n"
                        f"MSE: {mse:.4f}\n"
                        f"R²: {r2:.4f}\n"
                        f"MRE: {mre:.4f}")

    # Vẽ đồ thị so sánh giá trị thực tế và dự đoán
    plot_comparison(y_test, y_pred)


# Hàm để vẽ đồ thị so sánh
def plot_comparison(y_test, y_pred):
    plt.figure(figsize=(10, 6))

    # Vẽ biểu đồ so sánh giá trị thực tế và giá trị dự đoán
    plt.plot(y_test.values, label='Giá trị thực tế', marker='o')
    plt.plot(y_pred, label='Giá trị dự đoán', marker='x')

    plt.title('So sánh giá trị thực tế và dự đoán')
    plt.xlabel('Chỉ số mẫu')
    plt.ylabel('Potability')
    plt.legend()
    plt.grid(True)
    plt.show()


# Hàm để dự đoán chất lượng nước
def predict_potability():
    try:
        # Lấy giá trị từ các ô nhập liệu
        ph = float(entry_ph.get())
        hardness = float(entry_hardness.get())
        solids = float(entry_solids.get())
        chloramines = float(entry_chloramines.get())
        sulfate = float(entry_sulfate.get())
        conductivity = float(entry_conductivity.get())
        organic_carbon = float(entry_organic_carbon.get())
        trihalomethanes = float(entry_trihalomethanes.get())
        turbidity = float(entry_turbidity.get())

        # Kiểm tra xem đã huấn luyện mô hình chưa
        if model is None or scaler is None:
            messagebox.showerror("Lỗi", "Vui lòng huấn luyện mô hình trước khi sử dụng.")
            return

        # Chuẩn hóa dữ liệu đầu vào
        input_data = scaler.transform(
            [[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])

        # Dự đoán kết quả
        prediction = model.predict(input_data)

        # Hiển thị kết quả
        if prediction[0] == 1:
            messagebox.showinfo("Kết quả", "Nước an toàn để uống.")
        else:
            messagebox.showinfo("Kết quả", "Nước không an toàn để uống.")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng tất cả các chỉ số.")


# Hàm để chọn file CSV
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        train_model(file_path)


# Tạo cửa sổ GUI
root = tk.Tk()
root.title("Đánh giá độ an toàn của nước")
root.geometry("400x500")

# Tạo các ô nhập liệu
tk.Label(root, text="pH").grid(row=0, column=0, padx=10, pady=5)
entry_ph = tk.Entry(root)
entry_ph.grid(row=0, column=1)

tk.Label(root, text="Hardness").grid(row=1, column=0, padx=10, pady=5)
entry_hardness = tk.Entry(root)
entry_hardness.grid(row=1, column=1)

tk.Label(root, text="Solids").grid(row=2, column=0, padx=10, pady=5)
entry_solids = tk.Entry(root)
entry_solids.grid(row=2, column=1)

tk.Label(root, text="Chloramines").grid(row=3, column=0, padx=10, pady=5)
entry_chloramines = tk.Entry(root)
entry_chloramines.grid(row=3, column=1)

tk.Label(root, text="Sulfate").grid(row=4, column=0, padx=10, pady=5)
entry_sulfate = tk.Entry(root)
entry_sulfate.grid(row=4, column=1)

tk.Label(root, text="Conductivity").grid(row=5, column=0, padx=10, pady=5)
entry_conductivity = tk.Entry(root)
entry_conductivity.grid(row=5, column=1)

tk.Label(root, text="Organic Carbon").grid(row=6, column=0, padx=10, pady=5)
entry_organic_carbon = tk.Entry(root)
entry_organic_carbon.grid(row=6, column=1)

tk.Label(root, text="Trihalomethanes").grid(row=7, column=0, padx=10, pady=5)
entry_trihalomethanes = tk.Entry(root)
entry_trihalomethanes.grid(row=7, column=1)

tk.Label(root, text="Turbidity").grid(row=8, column=0, padx=10, pady=5)
entry_turbidity = tk.Entry(root)
entry_turbidity.grid(row=8, column=1)

# Tạo nút để dự đoán
predict_button = tk.Button(root, text="Kiểm tra", command=predict_potability)
predict_button.grid(row=9, column=0, columnspan=2, pady=10)

# Tạo nút để chọn file và huấn luyện mô hình
train_button = tk.Button(root, text="Chọn file và huấn luyện", command=load_file)
train_button.grid(row=10, column=0, columnspan=2, pady=10)

# Chạy ứng dụng
root.mainloop()
