'''
Manages all IO activity regarding the operation and usage of Commit Files. 

This will be able to read, save, etc commit files.
'''
import os

class Commit_File():
    '''commit file data class'''

    def __init__(self):
        self.author = ""
        self.date = ""
        self.message = ""

        self.tracked_files = [] # [["file","hex"],...]
        self.changes = [] # [{"type":"", "file":"", "changes":[]}]

        self.untracked = [] # [{"file":"", "data":b''}]
    
    @staticmethod
    def load(ctx, iid:int = None):
        output = Commit_File()
        if iid==None:
            iid = len(os.listdir(f'{ctx.cwd}/.MCVCS/branches/{ctx.branch}/commits'))-1 # get last commit
        
        idstr = repr(chr(iid))[3:-1]

        with open(f'{ctx.cwd}/.MCVCS/branches/{ctx.branch}/commits/{idstr}.commit','rb') as f:
            text = f.read().split(b'\n')
        
        current_change = {}
        collecting_bytes = False
        byte_collect_size = 0
        byte_collect_file = ""
        bytes_collected = b""
        for c, line in enumerate(text):
            if collecting_bytes and len(bytes_collected)<byte_collect_size:
                bytes_collected+=f'\n{line}'.encode()
            if collecting_bytes and len(bytes_collected)>=byte_collect_size:
                output.untracked.append({"file":byte_collect_file,"data":bytes_collected[1:]})
                collecting_bytes=False

            if line.startswith(b'#'): continue # acts like a comment
            elif c == 1: output.message=line
            elif c == 2: output.author=line
            elif c == 3: output.date=line

            elif line.startswith(b'|'):
                output.tracked_files.append({"file":line[1:].split(b' ')[0],"last-commit":line[1:].split(b' ')[1]})
            elif line.startswith(b'))'):
                output.changes.append(current_change)
                if current_change!={}: current_change = {}
                args = line[2:].split(b' ')
                current_change["type"] = args[0]
                current_change["file"] = args[1]
                current_change["changes"] = []
            elif line.startswith(b'(('):
                args = line[2:].split(b'<<')
                current_change["changes"].append({"line": int(args[0]),"data": args[1]})
            elif line.startswith(b']]'):
                args = line[2:].split(b' ')
                byte_collect_size = int(args[1])
                byte_collect_file = args[0]
                bytes_collected=b""
                collecting_bytes=True

        output.changes.append(current_change)



        return output
    
    def save(self, ctx, filename: str = None) -> None:
        if not filename:
            iid = len(os.listdir(f'{ctx.cwd}/.MCVCS/branches/{ctx.branch}/commits')) # get last commit +1
        
            filename = repr(chr(iid))[3:-1]


        tmp1 = ""
        for x in self.tracked_files:
            tmp1+=f"|{x['file']} {x['last-commit']}\n"

        tmp2 = "\n"
        for x in self.changes:
            tmp2+=f")){x['type']} {x['file']}\n"
            for y in x["changes"]: 
               tmp2+=f"(({y['line']}<<{y['data']}\n"

        tmp3 = b''
        for x in self.untracked:
            tmp3+=b']]'+ \
                x['file'].encode()+ \
                b' '+ \
                str(len(x["data"])).encode()+ \
                b'\n'+ \
                x["data"]+ \
                b'\n'
        
        constructed_string = f'''{'#'*10}
{self.message}
{self.author}
{self.date}
{'#'*10}
{tmp1}
{tmp2}

'''
        with open(f'{ctx.cwd}/.MCVCS/branches/{ctx.branch}/commits/{filename}.commit', 'wb+') as f:
            f.write(constructed_string.encode()+tmp3)