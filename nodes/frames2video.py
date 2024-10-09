import os
import subprocess
from ..func import get_image_size,generate_template_string

class Frames2Video:
 
    # 初始化方法
    def __init__(self): 
        pass 
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "frame_path": ("STRING", {"default": "C:/Users/Desktop",}), 
                "fps": ("FLOAT", {
                    "default": 30, 
                    "min": 1,
                    "max": 120,
                    "step": 1,
                    "display": "number",
                }),
                "video_name": ("STRING", {"default": "new_video"}),
                "output_path": ("STRING", {"default": "C:/Users/Desktop/output"}),
                "device":(["CPU","GPU"],{"default": "CPU",}),
            },
            "optional":{
                "audio_path":("STRING",{"default": "C:/Users/audio.mp3",}),
                }
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("frame_path","output_path",)
    FUNCTION = "frames2video" 
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg" 

    def frames2video(self,frame_path,fps,video_name,output_path,audio_path,device):
        try:
            frame_path = os.path.abspath(frame_path).strip()
            output_path = os.path.abspath(output_path).strip()
            if audio_path != "":
                audio_path = os.path.abspath(audio_path).strip()
                if not os.path.exists(audio_path):
                    raise ValueError("audio_path："+audio_path+"不存在（audio_path:"+audio_path+" does not exist）")
            if not os.path.exists(frame_path):
                raise ValueError("frame_path："+frame_path+"不存在（frame_path:"+frame_path+" does not exist）")
                
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path："+output_path+"不是目录（output_path:"+output_path+" is not a directory）")
            output_path =  f"{output_path}\{video_name}.mp4" # 将输出目录和输出文件名合并为一个输出路径
            # 获取输入目录中的所有图像文件
            valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
            # 获取所有图片并按文件名排序
            images = [os.path.join(frame_path, f) for f in os.listdir(frame_path) if f.endswith(valid_extensions)]
            # 按文件名进行排序
            images.sort()
            
            if len(images) == 0:
                raise FileNotFoundError("目录："+frame_path+"中没有图片文件（No image files found in directory："+frame_path+"）")

            # 构建ffmpeg命令
            width,height = get_image_size(images[0]);
            img_template_string = generate_template_string(os.path.basename(images[0]))
            if audio_path != '':
                if device == "CPU":
                    cmd = [
                        'ffmpeg',
                        '-framerate', str(fps),
                        '-i', f'{frame_path}/{img_template_string}',
                        '-i', audio_path,  # 添加音频文件路径
                        '-vf', f'scale={width}:{height}',
                        '-c:v', 'libx264',
                        '-crf', '28',
                        '-pix_fmt', 'yuv420p',
                        '-shortest',  
                        '-y',
                        str(output_path)
                    ]
                else:
                    cmd = [
                        'ffmpeg',
                        '-framerate', str(fps),
                        '-i', f'{frame_path}/{img_template_string}',
                        '-i', audio_path,  # 添加音频文件路径
                        '-vf', f'scale={width}:{height}',
                        '-c:v', 'h264_nvenc',  # 使用 GPU 加速的 NVENC 编码器
                        '-preset', 'fast',  # 选择一个合适的 preset
                        '-cq', '22',  # 设置质量，适应NVENC（类似 CRF）
                        '-pix_fmt', 'yuv420p',
                        '-shortest',  
                        '-y',
                        str(output_path)
                    ]

            else:
                if device == "CPU":
                    cmd = [
                        'ffmpeg',
                        '-framerate', str(fps),
                        '-i', f'{frame_path}/{img_template_string}',
                        '-vf', f'scale={width}:{height}',
                        '-c:v', 'libx264',
                        '-crf', '28',
                        '-pix_fmt', 'yuv420p',
                        '-shortest',  
                        '-y',
                        str(output_path)
                    ]
                else:
                    cmd = [
                        'ffmpeg',
                        '-framerate', str(fps),
                        '-i', f'{frame_path}/{img_template_string}',
                        '-vf', f'scale={width}:{height}',
                        '-c:v', 'h264_nvenc',  # 使用 GPU 加速的 NVENC 编码器
                        '-preset', 'fast',  # 选择一个合适的 preset
                        '-cq', '22',  # 设置质量，适应NVENC（类似 CRF）
                        '-pix_fmt', 'yuv420p',
                        '-shortest',  
                        '-y',
                        str(output_path)
                    ]
            # 执行ffmpeg命令
            result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if result.returncode != 0:
                # 如果有错误，输出错误信息
                 print(f"Error: {result.stderr.decode('utf-8')}")
                 raise ValueError(f"Error: {result.stderr.decode('utf-8')}")
            else:
                # 输出标准输出信息
                print(result.stdout)
            frame_path = str(frame_path) # 输出路径为字符串
            return (frame_path,output_path)
        except Exception as e:
            raise ValueError(e)