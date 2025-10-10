# Safe Opear

Sistema integrado de leitura de QR Code com detecção de Equipamentos de Proteção Individual (EPIs) usando YOLOv8.
O projeto valida se um funcionário possui o curso correto, está dentro da validade e se utiliza todos os EPIs obrigatórios, enviando as informações em tempo real para um dashboard web.

## Funcionalidades

- Leitura de QR Code com dados do funcionário (nome, curso, validade);
- Validação automática do curso e da validade;
- Detecção em tempo real dos EPIs via YOLOv8;
- Envio automático das informações para um backend Flask;
- Dashboard web que exibe o status atualizado de cada funcionário e dos EPIs;
- Feedback visual no vídeo com caixas e texto sobre o status da autorização.

## Tecnologias Utilizadas

- Python 3.8+;
- Flask (backend);
- OpenCV;
- Ultralytics YOLOv8;
- Roboflow;
- Pillow (PIL);
- HTML + JavaScript;
- JSON para leitura de dados do QR Code.

## Estrutura do projeto

```bash
epi-qr-detector/
│
├── safe_opear.py       # Leitura de QR Code e detecção YOLO
├── app.py              # Servidor Flask (recebe dados e fornece ao dashboard)
├── templates/
│   └── index.html      # Dashboard web em tempo real
├── runs/
│   └── detect/
│       └── train/
│           └── weights/
│               └── best.pt  # Modelo treinado YOLOv8
└── src/
    └── css/
        └── styles.css       # Estilo do dashboard
```

## Requisitos

- Python 3.8 ou superior;
- Pip instalado;
- Dependências:
```bash
pip install ultralytics opencv-python pillow flask requests
```

## Treinamento do Modelo (YOLOv8)

1. Crie ou baixe um dataset com as classes de EPIs (capacete, óculos, luvas etc.);
2. Faça upload no Roboflow (ou use localmente);
3. Treine o modelo e gere o arquivo best.pt no caminho:
```bash
main/runs/detect/train/weights/best.pt
```

## Uso

1. Inicie o servidor Flask

```bash
python app.py
```
O dashboard estará disponível em:
http://localhost:5000

2. Execute o detector:

```bash
python main/safe_opear.py
```

3. Aponte a câmera para o QR Code do funcionário

O sistema fará automaticamente:
- Validação de curso e validade;
- Detecção dos EPIs obrigatórios;
- Envio dos resultados para o dashboard.

## Personalização

- EPIs obrigatórios:
Edite no arquivo:
```bash
epis_ordem = ["helmet", "glasses"]
```
(Certifique-se de usar as mesmas classes que o modelo YOLO detecta.)

- Câmera:
Se você tiver mais de uma, altere:
```bash
cap = cv2.VideoCapture(0)
```

- Servidor remoto:
Para enviar os dados a outro servidor, altere no safe_opear.py:
```bash
requests.post("http://localhost:5000/registro", json=dados)
```

## Dashboard em Tempo Real

O arquivo index.html exibe:
- Nome, curso e validade do funcionário;
- Status atualizado dos EPIs (OK/FALTANDO);
- Última atualização (data e hora);
A página atualiza automaticamente a cada 1 segundo usando JavaScript.

## Licença

Este projeto é livre para uso educacional e pode ser modificado conforme necessário.
Créditos para a comunidade Ultralytics YOLOv8 e Roboflow.