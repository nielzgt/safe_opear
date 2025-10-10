# -*- coding: utf-8 -*-
import cv2
import json
from datetime import datetime
from ultralytics import YOLO
import time
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import requests

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

detector = cv2.QRCodeDetector()
ultimo_dado = ""
model = YOLO("main/runs/detect/train/weights/best.pt")

epis_ordem = ["helmet", "glasses", "vest", "gloves"]
ultima_deteccao = 0
boxes_atuais = []

mensagem = "Aponte o QR Code para a câmera"
fonte_ttf = "C:/Windows/Fonts/arial.ttf"
fonte_pillow = ImageFont.truetype(fonte_ttf, 20)

def enviar_para_dashboard(dados):
    try:
        requests.post("http://localhost:5000/registro", json=dados, timeout=1)
    except Exception as e:
        print("Erro ao enviar para dashboard:", e)

def draw_text_pillow(img_cv2, text, pos, font, text_color, border_color=(0, 0, 0)):
    img_pil = Image.fromarray(img_cv2)
    draw = ImageDraw.Draw(img_pil)
    x, y = pos
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=border_color)
    draw.text(pos, text, font=font, fill=text_color)
    return np.array(img_pil)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    dados, bbox, _ = detector.detectAndDecode(frame)
    if bbox is not None:
        pontos = bbox.astype(int).reshape(-1, 2)
        for i in range(len(pontos)):
            pt1 = tuple(pontos[i])
            pt2 = tuple(pontos[(i + 1) % len(pontos)])
            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

    frame = draw_text_pillow(frame, mensagem, (20, 30), fonte_pillow, (255, 255, 255))

    if dados and dados != ultimo_dado:
        try:
            funcionario = json.loads(dados)

            if not isinstance(funcionario, dict):
                raise ValueError("JSON não é um objeto")

            if not all(k in funcionario for k in ["nome", "curso", "validade"]):
                raise ValueError("Campos obrigatórios ausentes")

            nome = funcionario["nome"]
            curso = funcionario["curso"]
            validade = funcionario["validade"]

            if curso != True:
                mensagem = f"{nome} NÃO autorizado(a)! Curso inválido."
                enviar_para_dashboard({
                    "nome": funcionario["nome"],
                    "foto": funcionario.get("foto", ""),
                    "curso": "Curso inválido"
                })

            else:
                validade_dt = datetime.strptime(validade, "%Y-%m-%d").date()
                hoje = datetime.now().date()

                if validade_dt < hoje:
                    mensagem = f"{nome} NÃO autorizado(a)! Curso vencido."
                    enviar_para_dashboard({
                        "nome": funcionario["nome"],
                        "foto": funcionario.get("foto", ""),
                        "curso": "Curso válido",
                        "validade": f"Curso vencido: {funcionario['validade']}"
                    })

                else:
                    mensagem = f"{nome}, posicione-se para leitura do EPI: "
                    enviar_para_dashboard({
                        "nome": funcionario["nome"],
                        "foto": funcionario.get("foto", ""),
                        "curso": "Curso válido",
                        "validade": f"Curso vencido: {funcionario['validade']}"
                    })
                    ultimo_dado = dados

        except Exception as e:
            mensagem = "Erro: QR Code inválido."

    if ultimo_dado:
        results = model(frame)
        epis_detectados = [model.names[int(cls)] for result in results for cls in result.boxes.cls]
        boxes_atuais = []

        for result in results:
            for box, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
                x1, y1, x2, y2 = map(int, box)
                nome_epi = model.names[int(cls)]
                boxes_atuais.append((x1, y1, x2, y2, nome_epi, conf))

        ultima_deteccao = time.time()

        lista_status_epi = []
        todos_ok = True

        for epi in epis_ordem:
            if epi in epis_detectados:
                lista_status_epi.append(f"{epi.upper()}: Ok")
                status_epi = {
                    "capacete": "Ok" if "helmet" in epis_detectados else "Faltando",
                    "oculos": "Ok" if "glasses" in epis_detectados else "Faltando",
                    "colete": "Ok" if "vest" in epis_detectados else "Faltando",
                    "luvas": "Ok" if "gloves" in epis_detectados else "Faltando"
                }
                enviar_para_dashboard(status_epi)
                todos_ok = all(v == "Ok" for v in status_epi.values())

        if todos_ok:
            mensagem = f"{funcionario['nome']} autorizado(a)! Todos os EPIs verificados."
            enviar_para_dashboard(status_epi)

            ultimo_dado = ""
            funcionario = None
            boxes_atuais = []
        else:
            mensagem = f"Aguardando EPIs..."

        y_offset = 60
        for linha in lista_status_epi:
            frame = draw_text_pillow(frame, linha, (20, y_offset), fonte_pillow, (255, 255, 255))
            y_offset += 30

    if time.time() - ultima_deteccao < 3:
        for (x1, y1, x2, y2, nome_epi, conf) in boxes_atuais:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            texto_epi = f"{nome_epi} {conf:.2f}"
            frame = draw_text_pillow(frame, texto_epi, (x1, y1 - 25), fonte_pillow, (255, 255, 255))

    cv2.imshow("Leitura de QR Code e EPIs", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()