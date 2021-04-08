import config
import sys
import os
import argparse
import colorama
import json

colorama.init()
c_reset = colorama.Style.RESET_ALL

settings = {
    'dir': 'p:\\folder_icons\\',
    'dir_ignore': ['.git', '.gitignore', '.idea', 'demo.md', 'README.md', 'LICENSE']
}


def get_title(file):
    separators = {'_': ' ', '-': ' ', '|': ' '}
    trans = str.maketrans(separators)
    title = file.split('.')[0].translate(trans).title()
    return title


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interactive', action='store_const', const=True, default=False)
    parser.add_argument('-c', '--create', action='store_const', const=True, default=False)
    parser.add_argument('-p', '--parse', action='store_const', const=True, default=False)
    parser.add_argument('-d', '--debug', action='store_const', const=True, default=False)

    return parser


def files_parser(debug_mode):
    if debug_mode:
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + 'Запущен парсер файлов' + c_reset)
        print(colorama.Fore.GREEN + 'Работаем в: ' + c_reset + settings['dir'])
        try:
            print(colorama.Fore.GREEN + 'Смотрим на: ' + c_reset + ', '.join(set(os.listdir(settings['dir'])) - set(
                settings['dir_ignore'])))
        except FileNotFoundError:
            print(colorama.Fore.RED + 'Путь указан неверно' + c_reset)
            return False
    try:
        catalogs = sorted(set(os.listdir(settings['dir'])) - set(settings['dir_ignore']))
    except FileNotFoundError:
        catalogs = None
        print(
            colorama.Fore.RED + colorama.Style.BRIGHT + 'err: ' + c_reset + 'Путь к исходному каталогу указан неверно')
        return False
    output = dict()
    for catalog in catalogs:
        catalog_files = os.listdir(settings['dir'] + catalog)
        output[catalog] = {file_name: get_title(file_name) for file_name in catalog_files}

        if debug_mode:
            print(colorama.Fore.BLACK + colorama.Back.WHITE + catalog + ':' + c_reset + ' ' + str(catalog_files))

    if debug_mode: print('\n' + str(output) + '\n')
    with open('structure.json', 'w') as write_file:
        json.dump(output, write_file, indent=2)
        if debug_mode:
            print(colorama.Fore.GREEN + 'Создан structure.json' + c_reset)
    if debug_mode:
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + 'Завершен парсер файлов' + c_reset)
        return True


def create_table(debug_mode):
    if debug_mode:
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + 'Запущен генератор' + c_reset)
        try:
            f = open('structure.json', 'r')
            print(colorama.Fore.GREEN + 'Подключаем structure.json' + c_reset)
            f.close()
        except FileNotFoundError:
            print(colorama.Fore.RED + 'Файл structure.json не найден' + c_reset)
            return False
    try:
        with open('structure.json', 'r') as in_file:
            structure = json.load(in_file)
            if debug_mode: print(structure, type(structure))
    except FileNotFoundError:
        structure = None
        print(
            colorama.Fore.RED + colorama.Style.BRIGHT + 'err: ' + c_reset + 'Файл structure.json не найден. Запустите парсер')
        return False
    output = []

    for catalog in structure:
        output.extend(['<h2>{}</h2>'.format(catalog), '<table border="1px">', '<tbody>'])
        row_icons = []
        out = []
        for num, file_name in enumerate(structure[catalog], start=1):
            title = structure[catalog][file_name]
            html = '<td>' + str(num) + ' ' + file_name + ' ' + title + '</td>'
            if num == 1:
                row_icons.extend(['<tr>', html])
            elif num % 5 == 0 and num < len(structure[catalog]):
                row_icons.extend([html, '</tr>', '<tr>'])
            else:
                row_icons.append(html)
        else:
            row_icons.extend(['</tr>'])

        output.extend([*row_icons, '</tbody>', '</table><br>\n'])
    print(colorama.Fore.GREEN + 'Таблица создана' + c_reset)
    with open('table.html', 'w') as write_file:
        for line in output:
            write_file.write(line + '\n')
        if debug_mode:
            print(colorama.Fore.GREEN + 'Таблица записана в table.html' + c_reset)
    return True


if __name__ == "__main__":
    cli_parser = create_parser()
    namespace = cli_parser.parse_args(sys.argv[1:])

    print(
        colorama.Style.BRIGHT + '\nfolder_icons readme generator v{0}.{1}.{2} by {3}\n'.format(config.VERSION['major'],
                                                                                               config.VERSION['minor'],
                                                                                               config.VERSION['micro'],
                                                                                               config.AUTHOR) + c_reset)

    if namespace.interactive + namespace.create + namespace.parse > 1:
        # проверяем количество флагов
        print(colorama.Fore.RED + colorama.Style.BRIGHT + 'err: ' + c_reset + 'Слишком много аргументов. RTFM!')
        print(colorama.Style.RESET_ALL)
        exit(0)

    if namespace.parse:
        result = files_parser(namespace.debug)
        if namespace.debug and result:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + 'files_parser выполнен успешно' + c_reset)
        elif namespace.debug:
            print(colorama.Style.BRIGHT + colorama.Fore.RED + 'files_parser завершен с ошибкой' + c_reset)
        else:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + 'Готово!' + c_reset)

    if namespace.create:
        result = create_table(namespace.debug)
        if namespace.debug and result:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + 'create_table выполнен успешно' + c_reset)
        elif namespace.debug:
            print(colorama.Style.BRIGHT + colorama.Fore.RED + 'create_table завершен с ошибкой' + c_reset)
        else:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + 'Готово!' + c_reset)
else:
    print('fuckup')
