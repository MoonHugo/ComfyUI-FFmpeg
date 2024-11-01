import torch
from PIL import ImageOps
import comfy
from PIL import Image
import numpy as np
import gc

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

class ImagePath2Tensor:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "image_paths": (any_type,),
            },
        }

    RETURN_TYPES = ("IMAGE","INT")
    RETURN_NAMES = ("image","image_count")
    FUNCTION = "image_path_to_tensor"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg/auxiliary tool"
  
    def image_path_to_tensor(self, image_paths):
        
        #['D:\\Cache\\222\\frame_00000121.png', 'D:\\Cache\\222\\frame_00000122.png']
        images = []
        for image_path in image_paths:
            try:
                # Open and process the image
                with Image.open(image_path) as img:
                    img = ImageOps.exif_transpose(img).convert("RGB")
                    # 直接转换为张量
                    image_tensor = torch.from_numpy(np.array(img).astype(np.float32) / 255.0).unsqueeze(0)
                    images.append(image_tensor)
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
                continue  # Skip to the next image on error

        if not images:
            raise ValueError("No images loaded successfully.")
        
        if len(images) == 1:
            return (images[0], 1)

        # 合并多个图像
        
        image1 = images[0]
        for image2 in images[1:]:
            if image1.shape[1:] != image2.shape[1:]:
                # 调整大小并合并
                image2 = comfy.utils.common_upscale(image2.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear", "center").movedim(1, -1)
            image1 = torch.cat((image1, image2), dim=0)
        
        length = len(images)
        result = (image1, length)
        del images
        del image1
        torch.cuda.empty_cache()
        gc.collect()
        return result