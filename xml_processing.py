import xml.etree.ElementTree as ET
from functions import r
import cv2


def read_xml(xml_file, video):
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
