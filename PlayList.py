

class PlayList():

    def __init__(self,info):
        self.creator = info["playlist"]["creator"];
        self.tracks = info["playlist"]["tracks"];


    def songs_list(self):
        tracks = self.tracks;
        result = [];
        for song in tracks:
            info = {
                "name":song["name"],
                "id":song["id"],
                "picUrl":song["al"]["picUrl"]
            }
            result.append(info);
        return result;
