
"""
Created on Mon Sep 17 13:24:34 2018

@author: broch
"""
#
import cv2
import numpy as np
import time
import uuid
import math
import xml.etree.ElementTree as ET

##########  CONSTANT VALUES ##################################################
VIDEO_FILE = '../Dataset/video1.avi' # Local do video a ser analisado
XML_FILE = '../Dataset/video1.xml'
#XML_FILE = '3-xmlreader/video1.xml' # Igor

KERNEL_ERODE = np.ones((3, 3), np.uint8)  # Matriz (3,3) com 1 em seus valores -- Usa na funcao de erode
KERNEL_DILATE = np.ones((15, 15), np.uint8)  # Matriz (15,15) com 1 em seus valores -- Usa na funcao de dilate
# KERNEL_ERODE_SCND = np.ones((3,3), np.uint8)  # Matriz (8,8) com 1 em seus valores -- Usa na 2nd funcao de erode
RESIZE_RATIO = 0.35 # Resize, valores entre 0 e 1 | 1=Tamanho original do video
CLOSE_VIDEO = 2000  # Fecha o video no frame 400

# The maximum distance a blob centroid is allowed to move in order to
# consider it a match to a previous scene's blob.
BLOB_LOCKON_DISTANCE_PX = 50 # default = 80 # Aqui pode ser um limitador da veloc máx
LINE_THICKNESS = 1
# The number of seconds a blob is allowed to sit around without having
# any new blobs matching it.
BLOB_TRACK_TIMEOUT = 0.7 # Default 0.7

cap = cv2.VideoCapture(VIDEO_FILE)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Retorna a largura do video
#width = 672
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Retorna a altura do video

bgsMOG = cv2.createBackgroundSubtractorMOG2(history=10, varThreshold = 50, detectShadows=0)

# Variant Values
dict_lane1 = {}  # Dict que armazena os valores de "speed, frame_start, frame_end" da FAIXA 1
dict_lane2 = {}  # Dict que armazena os valores de "speed, frame_start, frame_end" da FAIXA 2
dict_lane3 = {}  # Dict que armazena os valores de "speed, frame_start, frame_end" da FAIXA 3
tracked_blobs = []  # Lista que salva os dicionários dos tracked_blobs

frameCount = 0  # Armazena a contagem de frames processados do video
rectCount  = 0
rectCount2 = 0
out = 0  # Armazena o frame com os contornos desenhados

# ##############  FUNÇÕES ####################################################################
def res(numero):  # Faz o ajuste de escala das posições de textos e retangulos
    return int(numero*RESIZE_RATIO)


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


def read_xml(xml_file):
# Funcão que lê o .xml e guarda as informações em um dicionário "iframe"
    tree = ET.parse(xml_file)
    root = tree.getroot()
    iframe = {}
    for child in root:
        if child.get('radar') == 'True':
            for subchild in child:
#                print('subchild {}'.format(subchild.attrib))                
                if subchild.tag == 'radar':
                    iframe[child.get('iframe')] = subchild.attrib # salva frame_end, frame_start, speed
                    iframe[child.get('iframe')]['lane'] = child.get('lane')
                    iframe[child.get('iframe')]['radar'] = child.get('radar')
                    iframe[child.get('iframe')]['moto'] = child.get('moto')
#                    iframe[child.get('iframe')]['plate'] = child.get('plate')  # Desnecessário
#                    iframe[child.get('iframe')]['sema'] = child.get('sema')  # Desnecessário
        if child.tag == 'videoframes':
            iframe[child.tag] = int(child.get('total'))
    print('Arquivo {} foi armazenado com sucesso !!'.format(xml_file))
    return iframe


def get_frame():
	#" Grabs a frame from the video vcture and resizes it. "
	ret, frame = cap.read()
	if ret:
		(h, w) = frame.shape[:2]
		frame = cv2.resize(frame, (int(w * RESIZE_RATIO), int(h * RESIZE_RATIO)), interpolation=cv2.INTER_CUBIC)
	return ret, frame


def calculate_speed (trails, fps):
    # distance: distance on the frame
	# location: x, y coordinates on the frame
	# fps: framerate
	# mmp: meter per pixel
#	dist = cv2.norm(trails[0], trails[10])
	dist_x = trails[0][0] - trails[10][0]
	dist_y = trails[0][1] - trails[10][1]

	mmp_y = 0.125 / (3 * (1 + (3.22 / 432)) * trails[0][1])
#    mmp_y = 0.2 / (3 * (1 + (3.22 / 432)) * trails[0][1])  # Default
	mmp_x = 0.125 / (5 * (1 + (1.5 / 773)) * (width - trails[0][1]))  
