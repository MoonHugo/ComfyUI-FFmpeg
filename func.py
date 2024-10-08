import numpy as np
from PIL import Image
import torch
import subprocess
import json
import re

def generate_template_string(filename):
    match = re.search(r'\d+', filename)
    return re.sub(r'\d+', lambda x: f'%0{len(x.group())}d', filename) if match else filename

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def getVideoInfo(video_path):
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
            width = int(stream.get('width'))
            height = int(stream.get('height'))
            duration = float(stream.get('duration'))
            return_data = {'fps': fps, 'width': width, 'height': height, 'duration': duration}
    else:
        return_data = {}
    return return_data

def get_image_size(image_path):
    # 打开图像文件
    with Image.open(image_path) as img:
        # 获取图像的宽度和高度
        width, height = img.size
        return width, height