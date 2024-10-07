import os
import subprocess
import re
from PIL import Image
from pathlib import Path

class Frames2Video:
 
    # 初始化方法
    def __init__(self): 
        pass 
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "frame_path": ("STRING", {"default": "C:/Users/Desktop",}), 
                "fps": ("FLOAT", {
                    "default": 30, 
                    "min": 1,
                    "max": 120,
                    "step": 1,
                    "display": "number"
                }),
                "video_name": ("STRING", {"default": "new_video"}),
                "output_path": ("STRING", {"default": "./output"}),
            },
            "optional":{
                "audio_path":("STRING",{"default": "C:/Users/audio.mp3",}),
                }
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("frame_path","output_path",)
    FUNCTION = "frames2video" 
    OUTPUT_NODE = True
    CATEGORY = "FFmpeg" 

    def frames2video(self,frame_path,fps,video_name,output_path,audio_path=None):
        try:
            if not os.path.exists(frame_path):
                raise ValueError("frame_path不存在（frame_path does not exist）")
            
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path不是目录（output_path is not a directory）")
            output_path =  f"{output_path}\{video_name}.mp4" # 将输出目录和输出文件名合并为一个输出路径
            # 获取输入目录中的所有图像文件
            frame_path = Path(frame_path)
            image_files = sorted(frame_path.glob('*.png')) + sorted(frame_path.glob('*.PNG')) + sorted(frame_path.glob('*.Png'))
            
            # 获取第一张图像的文件名,不要路径
            image_name = os.path.basename(image_files[0])
            print(f"第一张图像文件名: {image_name}")

            # 获取图像文件名中的数字个数，包括零
            num_digits = sum(c.isdigit() for c in image_name)
            print(f"转换后的图像文件名: {num_digits}")

            # 将图像文件名中的数字替换为%0{num_digits}d，只影响数字，不影响其他字符
            image_name = re.sub(r'\d+', '%0{}d'.format(num_digits), image_name)
            print(f"转换后的图像文件名: {image_name}")

            # 构建输出目录
            if not image_files:
                print(f"Files in directory: {os.listdir(frame_path)}")
                raise FileNotFoundError(f"No image files found in directory: {frame_path}")

            # 获取第一张图像的尺寸
            with Image.open(image_files[0]) as img:
                width, height = img.size
                scale = f'{width}:{height}'

            if audio_path:
                # 有音频文件，构建ffmpeg命令
                ffmpeg_cmd = [
                    'ffmpeg',
                    '-framerate', str(fps),
                    '-i', f'{frame_path}/{image_name}',
                    '-i', audio_path,  # 添加音频文件路径
                    '-vf', f'scale={scale}',
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '28',
                    '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac',  # 指定音频编解码器
                    '-shortest',  
                    '-y',
                    str(output_path)
                ]
                # 执行ffmpeg命令
                process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    print(f"ffmpeg 执行失败，错误信息: {stderr.decode('utf-8')}")
                else:
                    print(f"视频合成成功: {output_path}")

            else:
                # 无音频文件，构建ffmpeg命令
                ffmpeg_cmd = [
                    'ffmpeg',
                    '-framerate', str(fps),
                    '-i', f'{frame_path}/{image_name}',
                    '-vf', f'scale={scale}',
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '28',
                    '-pix_fmt', 'yuv420p',
                    '-y',
                    str(output_path)
                ]
                # 执行ffmpeg命令
                process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    print(f"ffmpeg 执行失败，错误信息: {stderr.decode('utf-8')}")
                else:
                    print(f"视频合成成功: {output_path}")
            frame_path = str(frame_path) # 输出路径为字符串
            return (frame_path,output_path)
        except Exception as e:
            raise ValueError(e)