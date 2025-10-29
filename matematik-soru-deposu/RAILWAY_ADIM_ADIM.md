# Railway Deploy - Adım Adım Rehber

## Yöntem 1: GitHub ile (Önerilen)

### Ön Hazırlık: Git Kurulumu

1. **Git İndir:**
   - https://git-scm.com/download/win
   - İndir ve kur (varsayılan ayarlarla)

2. **Git Kontrol:**
   ```bash
   git --version
   ```

### GitHub'a Yükleme

1. **GitHub Hesabı Oluştur:**
   - https://github.com → Sign up
   - Email doğrula

2. **Yeni Repository Oluştur:**
   - GitHub'da sağ üst → "+" → "New repository"
   - Repository name: `matematik-soru-deposu`
   - Public seç
   - "Create repository" tıkla

3. **Projeyi GitHub'a Yükle:**
   ```bash
   cd matematik-soru-deposu
   git init
   git add .
   git commit -m "İlk commit"
   git branch -M main
   git remote add origin https://github.com/KULLANICI_ADIN/matematik-soru-deposu.git
   git push -u origin main
   ```

### Railway'e Deploy

1. **Railway Hesabı Oluştur:**
   - https://railway.app
   - "Login with GitHub" tıkla
   - GitHub ile giriş yap ve izin ver

2. **Yeni Proje Oluştur:**
   - Dashboard'da "New Project" tıkla
   - "Deploy from GitHub repo" seç
   - `matematik-soru-deposu` reposunu seç
   - Railway otomatik olarak deploy edecek

3. **Deploy İzle:**
   - "Deployments" sekmesinde ilerlemeyi izle
   - Yeşil ✓ görünce hazır demektir

4. **Domain Al:**
   - Settings → Networking
   - "Generate Domain" tıkla
   - URL'i kopyala (örn: `matematik-soru-deposu-production.up.railway.app`)

5. **Environment Variables (Opsiyonel):**
   - Variables sekmesi
   - Gerekirse ekle:
     - `PORT`: 8000
     - `ROBOFLOW_API_KEY`: 92Ra4ByBVqzPhUmGYZvB

## Yöntem 2: Railway CLI (Git Olmadan)

### Railway CLI Kurulumu

1. **Node.js Kur:**
   - https://nodejs.org → LTS versiyonu indir
   - Kur (varsayılan ayarlarla)

2. **Railway CLI Kur:**
   ```bash
   npm install -g @railway/cli
   ```

3. **Railway'e Giriş:**
   ```bash
   railway login
   ```
   - Tarayıcı açılacak, GitHub ile giriş yap

### Deploy

1. **Proje Klasörüne Git:**
   ```bash
   cd matematik-soru-deposu
   ```

2. **Railway Projesi Oluştur:**
   ```bash
   railway init
   ```
   - Proje adı gir: `matematik-soru-deposu`

3. **Deploy Et:**
   ```bash
   railway up
   ```

4. **Domain Al:**
   ```bash
   railway domain
   ```

5. **URL'i Göster:**
   ```bash
   railway status
   ```

## Yöntem 3: Manuel Zip Yükleme (En Kolay - Git Gerektirmez)

### Adımlar:

1. **Projeyi Zipla:**
   - `matematik-soru-deposu` klasörünü sağ tık
   - "Sıkıştır" veya "Compress to ZIP"
   - `matematik-soru-deposu.zip` oluştur

2. **Railway'e Git:**
   - https://railway.app → GitHub ile giriş
   - "New Project" → "Empty Project"

3. **Service Ekle:**
   - "New" → "Empty Service"
   - Service'e tıkla

4. **Dosyaları Yükle:**
   ⚠️ **Not:** Railway direkt zip yüklemeyi desteklemiyor
   Bu yüzden GitHub veya CLI kullanmalısın

## Önerilen: GitHub Yöntemi

En stabil ve kolay yöntem GitHub ile deploy. Adımlar:

### Hızlı Başlangıç:

1. ✅ Git kur: https://git-scm.com/download/win
2. ✅ GitHub hesabı aç: https://github.com
3. ✅ Yeni repo oluştur
4. ✅ Projeyi push et (yukarıdaki komutlar)
5. ✅ Railway'e git: https://railway.app
6. ✅ GitHub ile giriş yap
7. ✅ "Deploy from GitHub repo" seç
8. ✅ Domain al
9. ✅ Bitti! 🎉

## Sorun Giderme

### "git not found" Hatası
- Git'i kur: https://git-scm.com/download/win
- Bilgisayarı yeniden başlat
- Tekrar dene

### "Permission denied" Hatası
- GitHub'da SSH key ekle
- Veya HTTPS kullan (yukarıdaki komutlar HTTPS)

### Deploy Başarısız
- Logs'u kontrol et: Railway dashboard → Deployments → View Logs
- `requirements.txt` dosyasının doğru olduğundan emin ol
- Python versiyonunu kontrol et (`runtime.txt`)

### Port Hatası
- Railway otomatik olarak `PORT` environment variable sağlar
- `main.py`'de `$PORT` kullanıldığından emin ol

## Test

Deploy sonrası test et:

1. **Backend Test:**
   ```
   https://SENIN-URL.up.railway.app/debug/test-roboflow
   ```
   Sonuç: `{"success": true, ...}`

2. **API Test:**
   ```
   https://SENIN-URL.up.railway.app/kategoriler
   ```
   Sonuç: Kategoriler listesi

3. **Frontend'te Kullan:**
   `frontend/app.js` dosyasında:
   ```javascript
   const API_BASE = 'https://SENIN-URL.up.railway.app';
   ```

## Sonraki Adım: InfinityFree

Backend Railway'de çalıştıktan sonra:
1. Frontend'i InfinityFree'ye yükle
2. `app.js`'te Railway URL'ini kullan
3. Test et

Tebrikler! 🎉
