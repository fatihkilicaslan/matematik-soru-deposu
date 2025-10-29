const API_BASE = 'https://matematik-soru-deposu-production.up.railway.app';

// Webcam stream
let webcamStream = null;

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', function() {
    setupUploadArea();
    loadCategories();
    loadQuestions();
    detectDevice();
});

// Cihaz tipini tespit et
function detectDevice() {
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    if (isMobile) {
        // Mobil cihazda telefon kamerası butonunu göster
        document.getElementById('mobileCameraBtn').style.display = 'inline-block';
    }
}

// Upload alanı kurulumu
function setupUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const cameraInput = document.getElementById('cameraInput');

    // Dosya seçildiğinde
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            uploadFile(e.target.files[0]);
        }
    });

    // Mobil kamera ile çekildiğinde
    const mobileCamera = document.getElementById('mobileCamera');
    mobileCamera.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            uploadFile(e.target.files[0]);
        }
    });

    // Drag & Drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].type.startsWith('image/')) {
            uploadFile(files[0]);
        }
    });
}

// Dosya yükleme
async function uploadFile(file) {
    const loadingDiv = document.getElementById('loadingDiv');
    const resultDiv = document.getElementById('uploadResult');
    
    loadingDiv.style.display = 'block';
    resultDiv.innerHTML = '';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE}/upload-soru`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        
        if (result.success) {
            showUploadSuccess(result);
            loadQuestions(); // Listeyi yenile
        } else {
            showError('Yükleme başarısız: ' + result.message);
        }
    } catch (error) {
        showError('Bağlantı hatası: ' + error.message);
    } finally {
        loadingDiv.style.display = 'none';
    }
}

// Yükleme başarı mesajı
function showUploadSuccess(result) {
    const resultDiv = document.getElementById('uploadResult');
    resultDiv.innerHTML = `
        <div class="alert alert-success">
            <i class="fas fa-check-circle me-2"></i>
            <strong>${result.message}</strong>
            <div class="mt-3">
                <h6>🤖 AI Tespit Sonuçları:</h6>
                <div class="row">
                    ${result.questions.map((q, index) => `
                        <div class="col-md-3 mb-3">
                            <div class="card">
                                <img src="${API_BASE}/${q.cropped_image}" 
                                     class="card-img-top" 
                                     style="height: 150px; object-fit: contain; cursor: pointer;" 
                                     onclick="showImageModal('${API_BASE}/${q.cropped_image}')">
                                <div class="card-body p-2">
                                    <small class="text-muted">Soru #${index + 1}</small><br>
                                    <span class="badge ${q.confidence > 0.8 ? 'bg-success' : q.confidence > 0.6 ? 'bg-warning' : 'bg-danger'}">
                                        %${Math.round(q.confidence * 100)} güven
                                    </span>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <div class="mt-2">
                    <small class="text-muted">
                        💡 <strong>İpucu:</strong> %80+ güven oranı mükemmel, %60+ iyi, %60 altı düşük kalite demektir.
                    </small>
                </div>
            </div>
        </div>
    `;
}

// Hata mesajı
function showError(message) {
    const resultDiv = document.getElementById('uploadResult');
    resultDiv.innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
        </div>
    `;
}

// Kategorileri yükle
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE}/kategoriler`);
        const data = await response.json();
        
        const kategoriFilter = document.getElementById('kategoriFilter');
        const questionCategory = document.getElementById('questionCategory');
        
        // Filtreleri temizle
        kategoriFilter.innerHTML = '<option value="">Tüm Kategoriler</option>';
        questionCategory.innerHTML = '<option value="">Kategori Seçin</option>';
        
        // Kategorileri ekle
        data.kategoriler.forEach(kategori => {
            const option1 = new Option(kategori.name, kategori.name);
            const option2 = new Option(kategori.name, kategori.id);
            
            kategoriFilter.appendChild(option1);
            questionCategory.appendChild(option2);
        });
    } catch (error) {
        console.error('Kategori yükleme hatası:', error);
    }
}

