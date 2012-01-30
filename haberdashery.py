#!/usr/bin/python
# -*- coding: utf-8 -*-
# INSTALL THAT SUCKER
#  --or--
# Haberdashery - the smart (mac) package manager front end.
# GPL v3 or later. (c) Jrabbit 2010.

import os
import sys
from subprocess import *

import baker

import pip

managers = ['fink', 'brew', 'port', 'pip', 'gem', 'cpan']
paths = []
verbosity=1

# lets find where you have your pack-mans installed
#def firstrun():
for x in managers:
    rawpath = Popen(['which', x], stdout=PIPE).communicate()[0]
    rootpath = os.path.split(os.path.split(rawpath)[0])[0]  # nasty, but it gets us the prefixes
    if rootpath:
        if x is not 'pip':
            if verbosity:
                print 'Found a ' + x + ' install at ' + rootpath
            paths.append(rootpath)
        elif pip.is_python():
            if verbosity:
                print 'Found a ' + x + ' install at ' + rootpath
            paths.append(rootpath)
    else:
        paths.append('None')

        # this may seem redundant but if brew isn't installed and then port is, calling the 2nd key would give the macports path.

    if not paths:
        print 'Sorry found no package managers. Is your $PATH setup correctly?'
        print 'Your current $PATH: %s' % os.environ['PATH']

if verbosity:
    print managers
    print paths

pacman = dict(zip(managers, paths))

@baker.command
def install(pac, man="solo"):
    """Try and install a package, need fucntino for multi-packages OR use -1 incides."""
    if man == "solo" and paths.count("None") == 5:
        # if theres only one package manger, find it and use it.
        #Ok this might not work since I added pip,gem, and cpan
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
        instain = {'fink': install_fink, 'brew': install_brew, 'port': install_port, 'pip': install_pip, 'gem': install_gem, 'cpan': install_cpan} 
        try:
            f = instain[man]
            print "Trying to install package %s on %s" % (pac, man)
            f(pac)
        except KeyError:
            print "Please use install like this: haberdashery.py install package manager: \nhaberdashery.py install %s %s" % (man, pac)

def install_fink(pac):
     os.system('fink install ' + pac)

def install_brew(pac):
    os.system('brew install ' + pac)

def install_port(pac):
    os.system('port install ' + pac)

def install_pip(pac):
    os.system('pip install ' + pac)

def install_gem(pac):
    os.system('gem install ' + pac)

def install_cpan(pac):
    os.system("PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install %s'" % (pac, ) )


def search_fink(pac):
    """ Searches fink for a package, returns a list of packages line by line"""
    things = Popen(['fink', 'list', pac], stdout=PIPE).communicate()[0]
    if not things:
        return
    else:
        print 'found ' + str(len(things.split('\n'))) + ' results for ' + pac\
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
        print 'found ' + str(len(things)) + ' results for ' + pac\
             + ' in your homebrew:'
        print things
        return things


def search_port(pac):
    """Search macports for a package, returns a list of package lines"""
    things = Popen(['port', 'search', pac], stdout=PIPE).communicate()[0]
    if not things:
        return
    else:
        print 'found ' + str(len(things.split('\n'))) + ' results for ' + pac\
             + ' in your MacPorts:'
        print things
        return things

@baker.command(name="whohas")
def search_whohas(pac):
    """Run the included or system whohas and print the findings"""
    p = Popen(['which', 'whohas'], stdout=PIPE).communicate()[0]
    if p:
       wh = p.strip() #FFFFFFFFF newline.
    else:
        wh = os.getcwd()+"/whohas-0.24/program/whohas"
    os.system(wh+" "+pac)

def search_pip(pac):
    # pip search "query"
    raw = Popen(['pip', 'search', "%s" % (pac, )], stdout=PIPE).communicate()[0]
    things = raw.split('\n')[:-1]
    if not things:
        return
    else:
        print 'found ' + str(len(things)) + ' results for ' + pac\
             + ' On pypi.python.org:'
        for x in things:
            print x
        return things

