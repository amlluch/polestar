from __future__ import unicode_literals

from rest_framework import status
from decimal import Decimal

from .models import Ships, Positions

class ResponseException(Exception):
    def __init__(self, message, status):
        self.message = message
        self.status = status


class ImportPositions():
    def __init__(self, file_path = None):
        self.file_path = file_path

    def update(self, file_path = None):
        if file_path:   # path given on constructor or on method
            self.file_path = file_path

        if not self.file_path:
            raise ResponseException ({'details': 'No file provided'}, status.HTTP_400_BAD_REQUEST)
        try:
            file = open(self.file_path, 'r')
        except IOError as err:
            raise ResponseException ({'details':err.strerror + ' ' + self.file_path}, status.HTTP_400_BAD_REQUEST)
        else:
            with file:
            
                rows = 0
                errors = 0
                error_lines = []
                for line in file:
                    imo = line.split(',')[0].strip()
                    elements = line.strip().split(',')

                    ship = Ships.objects.filter(imo__contains = imo)
                    if len(ship)==1:
                        try:
                            Positions.objects.create(ship=ship[0], timestamp = elements[1], latitude = Decimal(elements[2]), longitude = Decimal(elements[3]))
                            rows +=1
                        except:  # if errors on timestamp, latitude or longitude => discard
                            error_lines.append(line)
                            errors += 1
                    else:   # if there is no ship or more than one ship with the same code, discard
                        error_lines.append(line)
                        errors += 1
# it creates serialized response using a dict                  
            response = dict()
            if rows == 0:   # if everything went wrong
                response['details'] = 'No rows added to the database'
            else:
                response['details'] = str(rows) + ' row(s) added to the database'
            if errors >0:   # show line by line errors if any
                response['errors'] = str(errors) + ' line(s) with error'
                response['lines'] = error_lines
            return response
