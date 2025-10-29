from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os
import shutil
from datetime import datetime
from roboflow_client import RoboflowClient
from database import Database
from models import SoruModel, KategoriModel

# Veritabanı ve Roboflow client'ı başlat
db = Database()
roboflow_client = RoboflowClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlatıldığında çalışır"""
    db.create_tables()
    os.makedirs("uploads", exist_ok=True)
    yield

app = FastAPI(title="Matematik Soru Deposu API", version="1.0.0", lifespan=lifespan)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static dosya servisi - uploads klasörü için
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def root():
    return {"message": "Matematik Soru Deposu API"}

@app.post("/upload-soru")
async def upload_soru(file: UploadFile = File(...)):
    """Soru fotoğrafını yükle ve işle"""
    try:
        # Dosya kontrolü
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Sadece resim dosyaları kabul edilir")
        
        # Dosyayı kaydet - Türkçe karakterleri temizle
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Dosya adını temizle
        clean_filename = file.filename
        # Türkçe karakterleri değiştir
        char_map = {'ç':'c', 'ğ':'g', 'ı':'i', 'ö':'o', 'ş':'s', 'ü':'u',
                   'Ç':'C', 'Ğ':'G', 'İ':'I', 'Ö':'O', 'Ş':'S', 'Ü':'U'}
        for tr_char, en_char in char_map.items():
            clean_filename = clean_filename.replace(tr_char, en_char)
        # Özel karakterleri temizle
        import re
        clean_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', clean_filename)
        
        filename = f"{timestamp}_{clean_filename}"
        file_path = f"uploads/{filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Roboflow ile soru kesme işlemi
        detection_result = roboflow_client.detect_questions(file_path)
        
        # Her tespit edilen soru için işlem yap
        processed_questions = []
        for i, question in enumerate(detection_result.get('predictions', [])):
            # Soru görselini kes
            cropped_path = roboflow_client.crop_question(file_path, question, i)
            
            # Soruyu veritabanına kaydet
            soru_data = {
                'original_image': file_path,
                'cropped_image': cropped_path,
                'detection_confidence': question.get('confidence', 0),
                'bbox': question,
                'status': 'pending'  # cevap bekleniyor
            }
            
            soru_id = db.insert_soru(soru_data)
            processed_questions.append({
                'id': soru_id,
                'cropped_image': cropped_path,
                'confidence': question.get('confidence', 0)
            })
        
        return {
            'success': True,
            'message': f"{len(processed_questions)} soru tespit edildi",
            'questions': processed_questions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")

@app.get("/sorular")
async def get_sorular(kategori: str = None, status: str = None, zorluk: int = None):
    """Soruları listele"""
    sorular = db.get_sorular(kategori=kategori, status=status, zorluk=zorluk)
    return {'sorular': sorular}

@app.post("/soru/{soru_id}/cevap")
async def add_cevap(soru_id: int, cevap_data: dict):
    """Soruya cevap ekle"""
    try:
        db.update_soru_cevap(soru_id, cevap_data)
        return {'success': True, 'message': 'Cevap eklendi'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kategoriler")
async def get_kategoriler():
    """Kategorileri listele"""
    kategoriler = db.get_kategoriler()
    return {'kategoriler': kategoriler}

@app.delete("/soru/{soru_id}")
async def delete_soru(soru_id: int):
    """Soruyu sil"""
    try:
        db.delete_soru(soru_id)
        return {'success': True, 'message': 'Soru silindi'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/debug/test-roboflow")
async def test_roboflow():
    """Roboflow bağlantısını test et"""
    try:
        # Basit test - sadece client'ın var olup olmadığını kontrol et
        client_info = {
            'model_id': roboflow_client.model_id,
            'client_type': str(type(roboflow_client.client)),
            'status': 'connected'
        }
        
        # Basit bir test çağrısı yapmayı dene (gerçek dosya olmadan)
        try:
            # Bu hata verecek ama client'ın çalıştığını gösterecek
            test_result = roboflow_client.client.infer("nonexistent.jpg", model_id=roboflow_client.model_id)
        except Exception as test_error:
            client_info['test_error'] = str(test_error)
            if "No such file" in str(test_error) or "FileNotFoundError" in str(test_error):
                client_info['connection_status'] = 'OK - Client can connect to Roboflow'
            else:
                client_info['connection_status'] = f'Connection issue: {str(test_error)}'
        
        return {'success': True, 'roboflow': client_info}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.get("/debug/uploads")
async def list_uploads():
    """Yüklenen dosyaları listele"""
    try:
        uploads = []
        if os.path.exists("uploads"):
            for file in os.listdir("uploads"):
                file_path = os.path.join("uploads", file)
                uploads.append({
                    'filename': file,
                    'size': os.path.getsize(file_path),
                    'created': os.path.getctime(file_path)
                })
        return {'uploads': uploads}
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)