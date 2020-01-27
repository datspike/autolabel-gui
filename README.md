# autolabel-gui
GUI для [autolabel](https://github.com/datspike/autolabel) (автоматического этикетирования изображений)
### Сборка
- debug ``pyinstaller gui.py -y --clean -n autolabel --add-data "autolabel;autolabel" -d all``
- release ``pyinstaller gui.py -y --windowed --onefile --clean -n autolabel --add-data "autolabel;autolabel"``

![img](https://i.imgur.com/GsAVkWR.png)