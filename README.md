# Guia do Projeto

## Descrição Do Projeto

O sistema recebe as imagens de uma câmera comum, lê um QR Code que contém as informações do funcionário (nome, curso e validade), valida os dados e, se estiver tudo certo, libera o acesso. Caso haja problema (curso vencido), envia alerta ao supervisor e aciona a sirene. Tudo está integrado a um dashboard que atualiza as imagens e o diagnóstico final em tempo real

## Funcionalidades

- Leitura de QR Code contendo informações do funcionário.
- Validação de curso e validade do treinamento.
- Detecção em tempo real dos EPIs usando YOLOv8.
- Alerta visual e textual sobre autorização do funcionário.
- Desenho de caixas delimitadoras e nomes dos EPIs detectados no vídeo.

## Tecnologias

- Python 3.8+
- OpenCV
- Roboflow
- YOLOv8 (Ultralytics)
- JSON para leitura de dados do QR Code

## Requisitos

- Python 3.8 ou superior
- Pip
- Biblioteca `ultralytics` (YOLOv8)
- OpenCV
- Roboflow API Key

## Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seuusuario/epi-qr-detector.git
cd epi-qr-detector
```

2. Instale as dependências:

```bash
pip install ultralytics opencv-python roboflow
```

3. Baixe o dataset do Roboflow e treine o modelo:

- Faça o download do dataset no Roboflow (Yolov8)
- Treine o modelo localmente ou use o Roboflow Train Cloud
- Certifique-se de gerar o best.pt no caminho runs/detect/train/best.pt

## Uso

1. Adicione sua Roboflow API Key no código:

```bash
rf = Roboflow(api_key="SUA_API_KEY")
```

2. Ajuste o caminho do modelo YOLO:

```bash
caminho_modelo = "runs/detect/train/best.pt"
```

3. Execute o código principal:

```bash
python main.py
```

4. Aponte a câmera para o QR Code do funcionário. O sistema verificará:

- Curso válido
- Validade do curso
- Presença de todos os EPIs obrigatórios

5. O programa exibirá mensagens no terminal e desenhará caixas nos EPIs detectados.

## Personalização

- EPIs obrigatórios: altere a lista no código:

```bash
epis_obrigatorios = ["capacete", "luvas", "mascara"]
```

- Câmera: altere o índice em cv2.VideoCapture(0) caso tenha múltiplas câmeras.

## Observações

- Para melhor performance, é recomendado usar GPU.
- O modelo deve ser treinado com imagens do ambiente real de uso dos EPIs.
- A validação ocorre em tempo real, mas pode ser otimizada para rodar a cada N frames.
