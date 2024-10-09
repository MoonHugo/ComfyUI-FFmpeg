from ..func import copy_images_to_directory

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")

class ImageCopy:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "image_paths": (any_type,),
                "output_path": ("STRING", {"default": "C:/Users/Desktop/output"}),
            },
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("image_paths",)
    FUNCTION = "image_copy"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg/auxiliary tool"
  
    def image_copy(self, image_paths, output_path):
        try:
            image_output_path = copy_images_to_directory(image_paths,output_path)
            return (image_output_path,)
        except Exception as e:
            raise ValueError(e)