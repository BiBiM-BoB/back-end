from ..utils.localgit import commit_all
import os


class GeneratorBase:
    """Super Class"""
    user = os.getlogin()
    localgitdir = f'/home/{user}/bibim/resources_git/'

    def commit(self, message):
        commit_all(self.localgitdir, message)

    def post_action(self):
        pass
