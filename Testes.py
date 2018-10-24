''' -*- coding: utf-8 -*-'''
import numpy as np
import time
import uuid
import cv2
import tccfunctions as t

##########  CONSTANT VALUES ###################################################
VIDEO = 1
VIDEO_FILE = '../Dataset/video{}.avi'.format(VIDEO)
XML_FILE = '../Dataset/video{}.xml'.format(VIDEO)

RESIZE_RATIO = 0.35 # Resize, valores entre 0 e 1 | 1=Tamanho original do video
CLOSE_VIDEO = 1000 #6917 # Fecha o video no frame indicado
ARTG_FRAME = 0 #254  # Frame q usei para exemplo no Artigo

SHOW_ROI = True
SHOW_TRACKING_AREA = True
SHOW_LINEAR_REGRESSION = False
SHOW_CAR_RECTANGLE = True
SHOW_REAL_SPEEDS = True
SKIP_VIDEO = False


#----- Tracking Values --------------------------------------------------------
# The maximum distance a blob centroid is allowed to move in order to
# consider it a match to a previous scene's blob.
BLOB_LOCKON_DIST_PX_MAX = 150 # default = 50 p/ ratio 0.35
BLOB_LOCKON_DIST_PX_MIN = 10  # default 10
MIN_AREA_FOR_DETEC = 35000  # Default 40000 (não detecta Moto)
# Limites da Área de Medição, área onde é feita o Tracking
# Distancia de medição: default 915-430 = 485
BOTTOM_LIMIT_TRACK = 915  # Default 915
UPPER_LIMIT_TRACK = 430  # Default 430

# The number of seconds a blob is allowed to sit around without having
# any new blobs matching it.
BLOB_TRACK_TIMEOUT = 0.1 # Default 0.7

#----- Speed Values -----------------------------------------------------------
# Correction Factor
CF_LANE1 = 2.5869977  # default 2.3068397
CF_LANE2 = 2.5869977  # default 2.3068397
CF_LANE3 = 2.3068397  # default 2.3068397

#-----  Save Results Values ---------------------------------------------------
SAVE_FRAME_F1 = False  # Faixa 1
SAVE_FRAME_F2 = False  # Faixa 2
SAVE_FRAME_F3 = True  # Faixa 3

#----- Colors -----------------------------------------------------------------


######### END - CONSTANT VALUES ###############################################
cap = cv2.VideoCapture(VIDEO_FILE)
fps = cap.get(cv2.CAP_PROP_FPS)
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Retorna a largura do video
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Retorna a largura do video

bgsMOG = cv2.createBackgroundSubtractorMOG2(history=10, varThreshold=50, detectShadows=0)

# Variant Values
dict_lane1 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 1
dict_lane2 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 2
dict_lane3 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 3
tracked_blobs = []  # Lista que salva os dicionários dos tracked_blobs
average_speed = [1]
meas_speed_lane1 = [0]
meas_speed_lane2 = [0]
meas_speed_lane3 = [0]
real_speed_lane1 = [0]
real_speed_lane2 = [0]
real_speed_lane3 = [0]

prev_len_speed = []

total_cars = {'lane_1':0, 'lane_2':0, 'lane_3':0}
prev_speed = 1.0

frameCount = 0  # Armazena a contagem de frames processados do video
rectCount = 0
out = 0  # Armazena o frame com os contornos desenhados
color = 0

final_ave_speed = 0
ave_speed = 0
flag = 0

# ##############  FUNÇÕES #####################################################
def r(numero):
    return int(numero*RESIZE_RATIO)

def crop(frame):
    return frame[30:370, 205:620]

def calculate_speed(trails, fps):
    '''Calc velocidade'''
    med_area_meter = 3.5  # metros (Valor estimado)
    med_area_pixel = r(485)
    qntd_frames = len(trails) # default 11
    initial_pt, final_pt = t.linearRegression(trails, qntd_frames)  # Usando Regressão Linear
    dist_pixel = cv2.norm(final_pt, initial_pt)
#    dist_pixel1 = cv2.norm(trails[0], trails[10])  # Sem usar Regressão linear
    if SHOW_LINEAR_REGRESSION:
        cv2.line(frame, initial_pt, final_pt, t.PINK, 10)
