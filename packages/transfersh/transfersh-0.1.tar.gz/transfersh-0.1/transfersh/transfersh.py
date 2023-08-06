from requests import post
from os.path import isfile
from .exception import *

class TransferSh(object):


    def uploadFile(file, domain = "https://transfer.sh"):

        if not isfile(file):
            raise FileNotExists('"{}" is not exists!'.format(file))

        # read file
        with open(file, 'rb') as f:
            req = post(domain, files={'file': f})
            if req.ok:
                return req.text
            else:
                raise UnkownError(
                'Status Code: {}\ncontent: {}'.format(req.status_code, req.text)
                )
