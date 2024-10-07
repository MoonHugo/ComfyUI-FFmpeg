<h1 align="center">ComfyUI-FFmpeg</h1>

<p align="center">
    <br> <font size=5>English | <a href="README.md">中文</a></font>
</p>


## Introduction

Encapsulate the commonly used functions of FFmpeg into ComfyUI nodes, making it convenient for users to perform various video processing tasks within ComfyUI.<br>

## Installation 

#### Method 1:

1. Go to comfyUI custom_nodes folder, `ComfyUI/custom_nodes/`
2. `git clone https://github.com/MoonHugo/ComfyUI-FFmpeg.git`
3. `cd ComfyUI-FFmpeg`
4. `pip install -r requirements.txt`
5. restart ComfyUI

#### Method 2:
Directly download the node source package, then extract it into the custom_nodes directory, and finally restart ComfyUI.

#### Method 3：
Install through ComfyUI-Manager by searching for 'ComfyUI-BiRefNet-Hugo' and installing it.

## Nodes introduction

##### Video2Frames Node: The function is to convert a video into images and save them to a specified directory.<br>

![](./assets/1.png)

###### Parameter Description
**video_path**: The local video path, e.g：`C:\Users\Desktop\222.mp4`<br>
**output_path**: The path to save the output images, e.g：`C:\Users\Desktop\output`<br>
**frames_max_width**: This parameter can be used to resize the video. The default value is 0, which means the video will not be resized. If frames_max_width is larger than the actual width of the video, the video will not be enlarged and will retain its original width. If frames_max_width is smaller than the actual width of the video, the video will be scaled down.

___

##### Frames2Video Node: The function is to convert images into a video and save it to a specified directory.<br>
![](./assets/2.png)

###### Parameter Description
**frame_path**: local image path, e.g:`C:\Users\Desktop\output`<br>
**fps**: video frame rate, default is`30`<br>
**video_name**: saved video name, e.g:`222.mp4`<br>
**output_path**: video save path,e.g:`C:\Users\Desktop\output`<br>
**audio_path**: video audio path,e.g:`C:\Users\Desktop\222.mp3`<br>
___

##### AddTextWatermark Node: The function is to add a text watermark to the video.<br>

![](./assets/3.png)

###### Parameter Description
**video_path**: local video path,e.g:`C:\Users\Desktop\222.mp4`<br>
**output_path**: video save path,e.g:`C:\Users\Desktop\output`<br>
**font_file**: font file: The font file needs to be placed in the`custom_nodes\ComfyUI-FFmpeg\fonts` directory. Not only English fonts, but Chinese fonts can also be used.,e.g:`ComfyUI\custom_nodes\ComfyUI-FFmpeg\fonts\Alibaba-PuHuiTi-Heavy.ttf`<br>
**font_size**: watermark text size,e.g:`40`<br>
**font_color**: watermark text color,e.g:`#FFFFFF` or `white`<br>
**position_x**: watermark text x-coordinate,e.g:`100`<br>
**position_y**: watermark text y-coordinate,e.g:`100`<br>

___

##### AddImgWatermark Node: The function is to add an image watermark to the video.<br>

![](./assets/4.png)

###### Parameter Description
**video_path**: local video path,e.g:`C:\Users\Desktop\222.mp4`<br>
**output_path**: video save path,e.g:`C:\Users\Desktop\output`<br>
**watermark_image**: watermark image path,e.g:`C:\Users\Desktop\watermark.png`<br>
**watermark_img_width**: watermark image width,e.g:`100`<br>
**position_x**: watermark image x-coordinate in the video,e.g:`100`<br>
**position_y**: watermark image y-coordinate in the video,e.g:`100`<br>
___

## Social Account Homepage
- Bilibili：[My BILIBILI Homepage](https://space.bilibili.com/1303099255)

## Acknowledgments

Thanks to all the contributors of the FFmpeg repository. [FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg)

Some of the code references [Eden-yidun/ComfyUI-EdenVideoTool](https://github.com/Eden-yidun/ComfyUI-EdenVideoTool) Thanks!

## Star history

[![Star History Chart](https://api.star-history.com/svg?repos=MoonHugo/ComfyUI-FFmpeg&type=Date)](https://star-history.com/#MoonHugo/ComfyUI-FFmpeg&Date)