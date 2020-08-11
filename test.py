import requests

# Base URL
BASE = "http://127.0.0.1:5000/"

# create video/s (into database)
# data = [{"likes": 78, "name": "Juan", "views": 100000},
#         {"likes": 10000, "name": "How to make REST API", "views": 800000},
#         {"likes": 35, "name": "Jeffrey", "views": 2000}]
# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())

# input()

# view specific video from the database
# response = requests.get(BASE + "video/6")
# print(response.json())

# input()

# update specific video from the database
response = requests.patch(BASE + "video/2", {"name":"Jeffrey","views":99, "likes":101})
print(response.json())