import os
import re

import requests
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from logs_dashboard.models import LogEntry


class Command(BaseCommand):
    help = 'the custom command allows to download the log file and insert data into the database'
    LOG_REGEX = re.compile(r'(?P<ip>.*) - - \[(?P<date>.*)\] "(?P<method>\w*) (?P<request_path>.*) '
                           r'HTTP\/(?P<http_version>.*)" (?P<status_code>\d+) (?P<response_size>\d+) '
                           r'"(?P<referrer>.*)" "(?P<user_agent>.*)" "-"')

    def add_arguments(self, parser):
        parser.add_argument('log_url', type=str, action='store', help='url to the log file')

    def handle(self, **options):
        with requests.get(options['log_url'], stream=True) as r:
            if not r.ok:
                raise CommandError(f'URL status code: {r.status_code}')

            with tqdm(total=int(r.headers['Content-Length'])) as pbar:
                not_ended_line = None  # Переменная необходима, чтобы перенести незаконченную строку на следующий цикл
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        for line in chunk.decode('utf-8').splitlines():
                            try:
                                if not_ended_line:
                                    line = not_ended_line + line

                                data = self.LOG_REGEX.match(line).groupdict()

                                LogEntry(ip=data['ip'],
                                         date=data['date'],
                                         method=data['method'],
                                         request_path=data['request_path'],
                                         http_version=data['http_version'],
                                         status_code=data['status_code'],
                                         response_size=data['response_size'] if data['response_size'].isdigit() else 0,
                                         referrer=data['referrer'],
                                         user_agent=data['user_agent']
                                         ).save()

                                not_ended_line = None  # Должна быть всегда None, если регулярка успешно совпала

                            except AttributeError:  # В случае несовпадения регулярки, строку переносим на другой цикл
                                if line:
                                    not_ended_line = line
                            # except Exception as err:
                            #     print_err = f'ERR: {err}|nLINE: {line}'
                            #     print(print_err)

                        pbar.update(len(chunk))

            self.stdout.write(self.style.SUCCES('Custom command logparser completed'))
