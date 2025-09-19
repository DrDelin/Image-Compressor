#VERSION 1.0
#BUILD FILE / SOURCE CODE
#DEVELOPED BY DR.DELIN
#REQUIRE FFMPEG.EXE TO RUN, NEWER THE VERSION - BETTER

import subprocess,os,sys,time,threading
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from PIL import Image  

print("Image Compressor Version: 1.0\n")

#FFMPEG Binary Management:
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):  # PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

ffmpeg_path = resource_path("ffmpeg.exe")

#Final Image Size
target_size = int(input("Output file size target(in KBs): "))

#Source and Output Directory:
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)
inp_path = filedialog.askopenfilename(title="Select a file")
src_path = Path(inp_path)
dir_name, base_name = os.path.split(src_path)
name, ext = os.path.splitext(base_name)
output_file = os.path.join(dir_name, f"{name}_compress({target_size}){ext}")
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
    print("\n")
    done = False
    start = time.time()
    t = threading.Thread(target=show_elapsed,args=(start,"Compressing the Image..."))
    t.start()
    compress_to_jpg(src_path,output_file)
    done= True
    t.join()
    input(f"\rImage Compression Done in {int(time.time()-start)} seconds.\n\nCompressed Image ('{out_file}') stored on the same location of the original image.\nClick ENTER to Exit the program!!")