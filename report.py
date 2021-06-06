
DATE = f'video{VIDEO}_{now.day}-{now.month}-{now.year}_{now.hour}-{now.minute}-{now.second}'

if iframe[child.get('iframe')]['lane'] == '1':
    file = open(f'results/{DATE}/planilhas/video{video}_real_lane1.csv', 'a')
    file.write(
        f'frame_start, {frame_start}, frame_end, {frame_end}, speed, {speed} \n')
    file.close()
if iframe[child.get('iframe')]['lane'] == '2':
    file = open(f'results/{DATE}/planilhas/video{video}_real_lane2.csv', 'a')
    file.write(
        f'frame_start, {frame_start}, frame_end, {frame_end}, speed, {speed} \n')
    file.close()
if iframe[child.get('iframe')]['lane'] == '3':
    file = open(f'results/{DATE}/planilhas/video{video}_real_lane3.csv', 'a')
    file.write(
        f'frame_start, {frame_start}, frame_end, {frame_end}, speed, {speed} \n')
    file.close()


results_lane1[str(lane1_tracking.closest_blob['id'])] = dict(ave_speed=round(ave_speed, 2),
                                                             speeds=lane1_tracking.closest_blob[
    'speed'],
    frame=frameCount,
    real_speed=float(
    dict_lane1['speed']),
    abs_error=round(
    abs_error, 2),
    per_error=round(
    per_error, 3),
    trail=lane1_tracking.closest_blob[
    'trail'],
    car_id=lane1_tracking.closest_blob['id'])


results_lane2[str(lane2_tracking.closest_blob['id'])] = dict(ave_speed=round(ave_speed, 2),
                                                             speeds=lane2_tracking.closest_blob['speed'],
                                                             frame=frameCount,
                                                             real_speed=float(
                                                                 dict_lane2['speed']),
                                                             abs_error=round(
    abs_error, 2),
    per_error=round(
    per_error, 3),
    trail=lane2_tracking.closest_blob[
    'trail'],
    car_id=lane2_tracking.closest_blob['id'])


results_lane3[str(lane3_tracking.closest_blob['id'])] = dict(ave_speed=round(ave_speed, 2),
                                                             speeds=lane3_tracking.closest_blob[
    'speed'],
    frame=frameCount,
    real_speed=float(
    dict_lane3['speed']),
    abs_error=round(
    abs_error, 2),
    per_error=round(
    per_error, 3),
    trail=lane3_tracking.closest_blob[
    'trail'],
    car_id=lane3_tracking.closest_blob['id'])


def separar_por_kmh(abs_error_list_mod):
    list_3km = []  # erros até 3km/h
    list_5km = []  # erros até 5km/h
    list_maior5km = []  # maiores que 5km/h
    for value in abs_error_list_mod:
        if value <= 3:
            list_3km.append(value)
        elif value > 3 and value <= 5:
            list_5km.append(value)
        else:
            list_maior5km.append(value)
    return list_3km, list_5km, list_maior5km


def plot_graph(abs_error_list, ave_abs_error, ave_per_error, rate_detec_lane,
               real_total_lane, total_cars_lane, DATE, lane, VIDEO, cf, SHOW_LIN,
               list_3km, list_5km, list_maior5km):

    plt.figure(lane, figsize=[9, 7])
    plt.plot(abs_error_list, 'o-')

    plt.plot([0, len(abs_error_list) + 3], [0, 0],
             color='k', linestyle='-', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [3, 3],
             color='k', linestyle=':', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [-3, -3],
             color='k', linestyle=':', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [5, 5],
             color='k', linestyle='--', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [-5, -5],
             color='k', linestyle='--', linewidth=1)

    if lane == 'total':
        titulo = 'Resultado Total'
    else:
        titulo = f'Resultados da Faixa {lane}'
    plt.xlabel('Medições')
    plt.ylabel('Erro Absoluto (km/h)')
    plt.title(f'{titulo} - Video {VIDEO} \n\n'
              f'Média dos erros absolutos =  {ave_abs_error} km/h\n'
              f'Média dos erros percentuais = {ave_per_error} % \n'
              f' Qtnd de erros até 3km/h: {len(list_3km)} de {real_total_lane} ({round(len(list_3km)/real_total_lane*100, 2)} %)\n'
              f' Qtnd de erros até 5km/h: {len(list_5km)} de {real_total_lane} ({round(len(list_5km)/real_total_lane*100, 2)} %)\n'
              f' Qtnd de erros > 5km/h: {len(list_maior5km)} de {real_total_lane} ({round(len(list_maior5km)/real_total_lane*100, 2)} %)\n'
              f'Taxa de Detecção: {rate_detec_lane} % \n'
              f'Carros detectados: {total_cars_lane} de {real_total_lane} \n'
              f'Fator de correção: {cf}')
    plt.xlim(0, len(abs_error_list) + 3)
    plt.grid(False)

    plt.savefig(f'results/{DATE}/graficos/result_{DATE}_F{lane}.png',
                bbox_inches='tight', pad_inches=0.3)
    plt.savefig(f'results/{DATE}/graficos/pdfs/result_{DATE}_F{lane}.pdf',
                bbox_inches='tight', pad_inches=0.3)
    plt.show()

    if SHOW_LIN:
        plt.figure('Total', figsize=[9, 7])
        abs_list = []
        for value in abs_error_list:
            abs_list.append(abs(value))

        font = {'size': 16}
        plt.rc('font', **font)

        plt.xlabel('Medições')
        plt.ylabel('Erro Absoluto (km/h)')
