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

    if not paths:
        print 'Sorry found no package managers. Is your $PATH setup correctly?'


def install(pac, man='all'):
    """Try and install a package"""

    pass


def search_fink(pac):
    """ Searches fink for a package, returns a list of packages line by line"""

    things = Popen(['fink', 'list', pac], stdout=PIPE).communicate()[0]
    if not things:
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
    if not things:
        return
    else:
        print 'found ' + len(things) + ' results for ' + pac\
             + ' in your homebrew:'
        print things
        return things


def search_port(pac):
    """Search macports for a package, returns a list of package lines"""

    things = Popen(['port', 'search', pac], stdout=PIPE).communicate()[0]
    if not things:
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


def search(pac, man='all'):
    """Find a package in fink/brew/ports then run whohas"""
    if man == 'all':
        print "Searching all package managers"
        if managers[0] != 'None':
            search_fink(pac)
        if managers[1] != 'None':
            search_brew(pac)
        if managers[2] != 'None':
            search_port(pac)
        whohas(package)
    elif man == 'fink':
        search_fink(pac)
    elif man == 'port':
        search_port(pac)
    elif man == 'brew':
        search_brew(pac)
    elif man == 'whohas':
        whohas(pac)


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

#Spelling related stuff below:
def build_dict_fink():
    packages = []
    packages_raw = Popen(['fink', 'list'], stdout=PIPE).communicate()[0]
    #iterate over each line, split them on tabs, grab the third item in each TY DASH/#PYTHON
    for line in packages_raw.splitlines():
        packages.append(line.split('\t')[1])
    Popen(['aspell', 'create','master' ,'--lang=foo_fink', 'foo-fink'], stin=packages, stdout=PIPE).communicate()
    #return packages #is a list

def build_dict_macports():
    #untested. 
    packages = []
    packages_raw = Popen(['port', 'search'], stdout=PIPE).communicate()[0]
    for l in packages_raw.splitlines():
        packages.append(l.split('\t')[0])
    #aspell create master --lang=lang_code path/dict_name < wordlist
    Popen(['aspell', 'create','master' ,'--lang=foo_port', 'foo-port'], stin=packages, stdout=PIPE).communicate()
    #return packages # list

def build_dict_brew():
    packages_raw = Popen(['brew', 'search'], stdout=PIPE).communicate()[0]
    packages = packages_raw.splitlines()
    Popen(['aspell', 'create','master' ,'--lang=foo_brew', 'foo-brew'], stin=packages, stdout=PIPE).communicate()
    #return packages

def build_aspell_multi():
    #foo.multi add lang_code.rws
    f = open('foo.multi', 'rU')
    langs = []
    if managers[0] != 'None':
        build_dict_fink()
        langs.append("foo-fink.rws")
    if managers[1] != 'None':
        build_dict_brew()
        langs.append("foo-brew.rws")
    if managers[2] != 'None':
        build_dict_port()
        langs.append("foo-port.rws")
    f.write(langs)
    f.close()
    #aspell --lang=foo now

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
        print 'running maintince on all your package managers'
        if managers[0] != 'None':
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
    #print sys.argv
    if len(sys.argv) <= 2:
        print "Please run haberdashery with atleast one command. Run 'haberdashery.py help' for help"
        sys.exit(0)
    if sys.argv[1] == 'search':
        if len(sys.argv) >= 4:
            search(sys.argv[2], sys.argv[3])
        else:
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
    elif sys.argv[1] == 'spelling':
        build_aspell_multi()
    elif sys.argv[1] == 'help':
        pass #print list of commands and what args they take
