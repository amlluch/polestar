from django.db import models
from django.core.management.base import BaseCommand, CommandError
from restapi.utils import ImportPositions, ResponseException

import os
import json

class Command(BaseCommand):
    help = 'Import CSV positions'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str, help='CSV file(s) to be imported')
        parser.add_argument('-p', '--path', nargs=1, type=str, dest='path', help='Path to the import and result files directory')
        parser.add_argument( '--prefix', nargs=1, type=str, dest='prefix', help='Prefix for result files')
        parser.add_argument('--csv', action='store_true', dest='csv', help='Write results in csv files')
        parser.add_argument('--json', action='store_true', dest='json', help='Write results in json files')

    def handle(self, *args, **options):
        if options['path']:
            import_path = os.path.dirname(options['path'][0]) + '/'
        else:
            import_path = ''
        for file in options['file']:
            if import_path == '':
                import_path_file = os.path.dirname(file) + '/'
            else:
                import_path_file = import_path
            import_file = import_path_file + os.path.basename(file)
            positions = ImportPositions(import_file)
            try:
                result = positions.update()
            except ResponseException as err:
                self.stdout.write(self.style.ERROR(err.message['details']))
                continue
            if options['prefix']:
                prefix = options['prefix'][0]
            else:
                prefix = 'result_'
            if options['json']:
                try:
                    jsonfile = open(import_path_file + prefix + os.path.basename(file) + '.json', 'w')
                except IOError as err:
                    self.stdout.write(self.style.ERROR(err.strerror))
                    continue
                with jsonfile:
                    jsonfile.write('{"details":"' + result['details'] + '",')
                    if 'errors' in result:
                        jsonfile.write('"errors":"' + result['errors'] + '",')
                        jsonfile.write('"lines":')
                        mylines = ''.join('"' + line.rstrip('\n') + '",'  for line in result['lines'] )
                        jsonfile.write('[' + mylines + ']' + ',')
                    jsonfile.write('}')
            if options['csv']:
                try:
                    csvfile = open(import_path_file + prefix + os.path.basename(file) + '.csv', 'w')
                except IOError as err:
                    self.stdout.write(self.style.ERROR(err.strerror))
                    continue
                with csvfile:
                    csvfile.write('details: ' + result['details'] + '\n')
                    if 'errors' in result:
                        csvfile.write('errors: ' + result['errors'] + '\n')
                        csvfile.write('lines: \n')
                        csvfile.write(''.join(result['lines']))
            self.stdout.write(self.style.SUCCESS(result['details'] + ' from file {file}'.format(file=import_file)))
