# https://digi.bib.uni-mannheim.de/tesseract/

# BIBLIOTECAS #
import cv2 as cv
import mediapipe as mp
import math
import pytesseract
import os
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

# DIRETÓRIO DO EXECUTÁVEL #
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# KEYPOINTS DAS MAÕS # 
POLEGAR_TOPO = 4
INDICADOR_TOPO = 8

# VARIÁVEIS DE CAPTURA DA CÂMERA E HANDMARKS #
mp_hands = mp.solutions.hands
hands = mp_hands.Hands() 
cap = cv.VideoCapture(0)

# VARIÁVEIS DE CONTROLE #
modo_leitura = False
leitura_tempo = 5
ultimo_tempo = 0
controle_leitura = False

print(pytesseract.get_languages())

while cap.isOpened():
    status, frame = cap.read()

    if status == False:
        break

    frame_to_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    hand_results = hands.process(frame_to_rgb)
    
    # LEITURA DE TEXTO
    tempo_atual = cv.getTickCount()
    if modo_leitura == True and (tempo_atual - ultimo_tempo) / cv.getTickFrequency() > leitura_tempo:
        texto_detectado = pytesseract.image_to_string(frame_to_rgb, lang='por')
        ultimo_tempo = tempo_atual

        #if len(texto_detectado) > 0:
        print(texto_detectado)

    if hand_results.multi_hand_landmarks:
        for landmarks in hand_results.multi_hand_landmarks:
            for _id, landmark in enumerate(landmarks.landmark):
                h, w, c = frame.shape

                # POLEGAR
                polegar = landmarks.landmark[POLEGAR_TOPO]
                polegar_x, polegar_y = int(polegar.x * w), int(polegar.y * h)
                
                # INDICADOR
                indicador = landmarks.landmark[INDICADOR_TOPO]
                indicador_x, indicador_y = int(indicador.x * w), int(indicador.y * h)

                # Distância euclidiana -> d = √ ( X2 - X1 )^2 + ( Y2 - Y1 )^2
                distancia = math.sqrt( ( polegar_x - indicador_x ) ** 2 + ( polegar_y - indicador_y) ** 2 ) 
                max_distance = 20

                if distancia < max_distance and not controle_leitura:
                    controle_leitura = True
                    modo_leitura = not modo_leitura

                    if modo_leitura:
                        print('Modo leitura ativado.')
                    else:
                        print('Modo leitura desativado.')

                elif distancia > max_distance and controle_leitura:
                    controle_leitura = False

                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv.circle(frame, (cx, cy), 5, (0, 255, 0), 1)
                
    cv.imshow('TecVision', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()