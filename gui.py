# coding=utf-8
from shutil import copyfile
import PySimpleGUI as sg
from autolabel.autolabel import *

sg.theme('SystemDefault')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Выберите папку для обработки')],
          [sg.Text('Папка:'), sg.InputText(size=(45, 1), key='folder_input'),
           sg.FolderBrowse(button_text='Открыть', key='folder_browse')],
          [
              sg.Frame(layout=[
                  [sg.Checkbox('Левый верхний', size=(12, 1), enable_events=True, key='LeftTopCB'),
                   sg.Checkbox('Правый верхний', enable_events=True, key='RightTopCB',
                               pad=((0, 69), (0, 0)))],
                  [sg.Checkbox('Левый нижний', size=(12, 1), enable_events=True, key='LeftBottomCB'),
                   sg.Checkbox('Правый нижний', default=True, enable_events=True, key='RightBottomCB',
                               pad=((0, 69), (0, 0)))]
              ], title='Позиция этикетки на обработанном изображении')],
          [
              sg.Frame(pad=((5, 0), (0, 25)), layout=[
                  [sg.Text('Размер текста:', size=(12, 1)), sg.InputText(key='FontSize', size=(3, 1), default_text=50)],
                  [sg.Text('Прозрачность:', size=(12, 1)), sg.InputText(key='Opacity', size=(3, 1), default_text=30)]
              ], title='Этикетка'),
              sg.Frame(layout=[
                  [sg.Text('Размер X:', size=(10, 1)), sg.InputText(key='MaxResX', size=(6, 1), default_text=3000)],
                  [sg.Text('Размер Y:', size=(10, 1)), sg.InputText(key='MaxResY', size=(6, 1), default_text=2250)],
                  [sg.Text('Вес в Мб:', size=(10, 1)), sg.InputText(key='MaxSize', size=(6, 1), default_text=2)]
              ], title='Разрешение')
          ],
          [sg.Button('Открыть таблицу', key='table_open_event', pad=((5, 61), (0, 0))),
           sg.Button('Начать обработку', key='process_event', disabled=True)],
          [sg.Output(size=(60, 20))]]
checkbox_dict = {'LeftTopCB': (0, 0),
                 'RightTopCB': (1, 0),
                 'LeftBottomCB': (0, 1),
                 'RightBottomCB': (1, 1)}

# Create the Window
window = sg.Window('Autolabel-GUI', layout)

while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    if event in checkbox_dict.keys():
        copy = list(checkbox_dict.keys())
        copy.remove(event)
        for key in copy:
            window[key].Update(False)

    if event == 'table_open_event':
        # check for folder
        folder_path = values['folder_input']
        if not os.path.isdir(folder_path):
            print('Выбрана несуществующая папка!')
            continue

        # disable input
        window['folder_input'].update(disabled=True)
        window['folder_browse'].update(disabled=True)
        print('Работаем с папкой: {}'.format(folder_path))
        # copy a default new table to folder
        table_path = folder_path + '/autolabel.xlsx'
        copyfile('autolabel/example.xlsx', table_path)
        print('Создана таблица: {}'.format(table_path))
        # write folder_path to the new table
        work_book = load_workbook(table_path)
        work_sheet = work_book['example']
        work_sheet['B2'] = folder_path
        work_book.save(table_path)
        # write file names to the folder
        write_files_in_xlsx(table_path)
        # open the table
        os.startfile(table_path)

        # enable process button
        window['process_event'].update(disabled=False)

    if event == 'process_event':
        folder_path = values['folder_input']
        table_path = folder_path + '/autolabel.xlsx'

        # load defaults
        _, _, _, sample_text, _, _ = load_defaults(table_path)
        file_dict = load_rows_from_xlsx(table_path, sample_text=sample_text)
        if file_dict is None:
            exit('В таблице нет сведений о файлах для обработки!')
        # delete output folder
        output_folder = list(file_dict.keys())[0].parent / 'output'
        if output_folder.exists() and output_folder.is_dir():
            shutil.rmtree(output_folder)
        # create output folder
        print('Папка результатов: {}'.format(output_folder))
        time.sleep(0.5)  # stupid workaround for WinError 5
        Path(output_folder).mkdir(parents=True, exist_ok=True)

        # process files
        checked_box = 'RightBottomCB'
        for key in checkbox_dict.keys():
            if values[key] is True:
                checked_box = key

        for key in file_dict:
            process_image(key, file_dict[key], output_folder,
                          max_res_x=int(values['MaxResX']), max_res_y=int(values['MaxResY']),
                          max_size=float(values['MaxSize']), opacity=100 - int(values['Opacity']),
                          font_size=int(values['FontSize']), corner=checkbox_dict[checked_box])

        # enable input
        window['folder_input'].update(disabled=False)
        window['folder_browse'].update(disabled=False)

window.close()
