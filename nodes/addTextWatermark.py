import os
import subprocess
import folder_paths
import time

current_path = os.path.abspath(__file__)
font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.normpath(__file__))), 'fonts')
folder_paths.folder_names_and_paths["fonts"] = ([font_dir], {'.ttf'})

class AddTextWatermark:
 
    # 初始化方法
    def __init__(self): 
        pass 
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "video_path": ("STRING", {"default":"C:/Users/Desktop/video.mp4",}),
                "output_path": ("STRING", {"default":"C:/Users/Desktop/output/",}),
                'font_file': (["default"] + folder_paths.get_filename_list("fonts"), ),
                'font_size': ("INT", {"default": 15, "min": 1, "max": 1000, "step": 1}),
                'font_color': ("STRING", {"default": "#FFFFFF"}),
                "text": ("STRING", {"default": "Watermark"}),
                "position_x":  ("INT", {"default": 10, "step": 1}),
                "position_y":  ("INT", {"default": 10, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("video_path","output_path",)
    FUNCTION = "add_text_watermark" 
    OUTPUT_NODE = True
    CATEGORY = "FFmpeg" 

    def add_text_watermark(self,video_path,output_path,font_file,font_size,font_color,text,position_x,position_y):
        try:
            video_path = os.path.abspath(video_path).replace("\ufeff", "").strip()
            output_path = os.path.abspath(output_path).replace("\ufeff", "").strip()
             # 视频不存在
            if not video_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv','.rmvb')):
                raise ValueError("video_path不是视频文件（video_path is not a video file）")
            
            if not os.path.exists(video_path):
                raise ValueError("video_path不存在（video_path does not exist）")
            
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path不是目录（output_path is not a directory）")
            
            file_name = os.path.basename(video_path)
            file_extension = os.path.splitext(file_name)[1]
            #文件名根据年月日时分秒来命名
            file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + file_extension
            output_path = os.path.join(output_path, file_name)
            
            # 替换为双斜杠
            font_path = os.path.join(font_dir, font_file).replace("\\", "/").replace(":", "\\:")
            # 构建命令 C\\:/Windows/Fonts/simhei.ttf   fontfile='J\\:/Comfyui-for-OOTDiffusion/ComfyUI/custom_nodes/ComfyUI-FFmpeg/fonts/Alibaba-PuHuiTi-Heavy.ttf
            if font_file == "default":
                cmd = [
                    'ffmpeg',
                    '-i', video_path,
                    '-vf', f"drawtext=text='{text}':x={position_x}:y={position_y}:fontsize={font_size}:fontcolor={font_color}",
                    output_path,
                ]
            else:
                cmd = [
                    'ffmpeg',
                    '-i', video_path,
                    '-vf', f"drawtext=text='{text}':x={position_x}:y={position_y}:fontfile='{font_path}':fontsize={font_size}:fontcolor={font_color}",
                    output_path,
                ]
            result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # 检查返回码
            if result.returncode != 0:
                # 如果有错误，输出错误信息
                 print(f"Error: {result.stderr.decode('utf-8')}")
                 raise ValueError(f"Error: {result.stderr.decode('utf-8')}")
            else:
                # 输出标准输出信息
                print(result.stdout)
        except Exception as e:
            raise ValueError(e)
        
        return (video_path,output_path)