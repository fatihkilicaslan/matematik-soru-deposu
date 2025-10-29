import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path="matematik_sorular.db"):
        self.db_path = db_path
        
    def get_connection(self):
        """Veritabanı bağlantısı"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Dict-like access
        return conn
    
    def create_tables(self):
        """Tabloları oluştur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Kategoriler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kategoriler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sorular tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sorular (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_image TEXT NOT NULL,
                cropped_image TEXT,
                soru_text TEXT,
                cevap TEXT,
                kategori_id INTEGER,
                zorluk_seviyesi INTEGER DEFAULT 1,
                detection_confidence REAL,
                bbox TEXT,  -- JSON format
                status TEXT DEFAULT 'pending',  -- pending, answered, verified
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (kategori_id) REFERENCES kategoriler (id)
            )
        ''')
        
        # 8. Sınıf Matematik Konuları
        default_categories = [
            ('Çarpanlar ve Katlar', 'EBOB, EKOK, asal çarpanlar'),
            ('Üslü İfadeler', 'Üslü sayılar ve işlemler'),
            ('Kareköklü İfadeler', 'Karekök alma ve işlemler'),
            ('Veri Analizi', 'Grafik okuma, ortalama, medyan'),
            ('Basit Olayların Olma Olasılığı', 'Olasılık hesaplama'),
            ('Cebirsel İfadeler ve Özdeşlikler', 'Çarpanlara ayırma, özdeşlikler'),
            ('Doğrusal Denklemler', 'Birinci dereceden denklemler'),
            ('Eşitsizlikler', 'Birinci dereceden eşitsizlikler'),
            ('Üçgenler', 'Üçgen çeşitleri, açılar, kenarlar'),
            ('Eşlik ve Benzerlik', 'Eş ve benzer şekiller'),
            ('Dönüşüm Geometrisi', 'Öteleme, yansıma, dönme'),
            ('Geometrik Cisimler', 'Prizma, piramit, silindir, koni, küre')
        ]
        
        for name, desc in default_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO kategoriler (name, description) 
                VALUES (?, ?)
            ''', (name, desc))
        
        conn.commit()
        conn.close()
    
    def insert_soru(self, soru_data: Dict) -> int:
        """Yeni soru ekle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sorular (
                original_image, cropped_image, detection_confidence, 
                bbox, status
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            soru_data['original_image'],
            soru_data['cropped_image'],
            soru_data['detection_confidence'],
            json.dumps(soru_data['bbox']),
            soru_data['status']
        ))
        
        soru_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return soru_id
    
    def get_sorular(self, kategori: str = None, status: str = None, zorluk: int = None) -> List[Dict]:
        """Soruları getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT s.*, k.name as kategori_name 
            FROM sorular s 
            LEFT JOIN kategoriler k ON s.kategori_id = k.id
            WHERE 1=1
        '''
        params = []
        
        if kategori:
            query += ' AND k.name = ?'
            params.append(kategori)
            
        if status:
            query += ' AND s.status = ?'
            params.append(status)
        
        if zorluk:
            query += ' AND s.zorluk_seviyesi = ?'
            params.append(zorluk)
            
        query += ' ORDER BY s.created_at DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        sorular = []
        for row in rows:
            soru = dict(row)
            if soru['bbox']:
                soru['bbox'] = json.loads(soru['bbox'])
            sorular.append(soru)
        
        conn.close()
        return sorular
    
    def update_soru_cevap(self, soru_id: int, cevap_data: Dict):
        """Soruya cevap ekle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sorular 
            SET soru_text = ?, cevap = ?, kategori_id = ?, 
                zorluk_seviyesi = ?, status = 'answered',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            cevap_data.get('soru_text', ''),
            cevap_data.get('cevap', ''),
            cevap_data.get('kategori_id'),
            cevap_data.get('zorluk_seviyesi', 1),
            soru_id
        ))
        
        conn.commit()
        conn.close()
    
    def get_kategoriler(self) -> List[Dict]:
        """Kategorileri getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM kategoriler ORDER BY name')
        rows = cursor.fetchall()
        
        kategoriler = [dict(row) for row in rows]
        conn.close()
        return kategoriler
    
    def get_soru_by_id(self, soru_id: int) -> Optional[Dict]:
        """ID'ye göre soru getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.*, k.name as kategori_name 
            FROM sorular s 
            LEFT JOIN kategoriler k ON s.kategori_id = k.id
            WHERE s.id = ?
        ''', (soru_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            soru = dict(row)
            if soru['bbox']:
                soru['bbox'] = json.loads(soru['bbox'])
            return soru
        return None
    
    def delete_soru(self, soru_id: int):
        """Soruyu sil"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sorular WHERE id = ?', (soru_id,))
        
        conn.commit()
        conn.close()