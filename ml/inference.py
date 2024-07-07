import argparse
from pathlib import Path
from configs.config import MainConfig
from confz import BaseConfig, FileSource
import os
import torch
import numpy as np
from tqdm.notebook import tqdm
from utils.utils import load_detector, load_classificator, open_mapping, extract_crops
import pandas as pd
from itertools import repeat
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import torch.nn.functional as F

argparser = argparse.ArgumentParser()
argparser.add_argument('path_to_dataset', help='Путь к датасету')
args = argparser.parse_args()

pathes_to_imgs = []
for directory, _, _ in os.walk(args.path_to_dataset):
    pathes_to_imgs += [i for i in sorted(Path(directory).glob("*"))
                      if i.suffix.lower() in [".jpeg", ".jpg", ".png"]]
pathes_to_imgs[:10]

main_config = MainConfig(config_sources=FileSource(file=os.path.join("configs", "config.yml")))
print(main_config)
device = main_config.device

# Load imgs from source dir
# pathes_to_imgs = [i for i in sorted(Path(input_directory_path).glob("*"))
#                   if i.suffix.lower() in [".jpeg", ".jpg", ".png"]]

# Load mapping for classification task
mapping = open_mapping(path_mapping=main_config.mapping)

# Separate main config
detector_config = main_config.detector
classificator_config = main_config.classificator

# Load models
detector = load_detector(detector_config).to(device)
classificator = load_classificator(classificator_config).to(device)

def predict_with_baseline():
    if len(pathes_to_imgs) == 0:
        return

    list_predictions = []

    num_packages_det = np.ceil(len(pathes_to_imgs) / detector_config.batch_size).astype(np.int32)
    with torch.no_grad():
        for i in tqdm(range(num_packages_det), colour="green"):
            # Inference detector
            batch_images_det = pathes_to_imgs[detector_config.batch_size * i:
                                              detector_config.batch_size * (1 + i)]
            results_det = detector(batch_images_det,
                                   iou=detector_config.iou,
                                   conf=detector_config.conf,
                                   imgsz=detector_config.imgsz,
                                   verbose=False,
                                   device=device)

            filename = str(batch_images_det[0])[-14:]

            if len(results_det) > 0:
                # Extract crop by bboxes
                dict_crops = extract_crops(results_det, config=classificator_config)

                # Inference classificator
                for img_name, batch_images_cls in dict_crops.items():
                    # if len(batch_images_cls) > classificator_config.batch_size:
                    num_packages_cls = np.ceil(len(batch_images_cls) / classificator_config.batch_size).astype(np.int32)
                    for j in range(num_packages_cls):
                        batch_images_cls = batch_images_cls[classificator_config.batch_size * j:
                                                            classificator_config.batch_size * (1 + j)]
                        logits = classificator(batch_images_cls.to(device))
                        probabilities = torch.nn.functional.softmax(logits, dim=1)
                        top_p, top_class_idx = probabilities.topk(1, dim=1)

                        # Locate torch Tensors to cpu and convert to numpy
                        top_p = top_p.cpu().numpy().ravel()
                        top_class_idx = top_class_idx.cpu().numpy().ravel()

                        class_names = [mapping[top_class_idx[idx]] for idx, _ in enumerate(batch_images_cls)]

                        list_predictions.extend([[filename, cls, prob] for name, cls, prob in
                                                 zip(repeat(img_name, len(class_names)), class_names, top_p)])

if True:
    predictions = pd.read_csv('predictions.csv')
else:
    list_predictions = predict_with_baseline()
    predictions = pd.DataFrame(list_predictions, columns=["link", "class_name_predicted", "confidence"])

predictions_path = f'predictions{datetime.now()}.csv'
predictions.to_csv(predictions_path, index=False)
print(f'Saved to {predictions_path}')

def get_date_taken(path):
    exif = Image.open(path)._getexif()
    if not exif:
        raise Exception('Image {0} does not have EXIF data.'.format(path))
    return datetime.strptime(exif[36867], '%Y:%m:%d %H:%M:%S')

