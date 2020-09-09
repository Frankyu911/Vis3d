from django.test import TestCase, Client


# Create your tests here.


class easy_mode_tests(TestCase):
    def test_post_miss(self):
        myfile = open('Test.csv','r')
        data = {'file': myfile,'axis':'x'}
        c = Client()
        response = c.post('/easyUpload/', data)
        print(response.context.get('vis_success'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('vis_success'), 'True')

