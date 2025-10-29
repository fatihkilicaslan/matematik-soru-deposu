# Deploy Talimatları

## Railway ile Deploy (Önerilen)

### 1. GitHub'a Yükle
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADIN/matematik-soru-deposu.git
git push -u origin main
```

### 2. Railway'e Deploy
1. https://railway.app adresine git
2. GitHub ile giriş yap
3. "New Project" tıkla
4. "Deploy from GitHub repo" seç
5. `matematik-soru-deposu` reposunu seç
6. Otomatik deploy başlayacak

### 3. Environment Variables Ayarla
Railway dashboard'da:
- Settings → Variables
- Şu değişkenleri ekle:
  - `ROBOFLOW_API_KEY`: 92Ra4ByBVqzPhUmGYZvB
  - `ROBOFLOW_MODEL_ID`: sorukes-4akor/1

### 4. Domain Al
- Settings → Domains
- "Generate Domain" tıkla
- URL'ini kopyala (örn: matematik-soru-deposu.up.railway.app)

### 5. Frontend'i Güncelle
`frontend/app.js` dosyasında:
```javascript
const API_BASE = 'https://SENIN-RAILWAY-URL.up.railway.app';
```

## Render ile Deploy

### Backend:
1. https://render.com → "New Web Service"
2. GitHub repo bağla
3. Ayarlar:
   - Name: matematik-soru-backend
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Environment Variables ekle

### Frontend:
1. "New Static Site"
2. Ayarlar:
   - Name: matematik-soru-frontend
   - Build Command: (boş)
   - Publish Directory: `frontend`
3. `frontend/app.js`'te API_BASE'i backend URL'ine güncelle

## Vercel + Railway (Alternatif)

### Backend (Railway):
Yukarıdaki Railway adımlarını takip et

### Frontend (Vercel):
1. https://vercel.com
2. "Import Project"
3. GitHub repo seç
4. Root Directory: `frontend`
5. Deploy

## PythonAnywhere

1. https://www.pythonanywhere.com → Ücretsiz hesap aç
2. "Web" sekmesi → "Add a new web app"
3. "Manual configuration" → Python 3.10
4. Dosyaları yükle
5. WSGI dosyasını yapılandır

## Önemli Notlar

- **Veritabanı**: SQLite production'da sınırlıdır. PostgreSQL'e geçmeyi düşünün.
- **Uploads**: Kalıcı storage için AWS S3 veya Cloudinary kullanın.
- **HTTPS**: Tüm platformlar otomatik SSL sertifikası sağlar.
- **API Key**: Roboflow API key'ini environment variable olarak saklayın.

## Test

Deploy sonrası:
1. Backend URL'ini test et: `https://YOUR-URL/debug/test-roboflow`
2. Frontend'i aç ve soru yükle
3. Tüm özellikleri test et

## Sorun Giderme

- **CORS Hatası**: Backend'de CORS ayarlarını kontrol et
- **Dosya Yükleme Hatası**: Upload klasörü izinlerini kontrol et
- **Database Hatası**: Veritabanı dosyasının yazılabilir olduğundan emin ol
