import os
import subprocess
from ..func import video_type

class MultiCuttingVideo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video_path": ("STRING", {"default":"C:/Users/Desktop/video.mp4",}),
                "output_path": ("STRING", {"default":"C:/Users/Desktop/output",}),
                "segment_time": ("INT",{"default":10,"min":1,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_complete_path",)
    FUNCTION = "multi_cutting_video"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    # 视频切割,根据关键帧切割，所以时间不能太短，不能保证每一段视频都有关键帧，所以每一段时长不一定是segment_time，只是最接近的
    def multi_cutting_video(self, video_path, output_path,segment_time):
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
            
            file_full_name = os.path.basename(video_path)
            file_name = os.path.splitext(file_full_name)[0]
            file_extension = os.path.splitext(file_full_name)[1]
            
            #ffmpeg -i input.mp4 -f segment -segment_time 30 -c copy output%03d.mp4
            
            command = [
                'ffmpeg', '-i', video_path,  # 输入视频路径
                '-f', 'segment','-reset_timestamps','1',"-segment_time",str(segment_time),  # 使用scale滤镜缩放帧
                '-c','copy',output_path+os.sep+file_name+"_%08d"+file_extension,  # 输出视频路径
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