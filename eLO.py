import requests
from bs4 import BeautifulSoup

__author__ = 'ytpme'
__version__ = 0.2

class eLO():
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self): 
        self.session = requests.Session()
        # Hello! I'm Android WebView!
        self.headers = {'User-agent': 'Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30'}

        request = self.session.post('https://elo.edu.pl/session/form.html', headers = self.headers,
            data = {
                'controller': 'session',
                'action': 'submitlogin',
                'param[email]': self.email,
                'param[password]': self.password
            }
        )

        for i in request.history:
            if i.status_code == 302: return True
        return False

    def classmates(self): # Return dictionary with IDs' users and name

        request = self.session.get('https://elo.edu.pl/myclass', headers=self.headers)
        bs = BeautifulSoup(request.text, 'html.parser')

        classmates = bs.findAll('a', class_ = 'member')
        data = {}

        for classmate in classmates:
            id = classmate['href'][34:]
            names = classmate.findAll('p')
            firstname = names[0].text.replace('\xa0', ' ')
            surname = names[1].text.replace('\xa0', '')
            data[id] = firstname + surname

        return data

    def school(self): # Shows location, class and profile

        request = self.session.get('https://elo.edu.pl/profile/results', headers=self.headers)
        bs = BeautifulSoup(request.text, 'html.parser')

        data = []
        data.append(bs.find('div', class_='record').find('b').text)

        for details in bs.find('p', class_ = 'text').findAll('b'):
            data.append(details.text)

        return data
    def last_messages(self, limit): # Parse chat for class and return dictionary

        request = self.session.get('https://elo.edu.pl/myclass/wall/' + str(limit), headers = self.headers)
        bs = BeautifulSoup(request.text, 'html.parser')

        chat = bs.findAll('div', class_ = 'message ', limit = limit)
        
        data = {}
        key = 0

        for message in chat:
            details = message.findAll('p')
            data[key] = {'text': details[0].text, 'date': details[1].text, 'member': details[2].text}
            key += 1

        return data
    def send_message(self, text): # Must i explain?

        request = self.session.post('https://elo.edu.pl/form.html', headers = self.headers,
            data = {
                'controller': 'myclass',
                'action': 'sendmessage',
                'param[message]': text
            }
        )

    def set_avatar(self, avatar): 
        
        if 0 <= avatar <= 107:
            
            request = self.session.get('https://elo.edu.pl/profile/avatar/avatar' + str(avatar)  + '.png', headers = self.headers)
            return True

        else: 
            return False

    def set_color(self, color): # RRGGBB, remember!
        
        if len(list(color)) == 6:
            request = self.session.get('https://elo.edu.pl/profile/color/' + str(color), headers = self.headers)
            return True
        else:
            return False

    def modify_profile(self, firstname, surname, age, gender):

        request = self.session.post('https://elo.edu.pl/form.html', headers = self.headers,
            data = {
                'controller': 'profile',
                'action': 'update',
                'param[first_name]': firstname,
                'param[last_name]': surname,
                'param[age]': age,
                'param[gender]': gender
            }
        )

    def modify_notifications(self, results, community, message, elo, news):

        request = self.session.post('https://elo.edu.pl/form.html', headers = self.headers,
            data = {
                'controller': 'profile',
                'action': 'update_notifications',
                'param[push_results]': results,
                'param[push_community]': community,
                'param[push_message]': message,
                'param[push_elo]': elo,
                'param[push_news]': news
            }
        )

    def update_password(self, new_password):

        request = self.session.post('https://elo.edu.pl/form.html', headers = self.headers,
            data = {
                'controller': 'profile',
                'action': 'update_password',
                'param[old_password]' : self.password,
                'param[new_password]' : new_password,
                'param[repeat_password]' : new_password
            }
        )

    def get_person(self, id):
        person = Person(self.session, self.headers, id)
        return person

    def logout(self):
        request = self.session.get('https://elo.edu.pl/session/logout', headers = self.headers)


class Person():
    def __init__(self, session, headers, id):
        self.session = session
        self.headers = headers
        self.id = id

    def send_elo(self): # It's alternative for Facebook fuction poke
        
        request = self.session.get('https://elo.edu.pl/myclass/elo/' + str(self.id), headers = self.headers)
    
    # def last_message 
    def send_message(self, limit): # Private message

        request = self.session.get('https://elo.edu.pl/myclass/member/' + str(self.id), headers = self.headers)
        bs = BeautifulSoup(request.text, 'html.parser')
        
        recipient_id = bs.find('input', {'name': 'param[recipient_id]'}).get('value')
        
        request = self.session.post('http://elo.edu.pl/form.html', headers = self.headers,
            data = {
                'controller': 'myclass',
                'action': 'sendmessagetoone',
                'param[recipient_id]': recipient_id,
                'param[recipient_hid]': self.id
            }
        )
