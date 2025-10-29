# InfinityFree ile Deploy

## Hibrit Yaklaşım: Frontend InfinityFree + Backend Railway

### Adım 1: Backend'i Railway'e Deploy Et

1. **GitHub'a Yükle:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/KULLANICI_ADIN/matematik-soru-deposu.git
git push -u origin main
```

2. **Railway'e Deploy:**
   - https://railway.app → GitHub ile giriş
   - "New Project" → "Deploy from GitHub repo"
   - Repoyu seç
   - Otomatik deploy olacak
   - Settings → Generate Domain
   - URL'i kopyala (örn: `matematik-backend.up.railway.app`)

### Adım 2: Frontend'i InfinityFree'ye Yükle

1. **Frontend'i Hazırla:**
   
   `frontend/app.js` dosyasını aç ve API_BASE'i güncelle:
   ```javascript
   const API_BASE = 'https://matematik-backend.up.railway.app';
   ```

2. **InfinityFree Hesabı Oluştur:**
   - https://infinityfree.net adresine git
   - Ücretsiz hesap oluştur
   - Subdomain seç (örn: `matematik-soru.infinityfreeapp.com`)

3. **Dosyaları Yükle:**
   - FileZilla veya InfinityFree File Manager kullan
   - FTP bilgileri: InfinityFree control panel'den al
   - `frontend` klasöründeki tüm dosyaları `htdocs` klasörüne yükle:
     - index.html
     - app.js
     - (diğer frontend dosyaları)

4. **Yapılandırma:**
   
   `htdocs/.htaccess` dosyası oluştur:
   ```apache
   # CORS için gerekli
   <IfModule mod_headers.c>
       Header set Access-Control-Allow-Origin "*"
   </IfModule>
   
   # Hata sayfaları
   ErrorDocument 404 /index.html
   
   # Gzip sıkıştırma
   <IfModule mod_deflate.c>
       AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
   </IfModule>
   ```

### Adım 3: Test Et

1. InfinityFree URL'ini aç: `https://matematik-soru.infinityfreeapp.com`
2. Soru yükle ve test et
3. Backend Railway'de çalışıyor olmalı

## Alternatif: Tamamen Ücretsiz Çözümler

### A) Vercel (Frontend) + Railway (Backend)
- **Frontend**: https://vercel.com (ücretsiz, hızlı)
- **Backend**: https://railway.app (ücretsiz)

### B) Netlify (Frontend) + Render (Backend)
- **Frontend**: https://netlify.com (ücretsiz)
- **Backend**: https://render.com (ücretsiz)

### C) GitHub Pages (Frontend) + Railway (Backend)
- **Frontend**: GitHub Pages (ücretsiz, github.io domain)
- **Backend**: Railway (ücretsiz)

## InfinityFree Sınırlamaları

⚠️ **Dikkat:**
- Python/FastAPI desteklemiyor (sadece PHP)
- Günlük hit limiti var (50,000)
- Dosya yükleme limiti var
- Cron job yok

Bu yüzden backend için mutlaka başka bir platform gerekli.

## Önerilen Yapı

```
┌─────────────────────┐
│  InfinityFree       │
│  (Frontend)         │
│  - HTML/CSS/JS      │
│  - Kullanıcı arayüzü│
└──────────┬──────────┘
           │ API Calls
           ▼
┌─────────────────────┐
│  Railway            │
│  (Backend)          │
│  - Python/FastAPI   │
│  - Roboflow AI      │
│  - Database         │
└─────────────────────┘
```

## Maliyet

- **InfinityFree**: Tamamen ücretsiz
- **Railway**: Aylık $5 kredi (ücretsiz plan)
- **Toplam**: Ücretsiz (Railway kredisi yeterli)

## Sorun Giderme

### CORS Hatası
Backend'de CORS ayarlarını kontrol et:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # veya InfinityFree domain'ini ekle
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Dosya Yükleme Hatası
InfinityFree'de dosya boyutu limiti var. Railway'de sorun olmaz.

### SSL Sertifikası
Her iki platform da otomatik HTTPS sağlar.
