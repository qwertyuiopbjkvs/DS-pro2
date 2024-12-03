import flet as ft
import requests

# 地域リストを取得する関数
def get_area_list():
    url = "http://www.jma.go.jp/bosai/common/const/area.json"
    response = requests.get(url)
    return response.json()


# 選択した地域の天気予報を取得する関数
def get_weather_forecast(area_code):
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    response = requests.get(url)
    forecast_data = response.json()
    
    # 天気情報の取得（最初の地域を対象に）
    try:
        forecast = forecast_data[0]["timeSeries"][0]["areas"][0]["weather"]
    except KeyError:
        forecast = "天気情報が取得できませんでした。"
    
    return forecast

# Fletアプリケーション
def main(page: ft.Page):
    page.title = "気象庁 天気予報アプリ"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 地域リストを取得
    areas = get_area_list()

    # 地域選択用のドロップダウンリスト作成
    area_dropdown = ft.Dropdown(
        label="地域を選択", 
        options=[ft.dropdown.Option(area["name"], key=area["code"]) for area in areas],
        width=300
    )

    # 天気情報を表示するためのテキスト
    weather_text = ft.Text("", size=20, color="blue")

    # 地域が選択されたときに呼ばれる関数
    def on_area_change(e):
        selected_code = area_dropdown.value
        if selected_code:
            weather = get_weather_forecast(selected_code)
            weather_text.value = f"天気予報：{weather}"
        else:
            weather_text.value = "地域が選択されていません。"
        page.update()

    # ドロップダウンリストに変更イベントを追加
    area_dropdown.on_change = on_area_change

    # ページにUIコンポーネントを追加
    page.add(area_dropdown, weather_text)

# アプリを実行
ft.app(target=main)
