import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
import os

# 데이터 읽어오기
url = "https://raw.githubusercontent.com/SongJuHo-0410/AI-ML_study/master/Used%20Car%20Price/car%20data.csv"
df = pd.read_csv(url)

# Label Encoding을 통해 카테고리컬 변수를 숫자로 변환
label_encoder = LabelEncoder()
df['Car_Name'] = label_encoder.fit_transform(df['Car_Name'])
df['Fuel_Type'] = label_encoder.fit_transform(df['Fuel_Type'])
df['Selling_type'] = label_encoder.fit_transform(df['Selling_type'])
df['Transmission'] = label_encoder.fit_transform(df['Transmission'])

# Feature와 Target 설정
X = df.drop(['Selling_Price'], axis=1)
y = df['Selling_Price']

# 학습 데이터와 테스트 데이터로 나누기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost 모델 정의 및 학습
model = XGBRegressor()
model.fit(X_train, y_train)

# 테스트 데이터로 예측
y_pred_best = model.predict(X_test)

# 평가 지표 출력
mae_best = mean_absolute_error(y_test, y_pred_best)
print(f'Mean Absolute Error with Best Hyperparameters: {mae_best}')

# 현재 작업 디렉토리 확인
current_directory = os.getcwd()
print("Current Directory:", current_directory)

# 파일명
filename = 'used_car_predict.model'

# 모델 저장
model.save_model(filename)

# 저장된 파일 경로 출력
saved_model_path = os.path.join(current_directory, filename)
print("Model saved at:", saved_model_path)