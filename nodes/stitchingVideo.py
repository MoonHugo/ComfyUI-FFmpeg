import os
import subprocess
from ..func import has_audio,getVideoInfo,set_file_name,video_type
import torch
import math

device = "cuda" if torch.cuda.is_available() else "cpu"

class StitchingVideo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video1_path": ("STRING", {"default":"C:/Users/Desktop/video1.mp4",}),
                "video2_path": ("STRING", {"default":"C:/Users/Desktop/video2.mp4",}),
                "device": (["cpu","cuda"], {"default":device,}),
                "use_audio": (["video1","video2"], {"default":"video1",}),
                "stitching_type":(["horizontal","vertical"], {"default":"horizontal",}),
                "output_path": ("STRING", {"default": "C:/Users/Desktop/output"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_complete_path",)
    FUNCTION = "stitching_video"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    def stitching_video(self, video1_path, video2_path,device,use_audio,stitching_type,output_path):
        try:
            video1_path = os.path.abspath(video1_path).strip()
            video2_path = os.path.abspath(video2_path).strip()
            output_path = os.path.abspath(output_path).strip()
             # 视频不存在
            if not video1_path.lower().endswith(video_type()):
                raise ValueError("video1_path："+video1_path+"不是视频文件（video1_path:"+video1_path+" is not a video file）")
            if not os.path.isfile(video1_path):
                raise ValueError("video1_path："+video1_path+"不存在（video1_path:"+video1_path+" does not exist）")
            
            if not video2_path.lower().endswith(video_type()):
                raise ValueError("video2_path："+video2_path+"不是视频文件（video2_path:"+video2_path+" is not a video file）")
            if not os.path.isfile(video2_path):
                raise ValueError("video2_path："+video2_path+"不存在（video2_path:"+video2_path+" does not exist）")
            
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path："+output_path+"不是目录（output_path:"+output_path+" is not a directory）")
            
            video1_audio = has_audio(video1_path)
            video2_audio = has_audio(video2_path)
            
            final_output = set_file_name(video1_path)
            #文件名根据年月日时分秒来命名
            output_path = os.path.join(output_path, final_output)
            
            use_cuvid = ""
            use_encoder = "-c:v libx264" #默认用CPU编码

            if device == "cuda":
                use_cuvid = "-hwaccel cuda"
                use_encoder = "-c:v h264_nvenc"
            
            video_info = getVideoInfo(video1_path)
            
            # libx264、libx265等编码器要求宽高必须是2的倍数，如果报错，可以把device换为GPU
            width =  math.ceil(video_info['width']/2)*2
            height = math.ceil(video_info['height']/2)*2
            
            use_audio = {
                'video1': '0',
                'video2': '1',
            }.get(use_audio, '0')
            
            tack_type = {
                'horizontal': 'hstack',
                'vertical': 'vstack',
            }.get(stitching_type, 'hstack')
            
            scale = {
                'horizontal':f'-1:{height}',
                'vertical':  f'{width}:-1',
            }.get(stitching_type, f'{width}:-1')
            
           
            if video1_audio or video2_audio:
                #-map 1:a 指定使用第二个视频的音频流
                command = f'ffmpeg {use_cuvid} -i {video1_path} -i {video2_path} -filter_complex "[1:v]scale={scale}[vid2];[0:v][vid2]{tack_type}=inputs=2[v]" -map "[v]" -map {use_audio}:a? {use_encoder} -c:a aac -strict experimental {output_path}'
            else:
                command = f'ffmpeg {use_cuvid} -i {video1_path} -i {video2_path} -filter_complex "[1:v]scale={scale}[vid2];[0:v][vid2]{tack_type}=inputs=2[v]" -map "[v]" {use_encoder}  {output_path}'
            
            # 执行命令并检查错误
            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # 检查返回码
            if result.returncode != 0:
                # 如果有错误，输出错误信息
                 print(f"Error: {result.stderr.decode('utf-8')}")
                 raise ValueError(f"Error: {result.stderr.decode('utf-8')}")
            else:
                # 输出标准输出信息
                print(result.stdout)

            return (output_path,)
        except Exception as e:
            raise ValueError(e)