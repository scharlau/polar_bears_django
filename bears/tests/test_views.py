from django.test import Client, TestCase
from bears.models import Bear

# test the views
class BearViewTest(TestCase):
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
    
    def test_index(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Polar bears Tagged for Tracking")
    
    def test_bear(self):
        client = Client()
        response = self.client.get('/bear/1/')
       # print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bear:")
        self.assertContains(response, "222")