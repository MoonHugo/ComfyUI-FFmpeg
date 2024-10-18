import os
import subprocess
from ..func import set_file_name,video_type,audio_type,has_audio

class AddAudio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video_path": ("STRING", {"default":"C:/Users/Desktop/video.mp4",}),
                "audio_from":(["audio_file","video_file"], {"default":"audio_file",}),
                "file_path": ("STRING", {"default":"C:/Users/Desktop/output",}),
                'delay_play':("INT",{"default":0,"min":0,}),
                "output_path": ("STRING", {"default":"C:/Users/Desktop/output/",}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_complete_path",)
    FUNCTION = "add_audio"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    def add_audio(self, video_path, audio_from, file_path,delay_play,output_path):
        try:
            video_path = os.path.abspath(video_path).strip()
            file_path = os.path.abspath(file_path).strip()
            output_path = os.path.abspath(output_path).strip()
             # 视频不存在
            if not video_path.lower().endswith(video_type()):
                raise ValueError("video_path："+video_path+"不是视频文件（video_path:"+video_path+" is not a video file）")
            if not os.path.isfile(video_path):
                raise ValueError("video_path："+video_path+"不存在（video_path:"+video_path+" does not exist）")
            
            if not os.path.isfile(file_path):
                raise ValueError("file_path："+file_path+"不存在（file_path:"+file_path+" does not exist）")
            
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path："+output_path+"不是目录（output_path:"+output_path+" is not a directory）")
            
            if audio_from == "video_file":
                if not file_path.lower().endswith(video_type()):
                    raise ValueError("file_path："+file_path+"不是视频文件（file_path:"+file_path+" is not a video file）")
                
                if not has_audio(file_path):
                    raise ValueError("file_path："+file_path+"没有音频，请选择一个有音频的视频文件。（file_path:"+file_path+" has no audio, please select a video file that has audio.）")
                
            else:
                if not file_path.lower().endswith(audio_type()):
                    raise ValueError("file_path："+file_path+"不是音频文件（file_path:"+file_path+" is not a audio file）")
            
            file_name = set_file_name(video_path)
            
            output_path = os.path.join(output_path, file_name)
            
            # ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -strict experimental -shortest output.mp4
            
            if audio_from == "audio_file":
                #ffmpeg -i video.mp4 -i audio.mp3 -map 0:v -map 1:a -c:v copy -c:a copy -shortest output.mp4
                command = [
                    'ffmpeg', '-i', video_path, '-itsoffset', str(delay_play),# 输入视频路径
                    '-i', file_path, # 输入音频文件路径
                    '-map', '0:v',   #从第一个输入文件（video.mp4）中选择视频流。
                    '-map', '1:a',   #从第二个输入文件（audio.mp3）中选择音频流
                    '-c:v', 'copy',  # 复制视频流
                    '-c:a', 'copy',  # 复制音频流
                    '-shortest', #-shortest 参数让音频或视频的时间对齐，即音频或视频的长度较短的那个为准
                    output_path,
                ]
            else:
                # ffmpeg -i source_video.mp4 -i target_video.mp4 -map 0:a -map 1:v -c:v copy -c:a aac -strict experimental -shortest output.mp4
                command = [
                    'ffmpeg', '-itsoffset',str(delay_play),
                    '-i', file_path,'-i',video_path,  # 输入视频路径
                    '-map', '0:a', '-map', '1:v', '-c:v', 'copy', '-c:a', 'copy',
                    '-strict', 'experimental', 
                    '-shortest',
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