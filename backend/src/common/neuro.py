from itertools import repeat
import PIL
import PIL.Image

import cv2
from loguru import logger
import numpy as np

import torch
from torchvision.transforms.functional import normalize

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

from pathlib import Path

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

MEAN = [123.675, 116.28, 103.535]
STD = [58.395, 57.12, 57.375]

BATCH_SIZE  =  8

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
        



async def predict_image(img: PIL.Image.Image, filename: str, classificator, model: YOLO = YOLO('best.pt'), conf: float = 0.02, use_label: bool = False, show_conf: bool = False):
    result = model.predict(img, conf=conf)

    classes = result[0].boxes.data[:, -1]

    confs = result[0].boxes.data[:, -2]



    dict_crops = extract_crops(result)
    list_predictions = []
    with torch.no_grad():
        for img_name, batch_images_cls in dict_crops.items():
            # if len(batch_images_cls) > classificator_config.batch_size:
            num_packages_cls = np.ceil(len(batch_images_cls) / BATCH_SIZE).astype(
                np.int32)
            for j in range(num_packages_cls):
                batch_images_cls = batch_images_cls[1 * j:
                                                    BATCH_SIZE * (1 + j)]
                logits = classificator(batch_images_cls)

                probabilities = torch.nn.functional.softmax(logits, dim=1)
                top_p, classes = probabilities.topk(1, dim=1)

                # Locate torch Tensors to cpu and convert to numpy
                top_p = top_p.cpu().numpy().ravel()
                classes = classes.cpu().numpy().ravel()

                    
                class_names = [class_to_text[classes[idx]] for idx, _ in enumerate(batch_images_cls)]

                list_predictions.extend([[name, cls, prob] for name, cls, prob in
                                            zip(repeat(filename, len(class_names)), class_names, top_p)])


    for i in range(len(classes)):
        img = await bbox(img, classes[i], box=result[0].boxes[i], conf=confs[i], use_label=use_label, show_conf=show_conf)


    return [img, list_predictions]


def extract_crops(results: list, imgsz=[640,640]) -> dict[str, torch.Tensor]:
    dict_crops = {}
    for res_per_img in results:
        if len(res_per_img) > 0:
            crops_per_img = []
            for box in res_per_img.boxes:
                x0, y0, x1, y1 = box.xyxy.cpu().numpy().ravel().astype(np.int32)
                crop = res_per_img.orig_img[y0: y1, x0: x1]

                # Do squared crop
                # crop = letterbox(img=crop, new_shape=config.imgsz, color=(0, 0, 0))
                crop = cv2.resize(crop, imgsz, interpolation=cv2.INTER_LINEAR)

                # Convert Array crop to Torch tensor with [batch, channels, height, width] dimensions
                crop = torch.from_numpy(crop.transpose(2, 0, 1))
                crop = crop.unsqueeze(0)
                crop = normalize(crop.float(), mean=MEAN, std=STD)
                crops_per_img.append(crop)

            dict_crops[Path(res_per_img.path).name] = torch.cat(crops_per_img) # if len(crops_per_img) else None
    return dict_crops