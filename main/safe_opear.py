import cv2
import json
from datetime import datetime
from ultralytics import YOLO
from roboflow import Roboflow

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
ultimo_dado = ""

model = YOLO("runs/detect/train/weights/best.pt")

epis_obrigatorios = ["capacete", "luvas", "mascara"]

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

    cv2.putText(frame, "Aponte o QR Code para a câmera", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    if dados and dados != ultimo_dado:
        ultimo_dado = dados
        print("Dados lidos do QR Code:", dados)

        try:
            funcionario = json.loads(dados)
            nome = funcionario.get("nome", "")
            curso = funcionario.get("curso", "").strip().lower()
            validade = funcionario.get("validade", "")
            validade_dt = datetime.strptime(validade, "%Y-%m-%d").date()
            hoje = datetime.now().date()

            if curso != "sim":
                print(f"{nome} NÃO está autorizado! (Curso não válido)")
            elif validade_dt < hoje:
                print(f"{nome} está com curso vencido! (Venceu em {validade})")
            else:
                results = model(frame)
                epis_detectados = [model.names[int(cls)] for result in results for cls in result.boxes.cls]

                epis_faltando = [epi for epi in epis_obrigatorios if epi not in epis_detectados]

                if epis_faltando:
                    print(f"{nome} NÃO está autorizado! Faltando: {', '.join(epis_faltando)}")
                else:
                    print(f"{nome} está autorizado! Todos os EPIs presentes. Curso válido até {validade}")

                for result in results:
                    for box, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
                        x1, y1, x2, y2 = map(int, box)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(frame, f"{model.names[int(cls)]} {conf:.2f}", (x1, y1-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        except json.JSONDecodeError:
            print("Erro: Conteúdo do QR Code inválido.")

    cv2.imshow("Leitura de QR Code e EPIs", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()