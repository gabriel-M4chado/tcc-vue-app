# TCC
 Trabalho de conclusão de curso de Análise e Desenvolvimento de Sistemas (ADS)

# 🐓 Fair Value Prediction API

Um sistema de análise preditiva desenvolvido para determinar o valor justo a receber na indústria avícola, utilizando algoritmos de Machine Learning como Random Forest e Gradient Boosting. Esta aplicação fornece uma API construída com Flask, exposta via Ngrok, e uma interface frontend utilizando Vue.js com Vite.

## 📋 Índice
- [Pré-requisitos](https://github.com/gabriel-M4chado/tcc-vue-app?tab=readme-ov-file#-pr%C3%A9-requisitos)
- [Instalação](https://github.com/gabriel-M4chado/tcc-vue-app?tab=readme-ov-file#-instala%C3%A7%C3%A3o)
- [Configuração do Backend (Python ou Google Colab)](https://github.com/gabriel-M4chado/tcc-vue-app?tab=readme-ov-file#2-configura%C3%A7%C3%A3o-do-backend-python-ou-google-colab)
- [Configuração do Frontend (Vue.js)](https://github.com/gabriel-M4chado/tcc-vue-app?tab=readme-ov-file#3--configura%C3%A7%C3%A3o-do-frontend-vuejs)
- [Uso da API](https://github.com/gabriel-M4chado/tcc-vue-app?tab=readme-ov-file#4--uso-da-api)
- [Contribuição](#como-contribuir)

## 🛠 Pré-requisitos

Certifique-se de ter instalado em sua máquina:
- **Python 3.8+**
- **Node.js 14+** e **npm 6+**
- **Ngrok**
- **Google Colab** (opcional para execução no Jupyter Notebook)

> [!IMPORTANT]
> A planilha precisa conter os seguintes campos: 
> - Capacidade
> - peso
> - diasTratamento
> - bonificacaoEmpresa
> - Descontos
> - CreditoMortalidade
> - Temperatura
> - Umidade
> - QualidadeSolo
> - Infraestrutura
> - CA
> - ValorRecebido

<hr>

## 🚀 Instalação

### 1. Clone o repositório

```
git clone https://github.com/gabriel-M4chado/tcc-vue-app
cd tcc-vue-app/backend

```



### 2. 🔧Configuração do Backend (Python ou Google Colab)


#### 2.1. Configuração do Ambiente Virtual Python (Local)
> [!TIP]
> Arquivo testApiMachineLearning.py

##### 2.1.1. Criação do ambiente virtual
```
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

##### 2.1.2. Informar o token dentro do arquivo e execute o script
NGROK_AUTH_TOKEN=seu-token-ngrok 
```
python testApiMachineLearning.py
```

OBS: O servidor será iniciado em localhost:5000 e a URL pública do Ngrok será gerada automaticamente.

#### 2.2. Execução no Google Colab

<ol>
  <li>Abra o arquivo .ipynb diretamente no Google Colab.</li>
  <li>Faça o upload do arquivo fair_value_prediction.ipynb.</li>
  <li>Certifique-se de instalar as dependências conforme os comandos litados no arquivo <a href="https://github.com/gabriel-M4chado/tcc-vue-app/blob/main/scripts/testApiMachineLearning.ipynb">testApiMachineLearning.ipynb</a>, exemplo:</li>
</ol>

``` 
    !pip install Flask
```

<ol start="4">
  <li>Execute todas as células para iniciar o servidor Flask no ambiente do Colab.</li>
  <li>Copie a URL gerada pelo Ngrok para usar a API.</li>
</ol>

<hr>

### 3. 🌐 Configuração do Frontend (Vue.js)

#### 3.1. Instalar dependências do frontend

```
cd vue-app
npm install

```


### 4. 🎯 Uso da API

- Forma manual: 

Exemplo de requisição usando curl
```
curl -X POST http://localhost:5000/process -F 'file=@caminho/do/arquivo.csv'

```

Exemplo de resposta (JSON)

```
{
    "data_20000": [
        {"Capacidade": 20000, "ValorRecebido": 120000, "ValorPrevisto_GB": 118000, "ValorPrevisto_RF": 119000}
    ],
    "data_40000": [],
    "data_8000": []
}


```

- Usando via interface

Dentro do arquivo [App.vue](https://github.com/gabriel-M4chado/tcc-vue-app/blob/main/vue-app/src/App.vue) na constante ngrokUrl informe a URL do ngrok.
Após isso, execute:


```
npm run dev

```

Abra o navegador em http://localhost:5173 para acessar a aplicação.

<hr>

🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

### Como Contribuir:
<ol>
  <li>Faça um fork do projeto.</li>
  <li>Crie uma branch para sua feature (git checkout -b minha-feature).</li>
  <li>Commit suas mudanças (git commit -m 'Adicionei nova feature').</li>
  <li>Push para a branch (git push origin minha-feature).</li>
  <li>Abra um Pull Request.</li>
</ol>



