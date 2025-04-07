// Script para verificar e restaurar o modelo quando necessário
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// Caminho para o modelo e diretórios
const PROJECT_ROOT = path.resolve(__dirname, '../..');
const MODEL_PATH = path.join(PROJECT_ROOT, 'src/model/modelo_classificacao.pkl');
const DATASET_PATH = path.join(PROJECT_ROOT, 'data/dataset_tickets_prioridade.csv');

console.log('Iniciando serviço de verificação do modelo...');
console.log(`Diretório raiz do projeto: ${PROJECT_ROOT}`);
console.log(`Caminho do modelo: ${MODEL_PATH}`);
console.log(`Caminho do dataset: ${DATASET_PATH}`);

// Função para verificar e restaurar o modelo
function checkAndRestoreModel() {
  console.log(`[${new Date().toISOString()}] Verificando modelo...`);
  
  try {
    if (!fs.existsSync(MODEL_PATH)) {
      console.log('Modelo não encontrado. Iniciando processo de restauração...');
      
      // Verifica se existe o dataset
      if (!fs.existsSync(DATASET_PATH)) {
        console.log('Dataset não encontrado. Gerando dados sintéticos...');
        exec('python -m src.model.gerador_dados_sinteticos', { cwd: PROJECT_ROOT }, (error, stdout, stderr) => {
          if (error) {
            console.error(`Erro ao gerar dados: ${error.message}`);
            return;
          }
          console.log('Dados gerados com sucesso.');
          trainModel();
        });
      } else {
        console.log('Dataset encontrado. Treinando modelo...');
        trainModel();
      }
    } else {
      console.log('Modelo verificado e está presente.');
    }
  } catch (err) {
    console.error(`Erro ao verificar modelo: ${err}`);
  }
}

function trainModel() {
  exec('python -m src.model.treinar_modelo', { cwd: PROJECT_ROOT }, (error, stdout, stderr) => {
    if (error) {
      console.error(`Erro ao treinar modelo: ${error.message}`);
      return;
    }
    console.log('Modelo treinado com sucesso.');
    
    // Verifica se o modelo foi gerado corretamente
    if (fs.existsSync(MODEL_PATH)) {
      console.log('Modelo restaurado com sucesso!');
    } else {
      console.error('Falha ao restaurar o modelo.');
    }
  });
}

// Verificar o modelo na inicialização
checkAndRestoreModel();

// Verificar o modelo periodicamente (a cada 1 hora)
const INTERVAL = 60 * 60 * 1000; // 1 hora em milissegundos
setInterval(checkAndRestoreModel, INTERVAL);

// Manter o processo rodando
process.on('SIGINT', () => {
  console.log('Serviço de verificação do modelo encerrado.');
  process.exit(0);
}); 