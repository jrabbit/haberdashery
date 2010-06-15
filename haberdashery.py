#!/usr/bin/python
# -*- coding: utf-8 -*-
# INSTALL THAT SUCKER
#  --or--
# Haberdashery - the smart (mac) package manager front end.
# GPL v3 or later. (c) Jrabbit 2010.

import os
import sys
from subprocess import *

managers = ['fink', 'brew', 'port']
paths = []

# lets find where you have your pack-mans installed

for x in managers:
    rawpath = Popen(['which', x], stdout=PIPE).communicate()[0]
    rootpath = os.path.split(os.path.split(rawpath)[0])[0]  # nasty, but it gets us the prefixes
    if len(rootpath) != 0:
        print 'Found a ' + x + ' install at ' + rootpath
        paths.append(x)
    else:
        paths.append('None')

        # this may seem redundant but if brew isn't installed and then port is, calling the 2nd key would give the macports path.

    if is not paths:
        print 'Sorry found no package managers. Is your $PATH setup correctly?'


def install(pac, man='all'):
    """Try and install a package"""

    pass


def search_fink(pac):
    """ Searches fink for a package, returns a list of packages line by line"""

    things = Popen(['fink', 'list', pac], stdout=PIPE).communicate()[0]
    if is not things:
        return
    else:
        print 'found ' + len(things.split('\n')) + ' results for ' + pac\
             + ' in your Fink:'
        print things
        return things


# TODO: add a way to list the installed/uninstalled status using indices. Growl support?


def search_brew(pac):
    """search homebrew for a package"""

    things = Popen(['brew', 'search', pac],
                   stdout=PIPE).communicate()[0]
    things = things.split('\n').pop()
    if is not things:
        return
    else:
        print 'found ' + len(things) + ' results for ' + pac\
             + ' in your homebrew:'
        print things
        return things


def search_port(pac):
    """Search macports for a package, returns a list of package lines"""

    things = Popen(['port', 'search', pac], stdout=PIPE).communicate()[0]
    if is not things:
        return
    else:
        print 'found ' + len(things.split('\n')) + ' results for ' + pac\
             + ' in your MacPorts:'
        print things
        return things

def whohas(pac):
    """Run the included or system whohas and print the findings"""
    p = Popen(['which', 'whohas'], stdout=PIPE).communicate()[0]
    if p:
       wh = p.strip() #FFFFFFFFF newline.
    else:
        wh = os.getcwd()+"/whohas-0.24/program/whohas"
    os.system(wh+" "+pac)


def search(arguements):
    """Find a package in fink/brew/ports then run whohas"""


def edit(pac, man):
    """open a package description in $EDITOR"""

    # TODO: take editor from commandline
    # fink has no edit function

    if man == 'fink':

        # fink dumpinfo -finfofile pac | cut -d: -f2 | xargs $editor

        rawdump = Popen(['fink', 'dumpinfo', '-finfofile', pac],
                        stdout=PIPE).communicate()[0]
        os.system('open ' + rawdump.split(':')[1])
    elif man == 'brew':

        # this might need adjustments based on if .info files are asociated

        os.system('brew edit ' + pac)
    elif man == 'port':
        os.system('port edit ' + pac)


def maint_fink():
    os.system('fink selfupdate')
    os.system('fink cleanup')


def maint_brew():
    """I don't know what else brew needs."""
    os.system('brew update')


def maint_port():
    os.system('port selfupdate')
    os.system('port clean')


def maint(man='all'):
    if man == 'all':
        if managers[0] != 'None':
            print 'running maintince on all your package managers'
            maint_fink()
        if managers[1] != 'None':
            maint_brew()
        if managers[2] != 'None':
            maint_port()
    elif man == 'fink':
        maint_fink()
    elif man == 'port':
        maint_port()
    elif man == 'brew':
        maint_brew()


if __name__ == '__main__':
    print sys.argv
    if sys.argv[1] == 'search':
        search(sys.argv[2])
    elif sys.argv[1] == 'edit':

        # package (defaults to all)

        edit(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'install':

        # package , manager

        install(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'maint':

        # package , manager

        if len(sys.argv) >= 3:
            maint(sys.argv[2])
        else:
            maint()
    elif sys.argv[1] == 'whohas':
        whohas(sys.argv[2])