#    mmp_x = 0.2 / (5 * (1 + (1.5 / 773)) * (width - trails[0][1]))  # Default
	real_dist = math.sqrt(dist_x * mmp_x * dist_x * mmp_x + dist_y * mmp_y * dist_y * mmp_y)

	return real_dist * fps * 250 / 3.6


from itertools import *
def pairwise(iterable):
    r"s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def update_info_xml():
    try:
        # Verifica se naquele frame tem uma chave correspondente no dicionário "vehicle"
        if vehicle[str(frameCount)]['frame_start'] == str(frameCount):  
            lane_state = vehicle[str(frameCount)]['lane']
            
            if lane_state == '1':  # Se for na faixa 1, armazena as seguintes infos
                # print('Faixa 1')
                dict_lane1['speed'] = vehicle[str(frameCount)]['speed']
                dict_lane1['frame_start'] = vehicle[str(frameCount)]['frame_start']
                dict_lane1['frame_end'] = vehicle[str(frameCount)]['frame_end']
            elif lane_state == '2':
                #print('Faixa 2')
                dict_lane2['speed'] = vehicle[str(frameCount)]['speed']
                dict_lane2['frame_start'] = vehicle[str(frameCount)]['frame_start']
                dict_lane2['frame_end'] = vehicle[str(frameCount)]['frame_end']
            elif lane_state == '3':
                #print('Faixa 3')
                dict_lane3['speed'] = vehicle[str(frameCount)]['speed']
                dict_lane3['frame_start'] = vehicle[str(frameCount)]['frame_start']
                dict_lane3['frame_end'] = vehicle[str(frameCount)]['frame_end']
    except KeyError:
#            print('KeyError: Key Não encotrada no dicionário')
        pass


