'''
Manages all IO activity regarding the operation and usage of Commit Files. 

This will be able to read, save, etc commit files.
'''
import os
import re

class Commit_File():
    '''commit file data class'''

    def __init__(self):
        self.author = ""
        self.date = ""
        self.message = ""

        self.tracked_files = [] # [["file","hex"],...]
        self.changes = [] # [{"type":"", "file":"", "changes":[]}]

        self.untracked = [] # [{"file":"", "data":b''}]
    
    def add_tracked_file(self, file: str, last_commit: str):
        self.tracked_files.append(
                {"file":file, "last-commit":last_commit}
            )
    
    def add_change(self, change: dict):
        if change == {}: return
        self.changes.append(change)

    
    def save(self, ctx, filename: str = None) -> None:
        if not filename:
            iid = len(os.listdir(f'{ctx.cwd}/.MCVCS/branches/{ctx.branch}/commits')) # get last commit +1
        
            filename = hex(iid)[2:]

        tmp1 = []
        for x in self.tracked_files:
            tmp1.append(f"|{x['file']} {x['last-commit']}")

        tmp2 = []#"\n"
        for x in self.changes:
            tmp2.append(f")){x['type']} {x['file']}")
            
            for y in x["changes"]:
                mid = ">>" if y["old"] else "<<"
                tmp2.append(f"(({y['line']}{mid}{y['data']}")


        tmp3 = []
        for x in self.untracked:
            tmp3.append(b']]'+ \
                x['file'].encode()+ \
                b' '+ \
                str(len(x["data"])).encode())

            tmp3.append(x["data"])
        
        tmp1 = '\n'.join(tmp1)
        tmp2 = '\n'.join(tmp2)
        tmp3 = b'\n'.join(tmp3)
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

class Commit_Parser:
    '''parses commit files'''
    def __init__(self, ctx, iid:int = -1):
        self.commit = Commit_File()
        
        if iid==-1: 
            iid = len(
                    os.listdir(f'{ctx.cwd}/.MCVCS/branches/{ctx.branch}/commits')
                )-1 # get last commit

        self.idstr = hex(iid)[2:]
        self.cursor = 4 # skip past metadata
        self.current_change = {}
        self.collecting_bytes = False
        self.byte_collect_size = 0
        self.byte_collect_file = ""
        self.bytes_collected = b""

        with open(f'{ctx.cwd}/.MCVCS/branches/{ctx.branch}/commits/{self.idstr}.commit','rb') as f:
            self.input_text = f.read().split(b'\n')
        
        self.commit.message=self.input_text[1].decode()
        self.commit.author=self.input_text[2].decode()
        self.commit.date=self.input_text[3].decode()

    @staticmethod
    def parse_data_line(data: str) -> dict:
        output = {}
        _regex = r"^\(\(([0-9]+)((\<\<)|(\>\>))"
        match: re.Match[str] = re.match(_regex, data) #type: ignore
        line = re.compile(r'(\(\()|(\<\<)|(\>\>)').sub('', match[0])
        data = data[len(match[0]):]

        output['line'] = int(line)
        output['data'] = data
        output['old'] = '>>' in match[0]
        
        return output
    
    def make_commit(self, type: str, file: str):
        self.commit.add_change(self.current_change)
        self.current_change = {
            "type"    : type,
            "file"    : file,
            "changes" : [] 
        }
    
    def add_change(self, line: str):
        self.current_change["changes"].append(self.parse_data_line(line))
    
    def collect_bytes(self, line: bytes) -> bool:
        if self.collecting_bytes and len(self.bytes_collected)<self.byte_collect_size:
            self.bytes_collected+=b'\n'+line
        elif self.collecting_bytes and len(self.bytes_collected)>=self.byte_collect_size:
            self.commit.untracked.append({"file":self.byte_collect_file,"data":self.bytes_collected[1:]})
            self.collecting_bytes=False


        return self.collecting_bytes
    
    def step(self):
        if self.cursor > len(self.input_text)-1:
            return None
        
        line = self.input_text[self.cursor]
        self.cursor+=1
        
        if self.collect_bytes(line): return None

        if line.startswith(b'#'): return None

        self.cursor-=1

        if line.startswith(b'|'):
            file = line[1:].split(b' ')[0].decode()
            last_commit = line[1:].split(b' ')[1].decode()
            self.commit.add_tracked_file(file, last_commit)
        
        elif line.startswith(b'))'):
            args = line[2:].split(b' ')
            commit_type = args[0].decode()
            file = args[1].decode()

            self.make_commit(commit_type, file)

        elif line.startswith(b'(('):
                self.add_change(line.decode())
                
        elif line.startswith(b']]'):
            args = line[2:].split(b' ')
            self.byte_collect_size = int(args[1])
            self.byte_collect_file = args[0]
            self.bytes_collected=b""
            self.collecting_bytes=True

        self.cursor+=1
    
    def full_parse(self) -> Commit_File:
        while self.cursor <= len(self.input_text)-1:
            self.step()
        self.commit.add_change(self.current_change)
        return self.commit