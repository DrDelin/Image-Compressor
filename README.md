# IMAGE COMPRESSOR (Windows Only)
  ### History for developement of this program:
  As nowadays all exam applications, government services, banking etc.. went online, it requires our image file as profile picture for account creation, for exam or government services application stuff.  But limitation is most of our modern phone take picture >5 MB in size. But these applications require image <200 KB, some even lesser. Everytime it takes time to compress the image, meanwhile compressing, have to crop or to compromise the quality of image to achieve the size. Uploading the image to internet-based image compressor have its own risks. So i decided to create a small project using ffmpeg and somewhat minimal knowledge in python scripting, to developed this program, which compress the file to required size (in KBs / MBs) while maintaining the original quality as much as possible. As it is successful, i'm hoping this program will help others who are facing same issue like me. So I shared the program for all.
  ### Developer
  Owner and Developer: Dr.Delin

## Download:
  * Direct Download Link: https://github.com/DrDelin/Image-Compressor/releases/download/v.3.0/Image.Compressor.v3.0.exe (RECOMMENDED)
  * Direct Download Link: https://github.com/DrDelin/Image-Compressor/releases/download/v.2.0/Image.Compressor.V2.0.exe  (LITE VERSION)
  * For current and Old releases: https://github.com/DrDelin/Image-Compressor/releases
    
## Usage:
   1. Run the "Image_compressor Ver x.x.exe" file.
   2. Select the image file to compress.
   3. Make sure the image is correct.
   4. Type the size you want to compress (1 - 1024)(only Numbers).
   5. Select KB/MB (KB by default).
   6. Program will compress to the desired size.
   7. Compressed image will stored at the site of original image.
   8. Exit the program.
  
## TOOLS USED:
   1. Scripting: Python
   2. GUI: Kivy & TKinter library
   3. Image Compressor: FFMPEG.exe
   4. EXE Builder: pyinstaller
