#Even
#2018.5.3

#import sysfiles
import json
import hashlib
import requests
#import constfiles
#from ... import sysfiles
#from ... import constfiles
from api import Encrypt_Data

from PlayList import PlayList
#END



class User():

    def __init__(self):
        self.status = 0; #用户cookies未储存状态
        self.Requests_header = { #请求头
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Host": "music.163.com",
            "Referer": "http://music.163.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0"
        }
        self.connection = requests.Session();
        self.user_id = ""; #用户ID
        self.gender = ""; #性别
        self.nickname = ""; #昵称
        self.avatarUrl = ""; #头像地址
        self.backgroundUrl = ""; #背景地址
        self.description = ""; #简介
        self.signature = ""; #签名


    #登陆时初始化用户的信息
    def __init_user(self,info):

        self.user_id = info["account"]["id"]; #用户ID
        self.gender = info["profile"]["gender"]; #性别
        self.nickname = info["profile"]["nickname"]; #昵称
        self.avatarUrl = info["profile"]["avatarUrl"]; #头像地址
        self.backgroundUrl = info["profile"]["backgroundUrl"]; #背景地址
        self.description = info["profile"]["description"]; #简介
        self.signature = info["profile"]["signature"]; #签名

        return;








    #请求用户歌单时候返回简单的一些参数 checked at 2018.5.4
    #传入info 为dict参数, 应当为User.user_playlist返回值转化而来。
    def brief_playlists(self,info):
        playlists = info["playlist"];
        result = [];
        for playlist in playlists:
            info = {
                #关于创建者信息
                "userId":playlist["creator"]["userId"], #创建者的ID
                "nickname":playlist["creator"]["nickname"], #创建者的昵称
                "avatarImgId":playlist["creator"]["avatarImgId"], #创建者的头像地址ID
                #关于歌单信息
                "description":playlist["description"],#歌单简介
                "coverImgId":playlist["coverImgId"], #歌单封面的图片链接ID
                "trackCount":playlist["trackCount"], #歌单中歌曲的数量
                "playCount":playlist["playCount"], #歌单被播放的总次数
                "coverImgUrl":playlist["coverImgUrl"], #歌单封面图片的地址
                "subscribedCount":playlist["subscribedCount"], #订阅人数
                "name":playlist["name"], #歌单名字
                "id":playlist["id"] #歌单ID
            }
            result.append(info);
        return result;








    #使用手机号码登陆 checked at 2018.5.4
    def phone_login(self,username, password):
        url = "https://music.163.com/weapi/login/cellphone"
        #密码在函数内编码，在外部明码传输，可能有隐患
        password = hashlib.md5(password.encode('utf-8')).hexdigest();
        text = {
            'phone': username,
            'password': password,
            'rememberLogin': 'true'
        }

        data = Encrypt_Data(text);

        con = self.connection.post(url,data=data,headers=self.Requests_header).json();

        #con.encoding = 'UTF-8';
        #self.__init_user(con.json());

        if con["code"] == 200:
            self.__init_user(con);
            return "登陆成功！";
        else:
            return "登陆失败！";







    #用户歌单，包括自己创建的以及收藏的歌单 checked at 2018.5.4
    #List of playlist_ids
    def user_playlist(self,user_id,offset=0,limit=100):
        url = "http://music.163.com/api/user/playlist";

        text = {
            "offset":offset,
            "limit":limit,
            "uid":user_id
        }
        con = self.connection.get(url,params=text,headers=self.Requests_header);

        return con;


    #用户推荐歌单
    #List of song_ids
    def recommend_playlist(self):
        url = 'http://music.163.com/weapi/v1/discovery/recommend/songs?csrf_token=';
        csrf = "";
        for cookie in self.connection.cookies:
            if cookie.name == '__csrf':
                csrf = cookie.value
        if csrf == '':
            return [];
        url += csrf
        text = {
            "offset": 0,
            "total": True,
            "limit": 20,
            "csrf_token":csrf
        }
        page = self.connection.post(url,data=Encrypt_Data(text),headers=self.Requests_header);
        results = json.loads(page.text)['recommend']
        song_ids = []
        for result in results:
            song_ids.append(result['id'])
        return song_ids;







    #歌单详情
    #PlayList<class> checked at 2018.5.4
    def playlist_detail(self,playlist_id):
        url_detail = 'http://music.163.com/weapi/v3/playlist/detail';
        #self.connection.cookies.load();
        csrf = "";
        for cookie in self.connection.cookies:
            if cookie.name == "__csrf":
                csrf = cookie.value;
        #
        text = {
            "id" : playlist_id,
            "total" : "true",
            "csrf_token" : csrf,
            "limit" : 1000,
            "n" : 1000,
            "offset" : 0
        }
        con = self.connection.post(url_detail,data=Encrypt_Data(text),headers=self.Requests_header);
        return con;




    #歌曲的详细信息页面,获取歌词.
    #SongDetail<class>
    def song_detail(self, music_id):
        url = "http://music.163.com/api/song/detail/?id={}&ids=[{}]".format(music_id, music_id);
        lyric_url = 'http://music.163.com/api/song/lyric?os=osx&id={}&lv=-1&kv=-1&tv=-1'.format(music_id);

        con = self.connection.get(url,headers=self.Requests_header);
        con_lyric = self.connection.get(lyric_url,headers=self.Requests_header).json();

        if "tlyric" in con_lyric and con_lyric["tlyric"].get("lyric") is not None:
            tlyric_detail = con_lyric["tlyric"]["lyric"];
        else:
            tlyric_detail = "未找到歌词翻译";

        if "lrc" in con_lyric and con_lyric["lrc"]["lyric"] is not None:
            lyric_detail = con_lyric["lrc"]["lyric"];
        else:
            lyric_detail = "未能找到歌词";
        return [lyric_detail,tlyric_detail];










    #歌曲评论的详细
    # Comments<class>
    # limit 每次返回的评论数量，offset 从前向后多少评论开始取用
    def song_comments(self, music_id, offset=0, total='true', limit=100):
        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}?csrf_token='.format(music_id)

        #
        csrf = "";
        for cookie in self.connection.cookies:
            if cookie.name == "__csrf":
                csrf = cookie.value;
        #
        url = url + csrf;
        text = {
            "offset" : offset,
            "total" : total,
            "limit" : limit,
            "music_id" : music_id,
            "csrf_token" : csrf,
        }
        con = self.connection.post(url,data=text,headers=self.Requests_header);
        return con;










    #具体歌曲的播放链接
    #原理生成外链，对于有版权歌曲无效
    def song_url(self, music_ids, bit_rate=320000):
        #http://music.163.com/song/media/outer/url?id=476592630.mp3
        return "http://music.163.com/song/media/outer/url?id=" + str(music_ids) + ".mp3";









    #给定关键词搜索信息
    #post
    #搜索单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) stpye
    def search_info(self,s,stype=1,offset=0,total="true",limit=60):
        url = "http://music.163.com/api/search/get"
        datas = {
            's': s,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }
        con = self.connection.post(url,headers=self.Requests_header,data=datas);
        return con;
