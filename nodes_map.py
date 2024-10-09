from .nodes.addTextWatermark import *
from .nodes.frames2video import *
from .nodes.video2frames import *
from .nodes.addImgWatermark import *
from .nodes.videoFlip import *
from .nodes.extractAudio import *
from .nodes.loadImageFromDir import *
from .nodes.imageCopy import *
from .nodes.imagePath2Tensor import *

NODE_CLASS_MAPPINGS = {
    "Video2Frames": Video2Frames,
    "Frames2Video": Frames2Video,
    "AddTextWatermark": AddTextWatermark,
    "AddImgWatermark": AddImgWatermark,
    "VideoFlip": VideoFlip,
    "ExtractAudio": ExtractAudio,
    "LoadImageFromDir": LoadImageFromDir,
    "ImageCopy": ImageCopy,
    "ImagePath2Tensor": ImagePath2Tensor,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Video2Frames": "🔥Video2Frames",
    "Frames2Video": "🔥Frames2Video",
    "AddTextWatermark": "🔥AddTextWatermark",
    "AddImgWatermark": "🔥AddImgWatermark",
    "VideoFlip": "🔥VideoFlip",
    "ExtractAudio": "🔥ExtractAudio",
    "LoadImageFromDir": "🔥LoadImageFromDir",
    "ImageCopy": "🔥ImageCopy",
    "ImagePath2Tensor": "🔥ImagePath2Tensor",
}
