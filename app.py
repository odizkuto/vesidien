from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    url = "https://lichcupdien.org/lich-cup-dien-an-giang/" # Thay bằng link chính xác bạn đang dùng
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Tìm khối lớn chứa toàn bộ nội dung (dựa trên ảnh bạn chụp)
    container = soup.find('div', class_='lcd_detail_wrapper')
    
    danh_sach_lich = []
    # Giả định mỗi lịch cúp điện là một khối cha bao gồm các 'new_lcd_wrapper' bên trong
    # Nếu trang web chỉ có 1 danh sách dài, ta sẽ duyệt từng dòng
    blocks = container.find_all('div', class_='new_lcd_wrapper')
    
    # Logic nhóm dữ liệu (ví dụ cứ mỗi 5 dòng là 1 thông tin lịch mới)
    # Tùy thuộc vào trang web, bạn có thể cần điều chỉnh đoạn này
    for i in range(0, len(blocks), 5): 
        lich = {
            'dien_luc': blocks[i].find('span', class_='content_item_content_lcd_wrapper').text.strip(),
            'ngay': blocks[i+1].find('span', class_='content_item_content_lcd_wrapper').text.strip(),
            'thoi_gian': blocks[i+2].find('span', class_='content_item_content_lcd_wrapper').text.strip(),
            'khu_vuc': blocks[i+3].find('span', class_='content_item_content_lcd_wrapper').text.strip(),
            'ly_do': blocks[i+4].find('span', class_='content_item_content_lcd_wrapper').text.strip()
        }
        danh_sach_lich.append(lich)
            
    return render_template('index.html', lich_cup_dien=danh_sach_lich)

if __name__ == '__main__':
    app.run(debug=True)
