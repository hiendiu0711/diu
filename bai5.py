import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter, resample, convolve
from scipy.fft import fft, ifft
import tkinter as tk
from tkinter import ttk

# Hàm tạo tín hiệu mẫu
def generate_signal(sampling_rate, t_end=1.0):
    t = np.linspace(0, t_end, int(sampling_rate * t_end), endpoint=False)
    signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)
    return t, signal

# Hàm lọc thông thấp
def lowpass_filter(data, cutoff, sampling_rate, order=5):
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff / nyquist
    b = firwin(order + 1, normal_cutoff)
    filtered_data = lfilter(b, 1.0, data)
    return filtered_data

# Hàm hiển thị tín hiệu gốc và sau khi lọc
def plot_signals(t, original, filtered):
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, original, label="Tín hiệu gốc")
    plt.title("Tín hiệu trước khi lọc")
    plt.xlabel("Thời gian [s]")
    plt.ylabel("Biên độ")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(t, filtered, label="Tín hiệu sau khi lọc", color="orange")
    plt.title("Tín hiệu sau khi lọc thông thấp")
    plt.xlabel("Thời gian [s]")
    plt.ylabel("Biên độ")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Hàm hiển thị tín hiệu trong miền tần số
def plot_frequency(signal, sampling_rate, title="Phổ tần số của tín hiệu"):
    freqs = np.fft.fftfreq(len(signal), 1/sampling_rate)
    magnitude = np.abs(fft(signal))
    plt.figure()
    plt.plot(freqs[:len(freqs)//2], magnitude[:len(magnitude)//2])
    plt.title(title)
    plt.xlabel("Tần số [Hz]")
    plt.ylabel("Biên độ")
    plt.grid()
    plt.show()

# Giao diện tkinter
def run_app():
    root = tk.Tk()
    root.title("Phần mềm xử lý tín hiệu số")

    # Nhập tần số cắt, tần số lấy mẫu và bậc bộ lọc
    ttk.Label(root, text="Tần số cắt (Hz):").grid(row=0, column=0)
    entry_cutoff = ttk.Entry(root)
    entry_cutoff.insert(0, "100")
    entry_cutoff.grid(row=0, column=1)

    ttk.Label(root, text="Tần số lấy mẫu (Hz):").grid(row=1, column=0)
    entry_sampling = ttk.Entry(root)
    entry_sampling.insert(0, "1000")
    entry_sampling.grid(row=1, column=1)

    ttk.Label(root, text="Bậc bộ lọc:").grid(row=2, column=0)
    entry_order = ttk.Entry(root)
    entry_order.insert(0, "5")
    entry_order.grid(row=2, column=1)

    # Tạo tín hiệu và lọc tín hiệu
    def apply_filter():
        cutoff = float(entry_cutoff.get())
        sampling_rate = int(entry_sampling.get())
        order = int(entry_order.get())

        t, original_signal = generate_signal(sampling_rate)
        filtered_signal = lowpass_filter(original_signal, cutoff, sampling_rate, order)
        plot_signals(t, original_signal, filtered_signal)
        plot_frequency(original_signal, sampling_rate, "Tín hiệu gốc trong miền tần số")
        plot_frequency(filtered_signal, sampling_rate, "Tín hiệu sau khi lọc trong miền tần số")

    # Hiển thị FFT của tín hiệu
    def show_fft():
        sampling_rate = int(entry_sampling.get())
        t, signal = generate_signal(sampling_rate)
        plot_frequency(signal, sampling_rate, "Phổ tần số của tín hiệu")

    # Nút bấm
    ttk.Button(root, text="Lọc tín hiệu", command=apply_filter).grid(row=3, column=0)
    ttk.Button(root, text="Hiển thị FFT", command=show_fft).grid(row=3, column=1)

    root.mainloop()

# Chạy ứng dụng
if __name__ == "__main__":
    run_app()
