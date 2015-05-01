import os
import airship

class suppress_stdout_stderr(object): # http://stackoverflow.com/questions/11130156
    def __init__(self):
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])

def main():
    with suppress_stdout_stderr():
        airship.sync()
