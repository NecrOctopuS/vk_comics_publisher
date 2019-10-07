# Comics publisher
The program downloads a comic from the site [xkcd.com](http://xkcd.com)
and publishes it on the wall of your group in [VKontakte](https://vk.com/)

### How to install
To get started, get a token from VK, it can be obtained as follows:

you must follow the link: https://oauth.vk.com/authorize?client_id=`your_ID_client`&scope=photos,groups,wall,offline&response_type=token
where `your_ID_client` is the application ID that can be viewed in the settings of your [application](https://vk.com/apps?act=manage)
 

In the `.env` file, you need to write your VK token, the application ID and the ID of your group where you want to publish posts.
```text
ACCESS_VK_TOKEN = "Your Key"
CLIENT_ID = 'Your Application ID'
GROUP_ID = 'ID of your group'
```
Python3 should already be installed.
Then use `pip` (or` pip3`, there is a conflict with Python2) to install the dependencies:
```
pip install -r requirements.txt
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).