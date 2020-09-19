from django.test import TestCase, Client

"""
    Create your tests here.
    True -- visualize successfully
    False -- visualize unsuccessfully
    Out -- the value of axis is out of range
    NoResult -- No results match
"""

"""The following are upload methods for four modes."""

def easy_uplpad(filename,axis):
    myfile = open(filename,'r')
    data = {'file': myfile,'axis':axis}
    c = Client()
    response = c.post('/easyUpload/', data)
    return response

def accurate_uplpad(filename,axis,value):
    myfile = open(filename,'r')
    data = {'file': myfile,'axis':axis,'values':value}
    c = Client()
    response = c.post('/accurateUpload/', data)
    return response

def compare_uplpad(filename,axis,value,filename_second,axis_second,value_second):
    myfile = open(filename,'r')
    myfile_second = open(filename_second,'r')
    data = {'file': myfile,'axis':axis,'values':value,'files': myfile_second,'axiss':axis_second,'valuess':value_second}
    c = Client()
    response = c.post('/compareUpload/', data)
    return response

def calculate_uplpad(filename,x_value,y_value,z_value):
    myfile = open(filename,'r')
    c = Client()
    data = {'file': myfile,'x_values':x_value,'y_values':y_value,'z_values':z_value}
    response = c.post('/calculateUpload/', data)
    return response


"""The following are test cases for four modes.It is classified according to the test method."""
class easy_mode_tests(TestCase):
    def test_post_wrong_file(self):
        data = {'file': '','axis':'x'}
        c = Client()
        response = c.post('/easyUpload/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('vis_success'), 'False')

    def test_post_miss(self):
        response = easy_uplpad('Test.csv','x')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('vis_success'), 'True')

class accurate_mode_tests(TestCase):
    def test_post_wrong_file(self):
        data = {'file': '','axis':'x'}
        c = Client()
        response = c.post('/accurateUpload/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('vis_success'), 'False')

    def test_out_of_range(self):
        response = accurate_uplpad('Test.csv','x','1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('vis_success'), 'Out')

class compare_mode_tests(TestCase):
    def test_post_wrong_file(self):
        data = {'file': '','axis':'x'}
        c = Client()
        response = c.post('/compareUpload/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('vis_success'), 'False')

    def test_post_one_wrong_file(self):
        myfile = open('Test.csv','r')
        data = {'file': myfile,'axis':'x','values': 0.01,'files': '','axiss':'y','valuess':0.02}
        c = Client()
        response = c.post('/compareUpload/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('vis_success'), 'False')

    def test_out_of_range(self):
        response =compare_uplpad('Test.csv','x','1','Test.csv','x','1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('vis_success'), 'False')


class calculate_mode_tests(TestCase):
    def test_post_wrong_file(self):
        data = {'file': '','axis':'x'}
        c = Client()
        response = c.post('/calculateUpload/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('vis_success'), 'False')

    def test_no_result(self):
        response = calculate_uplpad('Test.csv','1','0.01','0.01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('vis_success'), 'NoResult')
