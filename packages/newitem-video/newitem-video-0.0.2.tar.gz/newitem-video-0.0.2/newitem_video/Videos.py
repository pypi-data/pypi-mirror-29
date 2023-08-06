from bson.objectid import ObjectId
from .database import DataBase
from bson.json_util import dumps

class Videos(DataBase):
    def __init__(self):
        super(Videos,self).__init__()
        self.videos = self.db.videos

    def add_video(self,video):
        object_id = None
        query = {"title": video['title'], "url": video["url"], "description":video["description"]}
        try:
            # result 은 upsert result를 가지고 있다.
            # r.raw_result를 보면 insert 될 시에는 upserted 키값을 가지고 있다.
            r = self.videos.update_one(query,
                                         {"$set": video},
                                         upsert=True)
        except Exception as e:
            print(e)

        return r

    def get_video_by_id(self, video_id):
        try:
            r = self.videos.find_one({"_id": ObjectId(video_id)})
        except Exception as e:
            print(e)
        return dumps(r)

    def get_videos(self):
        try:
            videos = self.videos.find({})
        except Exception as e:
            print(e)
        return dumps(videos)

    def remove_video_by_id(self, video_id):
        try:
            r = self.videos.remove({"_id": ObjectId(video_id)})
            print(r)
        except Exception as e:
            print(e)
        return r



    # def get_video_by_id(self, video_id):
    #     try:
    #         r = self.videos.find_one({"_id": ObjectId(video_id)})
    #     except Exception as e:
    #         print(e)
    #
    #     return r