def search_gem(pac):
    things = []
    raw = Popen(['gem', 'search','-b', pac], stdout=PIPE).communicate()[0]
    for x in raw.split('\n'):
        if x and x != '*** LOCAL GEMS ***' and x != '*** REMOTE GEMS ***':
            things.append(x)
    if not things:
       return
    else:
       print 'found ' + str(len(things)) + ' results for ' + pac\
            + ' in your configured rubygems sources:'
       print things
       return things
    

def search_cpan(pac):
    #perl -MCPAN -e 'CPAN::Shell->m( q[REGEXGOESHERE] )'
    #regex actally goes in q[] because it needs to be a string. silly perl.
    raw = Popen(['perl', '-MCPAN','-e', "'CPAN::Shell->m( q[/%s/] )'" % pac], stdout=PIPE, env ={"PERL_MM_USE_DEFAULT": "1"}).communicate()[0]
    things = []
    for x in raw.split('\n'):
        if x.startswith("Module"): #remove CPAN's garble.
            things.append(x)
    if not things:
        return
    else:
        print 'found ' + str(len(things)) + ' results for ' + pac\
             + ' in CPAN:'
        print things
        return things

@baker.command
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
        search_whohas(pac)
    else:
        nofunzone = {'fink': search_fink, 'brew': search_brew, 'port': search_port, 'pip': search_pip, 'gem': search_gem, 'cpan': search_cpan} 
        #print nofunzone
        try:
            f = nofunzone[man]
            print "trying to run a search on %s for %s" % (man, pac)
            f(pac)
        except KeyError:
            print "Please use search like this: haberdashery.py search package manager: \nhaberdashery.py search %s %s" % (man, pac)
       # locals()['search_%s(pac)' % man]

@baker.command
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

def build_dict_port():
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

@baker.command(name="spelling")
def build_aspell_multi():
    #foo.multi add lang_code.rws
    f = open('foo.multi', 'rU')
    langs = []
    for man in pacman:
        if pacman[man] != 'None':
            funct = build_dict_ + man
            funct()
            langs.append("foo-%s.rws" % man)
    # if pacman['fink'] != 'None':
    #     build_dict_fink()
    #     langs.append("foo-fink.rws")
    # if pacman['brew'] != 'None':
    #     build_dict_brew()
    #     langs.append("foo-brew.rws")
    # if pacman['port'] != 'None':
    #     build_dict_port()
    #     langs.append("foo-port.rws")
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


@baker.command
def maint(man='all'):
    if man == 'all':
        print 'running maintenance on all your package managers'
        if pacman['fink'] != 'None':
            maint_fink()
        if pacman['brew'] != 'None':
            maint_brew()
        if pacman['port'] != 'None':
            maint_port()
    else:
        maint = {'fink': maint_fink, 'brew': maint_brew, 'port': maint_port} 
        #'pip': maint_pip, 'gem': maint_gem, 'cpan': maint_cpan
        f = maint[man]
        print "running maintenance on %s" % man
        f()

def migrate(manager, orig, to):
    """Migrate packages in a package manager from one kind to another
    like from mercurial-py25 to mercurial-py27 but for all python 2.5 packages"""
    #TODO: Fix logic, expose to user.
    if manager not in pacman:
        sys.exit("wrong package manager")
    pass
    #is package installed?
    orig_pkgs = []
    packages_raw = Popen(['fink', 'list', orig], stdout=PIPE).communicate()[0]
    for line in packages_raw.splitlines():
        package_meta = line.split('\t')
        if package_meta[0].strip():
            #yes package is installed.
            name = (line.split('\t')[1])
            # fink's variants are denoted by -py25 so seperate by - and pop last value
            orig_pkgs.append(name)
    #does package match from
    #does package have a counterpart
    new_pkgs = []
    for pkg in orig_pkgs:
        new_pkgs.append(pkg[:-4] + to)
    #install counterparts
    fink_install(' '.join(new_pkgs))
    if remove:
        pass


if __name__ == '__main__':
    if verbosity:
        print sys.argv
        print pacman
    if len(sys.argv) < 2:
        print "Please run haberdashery with atleast one command. Run 'haberdashery.py help' for help"
        sys.exit(0)
    elif sys.argv[1] == 'help':
        baker.usage()
    baker.run()