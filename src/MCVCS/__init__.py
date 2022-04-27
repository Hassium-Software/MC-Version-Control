from . import io

import json, os

class Context():
    '''
    context object that just has data about:
     - what branch you are in
     - current server
     - working directory
    '''
    def __init__(self, branch="master",
        server=None):
        self.cwd = os.getcwd()
        self.branch= branch
        self.server = server

    @staticmethod
    def loaded():
        with open(f'{os.getcwd()}/.MCVCS/data_storage.json') as f:
            data = json.loads(f.read())
        return Context(branch = data['ctx']["branch"], server=data['ctx']['server'])