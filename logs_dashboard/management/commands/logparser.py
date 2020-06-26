import os
import pathlib
import re
from urllib.parse import urlparse

import requests
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from logs_dashboard.models import LogEntry


class Command(BaseCommand):
    help = 'the custom command allows to download the log file and insert data into the database'
    LOG_REGEX = re.compile(r'(?P<ip>[(\d\.)]+) - - \[(?P<date>.*?)\] "(?P<method>.*?) (?P<request_path>.*?) '
                           r'HTTP\/(?P<http_version>.*?)" (?P<status_code>\d+) (?P<response_size>\d+|-) '
                           r'"(?P<referrer>.*?)" "(?P<user_agent>.*?)"')

    def add_arguments(self, parser):
        parser.add_argument('log_url', type=str, action='store', help='url to the log file')
        parser.add_argument('-withoutdelete', action='store_true', help='file will not be deleted if passed')

    def handle(self, **options):
        logs_folder_path = f'{pathlib.Path(__file__).parent.absolute()}/logs_folder/'
        if not os.path.exists(logs_folder_path):
            os.makedirs(logs_folder_path)

        with requests.get(options['log_url'], stream=True) as r:
            if not r.ok:
                raise CommandError(f'URL status code: {r.status_code}')

            file_name = f"{urlparse(options['log_url']).netloc}.log"

            with open(file_name, 'wb') as file:
                with tqdm(total=int(r.headers['Content-Length'])) as pbar:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))

                file.seek(0)

                for line in file:
                    data = self.LOG_REGEX.match(line.decode('utf-8'))
                    try:
                        data = data.groupdict()

                        LogEntry(
                            ip=data['ip'],
                            date=data['date'],
                            method=data['method'],
                            request_path=data['request_path'],
                            http_version=data['http_version'],
                            status_code=data['status_code'],
                            response_size=data['response_size'] if data['response_size'] != '-' else 0,
                            referrer=data['referrer'],
                            user_agent=data['user_agent']
                        ).save()

                    except AttributeError:
                        pass

            self.stdout.write(self.style.SUCCES('Custom command logparser completed'))