def most_common(lst):
    return max(set(lst), key=lst.count)

def generate_registrations(predictions):
    # name_folder,class,date_registration_start,date_registration_end,count
    registrations = []

    predictions['name_folder'] = predictions['link'].apply(lambda x: x[:x.find('/')])
    for name_folder, group in predictions.groupby('name_folder'):
        dates = []
        classes = []
        counts = []
        for shortpath, obj in group.groupby('link'):
            path = path_to_dataset+shortpath

            counts.append(min(len(obj), 5))
            dates.append(get_date_taken(path))

            cls = []
            for id, obj in obj.iterrows():
                cls.append(obj['class_name_predicted'])
            classes.append(cls)
        # print(dates[:5])
        # print(counts[:5])
        # print(classes[:5])

        prev_date = dates[0]
        prev_class = most_common(classes[0])
        prev_count = counts[0]
        registrations.append({
            'name_folder': name_folder,
            'class': prev_class,
            'classdate_registration_start': prev_date,
            'date_registration_end': prev_date,
            'count': prev_count,
        })
        for i, (date, cls, count) in enumerate(zip(dates[1:], classes[1:], counts[1:])):
            cls = most_common(cls)

            if cls == prev_class and count == prev_count and (date - prev_date).seconds//3600 < 30:
                registrations[-1]['date_registration_end'] = date
            else:
                registrations.append({
                    'name_folder': name_folder,
                    'class': cls,
                    'classdate_registration_start': date,
                    'date_registration_end': date,
                    'count': count,
                })

            prev_date = date
            prev_class = cls
            prev_count = count
        registrations[-1]['date_registration_end'] = date

    return registrations

def get_sliding_window(dates, i, minutes):
    left = i
    right = i

    while left > 0 and (dates[i]-dates[left]).seconds // 60 < minutes:
        left -= 1
    while right < len(dates)-1 and (dates[right]-dates[i]).seconds // 60 < minutes:
        right += 1
    return left, right

def generate_registrations_with_windows(predictions):
    # name_folder,class,date_registration_start,date_registration_end,count
    registrations = []

    predictions['name_folder'] = predictions['link'].apply(lambda x: x[:x.find('/')])
    for name_folder, group in predictions.groupby('name_folder'):
        dates = []
        classes = []
        counts = []
        for shortpath, obj in group.groupby('link'):
            path = path_to_dataset+shortpath

            counts.append(min(len(obj), 5))
            dates.append(get_date_taken(path))

            cls = []
            for id, obj in obj.iterrows():
                cls.append(obj['class_name_predicted'])
            classes.append(most_common(cls))

        prev_date = dates[0]
        prev_class = most_common(classes[0])
        prev_count = counts[0]
        registrations.append({
            'name_folder': name_folder,
            'class': prev_class,
            'classdate_registration_start': prev_date,
            'date_registration_end': prev_date,
            'count': prev_count,
        })
        for i, (date, cls, count) in enumerate(zip(dates[1:], classes[1:], counts[1:])):
            left, right = get_sliding_window(dates, i, 30)

            curr_count = np.max(counts[left:i+1])
            curr_class = most_common(classes[left:right+1])

            if curr_class == prev_class and curr_count == prev_count and (dates[i] - prev_date).seconds//60 < 40:
                registrations[-1]['date_registration_end'] = date
            else:
                registrations.append({
                    'name_folder': name_folder,
                    'class': cls,
                    'classdate_registration_start': date,
                    'date_registration_end': date,
                    'count': count,
                })

            prev_date = dates[i]
            prev_class = curr_class
            prev_count = curr_count
            if i == 3:
                break
        registrations[-1]['date_registration_end'] = date

    return registrations

reqs = generate_registrations_with_windows(predictions)

def save_registrations(regs, out='submission.csv'):
    df = pd.DataFrame(regs)
    df.to_csv(out, index=False)
    print(f'Saved to {out}')

regs_path = f'submission_{datetime.now()}.csv'
save_registrations(regs, regs_path)
print(f'Saved to {regs_path}')
