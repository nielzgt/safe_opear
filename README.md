# Guia do Projeto

## Descrição Do Projeto

O sistema recebe as imagens de uma câmera comum, lê um QR Code que contém as informações do funcionário (nome, curso e validade), valida os dados e, se estiver tudo certo, libera o acesso. Caso haja problema (curso vencido), envia alerta ao supervisor e aciona a sirene. Tudo está integrado a um dashboard que atualiza as imagens e o diagnóstico final em tempo real

## Aplicativos E Softwares Para Baixar

• Python 3.x
• VS Code
• Arduino IDE
• GitHub (para hospedar o dashboard HTML/CSS/JS)

## Bibliotecas Python Para Instalar

terminal/cmd :
pip install flask opencv-python pyzbar pillow qrcode[pil] pyserial

## Estrutura Do Projeto


1. Captura de imagem com OpenCV (Python)
2. Leitura do QR Code com pyzbar
3. Validação da data de validade (comparação com data atual)
4. API Flask para centralizar o processamento
5. Dashboard em HTML/CSS/JS (hospedado no GitHub Pages)
6. Integração com Arduino/ESP32 usando PySerial para ativar sirene

## Plano De Implementação (Passo A Passo)


1. Preparar ambiente: instalar Python, VS Code, bibliotecas.
2. Gerar QR Codes de funcionários.
3. Criar script para abrir câmera e ler QR Codes.
4. Validar se o curso está dentro da validade.
5. Criar dashboard web simples para mostrar status.
6. Integrar com sirene via Arduino/ESP32.
7. Hospedar dashboard no GitHub Pages e fazer teste final.

## Dicas Importantes

• Testar cada parte separadamente (QR Code, câmera, dashboard).
• Usar JSON para facilitar leitura dos dados.
• Manter o código organizado em pastas (api/, dashboard/, testes/).
• Fazer backup do projeto no GitHub para não perder o código.

## Fluxo Do Sistema

Câmera → Leitura QR Code (Python) → Validação de Dados → Dashboard (HTML/CSS/JS) e Sirene/Alerta