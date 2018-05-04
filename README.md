# NeteaseAPI

## api.py
> 加密算法函数，目前只用于登陆中前台传输密码至后台，
主要应用函数，data = Encrypt_Data(arg)


## User.py
> 爬虫主体，实现了各种爬虫请求函数

### def phone_login(self,username, password)
>使用手机号登陆函数，username 和 password 类型 str。当一个User对象登录后，再使用后面的所有函数均为该用户的操作。


### def user_playlist(self,user_id,offset=0,limit=100)
>返回固定用户id的播放列表，offset偏移量，相当于从第几个歌单向后取。


### def playlist_detail(self,playlist_id)
> 返回歌单类型PlayList<class>,包括一个固定歌单ID的歌单详细，包括创建者，歌单歌曲列表

### def song_detail(self, music_id)
> 返回歌曲类型Song<class> 包括歌曲名称，封面图片，中英文歌词（如果存在），歌曲的外链播放链接（有版权限制歌曲暂时无法处理）

### def song_comments(self, music_id, offset=0, total='false', limit=100)
> 返回固定歌曲的评论，包括热评以及普通评论。