// Soruları yükle
async function loadQuestions() {
    const kategori = document.getElementById('kategoriFilter').value;
    const status = document.getElementById('statusFilter').value;
    const zorluk = document.getElementById('difficultyFilter').value;
    
    try {
        let url = `${API_BASE}/sorular`;
        const params = new URLSearchParams();
        
        if (kategori) params.append('kategori', kategori);
        if (status) params.append('status', status);
        if (zorluk) params.append('zorluk', zorluk);
        
        if (params.toString()) {
            url += '?' + params.toString();
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        displayQuestions(data.sorular);
        
        // Soru sayısını güncelle
        document.getElementById('questionCount').textContent = `${data.sorular.length} soru`;
        
    } catch (error) {
        console.error('Soru yükleme hatası:', error);
        showError('Sorular yüklenirken hata oluştu');
    }
}

// Soruları görüntüle
function displayQuestions(sorular) {
    const questionsList = document.getElementById('questionsList');
    
    if (sorular.length === 0) {
        questionsList.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="fas fa-inbox fa-3x mb-3"></i>
                <p>Henüz soru bulunmuyor</p>
            </div>
        `;
        return;
    }
    
    questionsList.innerHTML = sorular.map(soru => `
        <div class="question-card">
            <div class="row">
                <div class="col-md-3">
                    <img src="${API_BASE}/${soru.cropped_image || soru.original_image}" 
                         class="question-image" 
                         alt="Soru ${soru.id}"
                         style="cursor: pointer;"
                         onclick="showImageModal('${API_BASE}/${soru.cropped_image || soru.original_image}')">
                </div>
                <div class="col-md-6">
                    <h6>Soru #${soru.id}</h6>
                    ${soru.soru_text ? `<p><strong>Soru:</strong> ${soru.soru_text}</p>` : ''}
                    ${soru.cevap ? `<p><strong>Cevap:</strong> ${soru.cevap}</p>` : ''}
                    ${soru.kategori_name ? `<span class="category-badge">${soru.kategori_name}</span>` : ''}
                    ${soru.zorluk_seviyesi ? `<span class="badge bg-secondary ms-2">${getDifficultyText(soru.zorluk_seviyesi)}</span>` : ''}
                </div>
                <div class="col-md-3 text-end">
                    <div class="mb-2">
                        <span class="badge ${getStatusBadgeClass(soru.status)}">${getStatusText(soru.status)}</span>
                    </div>
                    ${soru.detection_confidence ? `<small class="text-muted d-block">Güven: %${Math.round(soru.detection_confidence * 100)}</small>` : ''}
                    <small class="text-muted d-block">${formatDate(soru.created_at)}</small>
                    <div class="mt-2">
                        <button class="btn btn-sm btn-primary me-2" onclick="openAnswerModal(${soru.id})">
                            <i class="fas fa-edit me-1"></i>
                            ${soru.status === 'pending' ? 'Cevapla' : 'Düzenle'}
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteSoru(${soru.id})">
                            <i class="fas fa-trash me-1"></i>
                            Sil
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Cevap modalını aç
async function openAnswerModal(questionId) {
    try {
        const response = await fetch(`${API_BASE}/sorular`);
        const data = await response.json();
        const soru = data.sorular.find(s => s.id === questionId);
        
        if (!soru) {
            showError('Soru bulunamadı');
            return;
        }
        
        // Modal alanlarını doldur
        document.getElementById('questionId').value = soru.id;
        document.getElementById('modalQuestionImage').src = `${API_BASE}/${soru.cropped_image || soru.original_image}`;
        document.getElementById('answerText').value = soru.cevap || '';
        document.getElementById('questionCategory').value = soru.kategori_id || '';
        document.getElementById('difficultyLevel').value = soru.zorluk_seviyesi || 1;
        
        // Modalı göster
        const modal = new bootstrap.Modal(document.getElementById('answerModal'));
        modal.show();
        
    } catch (error) {
        console.error('Modal açma hatası:', error);
        showError('Soru bilgileri yüklenirken hata oluştu');
    }
}

// Cevabı kaydet
async function saveAnswer() {
    const questionId = document.getElementById('questionId').value;
    const formData = {
        soru_text: '',  // Soru metni artık kullanılmıyor
        cevap: document.getElementById('answerText').value,
        kategori_id: parseInt(document.getElementById('questionCategory').value),
        zorluk_seviyesi: parseInt(document.getElementById('difficultyLevel').value)
    };
    
    try {
        const response = await fetch(`${API_BASE}/soru/${questionId}/cevap`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Modalı kapat
            const modal = bootstrap.Modal.getInstance(document.getElementById('answerModal'));
            modal.hide();
            
            // Listeyi yenile
            loadQuestions();
            
            // Başarı mesajı
            showSuccess('Cevap başarıyla kaydedildi');
        } else {
            showError('Kaydetme hatası: ' + result.message);
        }
    } catch (error) {
        console.error('Kaydetme hatası:', error);
        showError('Bağlantı hatası: ' + error.message);
    }
}

// Yardımcı fonksiyonlar
function getStatusText(status) {
    const statusMap = {
        'pending': 'Cevap Bekliyor',
        'answered': 'Cevaplandı',
        'verified': 'Doğrulandı'
    };
    return statusMap[status] || status;
}

function getStatusBadgeClass(status) {
    const classMap = {
        'pending': 'bg-warning',
        'answered': 'bg-success',
        'verified': 'bg-info'
    };
    return classMap[status] || 'bg-secondary';
}

function getDifficultyText(level) {
    const diffMap = {
        1: 'Kolay',
        2: 'Orta',
        3: 'Zor'
    };
    return diffMap[level] || 'Bilinmiyor';
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('tr-TR') + ' ' + date.toLocaleTimeString('tr-TR', {hour: '2-digit', minute: '2-digit'});
}

function showSuccess(message) {
    const resultDiv = document.getElementById('uploadResult');
    resultDiv.innerHTML = `
        <div class="alert alert-success alert-dismissible fade show">
            <i class="fas fa-check-circle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
}

// Görsel büyütme modal'ı
function showImageModal(imageSrc) {
    document.getElementById('modalImage').src = imageSrc;
    const modal = new bootstrap.Modal(document.getElementById('imageModal'));
    modal.show();
}

// Webcam aç
async function openCamera() {
    try {
        const modal = new bootstrap.Modal(document.getElementById('webcamModal'));
        modal.show();
        
        // Webcam'i başlat
        webcamStream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        
        const video = document.getElementById('webcamVideo');
        video.srcObject = webcamStream;
        
        // Modal kapandığında stream'i durdur
        document.getElementById('webcamModal').addEventListener('hidden.bs.modal', function () {
            if (webcamStream) {
                webcamStream.getTracks().forEach(track => track.stop());
                webcamStream = null;
            }
        });
        
    } catch (error) {
        console.error('Kamera erişim hatası:', error);
        alert('Kamera erişimi reddedildi veya kamera bulunamadı. Lütfen tarayıcı izinlerini kontrol edin.');
    }
}

// Fotoğraf çek
function capturePhoto() {
    const video = document.getElementById('webcamVideo');
    const canvas = document.getElementById('webcamCanvas');
    const context = canvas.getContext('2d');
    
    // Canvas boyutunu video boyutuna ayarla
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Video frame'ini canvas'a çiz
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Canvas'ı blob'a çevir ve yükle
    canvas.toBlob(function(blob) {
        const file = new File([blob], `webcam_${Date.now()}.jpg`, { type: 'image/jpeg' });
        
        // Modal'ı kapat
        const modal = bootstrap.Modal.getInstance(document.getElementById('webcamModal'));
        modal.hide();
        
        // Dosyayı yükle
        uploadFile(file);
    }, 'image/jpeg', 0.95);
}

// Soru silme
async function deleteSoru(soruId) {
    if (!confirm('Bu soruyu silmek istediğinize emin misiniz?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/soru/${soruId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Listeyi yenile
            loadQuestions();
            
            // Başarı mesajı
            showSuccess('Soru başarıyla silindi');
        } else {
            showError('Silme hatası: ' + result.message);
        }
    } catch (error) {
        console.error('Silme hatası:', error);
        showError('Bağlantı hatası: ' + error.message);
    }
}