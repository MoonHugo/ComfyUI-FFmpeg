<h1 align="center">ComfyUI-FFmpeg</h1>

<p align="center">
    <br> <font size=5>English | <a href="README.md">中文</a></font>
</p>


## Introduction

Encapsulate the commonly used functions of FFmpeg into ComfyUI nodes, making it convenient for users to perform various video processing tasks within ComfyUI.<br>

## Tips

You need to install FFmpeg before using this node, the FFmpeg installation method can refer to [here](https://www.bilibili.com/read/cv28108185/?spm_id_from=333.999.0.0&jump_opus=1)

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
**video_path**: The local video path, e.g.：`C:\Users\Desktop\222.mp4`<br>
**output_path**: The path to save the output images, e.g.：`C:\Users\Desktop\output`<br>
**frames_max_width**: This parameter can be used to resize the video. The default value is 0, which means the video will not be resized. If frames_max_width is larger than the actual width of the video, the video will not be enlarged and will retain its original width. If frames_max_width is smaller than the actual width of the video, the video will be scaled down.

___

##### Frames2Video Node: The function is to convert images into a video and save it to a specified directory.<br>
![](./assets/2.png)

###### Parameter Description
**frame_path**: local image path, e.g.:`C:\Users\Desktop\output`<br>
**fps**: video frame rate, default is`30`<br>
**video_name**: saved video name, e.g.:`222.mp4`<br>
**output_path**: video save path,e.g.:`C:\Users\Desktop\output`<br>
**audio_path**: video audio path,e.g.:`C:\Users\Desktop\222.mp3`<br>
___

##### AddTextWatermark Node: The function is to add a text watermark to the video.<br>

![](./assets/3.png)

###### Parameter Description
**video_path**: local video path,e.g.:`C:\Users\Desktop\222.mp4`<br>
**output_path**: video save path,e.g.:`C:\Users\Desktop\output`<br>
**font_file**: font file: The font file needs to be placed in the`custom_nodes\ComfyUI-FFmpeg\fonts` directory. Not only English fonts, but Chinese fonts can also be used.,e.g.:`ComfyUI\custom_nodes\ComfyUI-FFmpeg\fonts\Alibaba-PuHuiTi-Heavy.ttf`<br>
**font_size**: watermark text size,e.g.:`40`<br>
**font_color**: watermark text color,e.g.:`#FFFFFF` or `white`<br>
**position_x**: watermark text x-coordinate,e.g.:`100`<br>
**position_y**: watermark text y-coordinate,e.g.:`100`<br>

___

##### AddImgWatermark Node: The function is to add an image watermark to the video.<br>

![](./assets/4.png)

###### Parameter Description
**video_path**: local video path,e.g.:`C:\Users\Desktop\222.mp4`<br>
**output_path**: video save path,e.g.:`C:\Users\Desktop\output`<br>
**watermark_image**: watermark image path,e.g.:`C:\Users\Desktop\watermark.png`<br>
**watermark_img_width**: watermark image width,e.g.:`100`<br>
**position_x**: watermark image x-coordinate in the video,e.g.:`100`<br>
**position_y**: watermark image y-coordinate in the video,e.g.:`100`<br>
___

##### VideoFlip Node: The function is to flip the video<br>

![](./assets/5.png)

###### Parameter Description
**video_path**: local video path,e.g.:`C:\Users\Desktop\222.mp4`<br>
**output_path**: video save path,e.g.:`C:\Users\Desktop\output`<br>
**flip_type**: Flip type, e.g. `horizontal` horizontal flip, `vertical` vertical flip, `both` horizontal plus vertical flip<br>

___

##### ExtractAudio Node：The purpose is to extract the audio from the video<br>

![](./assets/6.png)

###### Parameter Description
**video_path**: local video path,e.g.:`C:\Users\Desktop\222.mp4`<br>
**output_path**: audio save path,e.g.:`C:\Users\Desktop\output`<br>
**audio_format**: Save audio formats, including **.m4a** , **.mp3** , **.wav** , **.aac** , **.flac** , **.wma** , **.ogg** , **.ac3** , **.amr** , **.aiff** , **.opus** , **.m4b** , **.caf** , **.dts** etc. <br>

___

##### MergingVideoByTwo Node: The purpose is to merge two videos, for example, to combine two one-hour videos into a single two-hour video.<br>

![](./assets/7.png)

###### Parameter Description
**video1_path**: local video path,e.g.:`C:\Users\Desktop\111.mp4`<br>
**video2_path**: local video path,e.g.:`C:\Users\Desktop\222.mp4`<br>
**device**: There are two options: CPU and GPU,if you encounter an error while merging two videos using the CPU option, you can try using the GPU instead.<br>
**resolution_reference**: What is the size of the merged video? You can refer to either the first video or the second video, that is, video1 or video2.<br>
**output_path**: video save path,e.g.:`C:\Users\Desktop\output`<br>

___

##### MergingVideoByPlenty Node: The purpose is to merge multiple short videos that have the same encoding format, resolution, and frame rate into a longer video.<br>

![](./assets/11.png)

###### Parameter Description
**video_path**: local video path,e.g.:`C:\Users\Desktop\111`,All videos in the specified path must have the same encoding format, frame rate, and resolution.<br>
**output_path**: video save path,e.g.:`C:\Users\Desktop\output`<br>

___

##### StitchingVideo Node: The purpose is to stitching two videos, which can be done in two ways: horizontal stitching and vertical stitching.<br>

![](./assets/8.png)

###### Parameter Description
**video1_path**: local video path,e.g.:`C:\Users\Desktop\111.mp4`<br>
**video2_path**: local video path,e.g.:`C:\Users\Desktop\222.mp4`<br>
**device**: There are two options: CPU and GPU, if you encounter an error while stitching two videos using the CPU, you can try using the GPU instead.<br>
**use_audio**: Which audio will be used in the stitched video? You can choose the audio from either the first video or the second video, that is, from video1 or video2.<br>
**stitching_type**: The methods for stitching videos are divided into two types: horizontal stitching and vertical stitching.<br>
**output_path**: video save path,e.g.:`C:\Users\Desktop\output`<br>

___

##### MultiCuttingVideo Node: The purpose is to split one video into several smaller videos.<br>

![](./assets/9.png)

###### Parameter Description
**video_path**: local video path,e.g.:`C:\Users\Desktop\111.mp4`<br>
**output_path**: video save path,e.g.:`C:\Users\Desktop\output`<br>
**segment_time**: The length of each cut video is measured in seconds. It’s important to note that the video is cut based on keyframes, so the duration cannot be too short. Since there is no guarantee that each segment of the video will have a keyframe, the duration of each segment may not be the same, but it will be the closest possible.<br>

___

##### SingleCuttingVideo Node: The purpose is to cut a specific time segment from a designated video.<br>

![](./assets/10.png)

###### Parameter Description
**video_path**: local video path,e.g.:`C:\Users\Desktop\111.mp4`<br>
**output_path**: video save path,e.g.:`C:\Users\Desktop\output`<br>
**start_time**: Set the start time for the cut; for example, setting it to 00:00:10 means cutting from the 10th second of the video.<br>
**end_time**: Set the end time for the cut; for example, setting it to 00:05:00 means cutting until the 5th minute of the video.<br>

## Social Account Homepage
- Bilibili：[My BILIBILI Homepage](https://space.bilibili.com/1303099255)

## Acknowledgments

Thanks to all the contributors of the FFmpeg repository. [FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg)

## Star history

[![Star History Chart](https://api.star-history.com/svg?repos=MoonHugo/ComfyUI-FFmpeg&type=Date)](https://star-history.com/#MoonHugo/ComfyUI-FFmpeg&Date)