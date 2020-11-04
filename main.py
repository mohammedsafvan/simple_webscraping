import json
import requests
import threading
import time

API_KEY = 'tHEEM1uYanDm'
PROJECT_TOKEN = 'tOci_W5hFPJE'


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            'api_key': self.api_key
        }
        self.get_data()
        self.data = self.get_data()


    def get_data(self):
        response = requests.get(
            f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={'api_key': API_KEY})
        data = json.loads(response.text)
        return data

    def update(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)

        def poll():
            print('''Data updation in progress, It will take sometime..
You can continue. If updation occured you will informed.. :)\n''')
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print('==================')
                    print('Data updated.')
                    print('==================')
                    break
                time.sleep(5)
        t = threading.Thread(target=poll)
        t.start()

    def get_country_case(self, country):
        data = self.data['country']
        for content in data:
            if content['name'].lower() == country:
                co = False
                for i in content:
                    if co:
                        print(f'{i.replace("_", " ")} : {content[i]}')
                    co = True

    def get_totals(self):
        data = self.data['worldwide']
        for content in data:
            print(f'''{content['name']}{content['cases']}''')


if __name__ == "__main__":
    while True:
        print('Enter your option : ')
        print('1. To get total number status')
        print('2. To get deatails of specific country')
        print('3. To update data')
        ch = str(input())
        person = Data(API_KEY, PROJECT_TOKEN)
        if ch in ['1', '2', '3', 'q']:
            if ch == '1':
                person.get_totals()
            elif ch == '2':
                country = input("Enter the name of counry : ").lower()
                print('\n')
                person.get_country_case(country)
                print('\n')
            elif ch == '3':
                person.update()
            elif ch == 'q':
                break
        else:
            print('Invalid choice..')
