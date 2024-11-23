import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog, Scale, HORIZONTAL, Frame, OptionMenu, StringVar
from PIL import Image, ImageTk

class ImageEnhancerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Enhancer")
        self.image_path = None
        self.original_image = None
        self.processed_image = None

        # Khung nút bấm
        button_frame = Frame(root)
        button_frame.pack(pady=10)

        # Nút chọn ảnh
        self.btn_select = Button(button_frame, text="Chọn ảnh", command=self.select_image)
        self.btn_select.pack(side="left", padx=5)

        # Nút lưu ảnh
        self.btn_save = Button(button_frame, text="Lưu ảnh", command=self.save_image, state="disabled")
        self.btn_save.pack(side="left", padx=5)

        # Khung chỉnh sửa ánh sáng và bộ lọc
        control_frame = Frame(root)
        control_frame.pack(pady=10)

        # Thanh trượt điều chỉnh độ tương phản
        self.alpha_scale = Scale(
            control_frame,
            from_=1.0,
            to=3.0,
            resolution=0.1,
            orient=HORIZONTAL,
            label="Độ tương phản (alpha)",
            command=self.update_image
        )
        self.alpha_scale.set(1.2)  # Giá trị mặc định
        self.alpha_scale.pack()

        # Thanh trượt điều chỉnh độ sáng
        self.beta_scale = Scale(
            control_frame,
            from_=0,
            to=100,
            resolution=1,
            orient=HORIZONTAL,
            label="Độ sáng (beta)",
            command=self.update_image
        )
        self.beta_scale.set(20)  # Giá trị mặc định
        self.beta_scale.pack()

        # Thanh trượt điều chỉnh sáng tối
        self.brightness_scale = Scale(
            control_frame,
            from_=-50,
            to=50,
            resolution=1,
            orient=HORIZONTAL,
            label="Điều chỉnh sáng tối",
            command=self.update_image
        )
        self.brightness_scale.set(0)
        self.brightness_scale.pack()

        # Khung xoay, lật và áp dụng bộ lọc
        options_frame = Frame(root)
        options_frame.pack(pady=10)

        # Xoay ảnh
        self.rotation_var = StringVar()
        self.rotation_var.set("Không xoay")
        self.rotation_options = ["Không xoay", "Xoay 90", "Xoay 180", "Xoay 270"]
        self.rotation_menu = OptionMenu(options_frame, self.rotation_var, *self.rotation_options, command=self.apply_rotation)
        self.rotation_menu.pack(side="left", padx=5)

        # Lật ảnh
        self.flip_var = StringVar()
        self.flip_var.set("Không lật")
        self.flip_options = ["Không lật", "Lật ngang", "Lật dọc"]
        self.flip_menu = OptionMenu(options_frame, self.flip_var, *self.flip_options, command=self.apply_flip)
        self.flip_menu.pack(side="left", padx=5)

        # Áp dụng bộ lọc
        self.filter_var = StringVar()
        self.filter_var.set("Không áp dụng")
        self.filter_options = ["Không áp dụng", "Đen trắng"]
        self.filter_menu = OptionMenu(options_frame, self.filter_var, *self.filter_options, command=self.apply_filter)
        self.filter_menu.pack(side="left", padx=5)

        # Label hiển thị ảnh
        self.image_label = Label(root)
        self.image_label.pack()

        # Label hiển thị ảnh gốc
        self.original_image_label = Label(root)
        self.original_image_label.pack()

    def select_image(self):
        # Mở hộp thoại chọn file
        self.image_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        if self.image_path:
            # Đọc và resize ảnh
            self.original_image = cv2.imread(self.image_path)
            if self.original_image is None:
                print("Không thể đọc ảnh.")
                return

            max_width, max_height = 800, 600
            height, width, _ = self.original_image.shape
            scale = min(max_width / width, max_height / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            self.original_image = cv2.resize(self.original_image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

            self.processed_image = self.original_image.copy()
            self.display_image()  # Hiển thị ảnh sau khi chọn
            self.display_original_image()  # Hiển thị ảnh gốc
            self.btn_save.config(state="normal")  # Kích hoạt nút lưu ảnh

    def display_image(self):
        if self.processed_image is None:
            return

        # Chuyển ảnh từ OpenCV sang định dạng Tkinter
        display_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
        display_image = Image.fromarray(display_image)
        display_image = ImageTk.PhotoImage(display_image)
        self.image_label.config(image=display_image)
        self.image_label.photo = display_image

    def display_original_image(self):
        if self.original_image is None:
            return

        # Chuyển ảnh gốc từ OpenCV sang định dạng Tkinter
        original_display = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        original_display = Image.fromarray(original_display)
        original_display = ImageTk.PhotoImage(original_display)
        self.original_image_label.config(image=original_display)
        self.original_image_label.photo = original_display

    def update_image(self, event=None):
        if self.original_image is None:
            return

        # Lấy giá trị từ thanh trượt
        alpha = self.alpha_scale.get()  # Độ tương phản
        beta = self.beta_scale.get()    # Độ sáng
        brightness = self.brightness_scale.get()  # Điều chỉnh sáng tối

        # Điều chỉnh độ sáng và tương phản
        enhanced_image = cv2.convertScaleAbs(self.original_image, alpha=alpha, beta=beta)
        self.processed_image = cv2.add(enhanced_image, np.array([brightness], dtype=np.uint8))

        self.display_image()

    def apply_rotation(self, event=None):
        if self.original_image is None:
            return

        # Xoay ảnh dựa trên lựa chọn
        if self.rotation_var.get() == "Xoay 90":
            self.processed_image = cv2.transpose(self.original_image)
            self.processed_image = cv2.flip(self.processed_image, flipCode=1)  # Lật ngang sau khi chuyển vị
        elif self.rotation_var.get() == "Xoay 180":
            self.processed_image = cv2.rotate(self.original_image, cv2.ROTATE_180)
        elif self.rotation_var.get() == "Xoay 270":
            self.processed_image = cv2.transpose(self.original_image)
            self.processed_image = cv2.flip(self.processed_image, flipCode=0)  # Lật dọc sau khi chuyển vị
        else:
            self.processed_image = self.original_image.copy()

        self.display_image()

    def apply_flip(self, event=None):
        if self.original_image is None:
            return

        # Lật ảnh dựa trên lựa chọn
        if self.flip_var.get() == "Lật ngang":
            self.processed_image = cv2.flip(self.original_image, 1)
        elif self.flip_var.get() == "Lật dọc":
            self.processed_image = cv2.flip(self.original_image, 0)
        else:
            self.processed_image = self.original_image.copy()

        self.display_image()

    def apply_filter(self, event=None):
        if self.original_image is None:
            return

        # Áp dụng bộ lọc dựa trên lựa chọn
        if self.filter_var.get() == "Đen trắng":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        else:
            self.processed_image = self.original_image.copy()

        self.display_image()

    def save_image(self):
        # Lưu ảnh đã chỉnh sửa
        if self.processed_image is not None:
            output_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
            )
            if output_path:
                cv2.imwrite(output_path, self.processed_image)
                print(f"Ảnh đã được lưu tại: {output_path}")
            else:
                print("Không lưu ảnh.")

def main():
    # Tạo cửa sổ ứng dụng
    root = Tk()
    app = ImageEnhancerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
