import os
import subprocess
from ..func import video_type

class ExtractAudio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video_path": ("STRING", {"default":"C:/Users/Desktop/video.mp4",}),
                "output_path": ("STRING", {"default":"C:/Users/Desktop/output",}),
                "audio_format": ([".m4a",".mp3",".wav",".aac",".flac",".wma",".ogg",".ac3",".amr",".aiff",".opus",".m4b",".caf",".dts"], {"default":".m4a",}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("audio_complete_path",)
    FUNCTION = "extract_audio"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    def extract_audio(self, video_path, output_path, audio_format):
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
            file_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(output_path, file_name + audio_format)
           
            if audio_format == ".m4a":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn', '-acodec', 'copy',  # 不处理视频流，复制音频流
                    output_path,
                ]
            elif audio_format == ".mp3":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn', '-c:a', 'libmp3lame', '-q:a','2', #-q:a 2：指定音频质量，范围是 0 到 9，其中 0 是最高质量，2 通常是非常好的质量和文件大小的平衡。
                    output_path,
                ]
            elif audio_format == ".wav":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','pcm_s16le',
                    output_path,
                ]
            elif audio_format == ".aac":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','aac',
                    output_path,
                ]
            elif audio_format == ".flac":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','flac',
                    output_path,
                ]
            elif audio_format == ".wma":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','wmav2',
                    output_path,
                ]
            elif audio_format == ".ogg":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','libvorbis','-q:a', '5',
                    output_path,
                ]
            elif audio_format == ".ac3":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','ac3',
                    output_path,
                ]
            elif audio_format == ".amr":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','libopencore_amrnb','-ar', '8000','-b:a','12.2k',
                    '-ac','1',
                    output_path,
                ]
            elif audio_format == ".aiff":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','pcm_s16be',
                    output_path,
                ]
            elif audio_format == ".opus":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','libopus',
                    output_path,
                ]
            elif audio_format == ".m4b":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','aac',
                    '-b:a', '128k',  # 设置比特率为 128kbps
                    output_path,
                ]
            elif audio_format == ".caf":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','pcm_s16le',
                    output_path,
                ]
            elif audio_format == ".dts":
                command = [
                    'ffmpeg', '-i', video_path,  # 输入视频路径
                    '-vn','-c:a','dca',
                    '-strict','-2',
                    output_path,
                ]
            else:
                raise ValueError("不支持的音频格式："+audio_format+"(Unsupported audio formats:"+audio_format+")")
            
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