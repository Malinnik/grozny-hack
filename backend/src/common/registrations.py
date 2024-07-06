
from datetime import datetime
from loguru import logger
import pandas as pd


def __most_common(lst):
    return max(set(lst), key=lst.count)

def get_exif_date(img, file):
    exif = img._getexif()
    if not exif:
        logger.error(f'Image {file} does not have EXIF data.')
    return datetime.strptime(exif[36867], '%Y:%m:%d %H:%M:%S')


def set_predictions(predictions: list):
    """
    Creates a DataFrame with the predictions from the model.

    link, class_name_predicted, confidence, exif
    """
    return pd.DataFrame(predictions, columns=["link", "class_name_predicted", "confidence", "exif"])

def generate_registrations(predictions):
    # name_folder,class,date_registration_start,date_registration_end,count
    registrations = []
    
    predictions['name_folder'] = predictions['link'].apply(lambda x: x[:x.find('/')])
    for name_folder, group in predictions.groupby('name_folder'):
        dates = []
        classes = []
        counts = []
        for shortpath, obj in group.groupby('link'):
            
            counts.append(min(len(obj), 5))
            dates.append(obj['exif'].iloc[0])

            cls = []
            for id, obj in obj.iterrows():
                cls.append(obj['class_name_predicted'])
            classes.append(cls)
        # print(dates[:5])
        # print(counts[:5])
        # print(classes[:5])

        prev_date = dates[0]
        prev_class = __most_common(classes[0])
        prev_count = counts[0]
        registrations.append({
            'name_folder': name_folder, 
            'class': prev_class,
            'classdate_registration_start': prev_date, 
            'date_registration_end': prev_date, 
            'count': prev_count,
        })
        for i, (date, cls, count) in enumerate(zip(dates[1:], classes[1:], counts[1:])):
            cls = __most_common(cls)

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
