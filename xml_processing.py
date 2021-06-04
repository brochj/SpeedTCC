import xml.etree.ElementTree as ET
from functions import r


def read_xml(xml_file, video, DATE):
    # Funcão que lê o .xml e guarda as informações em um dicionário "iframe"
    tree = ET.parse(xml_file)
    root = tree.getroot()
    iframe = {}
    lane1_count = 0
    lane2_count = 0
    lane3_count = 0
    for child in root:
        if child.get('radar') == 'True':
            for subchild in child:
                #                print('subchild {}'.format(subchild.attrib))
                if subchild.tag == 'radar':
                    # salva frame_end, frame_start, speed
                    iframe[child.get('iframe')] = subchild.attrib
                    iframe[child.get('iframe')]['lane'] = child.get('lane')
                    iframe[child.get('iframe')]['radar'] = child.get('radar')
                    iframe[child.get('iframe')]['moto'] = child.get('moto')
#                    iframe[child.get('iframe')]['plate'] = child.get('plate')  # Desnecessário
#                    iframe[child.get('iframe')]['sema'] = child.get('sema')  # Desnecessário
                    speed = iframe[child.get('iframe')]['speed']
                    frame_start = iframe[child.get('iframe')]['frame_start']
                    frame_end = iframe[child.get('iframe')]['frame_end']

                    if child.get('lane') == '1':
                        lane1_count += 1
                    if child.get('lane') == '2':
                        lane2_count += 1
                    if child.get('lane') == '3':
                        lane3_count += 1

                    # if iframe[child.get('iframe')]['lane'] == '1':
                    #     file = open(f'results/{DATE}/planilhas/video{video}_real_lane1.csv', 'a')
                    #     file.write(f'frame_start, {frame_start}, frame_end, {frame_end}, speed, {speed} \n')
                    #     file.close()
                    # if iframe[child.get('iframe')]['lane'] == '2':
                    #     file = open(f'results/{DATE}/planilhas/video{video}_real_lane2.csv', 'a')
                    #     file.write(f'frame_start, {frame_start}, frame_end, {frame_end}, speed, {speed} \n')
                    #     file.close()
                    # if iframe[child.get('iframe')]['lane'] == '3':
                    #     file = open(f'results/{DATE}/planilhas/video{video}_real_lane3.csv', 'a')
                    #     file.write(f'frame_start, {frame_start}, frame_end, {frame_end}, speed, {speed} \n')
                    #     file.close()
        if child.tag == 'videoframes':
            iframe[child.tag] = int(child.get('total'))

    iframe['total_cars_lane1'] = lane1_count
    iframe['total_cars_lane2'] = lane2_count
    iframe['total_cars_lane3'] = lane3_count

    file_name = xml_file[xml_file.rfind('/')+1:]
    print('Arquivo "{}" foi lido com sucesso !!'.format(file_name))

    return iframe


def update_info_xml(frameCount, vehicle, dict_lane1, dict_lane2, dict_lane3):
    def save_value(dict_lane):
        dict_lane['speed'] = vehicle[str(frameCount)]['speed']
        dict_lane['frame_start'] = vehicle[str(frameCount)]['frame_start']
        dict_lane['frame_end'] = vehicle[str(frameCount)]['frame_end']
    try:
        # Verifica se naquele frame tem uma chave correspondente no dicionário "vehicle"
        if vehicle[str(frameCount)]['frame_start'] == str(frameCount):
            lane_state = vehicle[str(frameCount)]['lane']

            if lane_state == '1':  # Se for na faixa 1, armazena as seguintes infos
                save_value(dict_lane1)
            elif lane_state == '2':
                save_value(dict_lane2)
            elif lane_state == '3':
                save_value(dict_lane3)
    except KeyError:
        pass


def print_xml_values(frame, dict_lane1, dict_lane2, dict_lane3):
    # Mostra no video os valores das velocidades das 3 Faixas.
    try:  # Posição do texto da FAIXA 1
        text_pos = (r(143), r(43))
        cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20),
                      (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
        cv2.putText(frame, 'speed: {}'.format(
            dict_lane1['speed']), text_pos, 2, .6, (255, 255, 0), 1)
    except:
        pass

    try:  # Posição do texto da FAIXA 2
        text_pos = (r(628), r(43))
        cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20),
                      (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
        cv2.putText(frame, 'speed: {}'.format(
            str(dict_lane2['speed'])), text_pos, 2, .6, (255, 255, 0), 1)
    except:
        pass

    try:  # Posição do texto da FAIXA 3
        text_pos = (r(1143), r(43))
        cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20),
                      (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
        cv2.putText(frame, 'speed: {}'.format(
            dict_lane3['speed']), text_pos, 2, .6, (255, 255, 0), 1)
    except:
        pass
