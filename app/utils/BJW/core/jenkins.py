import api4jenkins

class Jenkins(api4jenkins.Jenkins):
    def __init__(self, url, username, token):
        super().__init__(url, username, token)