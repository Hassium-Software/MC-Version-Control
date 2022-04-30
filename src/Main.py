'''
This file acts as the shell interface to the VCS
'''

import sys
import os
import MCVCS as vcs

args = sys.argv[1:]
func_dict = dict()

def vcs_function(name: str):
    global func_dict
    def wrapper(func, *args):
        func_dict[name] = func
        return func
    return wrapper

@vcs_function('init')
def init_project():
    vcs.io.Setup.init(os.getcwd())

@vcs_function('make-server')
def make_server(name: str, port: str):
    vcs.io.Setup.make_server(vcs.Context.load(), name, port)

@vcs_function('stage')
def stage(file: str):
    ctx = vcs.Context.load()
    ctx.stage.append(file)
    ctx.stage = list(set(ctx.stage)) # removes duplicates
    ctx.save()

@vcs_function('unstage')
def unstage(file: str):
    ctx = vcs.Context.load()
    ctx.stage.remove(file) # todo: throw a proper error
    ctx.save()

@vcs_function('test')
def test():

    e = vcs.io.Commit_Files.Commit_Parser(vcs.Context.load()).full_parse()
    e.add_tracked_file(f'gamingus-{len(e.tracked_files)}','1','0')
    e.save(vcs.Context.load())
    print(e.tracked_files, '\n')
    print(e.changes, '\n')
    print(e.untracked, '\n')


if __name__ == "__main__":
    func_dict[args[0]](*args[1:])