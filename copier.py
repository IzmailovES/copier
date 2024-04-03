#!/usr/bin/env python3
import os
import sys
import argparse
import shlex
import signal
from dataclasses import dataclass


DEFAULT_BACKUP = '/tmp/copier_backups'

class RetcodeError(Exception):
    pass

def command(*args, **kwargs):
    ret=os.system(*args, **kwargs)
    if ret:
        raise RetcodeError(ret)

class SignalHandlers:
    @classmethod
    def sigint_handler(cls, sig, frame):
        print("SIGINT done")
        exit(0)



@dataclass
class Hosts:
    src         : str | None = None
    dst         : str | None = None
    src_passwd  : str | None = None
    dst_passwd  : str | None = None
        
@dataclass
class Backup:
    hosts       :  Hosts
    bcp_dir     : str | None = None
    do_backup   : bool       = False
    
    def make_folder(self):
        if self.do_backup:
            command('mkdir -p {}'.format(self.bcp_dir))


    def backup(self, file):
        if self.do_backup:
            print('here I try to make backup')

@dataclass
class File:
    src : str
    dst : str

    def send(self):
        pass

    def __str__(self):
        return 'src: {} dst: {}'.format(self.src, self.dst)


@dataclass
class Copier:
    hosts: Hosts
    yes: bool = False

    def __call__(self, file):
        cmd = self._prepare_command(file)
        if not self.yes:
            ans = input('{cmd} ?(y/N)'.format(cmd=cmd))
            if ans.lower() not in ['y', 'yes']:
                return 1
        return command(cmd)

    def _prepare_command(self, file):
        return 'scp -r {}{} {}{}'.format(self.hosts.src + ':' if self.hosts.src else '',
                                           file.src,
                                           self.hosts.dst + ':' if self.hosts.dst else '',
                                           file.dst)


class Main:
    def __init__(self, parsed_args):
        self.args = parsed_args
        self.hosts = Hosts(src = self.args.src_host,
                           dst = self.args.dst_host
                           )
        self.backuper = Backup(do_backup=self.args.backup, bcp_dir=self.args.backup_folder, hosts=self.hosts)
        # make bcp_dir
        self.yes = self.args.force_yes
        self.copy = Copier(self.hosts, self.yes)
        self.backuper.make_folder()
       
    def print_settings(self):
        print('copy files from {} to {}, make backup: {}, force-yes: {}'.format(self.hosts.src or 'localhost',
                                                                                self.hosts.dst or 'localhost',
                                                                                self.backuper.do_backup,
                                                                                self.yes))

    def __call__(self):
        print(self.args.__dict__)
        self.print_settings()
        while True:
            s = shlex.split(input())
            if not s:
                print('done')
                exit(0)
            if len(s) != 2:
                print('bad input')
                continue
            file = File(*s )
            ## try to do backup
            self.backuper.backup(file)
            ## try to copy file with scp
            self.copy(file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_host', action='store', default='')
    parser.add_argument('-d', '--dst_host', action='store', default='')
    parser.add_argument('-b', '--backup', action='store_true', default=False)
    parser.add_argument('-y', '--force_yes', action='store_true', default=False)
    parser.add_argument('--backup_folder', action='store', default=DEFAULT_BACKUP)

    signal.signal(signal.SIGINT, SignalHandlers.sigint_handler)

    main = Main(parser.parse_args())
    main()
