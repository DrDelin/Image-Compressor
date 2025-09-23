#VERSION 3.0
#BUILD FILE / SOURCE CODE
#DEVELOPED BY DR.DELIN
#REQUIRE FFMPEG.EXE TO RUN, NEWER THE VERSION - BETTER

import os
import subprocess
import time
import threading
from pathlib import Path
from PIL import Image as PILImage
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
import sys

# Tkinter for Windows file selection
import tkinter as tk
from tkinter import filedialog

#FFMPEG Binary Management:
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):  # PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

ffmpeg_path = resource_path("ffmpeg.exe")

class CompressorUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=10, **kwargs)

        # Title
        self.add_widget(Label(
            text="[b]Image Compressor v3.0[/b]",
            markup=True,
            font_size=24,
            size_hint=(1, 0.1)
        ))

        # File selection button
        btn_layout = BoxLayout(size_hint=(1, 0.1))
        self.file_btn = Button(text="Select Image")
        self.file_btn.bind(on_release=self.select_filemanager)
        btn_layout.add_widget(self.file_btn)
        self.add_widget(btn_layout)

        # Image preview
        self.image_preview = Image(size_hint=(1, 0.5))
        self.add_widget(self.image_preview)

        # Original size label
        self.original_size_label = Label(text="No image selected", size_hint=(1, 0.1))
        self.add_widget(self.original_size_label)

        # Compression input + dropdown
        input_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        input_layout.add_widget(Label(text="Target Size (1-1024):", size_hint=(0.4, 1)))

        self.target_input = TextInput(
            hint_text="Enter size",
            input_filter="int",
            size_hint=(0.4, 1)
        )

        # Dropdown button for KB/MB
        self.unit_btn = Button(text="KB", size_hint=(0.2, 1))
        self.dropdown = DropDown()
        for option in ["KB", "MB"]:
            btn = Button(text=option, size_hint_y=None, height=35)
            btn.bind(on_release=lambda b: self.select_unit(b.text))
            self.dropdown.add_widget(btn)
        self.unit_btn.bind(on_release=self.dropdown.open)

        input_layout.add_widget(self.target_input)
        input_layout.add_widget(self.unit_btn)
        self.add_widget(input_layout)

        # Action buttons
        act_layout = BoxLayout(size_hint=(1, 0.1))
        self.compress_btn = Button(text="Compress")
        self.clear_btn = Button(text="Clear Selection")
        self.compress_btn.bind(on_release=self.compress_image)
        self.clear_btn.bind(on_release=self.clear_fields)
        act_layout.add_widget(self.compress_btn)
        act_layout.add_widget(self.clear_btn)
        self.add_widget(act_layout)

        # Status label
        self.status_label = Label(text="Status: Waiting for input...", size_hint=(1, 0.2))
        self.add_widget(self.status_label)

        self.selected_file = None

    def select_unit(self, value):
        self.unit_btn.text = value
        self.dropdown.dismiss()

    def select_filemanager(self, instance):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.JPG *.JPEG")]
        )
        if file_path:
            self.selected_file = file_path
            self.image_preview.source = self.selected_file
            size = os.path.getsize(self.selected_file)
            mb = size / (1024*1024)
            kb = size / 1024
            self.original_size_label.text = f"File size: {mb:.2f} MB ({kb:.0f} KB)"

    def compress_image(self, instance):
        if not self.selected_file:
            self.show_popup("No file selected!")
            return

        try:
            val = int(self.target_input.text)
        except ValueError:
            self.show_popup("Enter a valid number between 1 and 1024")
            return

        if not (1 <= val <= 1024):
            self.show_popup("Number must be between 1 and 1024")
            return

        unit = self.unit_btn.text
        target_bytes = val * 1024 if unit == "KB" else val * 1024*1024
        orig_size = os.path.getsize(self.selected_file)

        if target_bytes > orig_size:
            self.show_popup("Warning: Target size is larger than original!")
            return

        src_path = self.selected_file
        folder = Path(src_path).parent
        name, ext = os.path.splitext(Path(src_path).name)
        output_file = folder / f"{name}_compressed({val}{unit}){ext}"

        def compress_to_jpg(input_image, output_image, target_size_bytes):
            img = PILImage.open(input_image)
            orig_width, _ = img.size
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW

            for q in range(1, 31):
                current_width = orig_width
                while current_width >= 300:
                    command = [
                        ffmpeg_path, "-y",
                        "-i", input_image,
                        "-vf", f"scale={current_width}:-1",
                        "-q:v", str(q),
                        str(output_image)
                    ]
                    subprocess.run(command,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL,
                                   creationflags=creation_flags)
                    size_bytes = os.path.getsize(output_image)
                    if size_bytes <= target_size_bytes:
                        return True, size_bytes
                    current_width = int(current_width*0.9)
            return False, None

        def run_compression():
            start = time.time()
            self.status_label.text = "Compressing... 0s"
            final_size_bytes = None

            def update_elapsed():
                while final_size_bytes is None:
                    elapsed = int(time.time() - start)
                    self.status_label.text = f"Compressing... {elapsed}s"
                    time.sleep(1)

            threading.Thread(target=update_elapsed, daemon=True).start()
            ok, final_size_bytes = compress_to_jpg(src_path, output_file, target_bytes)

            elapsed = int(time.time() - start)
            if ok:
                if unit == "KB":
                    display_size = final_size_bytes / 1024
                    self.status_label.text = f"Done in {elapsed}s.\nFinal size: {display_size:.0f} KB\nSaved: {output_file}"
                else:
                    display_size = final_size_bytes / (1024*1024)
                    self.status_label.text = f"Done in {elapsed}s.\nFinal size: {display_size:.2f} MB\nSaved: {output_file}"
            else:
                self.status_label.text = "Failed to compress within target size."

        threading.Thread(target=run_compression, daemon=True).start()

    def clear_fields(self, instance):
        self.selected_file = None
        self.image_preview.source = ""
        self.image_preview.texture = None
        self.original_size_label.text = "No image selected"
        self.target_input.text = ""
        self.unit_btn.text = "KB"
        self.status_label.text = "Status: Waiting for input..."

    def show_popup(self, msg):
        Popup(title="Notice", content=Label(text=msg), size_hint=(0.7, 0.3)).open()


class ImageCompressor(App):
    def build(self):
        Window.size = (600, 600)
        return CompressorUI()


if __name__ == "__main__":
    ImageCompressor().run()