#    cv2.line(frame,trails[0],trails[10], t.GREEN, 2)
#    cv2.imwrite('img/regressao1_{}.png'.format(frameCount), frame)
    dist_meter = dist_pixel*(med_area_meter/med_area_pixel)
    speed = (dist_meter*3.6*cf)/(qntd_frames*(1/fps))
    return speed
# ########## FIM  FUNÇÕES #####################################################

vehicle = t.read_xml(XML_FILE)  # Dicionário que armazena todas as informações do xml
t.remove_old_csv_files()
#qntd_faixa1 = 0
#qntd_faixa2 = 0
##qntd_faixa3 = 0
#for vehicles in vehicle:
#    if vehicle[vehicles] == 6918:
#        break
#    if vehicle[vehicles]['lane'] == str(1):
#        qntd_faixa1 += 1
#    if vehicle[vehicles]['lane'] == str(2):
#        qntd_faixa2 += 1
#    if vehicle[vehicles]['lane'] == str(3):
#        qntd_faixa3 += 1

KERNEL_ERODE = np.ones((r(9), r(9)), np.uint8)  # Matriz (3,3) com 1 em seus valores
KERNEL_DILATE = np.ones((r(100), r(50)), np.uint8)  # Matriz (r(86), r(43)) com 1 em seus valores

while True:
    ret, frame = t.get_frame(cap, RESIZE_RATIO)
    frame_time = time.time()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    t.region_of_interest(frameGray, RESIZE_RATIO)
    if SHOW_ROI:
        t.region_of_interest(frame, RESIZE_RATIO)
    if SHOW_TRACKING_AREA:  # Desenha os Limites da Área de Tracking
            cv2.line(frame, (0, r(UPPER_LIMIT_TRACK)), (WIDTH, r(UPPER_LIMIT_TRACK)), t.CIAN, 2)
            cv2.line(frame, (0, r(BOTTOM_LIMIT_TRACK)), (WIDTH, r(BOTTOM_LIMIT_TRACK)), t.CIAN, 2)

    if SKIP_VIDEO:
        skip = t.skip_video(frameCount, VIDEO)
        if not skip:
            frameCount += 1
            continue

    # Equalizar Contraste
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(7, 7))
    hist = clahe.apply(frameGray)
    frameGray = hist
    
    if ret == True:
        t.update_info_xml(frameCount, vehicle, dict_lane1, dict_lane2, dict_lane3)
        if SHOW_REAL_SPEEDS:
            t.print_xml_values(frame, RESIZE_RATIO, dict_lane1, dict_lane2, dict_lane3)

        fgmask = bgsMOG.apply(frameGray, None, 0.01)
        erodedmask = cv2.erode(fgmask, KERNEL_ERODE, iterations=1) 
        dilatedmask = cv2.dilate(erodedmask, KERNEL_DILATE, iterations=1)
        _, contours, hierarchy = cv2.findContours(dilatedmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#        contornos =  cv2.drawContours(frame, contours, -1, BLUE, 2, 8, hierarchy) # IGOR

        # create hull array for convex hull points
        hull = []
        for i in range(len(contours)):  # calculate points for each contour
                # creating convex hull object for each contour
            hull.append(cv2.convexHull(contours[i], False))

        # create an empty black image
        drawing = np.zeros((dilatedmask.shape[0], dilatedmask.shape[1], 3), np.uint8)

        area = []
        areahull = []
        #draw contours and hull points
        for i in range(len(contours)): #default  for i in range(len(contours))
#            if cv2.contourArea(contours[i]) > 50000:
#                rectCount += 1
#                break
#            if cv2.contourArea(contours[i]) < 1500:
#                rectCount += 1
#                break

            if cv2.contourArea(contours[i]) > r(MIN_AREA_FOR_DETEC): # Default if cv2.contourArea(contours[i]) > 14000:
                # draw ith contour
                cv2.drawContours(drawing, contours, i, t.GREEN, 0, 8, hierarchy)
                # draw ith convex hull object
                out = cv2.drawContours(drawing, hull, i, t.WHITE, -1, 8)
                area.append(cv2.contourArea(contours[i]))
                areahull.append(cv2.contourArea(hull[i]))
                (x, y, w, h) = cv2.boundingRect(hull[i])
                center = (int(x + w/2), int(y + h/2))
                # out = cv2.rectangle(out, (x, y), (x + w, y + h), t.t.GREEN, 2) # printa na mask
                # CONDIÇÕES PARA CONTINUAR COM TRACKING
                if center[1] < r(UPPER_LIMIT_TRACK):
                        break
                
                if w < r(330) and h < r(330):  # ponto que da pra mudar
                    continue
                # Área de medição do Tracking
                if center[1] > r(BOTTOM_LIMIT_TRACK) or center[1] < r(UPPER_LIMIT_TRACK):
                    continue
                
                if SHOW_CAR_RECTANGLE:
                    if int(y + h/2) > r(UPPER_LIMIT_TRACK):
                        cv2.rectangle(frame, (x, y), (x + w, y + h), t.GREEN, 2)
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), t.PINK, 2)
                
