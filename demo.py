import hashlib
import requests
import os
from User import User
from api import Encrypt_Data

if __name__ == "__main__":


    y = User();
    phone_num = "18157438042";
    password = "netease3082606";
    res = y.phone_login(phone_num,password);

    re = y.search_info("dice");

    detail = y.song_detail(21311956)
    print(res);

    print(detail);
