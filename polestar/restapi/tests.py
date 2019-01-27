from django.test import TestCase

from restapi.models import Ships, Positions
from restapi.utils import ImportPositions
import datetime
from decimal import Decimal
from django.test import Client

# Create your tests here.

class RestapiTestCase(TestCase):

    def setUp(self):
        Ships.objects.create(imo = '9632179​', name='Mathilde Maersk​')
        Ships.objects.create(imo = '9247455​​', name='Australian Spirit​')
        Ships.objects.create(imo = '9595321​', name='MSC Preziosa​')
        ship = Ships.objects.get(imo = '9595321​')
        Positions.objects.create(ship = ship,
        timestamp = '2019-01-15 07:32:32+00',
        latitude = 17.8564491271973,
        longitude = -63.4953498840332)


    def test_Rest(self):

        ship = Ships.objects.get(imo = '9595321​')

        position = Positions.objects.filter(ship = ship).first()
        self.assertEqual(position.ship.imo, '9595321​')
        self.assertAlmostEqual(position.longitude, Decimal(-63.4953498840332))
# Check import classes (utils.py)
        filename = 'media/import/tests/positions.csv'
        imfile = ImportPositions(filename)
        resp = imfile.update()
        print (resp)
        self.assertEqual(str(resp), "{'details': '2000 row(s) added to the database'}")
# Check end points
        c = Client()
        response = c.post('/api/ships/', {'imo': '0123456', 'name': 'my vessel'})
        self.assertEqual(response.status_code, 200)
        response = c.get('/api/ships/')
        self.assertEqual(response.status_code, 200)

        response = c.get('/api/positions/9595321/')
        self.assertEqual(response.status_code, 200)

