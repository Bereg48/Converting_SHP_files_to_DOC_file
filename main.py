from utils import create_docx_from_shapefile, save_coordinates_to_shp, convert_shp_to_tab


def main():
    """Метод main() представляет собой основной цикл работы умного помощника. Он продолжается до тех пор,
    пока не будет дана команда "выход". Внутри цикла считывается пользовательский ввод с помощью функции input().
    Проверяем, с чего начинается пользовательский ввод, и выполняем соответствующие действия в зависимости от команды. """
    while True:
        user_input = input(
            "1 - Функция определения координат и создания перечня\n"
            "2 - Добавить координаты точек в таблицу атрибутов файла shapefile\n"
            "3 - Конвертировать shapefile в файл формата tab \n"
            "выход - для завершения введите выход;\n"
        )

        if user_input.startswith('1'):
            # Пример вызова функции
            shapefile_path = input('Задай путь файла с расширением .shp')

            # shapefile = 'Europe_National_Provinces_Capitals.shp'
            crs_list = ['EPSG:4326', 'EPSG:3857', 'EPSG:3857']
            doc_path = input('Задай путь файла с расширением .docx')
            # doc_path = 'output_document.docx'
            create_docx_from_shapefile(shapefile_path, crs_list, doc_path)
            result = create_docx_from_shapefile(shapefile_path, crs_list, doc_path)
            print(result)

        elif user_input.startswith('2'):
            # Пример вызова функции
            shapefile_path = input('Задай путь файла с расширением .shp')
            # shapefile = 'Europe_National_Provinces_Capitals.shp'
            save_coordinates_to_shp(shapefile_path)
            result = save_coordinates_to_shp(shapefile_path)
            print(result)

        elif user_input.startswith('3'):
            # Пример вызова функции
            shapefile_path = input('Задай путь файла с расширением .shp')
            # shapefile = 'Europe_National_Provinces_Capitals.shp'
            tabfile = input('Задай путь файла с расширением .tab')
            convert_shp_to_tab(shapefile_path, tabfile)
            result = convert_shp_to_tab(shapefile_path, tabfile)
            print(result)

        elif user_input.lower() == 'выход':
            break

        else:
            print("Неверная команда. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
