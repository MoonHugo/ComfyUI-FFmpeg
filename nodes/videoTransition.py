import os
import subprocess
from ..func import set_file_name,video_type,getVideoInfo,get_xfade_transitions,has_audio
import torch
    
device = "cuda" if torch.cuda.is_available() else "cpu"


class VideoTransition:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video1_path": ("STRING", {"default":"C:/Users/Desktop/video1.mp4",}),
                "video2_path": ("STRING", {"default":"C:/Users/Desktop/video2.mp4",}),
                #视频尺寸、帧率参考哪个视频
                "reference_video": (["video1","video2"], {"default":"video1","tooltip": "参考视频是哪个视频，决定了输出视频的尺寸和帧率！（Reference video is which video, determines the size and frame rate of the output video!）"}),
                "device": (["cpu","cuda"], {"default":device,}),
                "transition": (get_xfade_transitions(),{"default": "fade",}),
                "transition_duration": ("FLOAT",{"default":1,"min":0.1,"max":3.0,"step":0.1,"display":"number","tooltip": "转场持续时间，单位秒，最大值为3秒，不能小于0.1秒！（Transition duration, in seconds, the maximum value is 3 seconds, cannot be less than 0.1 seconds!）"}),
                "offset": ("FLOAT",{"default":1,"min":0.1,"step":0.1,"display":"number","tooltip": "转场开始时间，单位秒，不能大于等于视频1的时长减去转场持续时间（transition_duration）！（Transition start time, in seconds, cannot be greater than or equal to the duration of video1 minus the transition duration (transition_duration)!）"}),
                "output_path": ("STRING", {"default":"C:/Users/Desktop/output",}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_complete_path",)
    FUNCTION = "video_transition"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    def video_transition(self, video1_path, video2_path,reference_video, device,transition, transition_duration, offset,output_path):
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
            
            #offset不能大于视频1的时长-transition_duration
            video1_info = getVideoInfo(video1_path)
            reference_video_info = getVideoInfo(video1_path if reference_video == "video1" else video2_path)
            if video1_info is None:
                raise ValueError("无法获取视频1的信息（Cannot get video1 information）")

            if offset >= video1_info['duration'] - transition_duration:
                raise ValueError("offset："+str(offset)+"不能大于等于（视频1的时长-transition_duration），其中视频1的时长减去transition_duration为："+str(video1_info['duration']-transition_duration)+"（offset:"+str(offset)+" cannot be greater than (video1 duration - transition_duration), where video1 duration minus transition_duration is:"+str(video1_info['duration']-transition_duration))
            
            use_cuvid = []  # 改为列表
            use_encoder = "-c:v libx264"  # 默认用CPU编码
            
            if device == "cuda":
                use_cuvid = ['-hwaccel', 'cuda']  # 分开传递参数
                use_encoder = "-c:v h264_nvenc"
            
            file_name = set_file_name(video1_path)
            
            output_path = os.path.join(output_path, file_name)
            
            target_width = reference_video_info['width']
            target_height = reference_video_info['height']
            target_fps = reference_video_info['fps']
            
            has_audio1 = has_audio(video1_path)
            has_audio2 = has_audio(video2_path)

            filter_complex = (
                # 先将两个视频缩放到相同尺寸、帧率
                f'[0:v]settb=AVTB,fps={target_fps},format=yuv420p,'
                f'scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2[v0];'
                
                f'[1:v]settb=AVTB,fps={target_fps},format=yuv420p,'
                f'scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2[v1];'
                # 视频转场(使用缩放后的视频流)
                f'[v0][v1]xfade=transition={transition}:duration={transition_duration}:offset={offset}[outv]'
            )
            
            if has_audio1 and has_audio2:  # 两个视频都有音频
                filter_complex += (
                    f';[0:a]asplit[a0l][a0r];'
                    f'[1:a]asplit[a1l][a1r];'
                    f'[a0l]atrim=0:{offset}[a0start];'
                    f'[a0r]atrim={offset}:{offset+transition_duration},asetpts=PTS-STARTPTS[a0end];'
                    f'[a1l]atrim=0:{transition_duration},asetpts=PTS-STARTPTS[a1start];'
                    f'[a1r]atrim={transition_duration},asetpts=PTS-STARTPTS[a1end];'
                    f'[a0end][a1start]acrossfade=duration={transition_duration}[across];'
                    f'[a0start][across][a1end]concat=n=3:v=0:a=1[outa]'
                )
            elif has_audio1:  # 只有第一个视频有音频
                filter_complex += (
                    f';[0:a]atrim=0:{offset+transition_duration}[a0]'  # 只保留到转场结束
                )
            elif has_audio2:  # 只有第二个视频有音频
                filter_complex += (
                    # 从转场开始时间开始截取音频
                    f';[1:a]atrim=0,asetpts=PTS-STARTPTS+{offset}/TB[a1]'
                )

            command = ['ffmpeg']
            
            if use_cuvid:
                command.extend(use_cuvid)  # 使用extend添加CUDA参数
                
            command.extend([
                '-i', video1_path,
                '-i', video2_path,
                '-filter_complex', filter_complex,
                '-map', '[outv]',
            ])
            
            # 只有在两个视频都有音频时才添加音频映射
            if has_audio1 and has_audio2:
                command.extend(['-map', '[outa]'])
            elif has_audio1:
                command.extend(['-map', '[a0]'])
            elif has_audio2:
                command.extend(['-map', '[a1]'])
            if use_encoder:
                command.extend(use_encoder.split())
                
            command.append(f'{output_path}.mp4')

            # 执行命令
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