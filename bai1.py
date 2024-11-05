import tkinter as tk
from tkinter import messagebox
import numpy as np


class MatrixCalculatorApp:
  def __init__(self, master):
    self.master = master
    master.title("Máy tính ma trận")

    # Khung nhập kích thước ma trận
    self.size_frame = tk.Frame(master)
    self.size_frame.pack(pady=10)

    tk.Label(self.size_frame, text="Nhập kích thước ma trận (n x m):", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    self.rows_entry = tk.Entry(self.size_frame, width=5)
    self.rows_entry.pack(side=tk.LEFT, padx=5)
    self.cols_entry = tk.Entry(self.size_frame, width=5)
    self.cols_entry.pack(side=tk.LEFT, padx=5)

    self.create_button = tk.Button(self.size_frame, text="Tạo ma trận", command=self.create_matrix_input_fields)
    self.create_button.pack(side=tk.LEFT, padx=5)

    # Khung chứa các ô nhập liệu cho ma trận
    self.matrix_frame = tk.Frame(master)
    self.matrix_frame.pack(pady=10)

    # Menu chọn phép toán
    self.operation_frame = tk.Frame(master)
    self.operation_frame.pack(pady=10)

    tk.Label(self.operation_frame, text="Chọn phép toán:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    self.operations = ["Giải hệ phương trình", "Cộng ma trận", "Trừ ma trận", "Nhân ma trận", "Chia ma trận"]
    self.operation_combo = tk.StringVar()
    self.operation_combo.set(self.operations[0])
    self.operation_menu = tk.OptionMenu(self.operation_frame, self.operation_combo, *self.operations)
    self.operation_menu.pack(side=tk.LEFT, padx=5)

    # Khung kết quả
    self.result_label = tk.Label(master, text="", font=("Arial", 12), fg="blue")
    self.result_label.pack(pady=20)

  def create_matrix_input_fields(self):
    # Xóa các ô nhập liệu cũ (nếu có)
    for widget in self.matrix_frame.winfo_children():
      widget.destroy()

    try:
      self.rows = int(self.rows_entry.get())
      self.cols = int(self.cols_entry.get())
      if self.rows <= 0 or self.cols <= 0:
        raise ValueError("Kích thước ma trận phải lớn hơn 0.")

      # Tạo các ô nhập liệu cho ma trận A
      tk.Label(self.matrix_frame, text="Nhập ma trận A:", font=("Arial", 12)).grid(row=0, column=0,
                                                                                   columnspan=self.cols)
      self.matrix_entries_A = []
      for i in range(self.rows):
        row_entries = []
        for j in range(self.cols):
          entry = tk.Entry(self.matrix_frame, width=5)
          entry.grid(row=i + 1, column=j, padx=2, pady=2)
          row_entries.append(entry)
        self.matrix_entries_A.append(row_entries)

      # Tạo các ô nhập liệu cho vector B nếu cần
      if self.operation_combo.get() == "Giải hệ phương trình":
        tk.Label(self.matrix_frame, text="Nhập vector B:", font=("Arial", 12)).grid(row=0, column=self.cols,
                                                                                    columnspan=1)
        self.vector_entries_B = []
        for i in range(self.rows):
          entry = tk.Entry(self.matrix_frame, width=5)
          entry.grid(row=i + 1, column=self.cols, padx=2, pady=2)
          self.vector_entries_B.append(entry)
      else:
        tk.Label(self.matrix_frame, text="Nhập ma trận B:", font=("Arial", 12)).grid(row=0, column=self.cols,
                                                                                     columnspan=self.cols)
        self.matrix_entries_B = []
        for i in range(self.rows):
          row_entries = []
          for j in range(self.cols):
            entry = tk.Entry(self.matrix_frame, width=5)
            entry.grid(row=i + 1, column=self.cols + j, padx=2, pady=2)
            row_entries.append(entry)
          self.matrix_entries_B.append(row_entries)

      # Nút tính toán
      self.solve_button = tk.Button(self.matrix_frame, text="Tính toán", command=self.calculate)
      self.solve_button.grid(row=self.rows + 1, column=0, columnspan=self.cols * 2, pady=10)

    except ValueError as e:
      messagebox.showerror("Lỗi", f"Lỗi nhập liệu: {e}")

  def calculate(self):
    selected_operation = self.operation_combo.get()

    try:
      # Nhập ma trận A
      A = np.array([[float(entry.get()) for entry in row] for row in self.matrix_entries_A])

      if selected_operation == "Giải hệ phương trình":
        # Nhập vector B
        B = np.array([float(entry.get()) for entry in self.vector_entries_B])
        if A.shape[0] != A.shape[1] or A.shape[0] != len(B):
          raise ValueError("Kích thước ma trận hoặc vector không đúng.")

        # Giải hệ phương trình
        solution = np.linalg.solve(A, B)
        solution_text = "\n".join([f"x{i + 1} = {val:.2f}" for i, val in enumerate(solution)])
        self.result_label.config(text=f"Nghiệm của hệ phương trình:\n{solution_text}")

      elif selected_operation == "Cộng ma trận":
        B = np.array([[float(entry.get()) for entry in row] for row in self.matrix_entries_B])
        if A.shape != B.shape:
          raise ValueError("Hai ma trận phải có cùng kích thước.")
        result = A + B
        self.result_label.config(text=f"Kết quả của phép cộng:\n{result}")

      elif selected_operation == "Trừ ma trận":
        B = np.array([[float(entry.get()) for entry in row] for row in self.matrix_entries_B])
        if A.shape != B.shape:
          raise ValueError("Hai ma trận phải có cùng kích thước.")
        result = A - B
        self.result_label.config(text=f"Kết quả của phép trừ:\n{result}")

      elif selected_operation == "Nhân ma trận":
        B = np.array([[float(entry.get()) for entry in row] for row in self.matrix_entries_B])
        if A.shape[1] != B.shape[0]:
          raise ValueError("Số cột của ma trận A phải bằng số hàng của ma trận B.")
        result = A @ B
        self.result_label.config(text=f"Kết quả của phép nhân:\n{result}")

      elif selected_operation == "Chia ma trận":
        B = np.array([[float(entry.get()) for entry in row] for row in self.matrix_entries_B])
        if not np.linalg.det(B):
          raise ValueError("Ma trận B không khả nghịch.")
        B_inv = np.linalg.inv(B)
        result = A @ B_inv
        self.result_label.config(text=f"Kết quả của phép chia:\n{result}")

    except ValueError as e:
      messagebox.showerror("Lỗi", f"Lỗi nhập liệu: {e}")
    except np.linalg.LinAlgError:
      messagebox.showerror("Lỗi", "Phép tính không khả thi do đặc trưng của ma trận.")


root = tk.Tk()
app = MatrixCalculatorApp(root)
root.mainloop()
