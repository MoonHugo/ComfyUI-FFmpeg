import os
import subprocess
from ..func import has_audio,getVideoInfo,set_file_name,video_type
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

class MergingVideoByTwo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video1_path": ("STRING", {"default":"C:/Users/Desktop/video1.mp4",}),
                "video2_path": ("STRING", {"default":"C:/Users/Desktop/video2.mp4",}),
                "device": (["cpu","cuda"], {"default":device,}),
                "resolution_reference": (["video1","video2"], {"default":"video1",}),
                "output_path": ("STRING", {"default": "C:/Users/Desktop/output"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_complete_path",)
    FUNCTION = "merging_video_by_two"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    def merging_video_by_two(self, video1_path, video2_path,device,resolution_reference,output_path):
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
            
            video = {
                'video1': video1_path,
                'video2': video2_path,
            }.get(resolution_reference, video1_path)
            
            video_info = getVideoInfo(video)
            
            width = video_info['width']
            height = video_info['height']
            
            use_cuvid = []
            use_encoder = ['-c:v', 'libx264'] #默认用CPU编码

            if device == "cuda":
                use_cuvid = ['-hwaccel', 'cuda']
                use_encoder = ['-c:v', 'h264_nvenc']

            if video1_audio and video2_audio: #两个视频都有音频
                filter_complex = (
                    f'[0:v]scale={width}:{height},setsar=1,setpts=PTS-STARTPTS[v0];'
                    f'[1:v]scale={width}:{height},setsar=1,setpts=PTS-STARTPTS[v1];'
                    f'[v0][v1]concat=n=2:v=1:a=0[outv];'
                    f'[0:a][1:a]concat=n=2:v=0:a=1[outa]'
                )
                command = ['ffmpeg']
                command.extend(use_cuvid)
                command.extend(['-i', video1_path, '-i', video2_path])
                command.extend(['-filter_complex', filter_complex])
                command.extend(['-map', '[outv]', '-map', '[outa]', '-r', '30'])
                command.extend(use_encoder)
                command.extend(['-c:a', 'aac', '-ar', '44100', '-b:a', '128k', output_path])
            elif video1_audio and not video2_audio: #第一个视频有音频，第二个没有
                filter_complex = (
                    f'[0:v]scale={width}:{height},setsar=1,setpts=PTS-STARTPTS[v0];'
                    f'[1:v]scale={width}:{height},setsar=1,setpts=PTS-STARTPTS[v1];'
                    f'[v0][v1]concat=n=2:v=1:a=0[outv]'
                )
                command = ['ffmpeg']
                command.extend(use_cuvid)
                command.extend(['-i', video1_path, '-i', video2_path])
                command.extend(['-filter_complex', filter_complex])
                command.extend(['-map', '[outv]', '-map', '0:a', '-r', '30'])
                command.extend(use_encoder)
                command.extend(['-c:a', 'aac', '-ar', '44100', '-b:a', '128k', output_path])
            elif not video1_audio and video2_audio: #第一个视频没有音频，第二个有
                video_info = getVideoInfo(video1_path)
                duration = video_info['duration']
                delay_time = int(duration * 1000)  # 转换为毫秒

                filter_complex = (
                    f'[0:v]scale={width}:{height},setsar=1,setpts=PTS-STARTPTS[v0];'
                    f'[1:v]scale={width}:{height},setsar=1,setpts=PTS-STARTPTS[v1];'
                    f'[v0][v1]concat=n=2:v=1:a=0[outv];'
                    f'[1:a]adelay={delay_time}|{delay_time}[a1];'
                    f'[a1]concat=n=1:v=0:a=1[outa]'
                )
                command = ['ffmpeg']
                command.extend(use_cuvid)
                command.extend(['-i', video1_path, '-i', video2_path])
                command.extend(['-filter_complex', filter_complex])
                command.extend(['-map', '[outv]', '-map', '[outa]', '-r', '30'])
                command.extend(use_encoder)
                command.extend(['-c:a', 'aac', '-ar', '44100', '-b:a', '128k', output_path])
            else: #两个视频都没有音频
                filter_complex = (
                    f'[0:v]scale={width}:{height},setsar=1,setpts=PTS-STARTPTS[v0];'
                    f'[1:v]scale={width}:{height},setsar=1,setpts=PTS-STARTPTS[v1];'
                    f'[v0][v1]concat=n=2:v=1:a=0[outv]'
                )
                command = ['ffmpeg']
                command.extend(use_cuvid)
                command.extend(['-i', video1_path, '-i', video2_path])
                command.extend(['-filter_complex', filter_complex])
                command.extend(['-map', '[outv]', '-r', '30'])
                command.extend(use_encoder)
                command.extend(['-an', output_path]) 
            
            
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