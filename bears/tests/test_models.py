from django.test import Client, TestCase
from bears.models import Bear

#set up the models

class BearModelTest (TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up test data in database
        Bear.objects.create(bearID = 222,
                pTT_ID = 345,
                capture_lat = 70.87402954,
                capture_long = -152.5647827,
                sex = 'M',
                age_class = 'A',
                ear_applied = 'left',
                )
        Bear.objects.create(bearID = 223,
                pTT_ID = 346,
                capture_lat = 70.87402955,
                capture_long = -152.5647829,
                sex = 'F',
                age_class = 'A',
                ear_applied = 'left',
                )
        
    def test_bears(self):
        bear = Bear.objects.get(id=1)
        self.assertEqual(bear.pTT_ID, 345)
        bears =Bear.objects.all()
        self.assertEqual(bears.count(), 2)


