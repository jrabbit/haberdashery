#!/usr/bin/python
# -*- coding: utf-8 -*-
# INSTALL THAT SUCKER
#  --or--
# Haberdashery - the smart (mac) package manager front end.
# GPL v3 or later. (c) Jrabbit 2010.

import os
import sys
from subprocess import *

managers = ['fink', 'brew', 'port', 'pip', 'gem', 'cpan']
paths = []

# lets find where you have your pack-mans installed

for x in managers:
    rawpath = Popen(['which', x], stdout=PIPE).communicate()[0]
    rootpath = os.path.split(os.path.split(rawpath)[0])[0]  # nasty, but it gets us the prefixes
    if len(rootpath) != 0:
        print 'Found a ' + x + ' install at ' + rootpath
        paths.append(rootpath)
    else:
        paths.append('None')

        # this may seem redundant but if brew isn't installed and then port is, calling the 2nd key would give the macports path.

    if not paths:
        print 'Sorry found no package managers. Is your $PATH setup correctly?'

pacman = dict(zip(managers, paths))

def install(pac, man="solo"):
    """Try and install a package, need fucntino for multi-packages OR use -1 incides."""
    if man == "solo" and paths.count("None") == 2:
        # if theres only one package manger, find it and use it.
        if pacman['fink'] != 'None':
            install_fink(pac)
        if pacman['brew'] != 'None':
            install_brew(pac)
        if pacman['port'] != 'None':
            install_port(pac)
        if pacman['pip'] != 'None':
            install_pip(pac)
        if pacman['gem'] != 'None':
            install_gem(pac)
        if pacman['cpan'] != 'None':
            install_cpan(pac)
    else:
        locals()['install_%s' % man](pac)

        

def install_fink(pac):
     os.system('fink install ' + pac)

def install_brew(pac):
    os.system('brew install ' + pac)

def install_port(pac):
    os.system('port install ' + pac)

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

def search_whohas(pac):
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
        if pacman['fink'] != 'None':
            search_fink(pac)
        if pacman['brew'] != 'None':
            search_brew(pac)
        if pacman['port'] != 'None':
            search_port(pac)
        if pacman['pip'] != 'None':
            search_pip(pac)
        if pacman['gem'] != 'None':
            search_gem(pac)
        if pacman['cpan'] != 'None':
            search_cpan(pac)
        search_whohas(package)
    else:
        locals()['search_%s' % man](pac)
        #someone said this is wrong but its short and sweet.

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
    if pacman['fink'] != 'None':
        build_dict_fink()
        langs.append("foo-fink.rws")
    if pacman['brew'] != 'None':
        build_dict_brew()
        langs.append("foo-brew.rws")
    if pacman['port'] != 'None':
        build_dict_macports()
        langs.append("foo-port.rws")
    f.write(langs)
    f.close()
    #aspell --lang=foo now
#end spelling

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
        if pacman['fink'] != 'None':
            maint_fink()
        if pacman['brew'] != 'None':
            maint_brew()
        if pacman['port'] != 'None':
            maint_port()
    else:
        locals()['maint_%s' % man]()

if __name__ == '__main__':
    print sys.argv
    print pacman
    if len(sys.argv) < 2:
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
        helppage = open('help', 'r')
        print helppage
        #print list of commands and what args they take
