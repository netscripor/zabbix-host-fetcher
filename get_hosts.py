#!/usr/bin/env python3
import argparse
import getpass
import urllib3
from pyzabbix import ZabbixAPI

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_args():
    parser = argparse.ArgumentParser(
        description="Получение списка хостов из Zabbix по группе, шаблону и тегам"
    )
    parser.add_argument('--zabbix-url', default='https://10.10.10.10', help='URL сервера Zabbix')
    parser.add_argument('--user', help='Логин Zabbix')
    parser.add_argument('--password', help='Пароль Zabbix (не рекомендуется в командной строке)')
    parser.add_argument('--group', help='Имя группы хостов')
    parser.add_argument('--template', help='Имя шаблона')
    parser.add_argument('--tag', nargs='*', help='Фильтрация по тегам (key=value)')
    parser.add_argument('--mode', choices=['host', 'name'], default='host', help='Тип вывода: host (IP) или name')
    parser.add_argument('--output', default='output_hosts.txt', help='Файл для сохранения результатов')
    return parser.parse_args()

def main():
    args = get_args()

    z_username = args.user or input('Username: ')
    z_password = args.password or getpass.getpass('Password: ')

    zapi = ZabbixAPI(args.zabbix_url)
    zapi.session.verify = False
    zapi.login(z_username, z_password)

    # Получение groupid
    group_id = None
    if args.group:
        group = zapi.hostgroup.get(filter={'name': args.group})
        if group:
            group_id = group[0]['groupid']
        else:
            print(f'[!] Группа не найдена: {args.group}')
            return

    # Получение templateid
    template_id = None
    if args.template:
        template = zapi.template.get(filter={'name': args.template})
        if template:
            template_id = template[0]['templateid']
        else:
            print(f'[!] Шаблон не найден: {args.template}')
            return

    # Подготовка фильтра по тегам
    tags = []
    if args.tag:
        for tag_pair in args.tag:
            if '=' in tag_pair:
                key, value = tag_pair.split('=', 1)
                tags.append({'tag': key.strip(), 'value': value.strip()})
            else:
                print(f"[!] Неверный формат тега: {tag_pair}. Используйте key=value")

    # Получение хостов
    hosts = zapi.host.get(
        groupids=group_id,
        templateids=template_id,
        selectTags='extend',
        selectInterfaces=['ip'],
        output=['host', 'name']
    )

    # Фильтрация по тегам (если указаны)
    if tags:
        def host_matches_tags(host):
            host_tags = host.get('tags', [])
            return all(any(t['tag'] == ft['tag'] and t['value'] == ft['value'] for t in host_tags) for ft in tags)
        hosts = [h for h in hosts if host_matches_tags(h)]

    # Вывод
    with open(args.output, 'w') as f:
        for h in hosts:
            if args.mode == 'name':
                line = h['name']
            elif args.mode == 'host':
                interfaces = h.get('interfaces', [])
                line = interfaces[0]['ip'] if interfaces else '[no ip]'
            print(line)
            f.write(line + '\n')

    print(f'[✓] Найдено {len(hosts)} хостов. Сохранено в {args.output}')

if __name__ == '__main__':
    main()
