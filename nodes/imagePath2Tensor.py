import torch
from PIL import ImageOps
import comfy
from PIL import Image
import numpy as np

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
        try:
            #['D:\\Cache\\222\\frame_00000121.png', 'D:\\Cache\\222\\frame_00000122.png']
            images = []
            for image_path in image_paths:
                # Open and process the image
                with Image.open(image_path) as img:
                    img = ImageOps.exif_transpose(img).convert("RGB")
                    # Directly convert to torch tensor without numpy intermediate
                    image_tensor = torch.from_numpy(np.array(np.array(img).astype(np.float32) / 255.0))[None,]
                    images.append(image_tensor)
                
            if len(images) == 0:
                raise ValueError("No images loaded successfully.")
            if len(images) == 1:
                return (images[0], 1)

            elif len(images) > 1:
                image1 = images[0]
                for image2 in images[1:]:
                    if image1.shape[1:] != image2.shape[1:]:
                        image2 = comfy.utils.common_upscale(image2.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear", "center").movedim(1, -1)
                    image1 = torch.cat((image1, image2), dim=0)
                return (image1, len(images))

        except Exception as e:
            raise ValueError(e)