import streamlit as st
from PIL import Image
import io
import requests
import numpy as np
import cv2

i=1

st.title('アイドルに変身アプリ')
"""
## WEBカメラを使ってリアルタイムであなたの顔をアイドルにします。
### 使い方
- なりたいキャラクター(アイドル)をサイドバーから選択してください。
- 開始ボタンをクリックすると、カメラが起動します。終了したい場合は終了ボタン**ダブルクリック**してください。
- システムの仕様上ダブルクリックが認識されない場合があります。その際はもう一度終了ボタンをクリックしてください。
"""
kyara = st.sidebar.radio("キャラクター",('あずさ', 'はるか','みお','かなこ','みく','なな'))


if kyara == "あずさ":
    kyara = 'azusa.png'
    x_param = 20
    y_param = 0
    size_param = 2
elif kyara == 'はるか':
    kyara = 'haruka.png' 
    x_param = 40
    y_param = 0
    size_param = 2
elif kyara == 'みお':
    kyara = 'mio.png'
    x_param = 50
    y_param = 0
    size_param = 2
elif kyara == 'かなこ':
    kyara = 'kanako.png' 
    x_param = -40
    y_param = -60
    size_param = 3
elif kyara == 'みく':
    kyara = 'miku.png' 
    x_param = 0
    y_param = -60
    size_param = 3
elif kyara == 'なな':
    kyara = 'nana.png' 
    x_param = 20
    y_param = -80
    size_param = 3



on = st.button('開始')

image_loc = st.empty()

off = st.button('終了(ダブルクリック)')
print(i)
print("ループ外")

@st.cache
def overlayImage(src, overlay, location):
    overlay_height, overlay_width = overlay.shape[:2]

    # 背景をPIL形式に変換
    src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    pil_src = Image.fromarray(src)
    pil_src = pil_src.convert('RGBA')

    # オーバーレイをPIL形式に変換
    overlay = cv2.cvtColor(overlay, cv2.COLOR_BGRA2RGBA)
    pil_overlay = Image.fromarray(overlay)
    pil_overlay = pil_overlay.convert('RGBA')

    # 画像を合成
    pil_tmp = Image.new('RGBA', pil_src.size, (255, 255, 255, 0))
    pil_tmp.paste(pil_overlay, location, pil_overlay)
    result_image = Image.alpha_composite(pil_src, pil_tmp)

    # OpenCV形式に変換
    return cv2.cvtColor(np.asarray(result_image), cv2.COLOR_RGBA2BGRA)


if on:
    i=0
    print(i)
    print("ループ内")

    cap = cv2.VideoCapture()

    cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    while(cap.isOpened()):
        # フレームを取得
        ret, frame = cap.read()

        #frame = cv2.resize(frame, (1100,600))
        #time.sleep(0.01)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = cascade.detectMultiScale(gray,
                                        # detector options
                                        scaleFactor = 1.1,
                                        minNeighbors = 5,
                                        minSize = (24, 24))
        for (x, y, w, h) in faces:
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            img = cv2.imread(kyara, cv2.IMREAD_UNCHANGED)
            #画像重ねる。位置調整。サイズ調整
            size = (w*size_param,h*size_param)
            img = cv2.resize(img , size)
            
            x = int(x/2+x_param)
            y = int(y/2+y_param)
            # 画像のオーバーレイ
            frame = overlayImage(frame , img, (x, y))
        # フレームを表示
        #cv2.imshow("Flame", frame)

        #opencv画像から変換
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = frame.convert('RGBA')

        image_loc.image(frame)
        cv2.moveWindow('Flame', 100, 200)
    cap.release()
    #cv2.destroyAllWindows()

"""
>制作者:うーたん  
 [twitter](https://twitter.com/u____tan_)  
 [ポートフォリオサイト](http://utan.php.xdomain.jp/)
"""


