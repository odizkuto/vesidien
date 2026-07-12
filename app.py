from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ket_qua = ""
    if request.method == 'POST':
        url = "https://lichcupdien.org/lich-cup-dien-an-giang/"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Sử dụng set để lưu các dòng đã xuất hiện, tránh lặp lại
            tat_ca = soup.get_text(separator='\n')
            da_xuat_hien = set()
            
            for dong in tat_ca.splitlines():
                dong_sach = dong.strip()
                # Kiểm tra nếu có "Phú Tân" và chưa từng xuất hiện trong bộ nhớ
                if "Phú Tân" in dong_sach and dong_sach not in da_xuat_hien:
                    ket_qua += dong_sach + "<br>"
                    da_xuat_hien.add(dong_sach)
            
            if not ket_qua:
                ket_qua = "Hiện tại không tìm thấy thông tin cúp điện tại Phú Tân."
        except Exception as e:
            ket_qua = "Có lỗi xảy ra khi tải dữ liệu: " + str(e)
            
    return render_template('index.html', ket_qua=ket_qua)

if __name__ == '__main__':
    app.run()
