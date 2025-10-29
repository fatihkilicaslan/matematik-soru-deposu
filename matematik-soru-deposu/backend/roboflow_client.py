from inference_sdk import InferenceHTTPClient
import cv2
import numpy as np
from PIL import Image
import os

class RoboflowClient:
    def __init__(self):
        self.client = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key="92Ra4ByBVqzPhUmGYZvB"
        )
        self.model_id = "sorukes-4akor/1"
    
    def detect_questions(self, image_path):
        """Görüntüdeki soruları tespit et"""
        try:
            # Dosya varlığını kontrol et
            if not os.path.exists(image_path):
                print(f"Dosya bulunamadı: {image_path}")
                return {'predictions': []}
            
            print(f"Roboflow'a gönderiliyor: {image_path}")
            result = self.client.infer(image_path, model_id=self.model_id)
            print(f"Roboflow sonucu: {len(result.get('predictions', []))} soru tespit edildi")
            return result
        except Exception as e:
            print(f"Roboflow detection hatası: {e}")
            return {'predictions': []}
    
    def crop_question(self, image_path, detection, index):
        """Tespit edilen soruyu kes ve kaydet"""
        try:
            # Görüntüyü yükle
            image = cv2.imread(image_path)
            height, width = image.shape[:2]
            
            # Bounding box koordinatları
            x = detection.get('x', 0)
            y = detection.get('y', 0)
            w = detection.get('width', 0)
            h = detection.get('height', 0)
            
            # Koordinatları piksel değerlerine çevir
            x1 = int(x - w/2)
            y1 = int(y - h/2)
            x2 = int(x + w/2)
            y2 = int(y + h/2)
            
            # Sınırları kontrol et
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(width, x2)
            y2 = min(height, y2)
            
            # Soruyu kes
            cropped = image[y1:y2, x1:x2]
            
            # Kesilen soruyu kaydet
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            cropped_path = f"uploads/cropped_{base_name}_q{index}.jpg"
            cv2.imwrite(cropped_path, cropped)
            
            return cropped_path
            
        except Exception as e:
            print(f"Soru kesme hatası: {e}")
            return None
    
    def enhance_image(self, image_path):
        """Görüntü kalitesini artır (opsiyonel)"""
        try:
            image = cv2.imread(image_path)
            
            # Gürültü azaltma
            denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
            
            # Kontrast artırma
            lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            enhanced = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
            
            return enhanced
            
        except Exception as e:
            print(f"Görüntü iyileştirme hatası: {e}")
            return cv2.imread(image_path)