#        plt.title(f'{titulo} - Video {VIDEO} \n\n'
#              f'Média dos erros absolutos =  {ave_abs_error} km/h\n'
#              f'Média dos erros percentuais = {ave_per_error} % \n'
#              f' Qtnd de erros até 3km/h: {len(list_3km)} de {real_total_lane} ({round(len(list_3km)/real_total_lane*100, 2)} %)\n'
#              f' Qtnd de erros até 5km/h: {len(list_5km)} de {real_total_lane} ({round(len(list_5km)/real_total_lane*100, 2)} %)\n'
#              f' Qtnd de erros > 5km/h: {len(list_maior5km)} de {real_total_lane} ({round(len(list_maior5km)/real_total_lane*100, 2)} %)\n'
#              f'Taxa de Detecção: {rate_detec_lane} % \n'
#              f'Carros detectados: {total_cars_lane} de {real_total_lane} \n'
#              f'Fator de correção: {cf}')

        plt.plot([0, len(abs_error_list) + 3], [0, 0],
                 color='k', linestyle='-', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [3, 3],
                 color='k', linestyle=':', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [-3, -3],
                 color='k', linestyle=':', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [5, 5],
                 color='k', linestyle='--', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [-5, -5],
                 color='k', linestyle='--', linewidth=1)

        plt.plot(abs_error_list, 'ro-')
        plt.savefig(f'results/{DATE}/graficos/result_{DATE}_F{lane}_lin.png',
                    bbox_inches='tight', pad_inches=0.3)
        plt.savefig(f'results/{DATE}/graficos/pdfs/result_{DATE}_F{lane}_lin.pdf',
                    bbox_inches='tight', pad_inches=0.3)

#    if SHOW_LIN:
#        plt.figure('Total', figsize=[9,7])
#        abs_list = []
#        for value in abs_error_list:
#            abs_list.append(abs(value))
#
#        plt.xlabel('Medições')
#        plt.ylabel('Erro Absoluto (km/h)')
#        plt.title(f'{titulo} - Video {VIDEO} \n\n'
#              f'Média dos erros absolutos =  {ave_abs_error} km/h\n'
#              f'Média dos erros percentuais = {ave_per_error} % \n'
#              f' Qtnd de erros até 3km/h: {len(list_3km)} de {real_total_lane} ({round(len(list_3km)/real_total_lane*100, 2)} %)\n'
#              f' Qtnd de erros até 5km/h: {len(list_5km)} de {real_total_lane} ({round(len(list_5km)/real_total_lane*100, 2)} %)\n'
#              f' Qtnd de erros > 5km/h: {len(list_maior5km)} de {real_total_lane} ({round(len(list_maior5km)/real_total_lane*100, 2)} %)\n'
#              f'Taxa de Detecção: {rate_detec_lane} % \n'
#              f'Carros detectados: {total_cars_lane} de {real_total_lane} \n'
#              f'Fator de correção: {cf}')
#
#        plt.plot([0, len(abs_list) + 3], [0, 0], color='k', linestyle='-', linewidth=1)
#        plt.plot([0, len(abs_list) + 3], [3, 3], color='k', linestyle=':', linewidth=1)
#        plt.plot([0, len(abs_list) + 3], [5, 5], color='k', linestyle='--', linewidth=1)
#
#        plt.plot(sorted(abs_list), 'ro-')
#        plt.savefig(f'results/{DATE}/graficos/result_{DATE}_F{lane}_lin.png', bbox_inches='tight', pad_inches=0.3)
#        plt.savefig(f'results/{DATE}/graficos/pdfs/result_{DATE}_F{lane}_lin.pdf', bbox_inches='tight', pad_inches=0.3)
