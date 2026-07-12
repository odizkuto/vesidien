from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ket_qua_list = [] # Chuyển thành danh sách
    thong_bao = ""

    if request.method == 'POST':
        url = "https://lichcupdien.org/lich-cup-dien-an-giang"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            tat_ca = soup.get_text()
            
            da_xuat_hien = set()
            for dong in tat_ca.splitlines():
                dong_sach = dong.strip()
                if "phú tân" in dong_sach.lower():
                    if dong_sach not in da_xuat_hien and len(dong_sach) > 5:
                        # Tách dòng này thành các câu nhỏ dựa trên dấu chấm
                        # Sau đó thêm từng câu vào danh sách
                        cau_nho = [c.strip() for c in dong_sach.split('.') if c.strip()]
                        ket_qua_list.extend(cau_nho)
                        da_xuat_hien.add(dong_sach)
            
            if not ket_qua_list:
                thong_bao = "Hiện tại không tìm thấy thông tin cúp điện tại Phú Tân."
        except Exception as e:
            thong_bao = "Có lỗi xảy ra: " + str(e)
            
    return render_template('index.html', ket_qua_list=ket_qua_list, thong_bao=thong_bao)

if __name__ == '__main__':
    app.run(debug=True)
