<template>
  <div class="file-upload">
    <div class="drag-area" @dragover.prevent @dragenter.prevent @drop.prevent="handleDrop" @click="triggerFileInput">
      <p>Arraste e solte o arquivo CSV aqui ou clique para selecionar</p>
      <input type="file" ref="fileInput" @change="handleFileUpload" accept=".csv" />
    </div>
  
    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>
  
    <div v-if="file && !errorMessage">
      <p>Arquivo: {{ file.name }}</p>
      <button @click="uploadFile">Enviar Planilha</button>
    </div>
  </div>
</template>

<script>

import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  data() {
    return {
      file: null,
      errorMessage: ''
    };
  },
  methods: {
    handleDrop(event) {
      const files = event.dataTransfer.files;
      this.validateFile(files[0]);
    },
    handleFileUpload(event) {
      const files = event.target.files;
      this.validateFile(files[0]);
    },
    validateFile(file) {
      if (file && file.name.endsWith('.csv')) {
        this.errorMessage = '';
        this.file = file;
      } else {
        this.file = null;
        this.errorMessage = 'Por favor, envie um arquivo CSV separado por ponto e vírgula.';
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    async uploadFile() {
      if (!this.file) {
        return;
      };

      const formData = new FormData();
      formData.append('file', this.file);
      const ngrokUrl = 'https://f9d3-34-125-34-90.ngrok-free.app/';

      try {
        const response = await fetch(`${ngrokUrl}process`, {
          method: 'POST',
          body: formData,
        });

        const result = await response.json();

        console.log('Resultado da API:', result);

        if (!response.ok) {
          throw new Error('Erro ao enviar o arquivo');
        }

        alert('Arquivo enviado com sucesso!');

        this.file = null;
        this.$refs.fileInput.value = '';

        if (result.hasOwnProperty("data_20000") || result.hasOwnProperty("data_40000") || result.hasOwnProperty("data_8000")) {
          this.generateCharts(result);
        } else {
          this.errorMessage = 'Nenhum dado encontrado.';
        }
      } catch (error) {
        this.errorMessage = `Falha no upload do arquivo: ${error.message}`;
      }
    },
    generateCharts(data) {
      let canvasElements = document.querySelectorAll('canvas');

      if (canvasElements) {
        canvasElements.forEach(canvas => canvas.remove());
      }

      Object.keys(data).forEach(key => {
        const dataset = data[key];

        // Extração dos valores "Capacidade", "ValorRecebido", "ValorPrevisto_GB" e "ValorPrevisto_RF" para o gráfico
        const capacities = dataset.map(item => item.Capacidade);
        const receivedValues = dataset.map(item => item.ValorRecebido);
        const predictedGBValues = dataset.map(item => item.ValorPrevisto_GB);
        const predictedRFValues = dataset.map(item => item.ValorPrevisto_RF);

        const ctx = document.createElement('canvas');  // Cria um gráfico conforme cada capacidade
        document.body.appendChild(ctx);
        ctx.getContext('2d');

        new Chart(ctx, {
          type: 'line',
          data: {
            labels: capacities,
            datasets: [
              {
                label: 'Valor Recebido',
                data: receivedValues,
                borderColor: 'blue',
                backgroundColor: 'rgba(0, 0, 255, 0.1)',
                borderWidth: 2,
                fill: true
              },
              {
                label: 'Valor previsto pelo modelo GB',
                data: predictedGBValues,
                borderColor: 'green',
                backgroundColor: 'rgba(0, 255, 0, 0.1)',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: true
              },
              {
                label: 'Valor previsto pelo modelo RF',
                data: predictedRFValues,
                borderColor: 'red',
                backgroundColor: 'rgba(255, 0, 0, 0.1)',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: true
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Capacidade'
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'Valor'
                },
                beginAtZero: true,
                suggestedMin: 0,
                suggestedMax: 40000  // Ajustar o eixo Y para o intervalo correto
              }
            },
            plugins: {
              legend: {
                display: true,
                position: 'top'
              },
              title: {
                display: true,
                text: `Cash Flow - ${key} - Valor Recebido vs Valor previsto pelo modelo`  // Título dinâmico baseado na capacidade
              },
              tooltip: {
                mode: 'index',
                intersect: false
              }
            }
          }
        });
      });
    }
  },
};
</script>

<style>
.file-upload {
  border: 2px dashed #ccc;
  padding: 20px;
  width: 300px;
  text-align: center;
}

.drag-area {
  cursor: pointer;
  padding: 20px;
  border-radius: 5px;
  background-color: #f9f9f9;
}

input[type="file"] {
  display: none;
}

.error {
  color: red;
  margin-top: 10px;
}

canvas {
  max-width: 100%;
  height: 50vh;
  max-height: 900px;
}
</style>