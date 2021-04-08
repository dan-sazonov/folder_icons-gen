import config
import sys
import os
import argparse
import colorama

colorama.init()
c_reset = colorama.Style.RESET_ALL

settings = {
    'dir': 'p:\\folder_icons',
    'dir_ignore': ['.git', '.gitignore', '.idea', 'demo.md', 'README.md', 'LICENSE']
}


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interactive', action='store_const', const=True, default=False)
    parser.add_argument('-m', '--manual', action='store_const', const=True, default=False)
    parser.add_argument('-c', '--create', action='store_const', const=True, default=False)
    parser.add_argument('-p', '--parse', action='store_const', const=True, default=False)
    parser.add_argument('-d', '--debug', action='store_const', const=True, default=False)

    return parser


def files_parser(debug_mode):
    if debug_mode:
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + 'Запущен парсер файлов' + c_reset)
        print(colorama.Fore.GREEN + 'Работаем в: ' + c_reset + settings['dir'])
        print(colorama.Fore.GREEN + 'Смотрим на: ' + c_reset + ', '.join(set(os.listdir(settings['dir'])) - set(
            settings['dir_ignore'])))


def create_table(debug_mode):
    if debug_mode:
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + 'запущен генератор' + c_reset)


if __name__ == "__main__":
    cli_parser = create_parser()
    namespace = cli_parser.parse_args(sys.argv[1:])

    print(
        colorama.Style.BRIGHT + '\nfolder_icons readme generator v{0}.{1}.{2} by {3}\n'.format(config.VERSION['major'],
                                                                                               config.VERSION['minor'],
                                                                                               config.VERSION['micro'],
                                                                                               config.AUTHOR) + c_reset)

    if namespace.interactive + namespace.manual + namespace.create + namespace.parse > 1:
        # проверяем количество флагов
        print(colorama.Fore.RED + colorama.Style.BRIGHT + 'err: ' + c_reset + 'Слишком много аргументов. RTFM!')
        print(colorama.Style.RESET_ALL)
        exit(0)

    if namespace.parse:
        files_parser(namespace.debug)

    if namespace.create:
        create_table(namespace.debug)
