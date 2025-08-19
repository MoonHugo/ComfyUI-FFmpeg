import os
import subprocess
from ..func import has_audio, getVideoInfo, set_file_name, video_type
import torch
import math

device = "cuda" if torch.cuda.is_available() else "cpu"

class PipVideo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video1_path": ("STRING", {"default": "C:/Users/Desktop/video1.mp4", "tooltip": "说明：画中画背景画面！"}),
                "video2_path": ("STRING", {"default": "C:/Users/Desktop/video2.mp4", "tooltip": "说明：画中画前景画面！"}),
                "device": (["cpu", "cuda"], {"default": device}),
                "use_audio": (["video1", "video2"], {"default": "video1", "tooltip": "说明：最终视频使用哪个视频的音轨！"}),
                "use_duration": (["video1", "video2"], {"default": "video2", "tooltip": "说明：使用哪个视频作为最终参考时长！"}),
                "align_type": (["top-left", "top-right", "bottom-left", "bottom-right", "center"], {"default": "center"}),
                "pad_x": ("INT", {"default": 0, "min": -2000, "max": 2000, "step": 1, "tooltip": "X方向偏移量 (px)，0表示无偏移"}),
                "pad_y": ("INT", {"default": 0, "min": -2000, "max": 2000, "step": 1, "tooltip": "Y方向偏移量 (px)，0表示无偏移"}),
                "pip_fg_zoom": ("FLOAT", {"default": 2.5, "min": 1, "max": 100, "step": 0.5, "tooltip": "说明：前景缩放系数，越大前景越小"}),
                "output_path": ("STRING", {"default": "C:/Users/Desktop/output"}),
                "scale_and_crop": (["none", "540*960", "960*540"], {"default": "none", "tooltip": "说明：缩放和裁剪比例！"}),
                "fps": ("FLOAT", {"min": 0, "max": 60, "step": 0.1, "default": 30.0, "tooltip": "说明：帧率。0=video1帧率，1=video2帧率"}),
                "is_chromakey": ("BOOLEAN", {"default": False, "label_on": "绿幕去背景", "label_off": "关闭绿幕透明", "tooltip": "说明：是否进行绿幕去背景！"}),
            },
        }

    RETURN_TYPES = ("STRING", "INT", "INT", "FLOAT", "FLOAT",)
    RETURN_NAMES = ("video_complete_paths", "width", "height", "duration", "fps",)
    FUNCTION = "pip_video"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
    DESCRIPTION = """两个视频叠加成一个画中画效果，可以控制前景video2出现在video1上的位置，
                     可设置缩放、绿幕去背景和像素级偏移。"""

    def pip_video(self, video1_path, video2_path, device, use_audio, use_duration, 
                  align_type, pad_x, pad_y, pip_fg_zoom, output_path, scale_and_crop, fps, is_chromakey):
        try:
            video1_path = os.path.abspath(video1_path).strip()
            video2_path = os.path.abspath(video2_path).strip()
            output_path = os.path.abspath(output_path).strip()

            # --- 输入验证 ---
            if not video1_path.lower().endswith(video_type()):
                raise ValueError(f"video1_path: {video1_path} 不是视频文件")
            if not os.path.isfile(video1_path):
                raise ValueError(f"video1_path: {video1_path} 不存在")

            if not video2_path.lower().endswith(video_type()):
                raise ValueError(f"video2_path: {video2_path} 不是视频文件")
            if not os.path.isfile(video2_path):
                raise ValueError(f"video2_path: {video2_path} 不存在")

            if not os.path.isdir(output_path):
                raise ValueError(f"output_path: {output_path} 不是目录")

            video1_audio = has_audio(video1_path)
            video2_audio = has_audio(video2_path)

            final_output = set_file_name(video1_path)
            output_path = os.path.join(output_path, final_output)

            use_cuvid = ""
            use_encoder = "-c:v libx264"  # 默认CPU编码

            if device == "cuda":
                use_cuvid = "-hwaccel cuda"
                use_encoder = "-c:v h264_nvenc"

            video_info = getVideoInfo(video1_path)
            video_info1 = getVideoInfo(video2_path)

            if use_duration == "video1":
                duration_1 = video_info['duration']
            else:
                duration_1 = video_info1['duration']

            if fps == 0:
                fps = video_info['fps']
            elif fps == 1:
                fps = video_info1['fps']

            width = math.ceil(video_info['width'] / 2) * 2
            height = math.ceil(video_info['height'] / 2) * 2

            use_audio_index = {
                'video1': '0',
                'video2': '1',
            }.get(use_audio, '0')

            # --- 对齐逻辑 + 偏移 ---
            align_position = {
                "top-left": f"{pad_x}:{pad_y}",
                "top-right": f"(W-w)-{pad_x}:{pad_y}",
                "bottom-left": f"{pad_x}:(H-h)-{pad_y}",
                "bottom-right": f"(W-w)-{pad_x}:(H-h)-{pad_y}",
                "center": f"(W-w)/2+{pad_x}:(H-h)/2+{pad_y}",
            }.get(align_type, f"(W-w)/2+{pad_x}:(H-h)/2+{pad_y}")

            # --- 缩放/裁剪逻辑 ---
            if height * 540 / width > 960:
                pad_or_crop1 = 'crop=540:960:(ow-iw)/2:(oh-ih)/2'
            else:
                pad_or_crop1 = 'pad=540:960:(ow-iw)/2:(oh-ih)/2:color=black'

            if height * 960 / width > 540:
                pad_or_crop2 = 'crop=960:540:(ow-iw)/2:(oh-ih)/2'
            else:
                pad_or_crop2 = 'pad=960:540:(ow-iw)/2:(oh-ih)/2:color=black'

            scale_and_crop_data = {
                'none': 'null',
                '540*960': f'scale=540:-1,setsar=1,{pad_or_crop1}',
                '960*540': f'scale=960:-1,setsar=1,{pad_or_crop2}',
            }.get(scale_and_crop, 'null')

            video2_width = {
                'none': f'{width}',
                '540*960': '540',
                '960*540': '960',
            }.get(scale_and_crop, f'{width}')

            final_out = {
                'none': f'scale={width}:{height}:force_original_aspect_ratio=disable,setsar=1',
                '540*960': 'scale=540:960:force_original_aspect_ratio=disable,setsar=1',
                '960*540': 'scale=960:540:force_original_aspect_ratio=disable,setsar=1',
            }.get(scale_and_crop, f'scale={width}:{height}:force_original_aspect_ratio=disable,setsar=1')

            # --- 绿幕逻辑 ---
            chromakey = "chromakey=0x00FF00:0.3:0.1,format=yuva420p" if is_chromakey else "null"

            # --- 构建命令 ---
            if video1_audio or video2_audio:
                command = fr'ffmpeg -y {use_cuvid} -stream_loop -1 -i "{video1_path}" -stream_loop -1 -i "{video2_path}" -filter_complex "[0:v]fps={fps},setpts=PTS-STARTPTS[bg];[1:v]fps={fps},setpts=PTS-STARTPTS[fg];[bg]{scale_and_crop_data}[bg_out];[fg]{chromakey}[fgd];[fgd]scale={video2_width}/{pip_fg_zoom}:-1,setsar=1[fg_out];[bg_out][fg_out]overlay={align_position}[out];[out]{final_out}[final_out]" -map "[final_out]" -map {use_audio_index}:a? {use_encoder} -c:a aac -t {duration_1} "{output_path}"'
            else:
                command = fr'ffmpeg -y {use_cuvid} -stream_loop -1 -i "{video1_path}" -stream_loop -1 -i "{video2_path}" -filter_complex "[0:v]fps={fps},setpts=PTS-STARTPTS[bg];[1:v]fps={fps},setpts=PTS-STARTPTS[fg];[bg]{scale_and_crop_data}[bg_out];[fg]{chromakey}[fgd];[fgd]scale={video2_width}/{pip_fg_zoom}:-1,setsar=1[fg_out];[bg_out][fg_out]overlay={align_position}[out];[out]{final_out}[final_out]" -map "[final_out]" -t {duration_1} "{output_path}"'

            print(f">>> {command}")

            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

            if result.returncode != 0:
                print(f"Error: {result.stderr.decode('utf-8')}")
                if device == "cuda":
                    print("***当前运算模式 [cuda] 出错，尝试改用 CPU 编码重新运行***")
                    self.pip_video(video1_path, video2_path, "cpu", use_audio, use_duration,
                                   align_type, pad_x, pad_y, pip_fg_zoom,
                                   os.path.dirname(output_path), scale_and_crop, fps, is_chromakey)
            else:
                print(f">> FFmpeg 执行完毕！Completed!\t stdout: {result.stdout}")

            return (output_path, width, height, duration_1, fps,)
        except Exception as e:
            raise ValueError(e)
