from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ket_qua = ""
    if request.method == 'POST':
        url = "https://lichcupdien.org/lich-cup-dien-an-giang/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            tat_ca = soup.get_text()
            da_xuat_hien = set()
            danh_sach_loc = []
            
            for dong in tat_ca.splitlines():
                dong_sach = dong.strip()
                
                # Kiểm tra dòng có chứa "Phú Tân"
                co_phu_tan = "phú tân" in dong_sach.lower()
                # Kiểm tra dòng có chứa số (giờ giấc)
                co_chua_gio = re.search(r'\d', dong_sach)
                
                # Lọc: Có Phú Tân VÀ (có chứa giờ HOẶC là dòng quan trọng không bị trùng)
                if co_phu_tan:
                    if dong_sach not in da_xuat_hien and len(dong_sach) > 5:
                        danh_sach_loc.append(dong_sach)
                        da_xuat_hien.add(dong_sach)
            
            if danh_sach_loc:
                ket_qua = "<br>".join(danh_sach_loc)
            else:
                ket_qua = "Hiện tại không tìm thấy thông tin cúp điện tại Phú Tân."
                
        except Exception as e:
            ket_qua = "Có lỗi xảy ra khi tải dữ liệu: " + str(e)
            
    return render_template('index.html', ket_qua=ket_qua)

if __name__ == '__main__':
    app.run()
