import os
import subprocess
import torch
import time
from ..func import get_video_files,set_file_name

class MergingVideoByPlenty:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video_path": ("STRING", {"default":"C:/Users/Desktop/",}),
                "output_path": ("STRING", {"default": "C:/Users/Desktop/output"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_complete_path",)
    FUNCTION = "merging_video_by_plenty"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    def merging_video_by_plenty(self, video_path, output_path):
        try:
            video_path = os.path.abspath(video_path).strip()
            output_path = os.path.abspath(output_path).strip()

            #判断output_path是否是一个目录
            if not os.path.isdir(video_path):
                raise ValueError("video_path："+video_path+"不是目录（video_path:"+video_path+" is not a directory）")
            if not os.path.isdir(output_path):
                raise ValueError("output_path："+output_path+"不是目录（output_path:"+output_path+" is not a directory）")
            
            video_files = get_video_files(video_path)

            if len(video_files) == 0:
                raise ValueError("video_path："+video_path+"目录下没有视频文件（No video files found in the video_path directory）")
            
            filelist_file_name = os.path.join(output_path,'filelist.txt')
            
            with open(filelist_file_name, 'w', encoding='utf-8') as f:
                for video in video_files:
                    escaped = video.replace("'", "'\\''")
                    f.write(f"file '{escaped}'\n")
            
            file_name = set_file_name(video_files[0])
            output_path = os.path.join(output_path, file_name)
            
            command = [
                'ffmpeg', '-f', 'concat','-safe','0','-i',filelist_file_name,
                '-c','copy',output_path,  # 输出视频路径
            ]
            
            # 执行命令并检查错误
            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
            # 检查返回码
            if result.returncode != 0:
                # 如果有错误，输出错误信息
                 print(f"Error: {result.stderr}")
                 raise ValueError(f"Error: {result.stderr}")
            else:
                # 输出标准输出信息
                print(result.stdout)

            return (output_path,)
        except Exception as e:
            raise ValueError(e)