import json
import math
import os
import subprocess

class Video2Frames:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video_path": ("STRING", {"default":"C:/Users/Desktop/video.mp4",}),
                "output_path": ("STRING", {"default":"C:/Users/Desktop/output",}),
                "frames_max_width":("INT", {"default": 0, "min": 0, "max": 1920}),
            },
        }

    RETURN_TYPES = ("STRING", "FLOAT", "STRING", "INT","STRING")
    RETURN_NAMES = ("frame_path", "fps", "audio_path", "total_frames","output_path")
    FUNCTION = "video2frames"
    OUTPUT_NODE = True
    CATEGORY = "FFmpeg"
  
    def video2frames(self, video_path, output_path, frames_max_width):
        try:
            video_path = os.path.abspath(video_path).replace("\ufeff", "").strip()
            output_path = os.path.abspath(output_path).replace("\ufeff", "").strip()
             # 提取音频
            audio_path = os.path.join(output_path, 'audio.mp3')
             # 视频不存在
            if not video_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv','.rmvb')):
                raise ValueError("video_path不是视频文件（video_path is not a video file）")
            print("视频文件路径："+video_path)
            if not os.path.isfile(video_path):
                raise ValueError("video_path不存在（video_path does not exist）")
            
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path不是目录（output_path is not a directory）")
            
            # 判断frames_max_width是否是一个整数
            if not isinstance(frames_max_width, int):
                raise ValueError("frames_max_width不是整数（frames_max_width is not an integer）")
            
            audio_cmd = [
                'ffmpeg', '-i', video_path, 
                '-q:a', '0', '-map', 'a', '-y', audio_path
            ]
            subprocess.run(audio_cmd)

            # 获取视频帧率、时长、宽高信息
            command = [
                'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 
                'stream=avg_frame_rate,duration,width,height', '-of', 'json', video_path
            ]

            # 运行ffprobe命令
            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # 将输出转化为字符串
            output = result.stdout.decode('utf-8').strip()
            print(output)
            data = json.loads(output)
            # 查找视频流信息
            if 'streams' in data and len(data['streams']) > 0:
                stream = data['streams'][0]  # 获取第一个视频流
                fps = stream.get('avg_frame_rate')
                if fps is not None:
                    # 帧率可能是一个分数形式的字符串，例如 "30/1" 或 "20.233000"
                    if '/' in fps:
                        num, denom = map(int, fps.split('/'))
                        fps = num / denom
                    else:
                        fps = float(fps)  # 直接转换为浮点数
                else:
                    raise ValueError("无法获取视频的帧率")
                width = int(stream.get('width'))
                height = int(stream.get('height'))
                duration = float(stream.get('duration'))
            else:
                raise ValueError("无法获取视频信息")

            # 计算总帧数
            total_frames = math.ceil(fps * duration)
            print(f"视频的帧率是: {fps}, 宽度是: {width}, 高度是: {height}, 时长是: {duration}, 总帧数是: {total_frames}")
            # 提取帧
            frame_path = os.path.join(output_path, 'frames')
            os.makedirs(frame_path, exist_ok=True) # exist_ok=True表示如果目录已经存在，不会引发异常

            # 计算输出宽度和高度以保持比例
            if frames_max_width > 0:
                if width > frames_max_width:
                    out_width = frames_max_width
                    out_height = int(height * frames_max_width / width)  # 按比例计算新高度
                else:
                    out_width = width
                    out_height = height
            else:
                out_width = width
                out_height = height
                
            command = [
                'ffmpeg', '-i', video_path,  # 输入视频路径
                '-vf', f'scale={out_width}:{out_height}',  # 使用scale滤镜缩放帧
                os.path.join(frame_path, 'frame_%06d.png')  # 输出帧路径
            ]
            
            # 执行命令并检查错误
            if subprocess.run(command).returncode != 0:
                print("生成序列帧时出错，请检查输入文件和路径。")

            # 打印信息
            print(f"序列帧图片输出路径: {frame_path}")
            print(f"音频输出路径: {audio_path}")   
            print(f"总帧数: {total_frames}")
            print(f"帧率: {fps}")
            print(f"输出路径: {output_path}")

            return (frame_path, fps, audio_path, total_frames,output_path)
        except Exception as e:
            raise ValueError(e)