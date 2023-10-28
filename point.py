from tkinter import Tk, Button, OptionMenu, StringVar, Label
from tkinter import filedialog
from tkinter.ttk import Progressbar
import time


def option1():
    shapefile_path = filedialog.askopenfilename(filetypes=[("Shapefile files", "*.shp")])
    if shapefile_path:
        # Создание и размещение виджета OptionMenu внутри функции option1
        crs_list = ['EPSG:4326', 'EPSG:3857', 'EPSG:3857']
        selected_crs = StringVar(root)
        selected_crs.set(crs_list[0])  # Set the default selected crs value

        crs_option_menu = OptionMenu(root, selected_crs, *crs_list)
        crs_option_menu.pack()
        doc_path = filedialog.asksaveasfilename(defaultextension=".docx")
        if doc_path:
            # Использование прогресс бара для отображения прогресса операции
            progress = Progressbar(root, orient="horizontal", length=200, mode="determinate")
            progress.pack()

            progress["maximum"] = 100

            # Здесь вы можете вызвать вашу функцию create_docx_from_shapefile()
            for i in range(101):
                time.sleep(0.1)  # Замените это секцией вашего кода
                progress["value"] = i
                progress.update()

            label_result.config(text="Успешно созданный файл docx!")
        else:
            label_result.config(text="No docx path selected")
    else:
        label_result.config(text="No shapefile selected")


def option3():
    shapefile_path = filedialog.askopenfilename(filetypes=[("Shapefile files", "*.shp")])
    if shapefile_path:
        crs_list = ['EPSG:4326', 'EPSG:3857', 'EPSG:3857']
        tabfile = filedialog.asksaveasfilename(defaultextension=".tab")
        if tabfile:
            # Использование прогресс бара для отображения прогресса операции
            progress = Progressbar(root, orient="horizontal", length=200, mode="determinate")
            progress.pack()

            progress["maximum"] = 100

            # Здесь вы можете вызвать вашу функцию convert_shp_to_tab()
            for i in range(101):
                time.sleep(0.1)  # Замените это секцией вашего кода
                progress["value"] = i
                progress.update()

            label_result.config(text="Successfully converted shp file to tab!")
        else:
            label_result.config(text="No tab file path selected")
    else:
        label_result.config(text="No shapefile selected")


root = Tk()
root.title("Программа")

button_option1 = Button(root, text="Создание документа на основе слоя", command=option1)
button_option1.pack()

button_option3 = Button(root, text="Конвертирование shp файла в tab", command=option3)
button_option3.pack()

label_result = Label(root)
label_result.pack()

root.mainloop()
