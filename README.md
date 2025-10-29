# Matematik Soru Deposu

Yapay zeka destekli matematik soru işleme ve depolama sistemi. Telefondan yüklenen soru fotoğraflarını otomatik olarak keser, kategoriler ve cevaplarıyla birlikte depolar.

## Özellikler

- 📱 **Mobil Uyumlu**: Telefondan kolay fotoğraf yükleme
- 🤖 **AI Destekli**: Roboflow ile otomatik soru kesme
- 📂 **Kategorileme**: Matematik konularına göre otomatik sınıflandırma
- 💾 **Veritabanı**: SQLite ile güvenli depolama
- 🎯 **Zorluk Seviyeleri**: Kolay, Orta, Zor seviyeleri
- 🔍 **Filtreleme**: Kategori ve duruma göre arama

## Kurulum

### Backend Kurulumu

1. Python sanal ortamı oluşturun:
```bash
cd matematik-soru-deposu/backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Sunucuyu başlatın:
```bash
python main.py
```

Backend http://localhost:8000 adresinde çalışacak.

### Frontend Kurulumu

1. Frontend klasörüne gidin:
```bash
cd matematik-soru-deposu/frontend
```

2. Basit HTTP sunucusu başlatın:
```bash
# Python ile
python -m http.server 3000

# Node.js ile (npx gerekli)
npx serve .
```

Frontend http://localhost:3000 adresinde çalışacak.

## Kullanım

1. **Soru Yükleme**: 
   - Ana sayfada "Soru Fotoğrafı Yükle" alanına tıklayın
   - Matematik sorusu içeren fotoğrafı seçin
   - AI otomatik olarak soruları tespit edip kesecek

2. **Cevap Ekleme**:
   - Kesilen sorularda "Cevapla" butonuna tıklayın
   - Soru metnini yazın
   - Cevabı girin
   - Kategori ve zorluk seviyesi seçin
   - Kaydedin

3. **Filtreleme**:
   - Kategori ve durum filtrelerini kullanın
   - Belirli konulardaki soruları bulun

## API Endpoints

- `POST /upload-soru`: Soru fotoğrafı yükleme
- `GET /sorular`: Soruları listeleme (filtreleme destekli)
- `POST /soru/{id}/cevap`: Soruya cevap ekleme
- `GET /kategoriler`: Kategorileri listeleme

## Roboflow Entegrasyonu

Proje Roboflow'un Hosted Image Inference servisini kullanır:
- Model ID: `sorukes-4akor/1`
- API Key: Kodda tanımlı
- Otomatik soru tespit ve kesme

## Veritabanı Yapısı

### Kategoriler
- Cebir, Geometri, Trigonometri
- Analiz, Sayılar, İstatistik, Olasılık

### Sorular
- Original/cropped images
- Soru metni ve cevabı
- Kategori ve zorluk seviyesi
- AI güven skoru

## Geliştirme

### Yeni Kategori Ekleme
```python
# database.py içinde default_categories listesine ekleyin
('Yeni Kategori', 'Açıklama')
```

### AI Model Güncelleme
```python
# roboflow_client.py içinde model_id'yi değiştirin
self.model_id = "yeni-model/1"
```

## Deploy

Detaylı deploy talimatları için [DEPLOY.md](DEPLOY.md) dosyasına bakın.

**Hızlı Başlangıç:**
1. GitHub'a yükle
2. Railway.app'e deploy et
3. Environment variables ekle
4. Frontend'te API URL'ini güncelle

## Özellikler

- 🤖 Roboflow AI ile otomatik soru kesme
- 📱 Mobil ve masaüstü kamera desteği
- 🎯 8. sınıf matematik müfredatı
- 📊 Kategori ve zorluk seviyesi filtreleme
- 💾 SQLite veritabanı
- 🔍 A, B, C, D şıklı cevaplama

## Teknolojiler

- **Backend**: Python, FastAPI, Roboflow, OpenCV
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite
- **AI**: Roboflow Hosted Image Inference

## Lisans

MIT License