'''
All functionality required to setup a project for usage with MCVCS
'''
import os, shutil
import json
import datetime

def _copy_dir_to_dir(src: str, dest: str):
    files = os.listdir(src)

    for fname in files:
        shutil.copyfile(f'{src}/{fname}',f'{dest}/{fname}')

def setup_working_dir(ctx):
    '''
    coppies all files to working dir. This dir is a backup before any changes occure.
    All work done gets compared to this directory's contents.
    '''
    _copy_dir_to_dir(f'{ctx.cwd}/servers/{ctx.branch}', f'{ctx.cwd}/.MCVCS/branches/{ctx.branch}/working/servers')
    _copy_dir_to_dir(f'{ctx.cwd}/backups/{ctx.branch}', f'{ctx.cwd}/.MCVCS/branches/{ctx.branch}/working/backups')


def init(cwd: str):
    ''' setups the project'''
    preset_dir = f'{os.path.dirname(__file__)}/../presets'

    os.makedirs(f'{cwd}/.MCVCS/keys')
    os.makedirs(f'{cwd}/.MCVCS/branches/master/snapshots/servers')
    os.makedirs(f'{cwd}/.MCVCS/branches/master/commits')
    os.makedirs(f'{cwd}/.MCVCS/branches/master/working')
    shutil.copyfile(f'{preset_dir}/data_storage.json', f'{cwd}/.MCVCS/data_storage.json')

    os.makedirs(f'{cwd}/servers')
    os.makedirs(f'{cwd}/backups')
    master_branch = {
        "date-created": datetime.datetime.now().strftime("%Y-%m-%d--%H:%M:%S"),
        "created-by": "self",
        "lastest-commit": "None",
        "servers":[]
    }
    with open(f'{cwd}/.MCVCS/branches/master/info.json','w+') as f:
        f.write(json.dumps(master_branch, indent=4))

    
def make_server(ctx, name: str, port:str = "255565"):
    '''create a minecraft server'''
    os.makedirs(f'{ctx.cwd}/servers/{name}/{ctx.branch}')
    os.makedirs(f'{ctx.cwd}/backups/{name}/{ctx.branch}')

    info = {
        "ports": {
            ctx.branch: port
        },
        "backup-interval": -1 #in seconds. -1 is no backups
    }
    with open(f"{ctx.cwd}/servers/{name}/info.json",'w+') as f:
        f.write(json.dumps(info, indent=4))
    
    with open(f"{ctx.cwd}/servers/{name}/{ctx.branch}/mcvcs_plugin_store.json",'w+') as f:
        f.write('{}')