#                cv2.putText(frame, f'area = {x*y/RESIZE_RATIO:.0f}', (r(400),r(400)), 2, .6, t.WHITE, 1)
#                cv2.putText(frame, f'w={w}  h={h}', (r(450),r(480)), 2, .6, t.WHITE, 1)

#        outputFrame = cv2.drawContours(frame, contours, -1, (0,255,0),-1)


#        try: hierarchy = hierarchy[0]
#        except: hierarchy = []
#        a = []
#        for contour, hier in zip(contours, hierarchy):
#            (x, y, w, h) = cv2.boundingRect(contour)
#
#            if w < 60 and h < 60:
#                continue
##            if w > 400 and h > 280:
##                continue
##            area = h * w
##            if area > 10000 :
##                continue
#
#            center = (int(x + w/2), int(y + h/2))
#
#            if center[1] > 320 or center[1] < 150:
#                continue
#
#                # Optionally draw the rectangle around the blob on the frame that we'll show in a UI later
#            outputFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#
#            crop_img = frame[y:y+h , x:x+w]
#            cv2.imwrite('imagens/negatives/negativesframe{}.jpg'.format(frameCount),frame)
#
#            rectCount += 1
#
#################### TRACKING ################################################

            # Look for existing blobs that match this one
                closest_blob = None
                if tracked_blobs:
                    # Sort the blobs we have seen in previous frames by pixel distance from this one
                    closest_blobs = sorted(tracked_blobs, key=lambda b: cv2.norm(b['trail'][0], center))

                    # Starting from the closest blob, make sure the blob in question is in the expected direction
                    distance = 0.0
                    distance_five = 0.0
                    for close_blob in closest_blobs:
                        distance = cv2.norm(center, close_blob['trail'][0])
                        if len(close_blob['trail']) > 10:
                            distance_five = cv2.norm(center, close_blob['trail'][10])

                        # Check if the distance is close enough to "lock on"
                        if distance < r(BLOB_LOCKON_DIST_PX_MAX) and distance > r(BLOB_LOCKON_DIST_PX_MIN):
                            # If it's close enough, make sure the blob was moving in the expected direction
                            expected_dir = close_blob['dir']
                            if expected_dir == 'up' and close_blob['trail'][0][1] < center[1]:
                                continue
#                            elif expected_dir == 'right' and close_blob['trail'][0][0] > center[0]:
#                                continue
                            else:
                                closest_blob = close_blob
                                break

                    if closest_blob:
                        # If we found a blob to attach this blob to, we should
                        # do some math to help us with speed detection
                        prev_center = closest_blob['trail'][0]
                        if center[1] < prev_center[1]:
                            # It's moving up
                            closest_blob['dir'] = 'up'
                            closest_blob['bumper_x'] = y