def print_xml_values():
    # Mostra no video os valores das velocidades das 3 Faixas.
    try:  # Posição do texto da FAIXA 1
        text_pos = (res(143), res(43))
        cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20), (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
        cv2.putText(frame, 'speed: {}'.format(dict_lane1['speed']), text_pos, 2, .6, (255, 255, 0), 1)
    except:
        pass
    
    try:  # Posição do texto da FAIXA 2
        text_pos = (res(628), res(43))
        cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20), (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
        cv2.putText(frame, 'speed: {}'.format(str(dict_lane2['speed'])), text_pos, 2, .6, (255, 255, 0), 1)
    except:
        pass
    
    try:  # Posição do texto da FAIXA 3
        text_pos = (res(1143), res(43))
        cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20), (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
        cv2.putText(frame, 'speed: {}'.format(dict_lane3['speed']), text_pos, 2, .6, (255, 255, 0), 1)
    except:
            pass
# ########## FIM  FUNÇÕES ####################################################################

vehicle = read_xml(XML_FILE)  # Dicionário que armazena todas as informações do xml

while(True):
#    ret , frame = cap.read()
    ret, frame = get_frame()
    frame_time = time.time()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    if ret == True:
        update_info_xml()
        # Cria a máscara
        fgmask = bgsMOG.apply(frameGray, None, 0.01)
        erodedmask = cv2.erode(fgmask, KERNEL_ERODE , iterations=1) # usa pra tirar os pixels isolados (ruídos)
        dilatedmask = cv2.dilate(erodedmask, KERNEL_DILATE , iterations=1) # usa para evidenciar o objeto em movimento
#        erodedmask = cv2.erode(fgmask, KERNEL_ERODE_SCND ,iterations=1) # usa pra tirar os pixels isolados (ruídos)
        # Fim da máscara
        _, contours, hierarchy = cv2.findContours(dilatedmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#        contornos =  cv2.drawContours(frame, contours, -1, (255,0,0), 2, 8, hierarchy) # IGOR
        
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
        rectCount2 = 0
        for i in range(len(contours)): #default  for i in range(len(contours))
#            if cv2.contourArea(contours[i]) > 50000:
#                rectCount += 1
#                break
#            if cv2.contourArea(contours[i]) < 1500:
#                rectCount += 1
#                break

#            if rectCount2 < 2:
            if cv2.contourArea(contours[i]) > 14000: # Default if cv2.contourArea(contours[i]) > 14000:
                color_contours = (0, 255, 0) # green - color for contours
                color = (255, 255, 255) # blue - color for convex hull
                # draw ith contour
                cv2.drawContours(drawing, contours, i, color_contours, 0, 8, hierarchy)
                # draw ith convex hull object
                out = cv2.drawContours(drawing, hull, i, color, -1, 8)
                area.append(cv2.contourArea(contours[i]))
                areahull.append(cv2.contourArea(hull[i]))
                (x, y, w, h) = cv2.boundingRect(hull[i])
#                out = cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 255), 2) # printa na mask
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2) # printa na frame
                
                rectCount2 += 1
                
#                if y > 70:
##                    cv2.line(frame,(0,140),(640,140),(255,255,0),5)
##                    cv2.line(frame,(0,320),(640,320),(255,255,0),5)
##                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 4) # printa na mask
#                    pass
                
                if w < 60 and h < 60:  # ponto que da pra mudar
                    continue
                center = (int(x + w/2), int(y + h/2))
                
                if center[1] > 320 or center[1] < 150:  # ponto que da pra mudar
                    continue

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
#				# Optionally draw the rectangle around the blob on the frame that we'll show in a UI later
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
                        if distance < BLOB_LOCKON_DISTANCE_PX:
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
                            # It's moving left
                            closest_blob['dir'] = 'up'
                            closest_blob['bumper_x'] = y
#                        else:
#    						# It's moving right
#                            closest_blob['dir'] = 'right'
#                            closest_blob['bumper_x'] = x + w
    
    					# ...and we should add this centroid to the trail of
    					# points that make up this blob's history.
                        closest_blob['trail'].insert(0, center)
                        closest_blob['last_seen'] = frame_time
                        if len(closest_blob['trail']) > 10:
                            closest_blob['speed'].insert(0, calculate_speed (closest_blob['trail'], fps))
    
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
                    
################### FIM TRACKING ################################################
                    
                    
################## PRINTA OS BLOBS #############################################
        if tracked_blobs:
			# Prune out the blobs that haven't been seen in some amount of time
            for i in range(len(tracked_blobs) - 1, -1, -1): 
                if frame_time - tracked_blobs[i]['last_seen'] > BLOB_TRACK_TIMEOUT: # Deleta caso de timeout
                    print ("Removing expired track {}".format(tracked_blobs[i]['id']))
                    del tracked_blobs[i]

        # Draw information about the blobs on the screen
        print ('tracked_blobs', tracked_blobs)
        for blob in tracked_blobs:
            for (a, b) in pairwise(blob['trail']):
                cv2.circle(frame, a, 5, (255, 0, 0), LINE_THICKNESS)

                # print ('blob', blob)
                if blob['dir'] == 'up':
                    cv2.line(frame, a, b, (255, 255, 0), LINE_THICKNESS)
                else:
                    cv2.line(frame, a, b, (0, 255, 255), LINE_THICKNESS)            
################# FIM PRINTA OS BLOBS  ##########################################
                
            if blob['speed'] and blob['speed'][0] != 0:
                # remove zero elements on the speed list
                blob['speed'] = [item for item in blob['speed'] if item != 0.0]
                print ('========= speed list =========', blob['speed'])
                ave_speed = np.mean(blob['speed'])
                print ('========= ave_speed =========', ave_speed)
                cv2.putText(frame, str(int(ave_speed)) + 'km/h', (blob['trail'][0][0] - 10, blob['trail'][0][1] + 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), thickness=1, lineType=2)

        print ('*********************************************************************')
        
        print_xml_values()
        
        # Mostra a qntd de frames processados e a % do video
        outputFrame = cv2.putText(frame, 'frame: {} {}%'.format(frameCount, 
                                    str(int((100*frameCount)/vehicle['videoframes']))), 
                                    (res(14), res(1071)), 0, .65, (255, 255, 255), 2)
        outputFrame = cv2.putText(frame, 'Retangulos descartados: {}'.format(rectCount), 
                                    (200,375), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2)
        
#        cv2.line(outputFrame,(0,70),(672,70),(255,0,0),3) #Linha Horz de Cima
#        cv2.line(outputFrame,(0,320),(672,320),(255,0,0),3) #Linha Horz de Baixo
#        cv2.line(outputFrame,(570,0),(570,378),(255,0,0),3) #Linha Vertc da direita
#        
#        cv2.line(outputFrame,(0,140),(640,140),(255,255,0),5)#Linha Horz de Cima
#        cv2.line(outputFrame,(0,320),(640,320),(255,255,0),5)#Linha Horz de Baixo
#        cv2.rectangle(outputFrame, (0,70), (640,320), (255,255,255) , 2)
        
        crop_img = outputFrame[70:320, 0:640]
        
        # ########## MOSTRA OS VIDEOS  ################################################
#        cv2.imshow('crop_img', crop_img)
#        cv2.imshow('fgmask', fgmask)
        cv2.imshow('out',out)
#        cv2.imshow('erodedmask',erodedmask)
        cv2.imshow('dilatedmask', dilatedmask)
#        cv2.imshow('contornos',contornos)        
        cv2.imshow('outputFrame', outputFrame)
#        
        frameCount = frameCount + 1    # Conta a quantidade de Frames
        
        if frameCount == CLOSE_VIDEO: #  fecha o video
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'): #Pressiona a tecla Q para fechar o video
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
