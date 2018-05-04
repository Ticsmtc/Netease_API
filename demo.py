import hashlib
import requests
import os
from User import User
from api import Encrypt_Data

if __name__ == "__main__":


    y = User();
    phone_num = "";
    passowrd = "";
    y.phone_login(phone_num,password);

    url = y.song_url(27876900);

    print(url);
