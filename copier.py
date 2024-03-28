#!/usr/bin/env python3
import os
import sys
import argparse
import shlex
from dataclasses import dataclass


DEFAULT_BACKUP = '/tmp/copier_backups'

class RetcodeError(Exception):
    pass

def command(*args, **kwargs):
    ret=os.system(*args, **kwargs)
    if ret:
        raise RetcodeError(ret)


@dataclass
class Hosts:
    src_host   : str | None = None
    dst_host   : str | None = None
    src_user   : str | None = None
    dst_user   : str | None = None
    src_passwd : str | None = None
    dst_passwd : str | None = None
        
@dataclass
class Backup:
    bcp_dir    : str | None = None
    do_backup  : bool       = False
    
    def make_folder(self):
        if self.do_backup:
            os_system('mkdir -p {}'.format(self.bcp_dir))


    def do_backup(self, file):
        if self.do_backup:
            pass

@dataclass
class File:
    src : str
    dst : str
    hosts: Hosts

    def send(self):
        pass

    def __str__(self):
        return 'src: {} dst: {}'.format(self.src, self.dst)


class Main:
    def __init__(self, parsed_args):
        self.args = parsed_args
        self.backuper = Backup(do_backup=self.args.backup, bcp_dir=self.args.backup_folder)
        self.hosts = 
        # make bcp_dir
        self.backuper.make_folder()
        # fill hosts
        

    def __call__(self):
        print(self.args.__dict__)
        while True:
            s = shlex.split(input())
            if not s:
                print('done')
                exit(0)
            if len(s) != 2:
                print('bad input')
                break
            file = File(*s)
            print(file)
            ## try to do backup
            ## try to copy file with scp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_host', action='store')
    parser.add_argument('-d', '--dst_host', action='store')
    parser.add_argument('-b', '--backup', action='store_true', default=False)
    parser.add_argument('--backup_folder', action='store', default=DEFAULT_BACKUP)
    m = Main(parser.parse_args())
    m()