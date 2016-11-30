# Blogodt
## What is it?
This application is for download and upload posts to a blog (publish and draft) in Blogger, and to upload posts in a ODT format file to you blog in Blogger. You can use several blogs in you Blogger acount and choose with this application what blog to use. When you publish a post you can publicity the post in Twitter, but you must use a XML file with OAuth keys, and you can shorten links but you must include bitly OAuth keys. That XML file must be like the following way:

```XML
<?xml version='1.0' encoding='UTF-8'?>

<Redes>
    <twitter caracteres='140' CONSUMER_KEY='' CONSUMER_SECRET='' ACCESS_KEY='' ACCESS_SECRET='' BIT_LY_USERNAME='' BIT_LY_API_KEY=''>SOME TEXT TO PUT</twitter>
    <facebook>SOME TEXT TO PUT</facebook>
    <googlePlus>SOME TEXT TO PUT</googlePlus>
</Redes>
```

## Dependencies:
- wxPython
- python-pygments
- python-docutils
- gdata-python-client
- tweepy
- [bitlyapi](https://github.com/bitly/bitly-api-python)
- [odfpy](https://github.com/eea/odfpy)


## Screenshot
![Capture1](https://raw.githubusercontent.com/sermmor/Blogodt/master/Capture.png)

**IMPORTANT NOTE**: I finished this project in September 2012, and I won't do an update of this anymore.
