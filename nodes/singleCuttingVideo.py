import os
import subprocess
from datetime import datetime
from ..func import video_type,set_file_name,validate_time_format

class SingleCuttingVideo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video_path": ("STRING", {"default":"C:/Users/Desktop/video.mp4",}),
                "output_path": ("STRING", {"default":"C:/Users/Desktop/output",}),
                "start_time": ("STRING", {"default":"00:00:00",}),
                "end_time": ("STRING", {"default":"00:00:10",}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("cutting_video_single",)
    FUNCTION = "single_cutting_video"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    # 视频切割,根据关键帧切割，所以时间不能太短，不能保证每一段视频都有关键帧，所以每一段时长不一定是segment_time，只是最接近的
    def single_cutting_video(self, video_path, output_path,start_time,end_time):
        try:
            video_path = os.path.abspath(video_path).strip()
            output_path = os.path.abspath(output_path).strip()
             # 视频不存在
            if not video_path.lower().endswith(video_type()):
                raise ValueError("video_path："+video_path+"不是视频文件（video_path:"+video_path+" is not a video file）")
            if not os.path.isfile(video_path):
                raise ValueError("video_path："+video_path+"不存在（video_path:"+video_path+" does not exist）")
            
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path："+output_path+"不是目录（output_path:"+output_path+" is not a directory）")
            
            if not validate_time_format(start_time) or not validate_time_format(end_time):
                raise ValueError("start_time或者end_time时间格式不对（start_time or end_time is not in time format）")
            
            time_format = "%H:%M:%S"
            start_dt = datetime.strptime(start_time, time_format)
            end_dt = datetime.strptime(end_time, time_format)
            
            if start_dt >= end_dt:
                raise ValueError("start_time必须小于end_time（start_time must be less than end_time）")
            
            file_name = set_file_name(video_path)
            output_path = os.path.join(output_path, file_name)
            #ffmpeg -i input.mp4 -ss START_TIME -to END_TIME -c copy output.mp4
            command = [
                'ffmpeg', '-i', video_path,  # 输入视频路径
                '-ss', start_time,'-to', end_time,
                '-c','copy',output_path
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