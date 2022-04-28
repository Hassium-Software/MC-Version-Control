from . import io

import json, os

class Context():
    '''
    context object that just has data about:
     - what branch you are in
     - current server
     - working directory
    '''
    def __init__(self):
        self.cwd = os.getcwd()
        self.branch= None
        self.server = None
        self.stage = []
        self.data = dict()

    @staticmethod
    def load():
        output = Context()
        with open(f'{os.getcwd()}/.MCVCS/data_storage.json') as f:
            data = json.loads(f.read())

        output.branch = data["ctx"]["branch"]
        output.server = data["ctx"]["server"]
        output.stage = data["ctx"]["stage"]
        output.data = data
        return output
    
    def save(self):
        self.data["ctx"]["stage"] = self.stage
        self.data["ctx"]["server"] = self.server
        self.data["ctx"]["branch"] = self.branch

        with open(f'{self.cwd}/.MCVCS/data_storage.json','w') as f:
            f.write(json.dumps(self.data, indent=4),)