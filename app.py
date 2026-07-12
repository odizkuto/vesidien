from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ket_qua = ""
    if request.method == 'POST':
        # Cào dữ liệu từ trang lịch cúp điện
        url = "https://lichcupdien.org/lich-cup-dien-an-giang"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Lấy toàn bộ text và tìm Phú Tân
            tat_ca = soup.get_text()
            for dong in tat_ca.splitlines():
                if "Phú Tân" in dong:
                    ket_qua += dong.strip() + "<br>"
            
            if not ket_qua:
                ket_qua = "Hiện tại không tìm thấy thông tin cúp điện tại Phú Tân."
        except Exception as e:
            ket_qua = "Có lỗi xảy ra khi tải dữ liệu: " + str(e)
            
    return render_template('index.html', ket_qua=ket_qua)

if __name__ == '__main__':
    app.run()
