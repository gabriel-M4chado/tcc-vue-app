<template>
  <div class="file-upload">
    <div
      class="drag-area"
      @dragover.prevent
      @dragenter.prevent
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
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
export default {
  data() {
    return {
      file: null,
      errorMessage: '',
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
      if (!this.file) return;

      const formData = new FormData();
      formData.append('file', this.file);
      const ngrokUrl = 'https://a745-34-106-241-220.ngrok-free.app/';

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
      } catch (error) {
        this.errorMessage = 'Falha no upload do arquivo: ' + error.message;
      }
    },
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
</style>