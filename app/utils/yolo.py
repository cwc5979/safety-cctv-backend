import os
import cv2
import numpy as np
from ultralytics import YOLO
from app.config import settings

class YoloDetector:
    def __init__(self, model_dir: str = None):
        self.model_dir = model_dir or settings.yolo_model_dir
        weight_path = os.path.join(self.model_dir, "best.pt")
        if not os.path.isfile(weight_path):
            raise FileNotFoundError(f"YOLO weight file not found at {weight_path}")
        self.model = YOLO(weight_path)
        self.class_names = self.model.names

    def detect(self, image: np.ndarray):
        """
        :param image: BGR 형식의 numpy 배열
        :return: [ { 'cls': int, 'name': str, 'bbox': [x1,y1,x2,y2], 'conf': float }, … ]
        """
        results = self.model.predict(source=image, verbose=False)[0]
        detections = []
        # ultralytics v8+: results.boxes.data 는 [x1,y1,x2,y2,conf,cls]
        for *box, conf, cls in results.boxes.data.tolist():
            detections.append({
                "cls":   int(cls),
                "name":  self.class_names[int(cls)],
                "bbox":  [int(x) for x in box],
                "conf":  float(conf),
            })
        return detections

# 전역 싱글턴 인스턴스
yolo_detector: YoloDetector = None

def init_detector():
    global yolo_detector
    if yolo_detector is None:
        yolo_detector = YoloDetector()
    return yolo_detector
