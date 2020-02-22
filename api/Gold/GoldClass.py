import requests


class Gold:
    def get(self):
        try:
            r = requests.post(url='https://google.com')
            if r.ok:
                return r
            else:
                return None
        except requests.exceptions as e:
            return 'Bad Response.'

if __name__ == '__main__':
    obj = Gold()
    print(obj.get().status_code)