#
                        # ...and we should add this centroid to the trail of
                        # points that make up this blob's history.
                            closest_blob['trail'].insert(0, center)
                            closest_blob['last_seen'] = frame_time
                            if len(closest_blob['trail']) > 10:
                                if closest_blob['trail'][0][0] < r(570):
                                    cf = CF_LANE1
                                    closest_blob['speed'].insert(0, calculate_speed(closest_blob['trail'], fps))
                                elif closest_blob['trail'][0][0] >= r(570) and closest_blob['trail'][0][0] < r(1180):
                                    cf = CF_LANE2
                                    closest_blob['speed'].insert(0, calculate_speed(closest_blob['trail'], fps))
                                elif closest_blob['trail'][0][0] >= r(1180):
                                    cf = CF_LANE3
                                    closest_blob['speed'].insert(0, calculate_speed(closest_blob['trail'], fps))

                if not closest_blob: # Cria as variaves
                    # If we didn't find a blob, let's make a new one and add it to the list
                    b = dict(
                        id=str(uuid.uuid4())[:8],
                        first_seen=frame_time, # Coloca o mesmo valor na first_seen e last_seen
                        last_seen=frame_time, # Coloca o mesmo valor na first_seen e last_seen
                        dir=None,
                        bumper_x=None,
                        trail=[center],
                        speed=[0],  # Zera a velocidade
                        size=[0, 0], # Zera a tupla de tamanho
                    )
                    tracked_blobs.append(b)   # coloca as informacoes de "b" na lista "tracked_blobs"
                    # Agora tracked_blobs não será False

################### FIM TRACKING ##############################################
################## PRINTA OS BLOBS ############################################
        if tracked_blobs:
            # Prune out the blobs that haven't been seen in some amount of time
            for i in range(len(tracked_blobs) - 1, -1, -1):
                if frame_time - tracked_blobs[i]['last_seen'] > BLOB_TRACK_TIMEOUT: # Deleta caso de timeout
                    print("Removing expired track {}".format(tracked_blobs[i]['id']))
#                    save_csv()
#                    prev_speed = np.mean(tracked_blobs[i]['speed'])
                    prev_speed = ave_speed
                    final_ave_speed = 0.0
                    flag = 1
                    del tracked_blobs[i]

        # Draw information about the blobs on the screen
        #print ('tracked_blobs', tracked_blobs)
        for blob in tracked_blobs:
            for (a, b) in t.pairwise(blob['trail']):
                cv2.circle(frame, a, 5, t.BLUE, -1)
               # print ('blob', blob)
                if blob['dir'] == 'up':
                    cv2.line(frame, a, b, t.WHITE, 2)
                else:
                    cv2.line(frame, a, b, t.YELLOW, 2)

################# FIM PRINTA OS BLOBS  ########################################

            if blob['speed'] and blob['speed'][0] != 0:
                prev_len_speed.insert(0, len(blob['speed']))
                # limpa prev_len_speed se estiver muito grande
                # deixa no máx 20 valores
                if len(prev_len_speed) > 20:
                    while len(prev_len_speed) > 20:
                        del prev_len_speed[19]
                # remove zero elements on the speed list
                blob['speed'] = [item for item in blob['speed'] if item != 0.0]
                print('========= speed list =========', blob['speed'])
                prev_speed = ave_speed
                ave_speed = np.mean(blob['speed'])
                print('========= prev_speed =========', float("{0:.5f}".format(prev_speed)))
                print('========= ave_speed =========', float("{0:.5f}".format(ave_speed)))
                print('========prev_final_ave_speed==', float("{0:.5f}".format(final_ave_speed)))
                if ave_speed == prev_speed and final_ave_speed != 1:
                    final_ave_speed = ave_speed
                    print('========= final_ave_speed =========', float("{0:.5f}".format(final_ave_speed)))
