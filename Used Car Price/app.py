from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from xgboost import XGBRegressor

app = Flask(__name__)

# 모델 불러오기
model_path = os.path.join("D:/git_hub/AI-ML_study/Used Car Price", "used_car_predict.model")
model = XGBRegressor()
model.load_model(model_path)

# 매핑 정보 읽기
def load_mapping(file_path):
    mapping = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split(':')
            mapping[key.strip()] = int(value.strip())
    return mapping

# 매핑 정보
Car_Name_mapping = load_mapping('D:/git_hub/AI-ML_study/Used Car Price/data/label/Car_Name_mapping.txt')
fuel_type_mapping = load_mapping('D:/git_hub/AI-ML_study/Used Car Price/data/label/Fuel_Type_mapping.txt')
selling_type_mapping = load_mapping('D:/git_hub/AI-ML_study/Used Car Price/data/label/Selling_type_mapping.txt')
transmission_mapping = load_mapping('D:/git_hub/AI-ML_study/Used Car Price/data/label/Transmission_mapping.txt')

# 예측 함수
def predict_price(new_data):
    new_data['Car_Name'] = [Car_Name_mapping[new_data['Car_Name'][0]]]
    new_data['Fuel_Type'] = [fuel_type_mapping[new_data['Fuel_Type'][0]]]
    new_data['Selling_type'] = [selling_type_mapping[new_data['Selling_type'][0]]]
    new_data['Transmission'] = [transmission_mapping[new_data['Transmission'][0]]]

    # DataFrame 생성
    input_data = pd.DataFrame(new_data)

    # 모델 예측
    predicted_price = model.predict(input_data)

    return predicted_price[0]

# Flask 라우트
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_data = {
            'Car_Name': [request.form['Car_Name']],
            'Year': [int(request.form['Year'])],
            'Present_Price': [float(request.form['Present_Price'])],
            'Driven_kms': [int(request.form['Driven_kms'])],
            'Fuel_Type': [request.form['Fuel_Type']],
            'Selling_type': [request.form['Selling_type']],
            'Transmission': [request.form['Transmission']],
            'Owner': [int(request.form['Owner'])]
        }

        print(new_data)

        predicted_price = predict_price(new_data)
        return render_template('index.html', prediction=predicted_price)

    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)
