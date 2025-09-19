# IMAGE COMPRESSOR
  ### History for developement of this program:
      Hi all! As nowadays all exam applications, government services, banking went online, it requires our image file for account creation or application stuff.  But limitation is most of our modern phone take picture >5 MB in size.  But these applications require image <150KB. Everytime it takes time to compress the image. And meanwhile compressing, have to crop or compromise the quality of image to achieve the size.  Uploading the image to internet-based image compressor have its own risks.  So i decided to create a small project using ffmpeg and somewhat minimal knowledge in python scripting, to developed this program, which compress the file to required size (in KBs) while maintaining the original quality as much as possible.  As it is successful, i'm hoping this program will help others who are facing same issue like me. So I shared the program for all.
  
  ### Developer
  Owner and Developer: Dr.Delin

## Usage:
   1. Run the "Image_compressor.exe" file.
   2. Type the size you want to compress (1 - 1024)(in KBs).
   3. Select the desired image to compress.
   4. Program will compress to the desired size.
   5. Compressed image will stored at the site of original image.
   6. Exit the program.
  
## TOOLS USED:
   1. Scripting: Python
   2. Compressor: FFMPEG.exe
   3. EXE Builder: pyinstaller