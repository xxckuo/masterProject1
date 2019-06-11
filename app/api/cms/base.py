import os
import urllib.request
from flask import request

class File():

    def download(url,filename):
        curPath = os.getcwd()
        Download_url = url

        downPath = curPath + '\\excel文档'+'\\' + filename
        urllib.request.urlretrieve(Download_url, downPath)

    def delete(filename):
        curPath = os.getcwd()
        downPath = curPath + '\\excel文档'+'\\' + filename
        os.remove(downPath)
