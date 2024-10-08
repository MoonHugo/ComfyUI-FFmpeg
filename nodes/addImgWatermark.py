import os
from PIL import Image
import subprocess
import time
from ..func import get_image_size


class AddImgWatermark:
 
    # 初始化方法
    def __init__(self): 
        pass 
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "video_path": ("STRING", {"default":"C:/Users/Desktop/video.mp4",}),
                "output_path": ("STRING", {"default":"C:/Users/Desktop/output/",}),
                "watermark_image": ("STRING", {"default":"C:/Users/Desktop/logo.png",}),
                "watermark_img_width":  ("INT", {"default": 100,"min": 1, "step": 1}),
                "position_x":  ("INT", {"default": 10, "step": 1}),
                "position_y":  ("INT", {"default": 10, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_complete_path",)
    FUNCTION = "add_img_watermark" 
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg" 

    def add_img_watermark(self,video_path,output_path,watermark_image,watermark_img_width,position_x,position_y):
        try:
            
            video_path = os.path.abspath(video_path).strip()
            output_path = os.path.abspath(output_path).strip()
            # 视频不存在
            if not video_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv','.rmvb')):
                raise ValueError("video_path："+video_path+"不是视频文件（video_path:"+video_path+" is not a video file）")
            
            if not os.path.exists(video_path):
                raise ValueError("video_path："+video_path+"不存在（video_path:"+video_path+" does not exist）")
            
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path："+output_path+"不是目录（output_path:"+output_path+" is not a directory）")
            
            # 文件不是图片
            if not watermark_image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                raise ValueError("watermark_image不是图片文件（watermark file is not a image file）")
            
            if not os.path.exists(watermark_image):
                raise ValueError("watermark_image："+watermark_image+"不存在（watermark_image :"+watermark_image+" does not exist）")
            
            file_name = os.path.basename(video_path)
            file_extension = os.path.splitext(file_name)[1]
            #文件名根据年月日时分秒来命名
            file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + file_extension
            output_path = os.path.join(output_path, file_name)
            width,height = get_image_size(watermark_image)
            watermark_img_height = int(height * watermark_img_width / width)  # 按比例计算新高度
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', watermark_image,
                '-filter_complex',f"[1:v]scale={watermark_img_width}:{watermark_img_height}[wm];[0:v][wm]overlay=x={position_x}:y={position_y}:format=auto",
                output_path,
            ]
            result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            #os.remove(image_save_path) # 删除临时水印图片
            # 检查返回码
            if result.returncode != 0:
                # 如果有错误，输出错误信息
                 print(f"Error: {result.stderr.decode('utf-8')}")
                 raise ValueError(f"Error: {result.stderr.decode('utf-8')}")
            else:
                # 输出标准输出信息
                print(result.stdout)
        except Exception as e:
            raise ValueError(e)
        return (output_path,)