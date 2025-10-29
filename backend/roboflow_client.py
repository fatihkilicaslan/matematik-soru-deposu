import requests
import base64
from PIL import Image, ImageEnhance
import os

class RoboflowClient:
    def __init__(self):
        self.api_url = "https://detect.roboflow.com"
        self.api_key = "92Ra4ByBVqzPhUmGYZvB"
        self.model_id = "sorukes-4akor/1"
    
    def detect_questions(self, image_path):
        """Görüntüdeki soruları tespit et"""
        try:
            # Dosya varlığını kontrol et
            if not os.path.exists(image_path):
                print(f"Dosya bulunamadı: {image_path}")
                return {'predictions': []}
            
            print(f"Roboflow'a gönderiliyor: {image_path}")
            
            # Görüntüyü base64'e çevir
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")
            
            # API isteği
            url = f"{self.api_url}/{self.model_id}?api_key={self.api_key}"
            response = requests.post(
                url,
                json=image_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Roboflow sonucu: {len(result.get('predictions', []))} soru tespit edildi")
                return result
            else:
                print(f"Roboflow API hatası: {response.status_code}")
                return {'predictions': []}
                
        except Exception as e:
            print(f"Roboflow detection hatası: {e}")
            return {'predictions': []}
    
    def crop_question(self, image_path, detection, index):
        """Tespit edilen soruyu kes ve kaydet"""
        try:
            # Görüntüyü yükle
            image = Image.open(image_path)
            width, height = image.size
            
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
            cropped = image.crop((x1, y1, x2, y2))
            
            # Kesilen soruyu kaydet
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            cropped_path = f"uploads/cropped_{base_name}_q{index}.jpg"
            cropped.save(cropped_path, 'JPEG', quality=95)
            
            return cropped_path
            
        except Exception as e:
            print(f"Soru kesme hatası: {e}")
            return None
    
    def enhance_image(self, image_path):
        """Görüntü kalitesini artır (opsiyonel)"""
        try:
            image = Image.open(image_path)
            
            # Kontrast artırma
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Keskinlik artırma
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.3)
            
            return image
            
        except Exception as e:
            print(f"Görüntü iyileştirme hatası: {e}")
            return Image.open(image_path)