import os,sys,json
from datetime import datetime,timedelta
import requests

class userAccount:
    def __init__(self,username,password,email,age):
        self.Username=username
        self.Password=password
        self.Email=email
        self.Age=age
        self.created_at=datetime.now()
        self.last_login=None
        self.is_active=True
    def login(self,password):
        if password==self.Password:
            self.last_login=datetime.now()
            return True
        else:return False
    def get_account_info(self):return{'username':self.Username,'email':self.Email,'age':self.Age,'active':self.is_active}
    def update_password(self,old_password,new_password):
        if self.login(old_password):
            self.Password=new_password
            return True
        return False

def validate_email(email):
    if '@' in email and '.' in email:return True
    else:return False

def calculate_account_age(created_date):
    now=datetime.now()
    diff=now-created_date
    return diff.days

def fetch_user_data(user_id):
    url=f"https://api.example.com/users/{user_id}"
    response=requests.get(url)
    if response.status_code==200:
        return response.json()
    else:
        return None

if __name__=='__main__':
    user=userAccount('john_doe','secret123','john@example.com',25)
    print('User created:',user.get_account_info())
    if user.login('secret123'):print('Login successful')
    else:print('Login failed')
