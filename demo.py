import hashlib
import requests
import os
from User import User
from api import Encrypt_Data

if __name__ == "__main__":


    y = User();
    phone_num = input();
    password = input();
    res = y.phone_login(phone_num,password);


    print(str(y.user_id) + " " + y.backgroundUrl);
