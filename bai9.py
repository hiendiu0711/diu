import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, Scale, HORIZONTAL
from PIL import Image, ImageTk

# Hàm để tách biên ảnh với ngưỡng điều chỉnh
def edge_detection(image_path, threshold1, threshold2):
    # Đọc ảnh
    image = cv2.imread(image_path)

    if image is None:
        messagebox.showerror("Lỗi", "Không thể mở hoặc đọc tệp ảnh. Vui lòng kiểm tra đường dẫn.")
        return

    # Chuyển ảnh sang thang xám
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Áp dụng GaussianBlur để giảm nhiễu
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Tách biên bằng thuật toán Canny với ngưỡng điều chỉnh
    edges = cv2.Canny(blurred_image, threshold1, threshold2)

    # Hiển thị ảnh gốc và ảnh tách biên
    show_images(image, edges)

    return edges  # Trả về ảnh tách biên để có thể lưu

# Hàm để hiển thị ảnh trong GUI
def show_images(original, edges):
    # Chuyển đổi ảnh từ OpenCV (BGR) sang PIL (RGB)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

    # Tạo đối tượng Image từ numpy array
    original_image = Image.fromarray(original)
    edges_image = Image.fromarray(edges)

    # Chuyển đổi Image thành ImageTk
    original_photo = ImageTk.PhotoImage(original_image)
    edges_photo = ImageTk.PhotoImage(edges_image)

    # Cập nhật ảnh vào Label
    label_original.config(image=original_photo)
    label_original.image = original_photo  # Giữ tham chiếu để không bị garbage collection

    label_edges.config(image=edges_photo)
    label_edges.image = edges_photo  # Giữ tham chiếu để không bị garbage collection

# Hàm để chọn ảnh từ thư mục và hiển thị với ngưỡng điều chỉnh
def choose_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
    if image_path:
        update_edge_detection()  # Tự động hiển thị ảnh ban đầu với ngưỡng mặc định

# Hàm để cập nhật hiển thị tách biên khi điều chỉnh ngưỡng
def update_edge_detection():
    threshold1 = slider_threshold1.get()
    threshold2 = slider_threshold2.get()
    if image_path:
        edges = edge_detection(image_path, threshold1, threshold2)  # Lưu ảnh tách biên
        return edges  # Trả về ảnh tách biên để lưu

# Hàm để lưu ảnh tách biên
def save_image():
    threshold1 = slider_threshold1.get()
    threshold2 = slider_threshold2.get()
    if image_path:
        edges = edge_detection(image_path, threshold1, threshold2)
        if edges is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                cv2.imwrite(save_path, edges)  # Lưu ảnh tách biên

# Tạo giao diện chính
root = tk.Tk()
root.title("Điều Chỉnh Độ Tách Biên Ảnh")

# Khung cho ảnh
frame_image = tk.Frame(root)
frame_image.pack(pady=10)

# Nút để chọn ảnh
button_choose_image = tk.Button(frame_image, text="Chọn Ảnh", command=choose_image)
button_choose_image.pack(pady=10)

# Nút để lưu ảnh tách biên
button_save_image = tk.Button(frame_image, text="Lưu Ảnh Tách Biên", command=save_image)
button_save_image.pack(pady=10)

# Label để hiển thị ảnh gốc
label_original = tk.Label(frame_image)
label_original.pack(side="left", padx=5)

# Label để hiển thị ảnh tách biên
label_edges = tk.Label(frame_image)
label_edges.pack(side="right", padx=5)

# Thanh trượt để điều chỉnh ngưỡng tách biên
slider_threshold1 = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="Ngưỡng Thấp (Threshold1)",
                          command=lambda val: update_edge_detection())
slider_threshold1.set(100)  # Giá trị mặc định
slider_threshold1.pack(fill="x", padx=20, pady=5)

slider_threshold2 = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="Ngưỡng Cao (Threshold2)",
                          command=lambda val: update_edge_detection())
slider_threshold2.set(200)  # Giá trị mặc định
slider_threshold2.pack(fill="x", padx=20, pady=5)

# Biến toàn cục lưu đường dẫn ảnh
image_path = None

# Bắt đầu giao diện
root.mainloop()