#                    cv2.imwrite('img/{}speed_{}.png'.format(frameCount,final_ave_speed), frame)

                # MOSTRA RESULTADOS DAS VELOCIDADES CALCULADAS ###################################
                if blob['trail'][0][0] < r(571): # entao esta na faixa 1
                    lane = 1
                    t.show_results_on_screen(frame, frameCount, ave_speed, lane, blob, total_cars, RESIZE_RATIO, VIDEO,
                                             dict_lane1, dict_lane2, dict_lane3, SAVE_FRAME_F1, SAVE_FRAME_F2, SAVE_FRAME_F3)
                elif blob['trail'][0][0] >= r(571) and blob['trail'][0][0] < r(1143):  # entao esta na faixa 2
                    lane = 2
                    t.show_results_on_screen(frame, frameCount, ave_speed, lane, blob, total_cars, RESIZE_RATIO, VIDEO,
                                             dict_lane1, dict_lane2, dict_lane3, SAVE_FRAME_F1, SAVE_FRAME_F2, SAVE_FRAME_F3)
                elif blob['trail'][0][0] >= r(1143):  # entao esta na faixa 3
                    lane = 3
                    t.show_results_on_screen(frame, frameCount, ave_speed, lane, blob, total_cars, RESIZE_RATIO, VIDEO,
                                             dict_lane1, dict_lane2, dict_lane3, SAVE_FRAME_F1, SAVE_FRAME_F2, SAVE_FRAME_F3)

                # SALVA VALORES DE VELOCIDADE EM ARQUIVOS CSV
                # Ta ruim, nao tá salvando certinho
                t.save_real_speed_in_csv(total_cars, dict_lane1, real_speed_lane1, dict_lane2,
                                         real_speed_lane2, dict_lane3, real_speed_lane3)
                # Ta ruim, nao tá salvando certinho
                t.save_mea_speed_in_csv(blob, total_cars, prev_len_speed, final_ave_speed, lane,
                                        dict_lane1, meas_speed_lane1, dict_lane2, meas_speed_lane2,
                                        dict_lane3, meas_speed_lane3)
        print('*********************************************************************')


        # Mostra a qntd de frames processados e a % do video
        outputFrame = cv2.putText(frame, 'frame: {} {}%'.format(frameCount,
                                  str(int((100*frameCount)/vehicle['videoframes']))),
                                  (r(14), r(1071)), 0, .65,t.WHITE, 2)
#        outputFrame = cv2.putText(frame, 'Retangulos descartados: {}'.format(rectCount),
#                                    (r(571),r(1071)), cv2.FONT_HERSHEY_SIMPLEX, .5,t.WHITE, 2)

#        roi(frame) # Ver como esta a ROI

#        t.print_xml_values(outputFrame, RESIZE_RATIO, dict_lane1, dict_lane2, dict_lane3)

        # Mostra os limites entres as faixas
#        cv2.line(frame, (r(570), 0), (r(570),HEIGHT),t.YELLOW, 2)
#        cv2.line(frame, (r(1180), 0), (r(1180),HEIGHT),t.YELLOW, 2)



#        crop_img = outputFrame[70:320, 0:640]

        # ########## MOSTRA OS VIDEOS  ################################################
#        cv2.imshow('equ', equ)
#        cv2.imshow('res', res)
        cv2.imshow('fgmask', fgmask)
#        cv2.imshow('erodedmask',erodedmask)
        cv2.imshow('dilatedmask', dilatedmask)
#        cv2.imshow('contornos',contornos)
        cv2.imshow('out',out)
        cv2.imshow('outputFrame', outputFrame)
#        final = np.hstack((erodedmask, dilatedmask))
#        cv2.imshow('final', final)
#        cv2.imshow('mask_eroded', np.concatenate((fgmask, dilatedmask),0))
#        abdc = np.concatenate((fgmask, dilatedmask),1)


        # Salva imagens para o README do GITHUB
#        if frameCount == ARTG_FRAME:
#            cv2.imwrite('1frameGray.png', crop(frameGray))
#            cv2.imwrite('2hist.png', crop(hist))
#            cv2.imwrite('3fgmask.png', crop(fgmask))
#            cv2.imwrite('4erodedmask.png', crop(erodedmask))
#            cv2.imwrite('5dilatedmask.png', crop(dilatedmask))
#            cv2.imwrite('6Convexhull.png', crop(out))
#            cv2.imwrite('7resultado.png', crop(outputFrame))

#            cv2.imwrite('mask_eroded', np.hstack((fgmask, dilatedmask)))
#        cv2.imshow('dilate_convex', np.hstack((crop(dilatedmask), crop(out))))

#            cv2.imwrite('mask_eroded', vis)



#        if frameCount > 175 and frameCount < 192:
#            cv2.imwrite('{}.png'.format(frameCount), outputFrame)
#            cv2.imwrite('dilate{}.png'.format(frameCount), dilatedmask)
#        if frameCount == 600:
##            cv2.imwrite('{}.png'.format(frameCount), outputFrame)
#            break


        frameCount = frameCount + 1    # Conta a quantidade de Frames

        if frameCount == CLOSE_VIDEO: #  fecha o video
            break

        if cv2.waitKey(1) & 0xFF == ord('q'): #Pressiona a tecla Q para fechar o video
            break
    else:  # sai do while: ret == False
        break

cap.release()
cv2.destroyAllWindows()
