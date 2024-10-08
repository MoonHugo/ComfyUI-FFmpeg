import os
import time
import subprocess

class VideoFlip:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video_path": ("STRING", {"default":"C:/Users/Desktop/video.mp4",}),
                "output_path": ("STRING", {"default":"C:/Users/Desktop/output",}),
                "flip_type": (["horizontal","vertical","both"], {"default":"horizontal",}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_complete_path",)
    FUNCTION = "video_flip"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    def video_flip(self, video_path, output_path, flip_type):
        try:
            video_path = os.path.abspath(video_path).strip()
            output_path = os.path.abspath(output_path).strip()
             # 视频不存在
            if not video_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv','.rmvb')):
                raise ValueError("video_path："+video_path+"不是视频文件（video_path:"+video_path+" is not a video file）")
            if not os.path.isfile(video_path):
                raise ValueError("video_path："+video_path+"不存在（video_path:"+video_path+" does not exist）")
            
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path："+output_path+"不是目录（output_path:"+output_path+" is not a directory）")
            file_name = os.path.basename(video_path)
            file_extension = os.path.splitext(file_name)[1]
            #文件名根据年月日时分秒来命名
            file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + file_extension
            output_path = os.path.join(output_path, file_name)
            flip = {
                'horizontal': 'hflip',
                'vertical': 'vflip',
                'both': 'hflip,vflip',
            }.get(flip_type, 'horizontal')  # 默认为水平翻转

            command = [
                'ffmpeg', '-i', video_path,  # 输入视频路径
                '-vf', flip,  # 使用scale滤镜缩放帧
                output_path,
            ]
            
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