from PIL import Image, ImageDraw, ImageFont
import os

def create_test_math_image():
    """Test için basit matematik soruları içeren görsel oluştur"""
    
    # Beyaz arka plan
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Varsayılan font kullan
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        title_font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # Başlık
    draw.text((50, 30), "MATEMATİK SORULARI", fill='black', font=title_font)
    
    # Sorular
    questions = [
        "1) 2x + 5 = 13 denklemini çözünüz.",
        "2) 3² + 4² = ?",
        "3) ∫(2x + 1)dx = ?",
        "4) Sin(30°) = ?",
        "5) Bir üçgenin alanı 24 cm², tabanı 8 cm ise yüksekliği kaç cm'dir?"
    ]
    
    y_position = 100
    for question in questions:
        draw.text((50, y_position), question, fill='black', font=font)
        y_position += 80
    
    # Dosyayı kaydet
    os.makedirs("uploads", exist_ok=True)
    image_path = "uploads/test_math_questions.jpg"
    image.save(image_path)
    print(f"Test görsel oluşturuldu: {image_path}")
    return image_path

if __name__ == "__main__":
    create_test_math_image()