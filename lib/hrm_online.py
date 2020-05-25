import bs4
from faker import Faker
from requests import Session


class HrmOnline(object):
    def __init__(self, base_url='http://hrm-online.portnov.com/symfony/web/index.php'):
        self.url = base_url
        self.sess = Session()
        self.sess.headers.update({
                                     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                                                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 '
                                                   'Safari/537.36'}
                                 )
        self.faker = Faker()

    def extract_emp_id(self, resp):
        resp = self.sess.get(resp.url)
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        actual_emp_id = soup.select_one('#personal_txtEmployeeId')['value']
        return actual_emp_id

    def login(self, username, password):
        login_uri = "/auth/login"
        resp = self.sess.get(self.url + login_uri)
        token = self.extract_token(resp)
        authenticate_uri = '/auth/validateCredentials'
        login_data = {
            '_csrf_token': token,
            'txtUsername': username,
            'txtPassword': password
        }
        resp = self.sess.post(self.url + authenticate_uri, data=login_data)
        return resp

    def add_emp(self, emp_data):
        add_emp_uri = "/pim/addEmployee"
        resp = self.sess.get(self.url + add_emp_uri)
        token = self.extract_token(resp)
        emp_data['_csrf_token'] = token
        resp = self.sess.post(self.url + add_emp_uri, data=emp_data)
        return resp

    @staticmethod
    def extract_token(resp):
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        result = soup.find('input', attrs={'name': '_csrf_token'})
        return result['value']

    def generate_emp_json(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        emp_id = self.faker.random_number(6)
        emp_data = {
            'firstName': first_name,
            'lastName': last_name,
            'employeeId': emp_id,
        }
        return emp_data
