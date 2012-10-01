"""Checks isup.me to see if a website is up
@package ppbot

@syntax isup <word>

"""
from modules import *
from flask import request
import envoy

class Github(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""
        Module.__init__(self, kwargs=kwargs)

    def _register_events(self):
        """Register module commands."""

        self.add_http_route(self.postreceive, name='github/postreceive', methods=['POST'])

    def postreceive(self):
        hook_ips = ['207.97.227.253', '50.57.128.197', '108.171.174.178']
        if request.remote_addr in hook_ips:
            r = envoy.run('git pull --rebase')
            print r.std_out
            return 'ok'


