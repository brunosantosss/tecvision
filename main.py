import cv2 as cv
import mediapipe as mp
import math

#KEYPOINTS LOCALIZATIONS

POLEGAR_TOPO = 4
INDICADOR_TOPO = 8

mp_hands = mp.solutions.hands
hands = mp_hands.Hands() 

cap = cv.VideoCapture(0)

while cap.isOpened():
    status, frame = cap.read()

    if status == False:
        break

    #frame = cv.convertScaleAbs(frame, alpha=1.1, beta=50)

    frame_to_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    hand_results = hands.process(frame_to_rgb)

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
                max_distance = 30

                if(distancia < max_distance):
                    print('Ação!')

                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv.circle(frame, (cx, cy), 5, (0, 255, 0), 1)
                
                if _id > 0:
                    prev_landmark = landmarks.landmark[_id - 1]
                    lx, ly = int(prev_landmark.x * w), int(prev_landmark.y * h)
                    cv.line(frame, (lx, ly), (cx, cy), (255, 0, 0), 2)

    cv.imshow('TecVision', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()