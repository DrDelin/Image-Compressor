#VERSION 2.0
#BUILD FILE / SOURCE CODE
#DEVELOPED BY DR.DELIN
#REQUIRE FFMPEG.EXE TO RUN, NEWER THE VERSION - BETTER

import subprocess,os,sys,time,threading
import tkinter as tk
from tkinter import filedialog , messagebox , ttk
from pathlib import Path
from PIL import Image  

#FFMPEG Binary Management:
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):  # PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

ffmpeg_path = resource_path("ffmpeg.exe")

###USER INPUT GUI
def get_user_input():
    def on_enter():
        nonlocal user_input, dropdown_choice
        text = entry.get()

        try:
            value = int(text)
            if 1 <= value <= 1024:
                user_input = value
                dropdown_choice = dropdown_var.get()
                root.destroy()
            else:
                messagebox.showerror("Invalid Input", "Please enter the output size between 1 and 1024.")
                entry.focus_set()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number between 1 and 1024.")
            entry.focus_set()

    def on_cancel():
        nonlocal user_input, dropdown_choice
        user_input = None
        dropdown_choice = None
        root.destroy()

    root = tk.Tk()
    root.title("Image Compressor Ver_2.0")

    root.attributes('-topmost', True)
    root.focus_force()

    frame = tk.Frame(root)
    frame.pack(pady=10)

    label = tk.Label(frame, text="Desired Compressed Image File Size: ")
    label.pack(side=tk.LEFT, padx=5)

    entry = tk.Entry(frame, width=20)
    entry.pack(side=tk.LEFT, padx=5)

    dropdown_var = tk.StringVar()
    dropdown = ttk.Combobox(frame, textvariable=dropdown_var, values=["KB", "MB"], state="readonly")
    dropdown.current(0)
    dropdown.pack(side=tk.LEFT, padx=5)

    small_label = tk.Label(root, text="Allowed Output size (1 - 1024)(Number only) ", font=("TkDefaultFont", 8))
    small_label.pack()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    enter_btn = tk.Button(button_frame, text="Enter", command=on_enter)
    enter_btn.pack(side=tk.LEFT, padx=10)

    cancel_btn = tk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_btn.pack(side=tk.LEFT, padx=10)

    user_input, dropdown_choice = None, None

    root.mainloop()
    return user_input, dropdown_choice


if __name__ == "__main__":
    number, option = get_user_input()
    if number is not None:
        if option == "MB":
            target_size = int(number)*int(1024)
        else:
            target_size = int(number)
    else:
        input("User cancelled the program!!")
        exit()


#Source and Output Directory:
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)
inp_path = filedialog.askopenfilename(title="Select a file")
src_path = Path(inp_path)

#Size Comparision:
source_size = os.path.getsize(src_path) / 1024
if target_size > source_size:
    input("Compression Image file size entered is bigger than Original Image size!\n\nCompression Failed! Try again with lesser value!!\n")
    exit()

dir_name, base_name = os.path.split(src_path)
name, ext = os.path.splitext(base_name)
output_file = os.path.join(dir_name, f"{name}_compressed({str(number)+option}){ext}")
out_file = os.path.basename(output_file)

def compress_to_jpg(input_image, output_image, target_size_kb=target_size):
    img = Image.open(input_image)
    orig_width, _ = img.size

    for q in range(1, 31):
        current_width = orig_width

        while current_width >= 300: #Minimum Resolution Possible
            command = [
                ffmpeg_path, "-y",
                "-i", input_image,
                "-vf", f"scale={current_width}:-1",
                "-q:v", str(q),
                output_image
            ]
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Check output file size
            size_kb = os.path.getsize(output_image) // 1024
            if size_kb <= target_size_kb:
                print(f"\n\nSuccess!! Final Size: {size_kb} KB, Width= {current_width}, Quality= {q}\n")
                return

            # Reduce resolution by 10% each step
            current_width = int(current_width * 0.9)

    print("Could not compress below target size within limits.")

def show_elapsed(start,message):
    while not done:
        elapsed = int(time.time()-start)
        print(f"\r{message} (Time Elapsed: {elapsed} seconds)", end="")
        time.sleep(1)

if __name__ == "__main__":
    done = False
    start = time.time()
    t = threading.Thread(target=show_elapsed,args=(start,"Compressing the Image..."))
    t.start()
    compress_to_jpg(src_path,output_file)
    done= True
    t.join()
    input(f"\rImage Compression Done in {int(time.time()-start)} seconds.\n\nCompressed Image ('{out_file}') stored on the same location of the original image.\n\nClick ENTER to Exit the program!!")