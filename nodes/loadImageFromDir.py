from ..func import get_image_paths_from_directory

class LoadImageFromDir:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "images_path": ("STRING", {"default":"C:/Users/Desktop/",}),
                "start_index": ("INT",{"default":0,"min":0,}),
                "length": ("INT",{"default":0,"min":0,})
            },
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("image_paths",)
    FUNCTION = "load_image_from_dir"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg/auxiliary tool"
  
    def load_image_from_dir(self, images_path, start_index, length):
        try:
            image_paths = get_image_paths_from_directory(images_path, start_index, length)
            return (image_paths,)
        except Exception as e:
            raise ValueError(e)