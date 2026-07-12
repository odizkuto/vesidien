from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    ket_qua = ""

    if request.method == "POST":

        url = "https://lichcupdien.org/lich-cup-dien-an-giang"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:

            response = requests.get(url, headers=headers, timeout=15)
            response.encoding = "utf-8"

            soup = BeautifulSoup(response.text, "html.parser")

            ds = soup.find_all("div", class_="lcd_detail_wrapper")

            html = ""

            tong = 0

            for item in ds:

                data = {}

                rows = item.find_all("div", class_="new_lcd_wrapper")

                for row in rows:

                    tieu_de = row.find(
                        "span",
                        class_="title_item_lcd_wrapper"
                    )

                    noi_dung = row.find(
                        "span",
                        class_="content_item_content_lcd_wrapper"
                    )

                    if tieu_de and noi_dung:

                        key = tieu_de.get_text(strip=True).replace(":", "")
                        value = noi_dung.get_text(" ", strip=True)

                        data[key] = value

                text = " ".join(data.values()).lower()

                if "phú tân" in text:

                    tong += 1

                    html += f"""
                    <div style="
                    border:1px solid #ddd;
                    border-radius:10px;
                    padding:15px;
                    margin-bottom:20px;
                    background:white;
                    ">

                    <h3 style="color:#2563eb;">
                    📍 {data.get("Khu vực","")}
                    </h3>

                    <p><b>⚡ Điện lực:</b>
                    {data.get("Điện lực","")}</p>

                    <p><b>📅 Ngày:</b>
                    {data.get("Ngày","")}</p>

                    <p><b>🕒 Thời gian:</b>
                    {data.get("Thời gian","")}</p>

                    <p><b>📝 Lý do:</b>
                    {data.get("Lý do","")}</p>

                    <p><b>📌 Trạng thái:</b>
                    {data.get("Trạng thái","")}</p>

                    </div>
                    """

            if tong == 0:

                ket_qua = "Không có lịch cúp điện tại huyện Phú Tân."

            else:

                ket_qua = f"""
                <h2>🔎 Tìm thấy {tong} khu vực cúp điện tại Phú Tân</h2>
                {html}
                """

        except Exception as e:

            ket_qua = str(e)

    return render_template("index.html", ket_qua=ket_qua)


if __name__ == "__main__":
    app.run(debug=True)
