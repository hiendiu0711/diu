import numpy as np
import cv2  # Make sure to import cv2
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")

        self.img = None
        self.processed_image = None

        self.create_widgets()

    def create_widgets(self):
        # Nút chọn ảnh
        btn_select_image = ttk.Button(self.root, text="Select Image", command=self.select_image)
        btn_select_image.pack(side="top", padx=10, pady=10)

        # Khung chứa các nút bộ lọc
        frame_filters = Frame(self.root)
        frame_filters.pack(pady=10)

        filter_buttons = [("Blur", self.apply_blur), ("Sharpen", self.apply_sharpen), ("Grayscale", self.apply_grayscale),
                          ("Negative", self.apply_negative), ("Flip", self.flip_image), ("Remove Background", self.remove_background),
                          ("Smooth Skin", self.smooth_skin), ("Remove Impurities", self.remove_impurities),
                          ("Blur Background", self.blur_background)]

        for text, command in filter_buttons:
            btn = ttk.Button(frame_filters, text=text, command=command)
            btn.pack(side="left", padx=5, pady=5)

        # Nút lưu ảnh
        btn_save_image = ttk.Button(self.root, text="Save Image", command=self.save_image)
        btn_save_image.pack(side="bottom", padx=10, pady=10)

        # Khung hiển thị ảnh
        self.frame_image = Frame(self.root)
        self.frame_image.pack(pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img = cv2.imread(file_path)
            # Kiểm tra kích thước ảnh
            if self.img.shape[0] > 512 or self.img.shape[1] > 512:
                self.img = self.resize_image(self.img)  # Thay đổi kích thước ảnh về 512x512
                messagebox.showinfo("Info", "Image size exceeded 512x512 pixels. The image has been resized.")

            self.processed_image = self.img.copy()
            self.display_images(self.img, self.processed_image)

    def resize_image(self, image):
        # Tính tỉ lệ thay đổi kích thước
        height, width = image.shape[:2]
        if height > 512 or width > 512:
            new_height = 512
            new_width = 512
            aspect_ratio = width / height

            if aspect_ratio > 1:  # Ảnh ngang
                new_height = int(512 / aspect_ratio)
            else:  # Ảnh đứng
                new_width = int(512 * aspect_ratio)

            return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return image

    def display_images(self, img1, img2):
        # Xóa các widget cũ
        for widget in self.frame_image.winfo_children():
            widget.destroy()

        # Hiển thị ảnh gốc
        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)  # Chuyển sang RGB
        img1_pil = Image.fromarray(cv2.resize(img1_rgb, (400, 400)))  # Resize cho dễ hiển thị
        img1_tk = ImageTk.PhotoImage(img1_pil)

        label1 = Label(self.frame_image, image=img1_tk)
        label1.image = img1_tk  # Giữ tham chiếu ảnh
        label1.grid(row=0, column=0, padx=5, pady=5)
        label1.config(text="Original Image", compound="top")

        # Hiển thị ảnh đã xử lý
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        img2_pil = Image.fromarray(cv2.resize(img2_rgb, (400, 400)))  # Resize cho dễ hiển thị
        img2_tk = ImageTk.PhotoImage(img2_pil)

        label2 = Label(self.frame_image, image=img2_tk)
        label2.image = img2_tk  # Giữ tham chiếu ảnh
        label2.grid(row=0, column=1, padx=5, pady=5)
        label2.config(text="Processed Image", compound="top")

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                messagebox.showinfo("Success", f"Image saved at {file_path}")
        else:
            messagebox.showwarning("Warning", "No processed image to save.")

    def apply_blur(self):
        if self.img is not None:
            blurred = cv2.GaussianBlur(self.img, (9, 9), 0)
            self.processed_image = blurred
            self.display_images(self.img, self.processed_image)

    def apply_sharpen(self):
        if self.img is not None:
            kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharpened = cv2.filter2D(self.img, -1, kernel_sharpen)
            self.processed_image = sharpened
            self.display_images(self.img, self.processed_image)

    def apply_grayscale(self):
        if self.img is not None:
            grayscale = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR)
            self.display_images(self.img, self.processed_image)

    def apply_negative(self):
        if self.img is not None:
            negative = cv2.bitwise_not(self.img)
            self.processed_image = negative
            self.display_images(self.img, self.processed_image)

    def flip_image(self):
        if self.img is not None:
            flipped = cv2.flip(self.img, 1)  # Lật ngang ảnh
            self.processed_image = flipped
            self.display_images(self.img, self.processed_image)

    def remove_background(self):
        if self.processed_image is not None:
            img_rgb = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
            mask = np.zeros(img_rgb.shape[:2], np.uint8)

            # Hiển thị ảnh và chọn ROI
            cv2.imshow("Select ROI", img_rgb)
            cv2.resizeWindow("Select ROI", 400, 400)
            rect = cv2.selectROI("Select ROI", img_rgb, fromCenter=False, showCrosshair=True)

            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)

            cv2.grabCut(img_rgb, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            img_rgb_nobg = img_rgb * mask2[:, :, np.newaxis]

            self.processed_image = cv2.cvtColor(img_rgb_nobg, cv2.COLOR_RGB2BGR)
            self.display_images(self.img, self.processed_image)

    def smooth_skin(self):
        if self.processed_image is not None:
            img_rgb = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
            smoothed = cv2.GaussianBlur(img_rgb, (7, 7), 1.5)
            self.processed_image = cv2.cvtColor(smoothed, cv2.COLOR_RGB2BGR)
            self.display_images(self.img, self.processed_image)

    def remove_impurities(self):
        if self.processed_image is not None:
            img_rgb = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
            mask = np.zeros(img_rgb.shape[:2], np.uint8)

            cv2.imshow("Select ROI for Impurity Removal", img_rgb)
            cv2.resizeWindow("Select ROI for Impurity Removal", 400, 400)
            rect = cv2.selectROI("Select ROI for Impurity Removal", img_rgb, fromCenter=False, showCrosshair=True)

            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)

            cv2.grabCut(img_rgb, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            img_rgb_nobg = img_rgb * mask2[:, :, np.newaxis]

            self.processed_image = cv2.cvtColor(img_rgb_nobg, cv2.COLOR_RGB2BGR)
            self.display_images(self.img, self.processed_image)

    def blur_background(self):
        if self.processed_image is not None:
            img_rgb = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
            mask = np.zeros(img_rgb.shape[:2], np.uint8)

            cv2.imshow("Select ROI for Background Blurring", img_rgb)
            cv2.resizeWindow("Select ROI for Background Blurring", 400, 400)
            rect = cv2.selectROI("Select ROI for Background Blurring", img_rgb, fromCenter=False, showCrosshair=True)

            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)

            cv2.grabCut(img_rgb, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            img_rgb_nobg = img_rgb * mask2[:, :, np.newaxis]

            blurred_bg = cv2.GaussianBlur(img_rgb, (15, 15), 0)
            combined = np.where(mask2[:, :, np.newaxis] == 1, img_rgb, blurred_bg)

            self.processed_image = cv2.cvtColor(combined, cv2.COLOR_RGB2BGR)
            self.display_images(self.img, self.processed_image)


if __name__ == "__main__":
    root = Tk()
    app = ImageProcessingApp(root)
    root.mainloop()