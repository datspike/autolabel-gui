# coding=utf-8
import PySimpleGUI as sg

sg.theme('SystemDefault')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Выберите папку для обработки')],
          [sg.Text('Папка:'), sg.InputText(size=(45, 1)), sg.FolderBrowse(button_text='Открыть')],
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
          [sg.Button('Открыть таблицу', key='table_open_event', pad=((5, 61), (0, 0))), sg.Button('Начать обработку', key='process_event')],
          [sg.Output(size=(60, 20))]]
checkbox_keys = ['LeftTopCB', 'RightTopCB', 'LeftBottomCB', 'RightBottomCB']

# Create the Window
window = sg.Window('Autolabel-GUI', layout)

while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    if event in checkbox_keys:
        copy = list(checkbox_keys)
        copy.remove(event)
        for key in copy:
            window[key].Update(False)

window.close()
