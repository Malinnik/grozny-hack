import PIL
import PIL.Image

from loguru import logger
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
VIOLET = (75, 0, 130)
YELLOW = (255,255, 0)

label_to_color = {
    0: (128, 0, 0), 
    1: (0, 128, 0), 
    2: (0, 0, 128), 
    3: (128, 128, 0), 
    4: (0, 18, 128), 
    5: (128, 0, 128), 
    6: (128, 128, 128), 
    7: (0, 0, 0), 
    8: (128, 64, 0), 
    9: (0, 64, 128), 
    10: (64, 0, 128), 
    11: (64, 128, 0), 
    12: (128, 0, 64), 
    13: (0, 128, 64), 
    14: (64, 0, 0), 
    14: (0, 64, 0), 
    15: (0, 0, 64), 
    16: (64, 64, 0),
    17: (0, 64, 64), 
    18: (64, 0, 64), 
    19: (64, 64, 64), 
    20: (0, 0, 0)
}

class_to_text = {
    0:"Badger",
    1:"Bear",
    2:"Bison",
    3:"Cat",
    4:"Dog",
    5:"Empty",
    6:"Fox",
    7:"Goral",
    8:"Hare",
    9:"Lynx",
    10:"Marten",
    11:"Moose",
    12:"Mountain_Goat",
    13:"Musk_Deer",
    14:"Racoon_Dog",
    14:"Red_Deer",
    15:"Roe_Deer",
    16:"Snow_Leopard",
    17:"Squirrel",
    18:"Tiger",
    19:"Wolf",
    20:"Wolverine"
}

async def bbox(img: PIL.Image.Image, cls, box, conf, use_label, show_conf):

    img_np = np.array(img)

    # annotator = Annotator(img, pil=True)
    annotator = Annotator(img_np, pil=True)

    conf = f"{int(conf*100)}%"

    b = box.xyxy[0]

    if not use_label and not show_conf:
        annotator.box_label(b, '', label_to_color[int(cls)])    
    else:
        annotator.box_label(b, 
            f'{class_to_text[int(cls)] if use_label else ""} {conf if show_conf else ""}',
            label_to_color[int(cls)])

    # img = annotator.result()
    return PIL.Image.fromarray(annotator.result())
    logger.debug(f"{img=}")

    return img
        



async def predict_image(img: PIL.Image.Image, model: YOLO = YOLO('best.pt'), conf: float = 0.02, use_label: bool = False, show_conf: bool = False):
    result = model.predict(img, conf=conf)

    classes = result[0].boxes.data[:, -1]

    confs = result[0].boxes.data[:, -2]



    for i in range(len(classes)):
        img = await bbox(img, classes[i], box=result[0].boxes[i], conf=confs[i], use_label=use_label, show_conf=show_conf)


    return img
