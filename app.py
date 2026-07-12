from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ket_qua = ""
    if request.method == 'POST':
        # Giữ nguyên URL gốc của bạn
        url = "https://lichcupdien.org/lich-cup-dien-an-giang"
        
        # Thêm User-Agent đầy đủ để Render không bị trang gốc chặn
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
            # Ép kiểu dữ liệu về UTF-8 để không bị lỗi font tiếng Việt
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Sử dụng lại cách lấy text gốc của bạn để đảm bảo quét sạch dữ liệu
            tat_ca = soup.get_text()
            
            da_xuat_hien = set() # Giỏ chứa các dòng đã quét qua để chống trùng lặp
            danh_sach_loc = []
            
            for dong in tat_ca.splitlines():
                dong_sach = dong.strip()
                
                # Chuyển hết về chữ thường (.lower()) khi so sánh để tránh sót chữ "Phú Tân", "phú tân" hay "PHÚ TÂN"
                if "phú tân" in dong_sach.lower():
                    # Chỉ lấy dòng chưa tồn tại và loại bỏ các dòng chữ quá ngắn (rác)
                    if dong_sach not in da_xuat_hien and len(dong_sach) > 5:
                        danh_sach_loc.append(dong_sach)
                        da_xuat_hien.add(dong_sach)
            
            # Xuất kết quả ra giao diện
            if danh_sach_loc:
                ket_qua = "<br>".join(danh_sach_loc)
            else:
                ket_qua = "Hiện tại không tìm thấy thông tin cúp điện tại Phú Tân."
                
        except Exception as e:
            ket_qua = "Có lỗi xảy ra khi tải dữ liệu: " + str(e)
            
    return render_template('index.html', ket_qua=ket_qua)

if __name__ == '__main__':
    app.run()
