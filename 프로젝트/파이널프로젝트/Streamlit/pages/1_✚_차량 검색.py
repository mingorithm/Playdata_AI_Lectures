import streamlit as st
from PIL import Image
import torch
from torchvision import transforms
from efficientnet_pytorch import EfficientNet
import pandas as pd
import os
import mysql.connector
# 모델 파일의 경로를 설정
model_file_path = '/Users/imhogyun/my_project/streamit_web_deploy/car_model(10epochs).pt'

# 모델 초기화 및 가중치 적용
model = EfficientNet.from_name('efficientnet-b0')
model.load_state_dict(torch.load(model_file_path, map_location=torch.device('cpu')))
model.eval()

st.title('자동차 예측')

predicted_class_name = ""  # 변수 초기화

uploaded_file = st.file_uploader(" ", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")  # convert("RGB") 추가
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    if st.button('검색'):
        # 이미지를 텐서로 변환하기 위한 전처리 파이프라인 설정
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(image)  # 이미지 -> 텐서 변환
        input_batch = input_tensor.unsqueeze(0)  # 배치 차원 추가

        with torch.no_grad():
            prediction = model(input_batch)
        _, predicted_idx = torch.max(prediction, 1)
        class_names = ["MAXCRUZ", "MORNING", "SONATA", "TIVOLI", "SM5", "STINGER", "MOHAVE", "CARNIVAL", "TUCSON", "CLIO"]
        predicted_class_name = class_names[predicted_idx.item()]
        st.write(f'차종: {predicted_class_name}')

# DBeaverFH 데이터베이스 연결 설정
def create_conn():
    conn = mysql.connector.connect(
        host="localhost",
        port='3306',
        user="root",
        password="zasx1452",
        database="sys"
    )
    return conn

def run_query(query):
    conn = create_conn()
    df = pd.read_sql_query(query,conn)
    return df
query = f"select * from car_infos where 차종='{predicted_class_name}'"
df1 = run_query(query)

# 각 차종에 대응하는 동영상 파일의 경로
video_files = {
    "MAXCRUZ": "/Users/imhogyun/my_project/streamit_web_deploy/KakaoTalk_Video_2023-09-19-17-31-43.mp4",
    "MORNING": "/Users/imhogyun/my_project/streamit_web_deploy/KakaoTalk_Video_2023-09-19-17-31-50.mp4",
    "SONATA": "/Users/imhogyun/my_project/streamit_web_deploy/2023-09-19_234547_02_SONATA.mp4",
    "TIVOLI": "/Users/imhogyun/my_project/streamit_web_deploy/2023-09-20_014926_03_TIVOLI.mp4",
    "STINGER": "/Users/imhogyun/my_project/streamit_web_deploy/2023-09-20_030154_05_STINGER.mp4",
    "CARNIVAL": "/Users/imhogyun/my_project/streamit_web_deploy/2023-09-20_035457_07_CARNIVAL.mp4",
    "CLIO": "/Users/imhogyun/my_project/streamit_web_deploy/2023-09-20_061309_09_CLIO.mp4",
    }

# 예측된 차종에 해당하는 동영상 URL 가져오기
predicted_video_file = video_files.get(predicted_class_name)
if predicted_video_file:
    st.video(predicted_video_file)
else:
    st.write("해당 차량의 영상이 없습니다.")

st.dataframe(df1)
banner_image_url = 'https://ifh.cc/g/vbmRgR.jpg'
# 이미지를 sidebar에 추가
st.sidebar.image(banner_image_url, width=200)
