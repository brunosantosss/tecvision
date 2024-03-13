# https://digi.bib.uni-mannheim.de/tesseract/

# BIBLIOTECAS #
import cv2 as cv
import mediapipe as mp
import math
import pytesseract
from time import sleep
import os
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

# DIRETÓRIO DO EXECUTÁVEL #
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# KEYPOINTS DAS MAÕS # 
POLEGAR_TOPO = 4
MINDINHO_TOPO = 20

# VARIÁVEIS DE CAPTURA DA CÂMERA E HANDMARKS #
mp_hands = mp.solutions.hands
hands = mp_hands.Hands() 
cap = cv.VideoCapture(0)

#cap = cvLIBRARY.VideoCapture("/dev/video0", cvLIBRARY.CAP_V4L2)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 300)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 200)
cap.set(cv.CAP_PROP_FPS, 8)

# VARIÁVEIS DE CONTROLE #
modo_leitura = False
controle_leitura = False

print(pytesseract.get_languages())

while cap.isOpened():
    status, frame = cap.read()

    if status == False:
        break

    frame_to_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    hand_results = hands.process(frame_to_rgb)
    
    # LEITURA DE TEXTO
    if hand_results.multi_hand_landmarks:
        for landmarks in hand_results.multi_hand_landmarks:
            for _id, landmark in enumerate(landmarks.landmark):
                h, w, c = frame.shape

                # POLEGAR
                polegar = landmarks.landmark[POLEGAR_TOPO]
                polegar_x, polegar_y = int(polegar.x * w), int(polegar.y * h)
                
                # MINDINHO
                mindinho = landmarks.landmark[MINDINHO_TOPO]
                mindinho_x, mindinho_y = int(mindinho.x * w), int(mindinho.y * h)

                # Distância euclidiana -> d = √ ( X2 - X1 )^2 + ( Y2 - Y1 )^2
                distancia = math.sqrt( ( polegar_x - mindinho_x ) ** 2 + ( polegar_y - mindinho_y) ** 2 ) 
                max_distance = 15

                if distancia < max_distance and not controle_leitura:
                    controle_leitura = True
                    modo_leitura = not modo_leitura

                    if modo_leitura:
                       cap_frame = cv.imwrite('cap_frame.png', frame)
                       #os.system('espeak -v pt-br ' + 'Imagem captada, aguarde a leitura')
                       try:
                            text_to_frame = pytesseract.image_to_string(cap_frame, lang='por')
                            print(text_to_frame)
                            #os.system('espeak -v pt-br ' + text_to_frame)
                       except Exception as error:
                            print(f"Ocorreu um erro > {error}")
                            pass
                    else:
                        pass

                elif distancia > max_distance and controle_leitura:
                    controle_leitura = False

                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv.circle(frame, (cx, cy), 5, (0, 255, 0), 1)
                
    cv.imshow('TecVision', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()