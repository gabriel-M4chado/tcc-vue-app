# -*- coding: utf-8 -*-
"""testApiMachineLearning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B5Qbqpv0lmoyjXK3lfU_akkS1HSgR2q0
"""

import subprocess
subprocess.check_call(["pip", "install", "Flask", "pyngrok", "pandas", "scikit-learn", "flask_cors"])

import getpass
import os
import threading
from flask import Flask, request, jsonify
from pyngrok import ngrok
from flask_cors import CORS # uso do cors no ambiente local

#imports para predição
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import joblib  # Para salvar e carregar modelos
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV #- Grid Search para ajustar hiperparâmetros
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso

app = Flask(__name__)
CORS(app)

# Caminhos para os modelos salvos
MODEL_GB_PATH = 'model_gb.joblib'
MODEL_RF_PATH = 'model_rf.joblib'
SCALER_PATH = 'scaler.joblib'

@app.route('/process', methods=['POST'])
def process_data():
    # Verificar se o arquivo foi enviado
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Carregar a planilha enviada
        data = pd.read_csv(file, delimiter=';')

        # Remover espaços extras ao redor dos nomes das colunas
        data.columns = data.columns.str.strip()

        # Converter as colunas que precisam de conversão
        data['CA'] = data['CA'].str.replace(',', '.').astype(float)
        data['peso'] = pd.to_numeric(data['peso'].str.replace(',', '.'), errors='coerce')
        data['ValorRecebido'] = pd.to_numeric(data['ValorRecebido'].str.replace(',', '.'), errors='coerce')
        data['bonificacaoEmpresa'] = pd.to_numeric(data['bonificacaoEmpresa'].str.replace(',', '.'), errors='coerce')
        data['CreditoMortalidade'] = pd.to_numeric(data['CreditoMortalidade'].str.replace(',', '.'), errors='coerce')
        data['Descontos'] = pd.to_numeric(data['Descontos'].str.replace(',', '.'), errors='coerce')

        # Criação de variáveis derivadas necessárias
        data['Temp_Umidade'] = data['Temperatura'] * data['Umidade']
        data['Temp_QualidadeSolo'] = data['Temperatura'] * data['QualidadeSolo']
        data['Temp_Infraestrutura'] = data['Temperatura'] * data['Infraestrutura']
        data['Umidade_QualidadeSolo'] = data['Umidade'] * data['QualidadeSolo']
        data['Umidade_Infraestrutura'] = data['Umidade'] * data['Infraestrutura']
        data['QualidadeSolo_Infraestrutura'] = data['QualidadeSolo'] * data['Infraestrutura']
        data['CA_peso'] = data['CA'] * data['peso']

        # Selecione as colunas que serão usadas como features
        features = [
            'Capacidade', 'peso', 'diasTratamento', 'bonificacaoEmpresa',
            'Descontos', 'CreditoMortalidade', 'Temperatura', 'Umidade',
            'QualidadeSolo', 'Infraestrutura', 'CA',
            'Temp_Umidade', 'Temp_QualidadeSolo', 'Temp_Infraestrutura',
            'Umidade_QualidadeSolo', 'Umidade_Infraestrutura',
            'QualidadeSolo_Infraestrutura', 'CA_peso'
        ]

        X = data[features]
        y = data['ValorRecebido']

        # Verificar se o scaler já existe
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
        else:
            scaler = StandardScaler()
            joblib.dump(scaler, SCALER_PATH)

        # Normalizando as características
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Verificando se os modelos já foram treinados e salvos
        if os.path.exists(MODEL_GB_PATH) and os.path.exists(MODEL_RF_PATH):
            model_gb = joblib.load(MODEL_GB_PATH)
            model_rf = joblib.load(MODEL_RF_PATH)
        else:
            # Dividisão dos dados
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

            # Treinar o modelo (Gradient Boosting)
            model_gb = GradientBoostingRegressor()
            model_gb.fit(X_train, y_train)

            # Treinar e avaliar o modelo Random Forest
            model_rf = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42)
            model_rf.fit(X_train, y_train)

            # Salvar os modelos treinados
            joblib.dump(model_gb, MODEL_GB_PATH)
            joblib.dump(model_rf, MODEL_RF_PATH)


        # Fazendo as previsões com os modelos salvos
        data['ValorPrevisto_GB'] = model_gb.predict(scaler.transform(X))
        data['ValorPrevisto_RF'] = model_rf.predict(scaler.transform(X))

        # Filtrando os dados por capacidade
        data_20000 = data[data['Capacidade'] == 20000]
        data_40000 = data[data['Capacidade'] == 40000]
        data_8000 = data[data['Capacidade'] == 8000]

        # Retornando os resultados como JSON
        return jsonify({
            'data_20000': data_20000.to_dict(orient='records'),
            'data_40000': data_40000.to_dict(orient='records'),
            'data_8000': data_8000.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN") #remova o comentário e informe o token ngrok

# Expor o app Flask usando ngrok
public_url = ngrok.connect(5000)
print(f" * ngrok URL: {public_url}")

# Rodar o Flask
app.run(port=5000)