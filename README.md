<h1 align="center">ComfyUI-FFmpeg</h1>

<p align="center">
    <br> <font size=5>中文 | <a href="README_EN.md">English</a></font>
</p>


## 介绍

把FFmpeg常用功能封装成ComfyUI节点，方便用户可以在ComfyUI上也可以进行各种视频处理。<br>

## 安装 

#### 方法1:

1. 进入节点目录, `ComfyUI/custom_nodes/`
2. `git clone https://github.com/MoonHugo/ComfyUI-FFmpeg.git`
3. `cd ComfyUI-FFmpeg`
4. `pip install -r requirements.txt`
5. 重启ComfyUI

#### 方法2:
直接下载节点源码包，然后解压到custom_nodes目录下，最后重启ComfyUI

#### 方法3：
通过ComfyUI-Manager安装，搜索“ComfyUI-FFmpeg”进行安装

## 节点介绍

##### Video2Frames节点: 作用是将视频转为一张一张的图片，并保存到指定目录中<br>

![](./assets/1.png)

###### 参数说明
**video_path**: 本地视频路径，比如：`C:\Users\Desktop\222.mp4`<br>
**output_path**: 输出图片保存路径，比如：`C:\Users\Desktop\output`<br>
**frames_max_width**: 这个参数可以用来缩放视频，默认为0，表示不缩放视频，如果frames_max_width大于视频实际宽度，则视频不会被放大，保持原宽度，如果frames_max_width小于视频实际宽度，则视频会被缩小。

___

##### Frames2Video节点: 作用是将图片转为视频，并保存到指定目录中<br>
![](./assets/2.png)

###### 参数说明
**frame_path**: 本地图片路径，比如：`C:\Users\Desktop\output`<br>
**fps**: 视频帧率，默认为`30`<br>
**video_name**: 保存视频名称，比如：`222.mp4`<br>
**output_path**: 视频保存路径，比如：`C:\Users\Desktop\output`<br>
**audio_path**: 视频音频路径，比如：`C:\Users\Desktop\222.mp3`<br>
___

##### AddTextWatermark节点: 作用是在视频上添加文字水印<br>

![](./assets/3.png)

###### 参数说明
**video_path**: 本地视频路径，比如：`C:\Users\Desktop\222.mp4`<br>
**output_path**: 视频保存路径，比如：`C:\Users\Desktop\output`<br>
**font_file**: 字体文件，需要把字体文件放到`custom_nodes\ComfyUI-FFmpeg\fonts`目录下，不仅英文字体，中文字体也可以，比如：`ComfyUI\custom_nodes\ComfyUI-FFmpeg\fonts\Alibaba-PuHuiTi-Heavy.ttf`<br>
**font_size**: 水印文字大小，比如：`40`<br>
**font_color**: 水印文字颜色，比如：`#FFFFFF`或者`white`<br>
**position_x**: 水印文字x坐标，比如：`100`<br>
**position_y**: 水印文字y坐标，比如：`100`<br>

___

##### AddImgWatermark节点: 作用是在视频上添加图片水印<br>

![](./assets/4.png)

###### 参数说明
**video_path**: 本地视频路径，比如：`C:\Users\Desktop\222.mp4`<br>
**output_path**: 视频保存路径，比如：`C:\Users\Desktop\output`<br>
**watermark_image**: 水印图片路径，比如：`C:\Users\Desktop\watermark.png`<br>
**watermark_img_width**: 水印图片宽度，比如：`100`<br>
**position_x**: 水印图片在视频中的x坐标，比如：`100`<br>
**position_y**: 水印图片在视频中的y坐标，比如：`100`<br>
___

## 社交账号
- Bilibili：[我的B站主页](https://space.bilibili.com/1303099255)

## 感谢

感谢FFmpeg仓库的所有作者 [FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg)

部分代码参考了 [Eden-yidun/ComfyUI-EdenVideoTool](https://github.com/Eden-yidun/ComfyUI-EdenVideoTool) 感谢！

## 关注历史

[![Star History Chart](https://api.star-history.com/svg?repos=MoonHugo/ComfyUI-FFmpeg&type=Date)](https://star-history.com/#MoonHugo/ComfyUI-FFmpeg&Date)