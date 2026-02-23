import ctypes
import os
from ctypes import wintypes
from datetime import datetime
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from io import BytesIO
import tkinter.font as tkFont


class BinaryzacjaApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Binaryzacja lokalna')

        # Ustawienia okna
        SPI_GETWORKAREA = 48
        rcWork = wintypes.RECT()
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rcWork), 0)
        work_width = rcWork.right - rcWork.left
        work_height = rcWork.bottom - rcWork.top
        width_95 = int(work_width * 0.9)
        height_95 = int(work_height * 0.9)
        pos_x = rcWork.left + (work_width - width_95) // 2
        pos_y = rcWork.top + (work_height - height_95) // 2
        self.root.geometry(f'{width_95}x{height_95}+{pos_x}+{pos_y}')

        # Czcionki i kolory
        self.base_width = 1600
        self.base_height = 900
        self.font_base_size = 11
        self.font_base = tkFont.Font(family='Arial', size=self.font_base_size, weight='bold')
        self.font_base_normal = tkFont.Font(family='Arial', size=15)
        self.font_title = tkFont.Font(family='Arial', size=20, weight='bold')
        self.font_label = tkFont.Font(family='Arial', size=15, weight='bold')
        self.min_font_size = 8
        self.max_font_size = 20

        background_color = '#E4E0E1'
        self.root.configure(bg=background_color)
        self.root.bind('<Configure>', self.on_resize)

        # Zmienne aplikacji
        self.original_image = None
        self.binary_image = None
        self.method_var = tk.StringVar(value='method1')
        self.current_language = 'pl'

        # Słownik tłumaczeń
        self.texts = {
            'pl': {
                'title': 'Binaryzacja lokalna',
                'load_image': 'Wczytaj obraz',
                'binary': 'Binaryzuj',
                'save_result': 'Zapisz obraz wynikowy',
                'clear_settings': 'Wyczyść ustawienia',
                'language': 'Polski/English',
                'window_size': 'Wybierz rozmiar okna',
                'method': 'Wybierz algorytm/metodę:',
                'method1': 'Globalna Binaryzacja 1 progowa',
                'method2': 'Globalna Binaryzacja 2 progowa',
                'method3': 'Lokalna Metoda Otsu',
                'method4': 'Metoda Sauvoli',
                'method5': 'Lokalna Binaryzacja ze średnią',
                'method6': 'Lokalna Binaryzacja z przesunięciem',
                'threshold1_menu': 'Podaj pierwszy próg:',
                'threshold2_menu': 'Podaj drugi próg:',
                'threshold1': 'Podaj pierwszy próg',
                'threshold2': 'Podaj drugi próg',
                'offset_menu': 'Wybierz przesunięcie progu:',
                'error_load_image': 'Nie można wczytać obrazu',
                'warning_no_image': 'Najpierw wczytaj obraz',
                'warning_no_binary_image': 'Najpierw przeprowadź binaryzację',
                'success_save_image': 'Obraz został zapisany',
                'histogram_original': 'Histogram oryginalnego obrazu',
                'histogram_binary': 'Histogram binaryzowanego obrazu',
                'select_method_warning': 'Wybierz poprawną metodę.',
                'invalid_window_size': 'Nieprawidłowy rozmiar okna.',
                'invalid_offset': 'Nieprawidłowe przesunięcie.'
            },
            'en': {
                'title': 'Local Binarization',
                'load_image': 'Load Image',
                'binary': 'Binarise',
                'save_result': 'Save Image',
                'clear_settings': 'Clear Settings',
                'language': 'Polish/English',
                'window_size': 'Select Window Size',
                'method': 'Select the Algorithm/Method:',
                'method1': 'Global Binarisation with one Threshold',
                'method2': 'Global Binarisation with two Thresholds',
                'method3': 'Local Otsu Method',
                'method4': 'Sauvola Method',
                'method5': 'Local Binarisation with average',
                'method6': 'Local Binarisation with offset',
                'threshold1_menu': 'Enter First Threshold:',
                'threshold2_menu': 'Enter Second Threshold:',
                'threshold1': 'Enter first threshold',
                'threshold2': 'Enter second threshold',
                'offset_menu': 'Select threshold offset:',
                'error_load_image': 'Cannot load image',
                'warning_no_image': 'Load an image first',
                'warning_no_binary_image': 'Binarise an image first',
                'success_save_image': 'Image saved successfully',
                'histogram_original': 'Input Image Histogram',
                'histogram_binary': 'Output Image Histogram',
                'select_method_warning': 'Please select a valid binarisation method.',
                'invalid_window_size': 'Invalid window size.',
                'invalid_offset': 'Invalid threshold offset.'
            }
        }

        self.radio_buttons = []
        self.create_widgets()

    def create_widgets(self):
        button_color = '#AB886D'
        active_button_color = '#C2A18A'
        color = '#D6C0B3'

        self.left_panel = tk.Frame(self.root, bg=color)
        self.left_panel.place(relx=0, rely=0, relwidth=0.33, relheight=1.0)

        self.right_panel = tk.Frame(self.root, bg='#E4E0E1')
        self.right_panel.place(relx=0.33, rely=0, relwidth=0.72, relheight=1.0)

        self.title_label = tk.Label(self.right_panel, text=self.texts[self.current_language]['title'],
                                    font=self.font_title, bg='#E4E0E1')
        self.title_label.place(relx=0.5, rely=0.05, anchor='center')

        self.load_button = tk.Button(self.left_panel, text=self.texts[self.current_language]['load_image'],
                                     command=self.load_image, bg=button_color, activebackground=active_button_color,
                                     bd=3, font=self.font_base)
        self.load_button.place(relx=0.1, rely=0.02, relwidth=0.8, relheight=0.05)

        self.binary_button = tk.Button(self.left_panel, text=self.texts[self.current_language]['binary'],
                                       command=self.binaryzacja, bg=button_color, activebackground=active_button_color,
                                       bd=3, font=self.font_base)
        self.binary_button.place(relx=0.1, rely=0.08, relwidth=0.8, relheight=0.05)

        self.save_button = tk.Button(self.left_panel, text=self.texts[self.current_language]['save_result'],
                                     command=self.save_image, bg=button_color, activebackground=active_button_color,
                                     bd=3, font=self.font_base)
        self.save_button.place(relx=0.1, rely=0.14, relwidth=0.8, relheight=0.05)

        self.clear_button = tk.Button(self.left_panel, text=self.texts[self.current_language]['clear_settings'],
                                      command=self.clear_settings, bg=button_color,
                                      activebackground=active_button_color, bd=3, font=self.font_base)
        self.clear_button.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.05)

        self.language_button = tk.Button(self.left_panel, text=self.texts[self.current_language]['language'],
                                         command=self.switch_language, bg=button_color,
                                         activebackground=active_button_color, bd=3, font=self.font_base)
        self.language_button.place(relx=0.1, rely=0.26, relwidth=0.8, relheight=0.05)

        self.size_label = tk.Label(self.left_panel, text=self.texts[self.current_language]['window_size'],
                                   font=self.font_label, bg=color)
        self.size_label.place(relx=0.1, rely=0.32)

        self.window_size = tk.StringVar(value='4x4')
        self.size_menu = ttk.Combobox(self.left_panel, textvariable=self.window_size,
                                      values=['4x4', '8x8', '16x16', '32x32'], state='readonly',
                                      font=self.font_base_normal)
        self.size_menu.place(relx=0.1, rely=0.35, relwidth=0.8)

        self.method_label = tk.Label(self.left_panel, text=self.texts[self.current_language]['method'],
                                     font=self.font_label, bg=color)
        self.method_label.place(relx=0.1, rely=0.39)

        self.radio_button1 = tk.Radiobutton(self.left_panel, text=self.texts[self.current_language]['method1'],
                                            variable=self.method_var, value='method1', bg=color,
                                            font=self.font_base_normal, activebackground=active_button_color,
                                            command=self.update_thresholds_state, anchor='w', justify='left')
        self.radio_button1.place(relx=0.1, rely=0.42, relwidth=0.8)
        self.radio_button2 = tk.Radiobutton(self.left_panel, text=self.texts[self.current_language]['method2'],
                                            variable=self.method_var, value='method2', bg=color,
                                            font=self.font_base_normal, activebackground=active_button_color,
                                            command=self.update_thresholds_state, anchor='w', justify='left')
        self.radio_button2.place(relx=0.1, rely=0.46, relwidth=0.8)
        self.radio_button3 = tk.Radiobutton(self.left_panel, text=self.texts[self.current_language]['method3'],
                                            variable=self.method_var, value='method3', bg=color,
                                            font=self.font_base_normal, activebackground=active_button_color,
                                            command=self.update_thresholds_state, anchor='w', justify='left')
        self.radio_button3.place(relx=0.1, rely=0.5, relwidth=0.8)
        self.radio_button4 = tk.Radiobutton(self.left_panel, text=self.texts[self.current_language]['method4'],
                                            variable=self.method_var, value='method4', bg=color,
                                            font=self.font_base_normal, activebackground=active_button_color,
                                            command=self.update_thresholds_state, anchor='w', justify='left')
        self.radio_button4.place(relx=0.1, rely=0.54, relwidth=0.8)
        self.radio_button5 = tk.Radiobutton(self.left_panel, text=self.texts[self.current_language]['method5'],
                                            variable=self.method_var, value='method5', bg=color,
                                            font=self.font_base_normal, activebackground=active_button_color,
                                            command=self.update_thresholds_state, anchor='w', justify='left')
        self.radio_button5.place(relx=0.1, rely=0.58, relwidth=0.8)
        self.radio_button6 = tk.Radiobutton(self.left_panel, text=self.texts[self.current_language]['method6'],
                                            variable=self.method_var, value='method6', bg=color,
                                            font=self.font_base_normal, activebackground=active_button_color,
                                            command=self.update_thresholds_state, anchor='w', justify='left')
        self.radio_button6.place(relx=0.1, rely=0.62, relwidth=0.8)

        self.radio_buttons = [self.radio_button1, self.radio_button2, self.radio_button3, self.radio_button4,
                              self.radio_button5, self.radio_button6]

        self.threshold1_label = tk.Label(self.left_panel, text=self.texts[self.current_language]['threshold1_menu'],
                                         font=self.font_base_normal, bg=color)
        self.threshold1_label.place(relx=0.1, rely=0.66)
        self.threshold1_entry = tk.Entry(self.left_panel, font=self.font_base_normal)
        self.threshold1_entry.place(relx=0.1, rely=0.7, relwidth=0.8)

        self.threshold2_label = tk.Label(self.left_panel, text=self.texts[self.current_language]['threshold2_menu'],
                                         font=self.font_base_normal, bg=color)
        self.threshold2_label.place(relx=0.1, rely=0.74)
        self.threshold2_entry = tk.Entry(self.left_panel, font=self.font_base_normal)
        self.threshold2_entry.place(relx=0.1, rely=0.78, relwidth=0.8)

        self.offset_label = tk.Label(self.left_panel, text=self.texts[self.current_language]['offset_menu'],
                                     font=self.font_base_normal, bg=color)
        self.offset_label.place(relx=0.1, rely=0.82)

        self.offset_values = [str(i) for i in range((-10), 11)]
        self.offset_var = tk.StringVar(value='0')
        self.offset_menu = ttk.Combobox(self.left_panel, textvariable=self.offset_var, values=self.offset_values,
                                        state='disabled', width=10, font=self.font_base_normal)
        self.offset_menu.place(relx=0.1, rely=0.86, relwidth=0.3)

        self.image_label = tk.Label(self.right_panel, bg='#E4E0E1')
        self.image_label.place(relx=0.0015, rely=0.1, relwidth=0.4, relheight=0.35)

        self.result_label = tk.Label(self.right_panel, bg='#E4E0E1')
        self.result_label.place(relx=0.0015, rely=0.55, relwidth=0.4, relheight=0.35)

        self.histogram_before_label = tk.Label(self.right_panel, bg='#E4E0E1')
        self.histogram_before_label.place(relx=0.45, rely=0.1, relwidth=0.4, relheight=0.35)

        self.histogram_after_label = tk.Label(self.right_panel, bg='#E4E0E1')
        self.histogram_after_label.place(relx=0.45, rely=0.55, relwidth=0.4, relheight=0.35)

        self.update_texts()
        self.update_thresholds_state()

    def on_resize(self, event):
        width_scale = event.width / self.base_width
        height_scale = event.height / self.base_height
        scale = min(width_scale, height_scale)
        new_size_base = max(self.min_font_size, min(int(self.font_base_size * scale), self.max_font_size))
        self.font_base.configure(size=new_size_base)
        self.font_base_normal.configure(size=max(self.min_font_size, min(int(10 * scale), self.max_font_size)))
        self.font_label.configure(size=max(self.min_font_size, min(int(12 * scale), self.max_font_size)))
        self.font_title.configure(size=max(self.min_font_size, min(int(20 * scale), self.max_font_size)))
        self.left_panel.update_idletasks()
        panel_width = self.left_panel.winfo_width()
        wrap_len = int(panel_width * 0.9)
        for rb in self.radio_buttons:
            rb.config(wraplength=wrap_len)

    def update_thresholds_state(self):
        method = self.method_var.get()
        self.threshold1_entry.config(state='disabled')
        self.threshold2_entry.config(state='disabled')
        self.offset_menu.config(state='disabled')

        if method == 'method1':
            self.threshold1_entry.config(state='normal')
        elif method == 'method2':
            self.threshold1_entry.config(state='normal')
            self.threshold2_entry.config(state='normal')
        elif method in ['method3', 'method4', 'method5']:
            pass  # Pozostają disabled
        elif method == 'method6':
            self.offset_menu.config(state='readonly')

    def switch_language(self):
        self.current_language = 'en' if self.current_language == 'pl' else 'pl'
        self.update_texts()
        self.update_thresholds_state()

    def update_texts(self):
        texts = self.texts[self.current_language]
        self.title_label.config(text=texts['title'])
        self.load_button.config(text=texts['load_image'])
        self.binary_button.config(text=texts['binary'])
        self.save_button.config(text=texts['save_result'])
        self.clear_button.config(text=texts['clear_settings'])
        self.language_button.config(text=texts['language'])
        self.size_label.config(text=texts['window_size'])
        self.method_label.config(text=texts['method'])
        self.radio_button1.config(text=texts['method1'])
        self.radio_button2.config(text=texts['method2'])
        self.radio_button3.config(text=texts['method3'])
        self.radio_button4.config(text=texts['method4'])
        self.radio_button5.config(text=texts['method5'])
        self.radio_button6.config(text=texts['method6'])
        self.threshold1_label.config(text=texts['threshold1_menu'])
        self.threshold2_label.config(text=texts['threshold2_menu'])
        self.offset_label.config(text=texts['offset_menu'])

    def get_threshold(self, entry):
        try:
            return int(entry.get())
        except ValueError:
            return None

    def binaryzacja(self):
        if self.original_image is None:
            messagebox.showwarning('Uwaga', self.texts[self.current_language]['warning_no_image'])
            return

        method = self.method_var.get()
        texts = self.texts[self.current_language]
        valid_methods = ['method1', 'method2', 'method3', 'method4', 'method5', 'method6']

        if method not in valid_methods:
            messagebox.showwarning('Uwaga',
                                   texts.get('select_method_warning', 'Please select a valid binarisation method.'))
            return

        window_size_str = self.window_size.get()
        try:
            window_size = int(window_size_str.split('x')[0])
        except ValueError:
            messagebox.showwarning('Uwaga', texts.get('invalid_window_size', 'Invalid window size.'))
            return

        if window_size % 2 == 0:
            window_size += 1

        img_height, img_width = self.original_image.shape

        if method == 'method1':
            threshold1 = self.get_threshold(self.threshold1_entry)
            if threshold1 is None:
                messagebox.showwarning('Uwaga', texts['threshold1'])
                return
            _, self.binary_image = cv2.threshold(self.original_image, threshold1, 255, cv2.THRESH_BINARY)

        elif method == 'method2':
            threshold1 = self.get_threshold(self.threshold1_entry)
            threshold2 = self.get_threshold(self.threshold2_entry)
            if threshold1 is None:
                messagebox.showwarning('Uwaga', texts['threshold1'])
                return
            if threshold2 is None:
                messagebox.showwarning('Uwaga', texts['threshold2'])
                return
            self.binary_image = cv2.inRange(self.original_image, threshold1, threshold2)

        elif method == 'method3':
            self.binary_image = np.zeros_like(self.original_image)
            for y in range(0, img_height, window_size):
                for x in range(0, img_width, window_size):
                    y_end = min(y + window_size, img_height)
                    x_end = min(x + window_size, img_width)
                    block = self.original_image[y:y_end, x:x_end]
                    if block.size > 0:
                        _, local_otsu = cv2.threshold(block, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                        self.binary_image[y:y_end, x:x_end] = local_otsu

        elif method == 'method4':
            self.binary_image = cv2.adaptiveThreshold(self.original_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                      cv2.THRESH_BINARY, window_size, 10)

        elif method == 'method5':
            self.binary_image = np.zeros_like(self.original_image)
            half = window_size // 2
            for y in range(img_height):
                for x in range(img_width):
                    y_start = max(0, y - half)
                    y_end = min(img_height, y + half + 1)
                    x_start = max(0, x - half)
                    x_end = min(img_width, x + half + 1)
                    block = self.original_image[y_start:y_end, x_start:x_end]
                    mean_val = np.mean(block)
                    self.binary_image[y, x] = 255 if self.original_image[y, x] > mean_val else 0

        elif method == 'method6':
            try:
                offset = int(self.offset_var.get())
            except ValueError:
                messagebox.showwarning('Uwaga', texts.get('invalid_offset', 'Invalid threshold offset.'))
                return
            self.binary_image = np.zeros_like(self.original_image)
            half = window_size // 2
            for y in range(img_height):
                for x in range(img_width):
                    y_start = max(0, y - half)
                    y_end = min(img_height, y + half + 1)
                    x_start = max(0, x - half)
                    x_end = min(img_width, x + half + 1)
                    block = self.original_image[y_start:y_end, x_start:x_end]
                    mean_val = np.mean(block)
                    threshold_val = mean_val + offset
                    self.binary_image[y, x] = 255 if self.original_image[y, x] > threshold_val else 0

        self.display_image(self.binary_image, self.result_label)
        self.show_histogram(self.original_image, self.histogram_before_label, 'histogram_original')
        self.show_histogram(self.binary_image, self.histogram_after_label, 'histogram_binary')

    def load_image(self):
        file_path = filedialog.askopenfilename(initialdir='obrazy',
                                               title=self.texts[self.current_language]['load_image'],
                                               filetypes=[('Image files', '*.jpg *.jpeg *.png *.bmp')])
        if file_path:
            self.original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if self.original_image is None:
                messagebox.showerror('Błąd', self.texts[self.current_language]['error_load_image'])
            else:
                self.display_image(self.original_image, self.image_label)

    def clear_settings(self):
        self.threshold1_entry.config(state='disabled')
        self.threshold2_entry.config(state='disabled')
        self.offset_menu.config(state='disabled')
        self.threshold1_entry.delete(0, tk.END)
        self.threshold2_entry.delete(0, tk.END)
        self.offset_var.set('0')
        self.method_var.set('method1')
        self.window_size.set('4x4')
        self.image_label.config(image='')
        self.result_label.config(image='')
        self.histogram_before_label.config(image='')
        self.histogram_after_label.config(image='')
        self.update_thresholds_state()

    def save_image(self):
        if self.binary_image is None:
            messagebox.showwarning('Brak obrazu', self.texts[self.current_language]['warning_no_binary_image'])
            return

        folder_path = 'Wynikowe obrazy'
        os.makedirs(folder_path, exist_ok=True)
        file_name = filedialog.asksaveasfilename(defaultextension='.png',
                                                 filetypes=[('PNG files', '*.png'), ('JPEG files', '*.jpg')],
                                                 initialdir=folder_path)
        if file_name:
            cv2.imwrite(file_name, self.binary_image)
            messagebox.showinfo('Sukces', f"{self.texts[self.current_language]['success_save_image']} {file_name}")

    def display_image(self, img, label):
        label.update_idletasks()
        label_width = label.winfo_width()
        label_height = label.winfo_height()
        if img is None:
            return

        img_display = img.copy()
        img_height, img_width = img_display.shape
        scale = min(label_width / img_width, label_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        img_resized = cv2.resize(img_display, (new_width, new_height))
        img_resized = Image.fromarray(img_resized)
        img_tk = ImageTk.PhotoImage(image=img_resized)
        label.config(image=img_tk)
        label.image = img_tk

    def show_histogram(self, img, label, title_key):
        if img is None:
            return

        title = self.texts[self.current_language][title_key]
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.hist(img.ravel(), bins=256, range=[0, 256], color='gray')
        ax.set_title(title)
        ax.set_xlabel('Wartość odcienia szarości' if self.current_language == 'pl' else 'Gray scale value')
        ax.set_ylabel('Liczebność' if self.current_language == 'pl' else 'Quantity')
        canvas = BytesIO()
        plt.savefig(canvas, format='png', bbox_inches='tight')
        canvas.seek(0)
        plt.close(fig)
        histogram_image = Image.open(canvas)
        label.update_idletasks()
        label_width = label.winfo_width()
        label_height = label.winfo_height()
        if label_width > 0 and label_height > 0:
            histogram_image = histogram_image.resize((label_width, label_height), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(histogram_image)
        label.config(image=img_tk)
        label.image = img_tk


if __name__ == '__main__':
    root = tk.Tk()
    app = BinaryzacjaApp(root)
    root.mainloop()