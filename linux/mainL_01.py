# BIBLIOTECAS #
import cv2 as cv
import mediapipe as mp
import math
import pytesseract
from time import time
import os

# DIRETÓRIO DO EXECUTÁVEL #
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# KEYPOINTS DAS MAÕS # 
POLEGAR_TOPO = 4
MINDINHO_TOPO = 20

# VARIÁVEIS DE CAPTURA DA CÂMERA E HANDMARKS #
mp_hands = mp.solutions.hands
hands = mp_hands.Hands() 
cap = cv.VideoCapture(1)

cap = cv.VideoCapture("/dev/video0", cv.CAP_V4L2)
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 300)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 200)
# cap.set(cv.CAP_PROP_FPS, 8)

# VARIÁVEIS DE CONTROLE #
modo_leitura = False
controle_leitura = False
tempo = 0

# LOOP CENTRAL ( CAPTURA E TRATAMENTO DE FRAMES ) 
while cap.isOpened():
    status, frame = cap.read()

    if status == False:
        break

    frame_to_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    hand_results = hands.process(frame_to_rgb)
    
    # DETECÇÃO DE MÃO
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
                max_distance = 20

                if distancia < max_distance and not controle_leitura:
                    controle_leitura = True
                    modo_leitura = not modo_leitura

                    if modo_leitura:
                        tempo = time()
                        print('sinal de mao detectado')
                        os.system(f'espeak -v pt-br ' + 'Captando imagem, aguarde e evite movimentar-se')

                elif distancia > max_distance and controle_leitura:
                    controle_leitura = False
                
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv.circle(frame, (cx, cy), 5, (0, 255, 0), 1)

    # LEITURA DE TEXTO
    # VERIFICAÇÃO DE TEMPO
    if modo_leitura and ( time() - tempo ) >= 10:
        print('passou 10s')
        cv.imwrite('cap_frame.png', frame)
        modo_leitura = False
        text = pytesseract.image_to_string('cap_frame.png', lang='por')
        if len(text):
            os.system(f'espeak -v pt-br ' + 'Texto detectado.')
            os.system(text)
        else:
            os.system(f'espeak -v pt-br ' + 'Nenhum texto detectado.')

    cv.imshow('TecVision', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()