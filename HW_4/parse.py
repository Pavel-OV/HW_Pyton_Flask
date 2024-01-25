import argparse


def parse():
    parser = argparse.ArgumentParser(
        description='Загружает изображения из заданного списка URL-адресов')
    parser.add_argument('-u', '--urls', nargs='+', type=str,
                        help='URL-адреса изображений, разделенные пробелом')
    return parser.parse_args()
