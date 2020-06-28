#!/usr/bin/env python

#===========================================================================
#
# Checkout and build LROSE, using autoconf and configure.
#
# This script performs the following steps:
#
#   1. clone lrose-core from git
#   2. setup autoconf Makefile.am files
#   3. run configure to create makefiles
#   4. perform the build and install
#   5. check the build
#
# You can optionally specify a release date.
#
# Use --help to see the command line options.
#
#===========================================================================

from __future__ import print_function
import os
import sys
import shutil
import subprocess
from optparse import OptionParser
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
import glob

def main():

    # globals

    global thisScriptName
    thisScriptName = os.path.basename(__file__)

    global thisScriptDir
    thisScriptDir = os.path.dirname(__file__)

    global options
    global package
    global prefix
    global releaseName
    global releaseTag
    global releaseDate
    global netcdfDir
    global displaysDir
    global coreDir
    global codebaseDir
    global scratchBuildDir
    global tmpBinDir
    global tmpLibDir
    global binDir
    global scriptsDir
    global libDir
    global runtimeLibRelDir
    global includeDir
    global shareDir
    global dateStr
    global debugStr
    global logPath
    global logFp

    # parse the command line

    usage = "usage: " + thisScriptName + " [options]"
    homeDir = os.environ['HOME']
    prefixDirDefault = os.path.join(homeDir, 'lrose')
    buildDirDefault = '/tmp/lrose_build'
    logDirDefault = '/tmp/lrose_build/logs'
    parser = OptionParser(usage)
    parser.add_option('--clean',
                      dest='clean', default=False,
                      action="store_true",
                      help='Cleanup tmp build dir')
    parser.add_option('--debug',
                      dest='debug', default=True,
                      action="store_true",
                      help='Set debugging on')
    parser.add_option('--verbose',
                      dest='verbose', default=False,
                      action="store_true",
                      help='Set verbose debugging on')
    parser.add_option('--package',
                      dest='package', default='lrose-core',
                      help='Package name. Options are: ' + \
                      'lrose-core (default), lrose-blaze, lrose-cyclone, lrose-cidd, samurai')
    parser.add_option('--releaseDate',
                      dest='releaseDate', default='latest',
                      help='Date from which to compute tag for git clone. Applies if --tag is not used.')
    parser.add_option('--tag',
                      dest='tag', default='master',
                      help='Tag to check out lrose. Overrides --releaseDate')
    parser.add_option('--prefix',
                      dest='prefix', default=prefixDirDefault,
                      help='Install directory, default is ~/lrose')
    parser.add_option('--buildDir',
                      dest='buildDir', default=buildDirDefault,
                      help='Temporary build dir, default is /tmp/lrose_build')
    parser.add_option('--logDir',
                      dest='logDir', default=logDirDefault,
                      help='Logging dir, default is /tmp/lrose_build/logs')
    parser.add_option('--static',
                      dest='static', default=False,
                      action="store_true",
                      help='use static linking, default is dynamic')
    parser.add_option('--installAllRuntimeLibs',
                      dest='installAllRuntimeLibs', default=False,
                      action="store_true",
                      help=\
                      'Install dynamic runtime libraries for all binaries, ' + \
                      'in a directory relative to the bin dir. ' + \
                      'System libraries are included.')
    parser.add_option('--installLroseRuntimeLibs',
                      dest='installLroseRuntimeLibs', default=False,
                      action="store_true",
                      help=\
                      'Install dynamic runtime lrose libraries for all binaries, ' + \
                      'in a directory relative to the bin dir. ' + \
                      'System libraries are not included.')
    parser.add_option('--noScripts',
                      dest='noScripts', default=False,
                      action="store_true",
                      help='Do not install runtime scripts as well as binaries')
    parser.add_option('--buildNetcdf',
                      dest='buildNetcdf', default=False,
                      action="store_true",
                      help='Build netcdf and hdf5 from source')
    parser.add_option('--fractl',
                      dest='build_fractl', default=False,
                      action="store_true",
                      help='Checkout and build fractl after core build is complete')
    parser.add_option('--vortrac',
                      dest='build_vortrac', default=False,
                      action="store_true",
                      help='Checkout and build vortrac after core build is complete')
    parser.add_option('--samurai',
                      dest='build_samurai', default=False,
                      action="store_true",
                      help='Checkout and build samurai after core build is complete')
    parser.add_option('--cmake3',
                      dest='use_cmake3', default=False,
                      action="store_true",
                      help='Use cmake3 instead of cmake for samurai')
    parser.add_option('--geolib',
                      dest='build_geolib', default=False,
                      action="store_true",
                      help='Build and install geolib - for fractl, samurai')
    parser.add_option('--no_core_apps',
                      dest='no_core_apps', default=False,
                      action="store_true",
                      help='Do not build the lrose core apps')

    (options, args) = parser.parse_args()
    
    if (options.verbose):
        options.debug = True

    # check package name

    if (options.package != "lrose-core" and
        options.package != "lrose-blaze" and
        options.package != "lrose-cyclone" and
        options.package != "lrose-cidd" and
        options.package != "samurai") :
        print("ERROR: invalid package name: %s:" % options.package, file=sys.stderr)
        print("  options: lrose-core, lrose-blaze, lrose-cyclone, lrose-cidd, samurai",
              file=sys.stderr)
        sys.exit(1)

    # for CIDD, set to static linkage
    if (options.package == "lrose-cidd"):
        options.static = True
        
    debugStr = " "
    if (options.verbose):
        debugStr = " --verbose "
    elif (options.debug):
        debugStr = " --debug "

    package = options.package
    prefix = options.prefix
    runtimeLibRelDir = package + "_runtime_libs"

    # runtime

    now = time.gmtime()
    nowTime = datetime(now.tm_year, now.tm_mon, now.tm_mday,
                       now.tm_hour, now.tm_min, now.tm_sec)
    dateStr = nowTime.strftime("%Y%m%d")

    # set release tag

    if (options.tag != "master"):
        releaseTag = options.tag
        releaseName = options.tag
        releaseDate = "not-set"
    elif (options.releaseDate == "latest"):
        releaseDate = datetime(int(dateStr[0:4]),
                               int(dateStr[4:6]),
                               int(dateStr[6:8]))
        releaseTag = "master"
        releaseName = options.package + "-" + dateStr
    else:
        # check we have a good release date
        releaseDate = datetime(int(options.releaseDate[0:4]),
                               int(options.releaseDate[4:6]),
                               int(options.releaseDate[6:8]))
        releaseTag = options.package + "-" + options.releaseDate[0:8]
        releaseName = releaseTag

    # set directories
    
    scratchBuildDir = os.path.join(options.buildDir, 'scratch')
    coreDir = os.path.join(options.buildDir, "lrose-core")
    displaysDir = os.path.join(options.buildDir, "lrose-displays")
    netcdfDir = os.path.join(options.buildDir, "lrose-netcdf")
    codebaseDir = os.path.join(coreDir, "codebase")

    tmpBinDir = os.path.join(scratchBuildDir, 'bin')
    tmpLibDir = os.path.join(scratchBuildDir, 'lib')
    binDir = os.path.join(prefix, 'bin')
    scriptsDir = os.path.join(prefix, 'scripts')
    libDir = os.path.join(prefix, 'lib')
    includeDir = os.path.join(prefix, 'include')
    shareDir = os.path.join(prefix, 'share')
    
    # debug print

    if (options.debug):
        print("Running %s:" % thisScriptName, file=sys.stderr)
        print("  package: ", package, file=sys.stderr)
        print("  releaseDate: ", releaseDate, file=sys.stderr)
        print("  releaseName: ", releaseName, file=sys.stderr)
        print("  releaseTag: ", releaseTag, file=sys.stderr)
        print("  static: ", options.static, file=sys.stderr)
        print("  buildDir: ", options.buildDir, file=sys.stderr)
        print("  logDir: ", options.logDir, file=sys.stderr)
        print("  coreDir: ", coreDir, file=sys.stderr)
        print("  codebaseDir: ", codebaseDir, file=sys.stderr)
        print("  displaysDir: ", displaysDir, file=sys.stderr)
        print("  netcdfDir: ", netcdfDir, file=sys.stderr)
        print("  prefixDir: ", prefix, file=sys.stderr)
        print("  binDir: ", binDir, file=sys.stderr)
        print("  libDir: ", libDir, file=sys.stderr)
        print("  includeDir: ", includeDir, file=sys.stderr)
        print("  shareDir: ", shareDir, file=sys.stderr)
        print("  buildNetcdf: ", options.buildNetcdf, file=sys.stderr)
        print("  package: ", package, file=sys.stderr)
        print("  use_cmake3: ", options.use_cmake3, file=sys.stderr)
        print("  build_geolib: ", options.build_geolib, file=sys.stderr)
        print("  build_fractl: ", options.build_fractl, file=sys.stderr)
        print("  build_vortrac: ", options.build_vortrac, file=sys.stderr)
        print("  build_samurai: ", options.build_samurai, file=sys.stderr)
        print("  no_core_apps: ", options.no_core_apps, file=sys.stderr)

    # create build dir
    
    createBuildDir()

    # initialize logging

    if (os.path.isdir(options.logDir) == False):
        os.makedirs(options.logDir)
    logPath = os.path.join(options.logDir, "initialize");
    logFp = open(logPath, "w+")
    
    # make tmp dirs

    try:
        os.makedirs(scratchBuildDir)
        os.makedirs(tmpBinDir)
        os.makedirs(options.logDir)
    except:
        print("  note - dirs already exist", file=sys.stderr)

    # get repos from git

    logPath = prepareLogFile("git-checkout");
    gitCheckout()

    # install the distribution-specific makefiles

    logPath = prepareLogFile("install-package-makefiles");
    os.chdir(codebaseDir)
    scriptPath = "../build/scripts/installPackageMakefiles.py"
    shellCmd(scriptPath + " --debug --package " + package)

    # trim libs and apps to those required by distribution makefiles

    trimToMakefiles("libs")
    trimToMakefiles("apps")

    # set up autoconf

    logPath = prepareLogFile("setup-autoconf");
    setupAutoconf()

    # create the release information file
    
    createReleaseInfoFile()

    # run qmake for QT apps to create moc_ files

    if (options.package != "samurai"):
        logPath = prepareLogFile("create-qt-moc-files");
        hawkEyeDir = os.path.join(codebaseDir, "apps/radar/src/HawkEye")
        createQtMocFiles(hawkEyeDir)

    # prune any empty directories

    prune(codebaseDir)

    # build netcdf support
    
    if (options.buildNetcdf):
        logPath = prepareLogFile("build-netcdf");
        buildNetcdf()

    # build the package

    buildPackage()

    # detect which dynamic libs are needed
    # copy the dynamic libraries into a directory relative
    # to the binary install dir:
    #     bin/${package}_runtime_libs

    os.chdir(codebaseDir)
    if (options.installAllRuntimeLibs):
        scriptPath = "../build/scripts/installOriginLibFiles.py"
        cmd = scriptPath + \
              " --binDir " + tmpBinDir + \
              " --relDir " + runtimeLibRelDir
        if (options.verbose):
            cmd = cmd + " --verbose"
        elif (options.debug):
            cmd = cmd + " --debug"
        shellCmd(cmd)
    elif (options.installLroseRuntimeLibs):
        scriptPath = "../build/scripts/installOriginLroseLibs.py"
        cmd = scriptPath + \
              " --binDir " + tmpBinDir + \
              " --libDir " + tmpLibDir + \
              " --relDir " + runtimeLibRelDir
        if (options.verbose):
            cmd = cmd + " --verbose"
        elif (options.debug):
            cmd = cmd + " --debug"
        shellCmd(cmd)

    # perform the install

    logPath = prepareLogFile("do-final-install");
    doFinalInstall();

    # check the install

    logPath = prepareLogFile("no-logging");
    checkInstall()

    # build CSU packages

    if (options.build_geolib):
        logPath = prepareLogFile("geolib");
        buildGeolib()

    if (options.build_fractl):
        logPath = prepareLogFile("fractl");
        buildFractl()

    if (options.build_vortrac):
        logPath = prepareLogFile("vortrac");
        buildVortrac()

    if (options.build_samurai):
        logPath = prepareLogFile("samurai");
        buildSamurai()

    sys.exit(0)

    # delete the tmp dir

    if (options.clean):
        shutil.rmtree(options.buildDir)

    logFp.close()
    sys.exit(0)

########################################################################
# create the build dir

def createBuildDir():

    # check if exists already

    if (os.path.isdir(options.buildDir)):

        print("WARNING: you are about to remove all contents in dir: " + 
              options.buildDir)
        print("===============================================")
        contents = os.listdir(options.buildDir)
        for filename in contents:
            print(("  " + filename))
        print("===============================================")
        answer = "n"
        if (sys.version_info > (3, 0)):
            answer = input("WARNING: do you wish to proceed (y/n)? ")
        else:
            answer = raw_input("WARNING: do you wish to proceed (y/n)? ")
        if (answer != "y"):
            print("  aborting ....")
            sys.exit(1)
                
        # remove it

        shutil.rmtree(options.buildDir)

    # make it clean
    
    print(("INFO: you are about to create build dir: " + 
          options.buildDir))
    
    os.makedirs(options.buildDir)

########################################################################
# check out repos from git

def gitCheckout():

    os.chdir(options.buildDir)

    # lrose core

    shellCmd("/bin/rm -rf lrose-core")
    if (options.tag == "master"):
        shellCmd("git clone https://github.com/NCAR/lrose-core")
    else:
        shellCmd("git clone --branch " + releaseTag + \
                 " https://github.com/NCAR/lrose-core")

    # netcdf and hdf5

    if (options.buildNetcdf):
        shellCmd("/bin/rm -rf lrose-netcdf")
        shellCmd("git clone https://github.com/NCAR/lrose-netcdf")

    # color scales and maps in displays repo

    if (options.package != "samurai") :
        shellCmd("/bin/rm -rf lrose-displays")
        shellCmd("git clone https://github.com/NCAR/lrose-displays")

########################################################################
# set up autoconf for configure etc

def setupAutoconf():

    os.chdir(codebaseDir)

    # create files for configure

    shutil.copy("../build/autoconf/Makefile.top",
                "./Makefile")
    
    if (options.static):
        if (package == "lrose-cidd"):
            shutil.copy("../build/autoconf/configure.base.cidd",
                        "./configure.base")
        else:
            shutil.copy("../build/autoconf/configure.base",
                        "./configure.base")
        shellCmd("../build/autoconf/createConfigure.am.py --dir . " +
                 " --baseName configure.base" +
                 " --pkg " + package + debugStr)
    else:
        if (package == "lrose-cidd"):
            shutil.copy("../build/autoconf/configure.base.shared.cidd",
                        "./configure.base.shared")
        else:
            shutil.copy("../build/autoconf/configure.base.shared",
                        "./configure.base.shared")
        shellCmd("../build/autoconf/createConfigure.am.py --dir . " +
                 " --baseName configure.base.shared --shared" +
                 " --pkg " + package + debugStr)

########################################################################
# Run qmake for QT apps such as HawkEye to create _moc files

def createQtMocFiles(appDir):
    
    if (os.path.isdir(appDir) == False):
        return

    os.chdir(appDir)
    shellCmd("rm -f moc*");
    shellCmd("qmake -o Makefile.qmake");
    shellCmd("make -f Makefile.qmake mocables");

########################################################################
# write release information file

def createReleaseInfoFile():

    # go to core dir

    os.chdir(scratchBuildDir)

    # open info file

    releaseInfoPath = os.path.join(coreDir, "ReleaseInfo.txt")
    info = open(releaseInfoPath, 'w')

    # write release info

    info.write("package:" + package + "\n")
    info.write("version:" + dateStr + "\n")
    info.write("release:" + releaseName + "\n")

    # close

    info.close()

########################################################################
# get string value based on search key
# the string may span multiple lines
#
# Example of keys: SRCS, SUB_DIRS, MODULE_NAME, TARGET_FILE
#
# value is returned

def getValueListForKey(path, key):

    valueList = []

    try:
        fp = open(path, 'r')
    except IOError as e:
        if (options.verbose):
            print("ERROR - ", thisScriptName, file=sys.stderr)
            print("  Cannot open file:", path, file=sys.stderr)
        return valueList

    lines = fp.readlines()
    fp.close()

    foundKey = False
    multiLine = ""
    for line in lines:
        if (foundKey == False):
            if (line[0] == '#'):
                continue
        if (line.find(key) >= 0):
            foundKey = True
            multiLine = multiLine + line
            if (line.find("\\") < 0):
                break;
        elif (foundKey):
            if (line[0] == '#'):
                break
            if (len(line) < 2):
                break
            multiLine = multiLine + line;
            if (line.find("\\") < 0):
                break;

    if (foundKey == False):
        return valueList

    multiLine = multiLine.replace(key, " ")
    multiLine = multiLine.replace("=", " ")
    multiLine = multiLine.replace("\t", " ")
    multiLine = multiLine.replace("\\", " ")
    multiLine = multiLine.replace("\r", " ")
    multiLine = multiLine.replace("\n", " ")

    toks = multiLine.split(' ')
    for tok in toks:
        if (len(tok) > 0):
            valueList.append(tok)

    return valueList

########################################################################
# Trim libs and apps to those required by distribution

def trimToMakefiles(subDir):

    if (options.verbose):
        print("Trimming unneeded dirs, subDir: " + subDir, file=logFp)

    # get list of subdirs in makefile

    dirPath = os.path.join(codebaseDir, subDir)
    os.chdir(dirPath)

    # need to allow upper and lower case Makefile (makefile or Makefile)
    subNameList = getValueListForKey("makefile", "SUB_DIRS")
    if not subNameList:
        if (options.verbose):
            print("Trying uppercase Makefile ... ", file=logFp)
        subNameList = getValueListForKey("Makefile", "SUB_DIRS")
    
    for subName in subNameList:
        if (os.path.isdir(subName)):
            if (options.verbose):
                print("  need sub dir: " + subName, file=logFp)
            
    # get list of files in subDir

    entries = os.listdir(dirPath)
    for entry in entries:
        theName = os.path.join(dirPath, entry)
        if (options.verbose):
            print("considering: " + theName, file=logFp)
        if (entry == "perl5") or (entry == "scripts") or (entry == "include"):
            # always keep scripts directories
            continue
        if (entry == "images") or (entry == "resources"):
            # always keep QT resources
            continue
        if (os.path.isdir(theName)):
            if (entry not in subNameList):
                if (options.verbose):
                    print("discarding it", file=logFp)
                shutil.rmtree(theName)
            else:
                if (options.verbose):
                    print("keeping it and recursing", file=logFp)
                # check this child's required subdirectories (recurse)
                trimToMakefiles(os.path.join(subDir, entry))

########################################################################
# build netCDF

def buildNetcdf():

    os.chdir(netcdfDir)
    if (package == "lrose-cidd"):
        shellCmd("./build_and_install_netcdf.cidd_linux32 -x " + scratchBuildDir)
    else:
        if sys.platform == "darwin":
            shellCmd("./build_and_install_netcdf.osx -x " + scratchBuildDir)
        else:
            shellCmd("./build_and_install_netcdf -x " + scratchBuildDir)

########################################################################
# build package

def buildPackage():

    global logPath

    # set the environment

    os.environ["LDFLAGS"] = "-L" + scratchBuildDir + "/lib " + \
                            "-Wl,--enable-new-dtags," + \
                            "-rpath," + \
                            "'$$ORIGIN/" + runtimeLibRelDir + \
                            ":$$ORIGIN/../lib" + \
                            ":" + libDir + \
                            ":" + tmpLibDir + "'"
    os.environ["FC"] = "gfortran"
    os.environ["F77"] = "gfortran"
    os.environ["F90"] = "gfortran"

    if (sys.platform == "darwin"):
        os.environ["PKG_CONFIG_PATH"] = "/usr/local/opt/qt/lib/pkgconfig"
    else:
        os.environ["CXXFLAGS"] = " -std=c++11 "

    # print out environment

    logPath = prepareLogFile("print-environment");
    cmd = "env"
    shellCmd(cmd)

    # run configure

    logPath = prepareLogFile("run-configure");
    os.chdir(codebaseDir)
    if (options.buildNetcdf):
        cmd = "./configure --with-hdf5=" + scratchBuildDir + \
              " --with-netcdf=" + scratchBuildDir + \
                                " --prefix=" + scratchBuildDir
    else:
        cmd = "./configure --prefix=" + scratchBuildDir
    shellCmd(cmd)

    # build the libraries

    logPath = prepareLogFile("build-libs");
    os.chdir(os.path.join(codebaseDir, "libs"))
    cmd = "make -k -j 8"
    shellCmd(cmd)

    # install the libraries

    logPath = prepareLogFile("install-libs-to-tmp");

    cmd = "make -k install-strip"
    shellCmd(cmd)

    if (options.no_core_apps == False):

        # build the apps

        logPath = prepareLogFile("build-apps");
        os.chdir(os.path.join(codebaseDir, "apps"))
        cmd = "make -k -j 8"
        shellCmd(cmd)
        
        # install the apps
        
        logPath = prepareLogFile("install-apps-to-tmp");
        cmd = "make -k install-strip"
        shellCmd(cmd)

    # optionally install the scripts

    if (options.package == "lrose-core" and options.noScripts == False):

        logPath = prepareLogFile("install-scripts-to-tmp");

        # install perl5
        
        perl5InstallDir = os.path.join(prefix, "lib/perl5")
        try:
            os.makedirs(perl5InstallDir)
        except:
            print("Dir exists: " + perl5InstallDir, file=logFp)

        perl5SourceDir = os.path.join(codebaseDir, "libs/perl5/src")
        print("==>> perl5SourceDir:", perl5SourceDir, file=logFp)
        print("==>> perl5InstallDir:", perl5InstallDir, file=logFp)
        if (os.path.isdir(perl5SourceDir)):
            os.chdir(perl5SourceDir)
            cmd = "rsync -av *pm " + perl5InstallDir
            print("running cmd:", cmd, file=logFp)
            shellCmd("rsync -av *pm " + perl5InstallDir)

        # procmap

        procmapScriptsDir = os.path.join(codebaseDir, "apps/procmap/src/scripts")
        if (os.path.isdir(procmapScriptsDir)):
            os.chdir(procmapScriptsDir)
            shellCmd("./install_scripts.lrose " + scriptsDir)

        # general

        generalScriptsDir = os.path.join(codebaseDir, "apps/scripts/src")
        if (os.path.isdir(generalScriptsDir)):
            os.chdir(generalScriptsDir)
            shellCmd("./install_scripts.lrose " + scriptsDir)

########################################################################
# perform final install

def doFinalInstall():

    # make target dirs

    try:
        os.makedirs(binDir)
        os.makedirs(libDir)
        os.makedirs(includeDir)
        os.makedirs(shareDir)
    except:
        print("  note - dirs already exist", file=logFp)
    
    # install docs etc
    
    os.chdir(coreDir)

    shellCmd("rsync -av LICENSE.txt " + prefix)
    shellCmd("rsync -av release_notes " + prefix)
    shellCmd("rsync -av docs " + prefix)

    if (package == "lrose-cidd"):
        shellCmd("rsync -av ./codebase/apps/cidd/src/CIDD/scripts " +
                 options.prefix)

    # install color scales

    if (os.path.isdir(displaysDir)):
        os.chdir(displaysDir)
        shellCmd("rsync -av color_scales " + shareDir)

    # install binaries and libs

    os.chdir(scratchBuildDir)

    shellCmd("rsync -av bin " + prefix)
    shellCmd("rsync -av lib " + prefix)
    shellCmd("rsync -av include " + prefix)

########################################################################
# check the install

def checkInstall():

    os.chdir(coreDir)
    print(("============= Checking libs for " + package + " ============="))
    shellCmd("./build/scripts/checkLibs.py" + \
             " --prefix " + prefix + \
             " --package " + package)
    print("====================================================")

    if (options.no_core_apps == False):
        print(("============= Checking apps for " + package + " ============="))
        shellCmd("./build/scripts/checkApps.py" + \
                 " --prefix " + prefix + \
                 " --package " + package)
        print("====================================================")
    
    print("**************************************************")
    print("*** Done building auto release *******************")
    print(("*** Installed in dir: " + prefix + " ***"))
    print("**************************************************")

########################################################################
# prune empty dirs

def prune(tree):

    # walk the tree
    if (os.path.isdir(tree)):
        contents = os.listdir(tree)

        if (len(contents) == 0):
            if (options.verbose):
                print("pruning empty dir: " + tree, file=logFp)
            shutil.rmtree(tree)
        else:
            for l in contents:
                # remove CVS directories
                if (l == "CVS") or (l == ".git"): 
                    thepath = os.path.join(tree,l)
                    if (options.verbose):
                        print("pruning dir: " + thepath, file=logFp)
                    shutil.rmtree(thepath)
                else:
                    thepath = os.path.join(tree,l)
                    if (os.path.isdir(thepath)):
                        prune(thepath)
            # check if this tree is now empty
            newcontents = os.listdir(tree)
            if (len(newcontents) == 0):
                if (options.verbose):
                    print("pruning empty dir: " + tree, file=logFp)
                shutil.rmtree(tree)

########################################################################
# build geographiclib

def buildGeolib():

    global logPath

    print("==>> buildGeolib", file=sys.stderr)
    print("====>> prefix: ", prefix, file=sys.stderr)

    # check out fractl

    os.chdir(options.buildDir)
    shellCmd("/bin/rm -rf geographiclib")
    shellCmd("git clone git://git.code.sourceforge.net/p/geographiclib/code geographiclib")
    os.chdir("./geographiclib")
    shellCmd("mkdir BUILD");
    os.chdir("./BUILD")

    # set the install environment

    os.environ["LROSE_PREFIX"] = prefix
    
    # create makefiles

    if (options.use_cmake3):
        cmd = "cmake3 -D CMAKE_INSTALL_PREFIX=" + prefix + " .."
    else:
        cmd = "cmake -D CMAKE_INSTALL_PREFIX=" + prefix + " .."
    shellCmd(cmd)

    # do the build

    cmd = "make -j 4"
    shellCmd(cmd)

    # do the install

    cmd = "make install"
    shellCmd(cmd)

    return

########################################################################
# build fractl package

def buildFractl():

    global logPath

    print("==>> buildFractl", file=sys.stderr)
    print("====>> prefix: ", prefix, file=sys.stderr)
    print("====>> includeDir: ", includeDir, file=sys.stderr)
    print("====>> libDir: ", libDir, file=sys.stderr)
    print("====>> binDir: ", binDir, file=sys.stderr)

    # check out fractl

    os.chdir(options.buildDir)
    shellCmd("/bin/rm -rf fractl")
    shellCmd("git clone https://github.com/mmbell/fractl")
    os.chdir("./fractl")

    # set the environment

    os.environ["LROSE_PREFIX"] = prefix
    os.environ["LROSE_ROOT_DIR"] = prefix
    os.environ["LROSE_INCLUDE_DIRS"] = includeDir
    os.environ["LROSE_LIB_DIR"] = libDir
    os.environ["LROSE_BIN_DIR"] = binDir
    os.environ["CMAKE_INSTALL_PREFIX"] = prefix
    
    # create makefiles

    cmd = "cmake -DCMAKE_INSTALL_PREFIX=" + prefix + " ."
    shellCmd(cmd)

    # do the build

    cmd = "make -j 4"
    shellCmd(cmd)

    # do the install

    cmd = "make install"
    shellCmd(cmd)

    return

########################################################################
# build vortrac package

def buildVortrac():

    global logPath

    print("====>> buildVortrac", file=sys.stderr)
    print("====>> prefix: ", prefix, file=sys.stderr)

    # check out vortrac

    os.chdir(options.buildDir)
    shellCmd("/bin/rm -rf vortrac")
    shellCmd("git clone https://github.com/mmbell/vortrac")
    os.chdir("./vortrac/src")

    # set the environment

    os.environ["LROSE_INSTALL_DIR"] = prefix

    osType = getOSType()
    if (osType == 'Debian GNU/Linux 10 (buster)' or
        osType == 'Ubuntu 19.10'):
        # cmake does not work in latest Debian versions
        # so copy in Makefile instead of using qmake
        shellCmd("/bin/cp -f _makefiles/Makefile.debian10 Makefile")
    else:
        # create Makefile using cmake
        cmd = "qmake ."
        shellCmd(cmd)

    # do the build

    cmd = "make -j 4"
    shellCmd(cmd)
    
    if (sys.platform == "darwin"):
        cmd = "rsync ../Resources/*.xml vortrac.app/Contents/Resources"
        shellCmd(cmd)

    cmd = "rsync ../Resources " + prefix
    shellCmd(cmd)
    
    # do the install

    cmd = "rsync ./vortrac " + binDir
    shellCmd(cmd)

    return

########################################################################
# build samurai package

def buildSamurai():

    global logPath

    print("==>> buildSamurai", file=sys.stderr)
    print("====>> prefix: ", prefix, file=sys.stderr)
    print("====>> includeDir: ", includeDir, file=sys.stderr)
    print("====>> libDir: ", libDir, file=sys.stderr)
    print("====>> binDir: ", binDir, file=sys.stderr)

    # check out samurai

    os.chdir(options.buildDir)
    shellCmd("/bin/rm -rf samurai")
    shellCmd("git clone https://github.com/mmbell/samurai")
    os.chdir("./samurai")

    # set the environment

    os.environ["LROSE_PREFIX"] = prefix
    os.environ["LROSE_ROOT_DIR"] = prefix
    os.environ["LROSE_INCLUDE_DIRS"] = includeDir
    os.environ["LROSE_LIB_DIR"] = libDir
    os.environ["LROSE_BIN_DIR"] = binDir
    os.environ["CMAKE_INSTALL_PREFIX"] = prefix
    
    # create makefiles

    if (options.use_cmake3):
        cmd = "cmake3 -DCMAKE_INSTALL_PREFIX=" + prefix + " ."
    else:
        cmd = "cmake -DCMAKE_INSTALL_PREFIX=" + prefix + " ."
    shellCmd(cmd)

    # do the build

    cmd = "make -j 4"
    shellCmd(cmd)

    # do the install

    cmd = "make install"
    shellCmd(cmd)

    return

########################################################################
# get the OS type from the /etc/os-release file in linux

def getOSType():

    osrelease_file = open("/etc/os-release", "rt")
    lines = osrelease_file.readlines()
    osrelease_file.close()
    osType = "unknown"
    for line in lines:
        if (line.find('PRETTY_NAME') == 0):
            lineParts = line.split('=')
            osParts = lineParts[1].split('"')
            osType = osParts[1]
    return osType

########################################################################
# prepare log file

def prepareLogFile(logFileName):

    global logFp

    logFp.close()
    logPath = os.path.join(options.logDir, logFileName + ".log");
    if (logPath.find('no-logging') >= 0):
        return logPath
    print("========================= " + logFileName + " =========================", file=sys.stderr)
    if (options.verbose):
        print("====>> Creating log file: " + logPath + " <<==", file=sys.stderr)
    logFp = open(logPath, "w+")
    logFp.write("===========================================\n")
    logFp.write("Log file from script: " + thisScriptName + "\n")
    logFp.write(logFileName + "\n")

    return logPath

########################################################################
# Run a command in a shell, wait for it to complete

def shellCmd(cmd):

    print("Running cmd:", cmd, file=sys.stderr)
    
    if (logPath.find('no-logging') >= 0):
        cmdToRun = cmd
    else:
        print("Log file is:", logPath, file=sys.stderr)
        print("    ....", file=sys.stderr)
        cmdToRun = cmd + " 1>> " + logPath + " 2>&1"

    try:
        retcode = subprocess.check_call(cmdToRun, shell=True)
        if retcode != 0:
            print("Child exited with code: ", retcode, file=sys.stderr)
            sys.exit(1)
        else:
            if (options.verbose):
                print("Child returned code: ", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
        sys.exit(1)

    print("    done", file=sys.stderr)
    
########################################################################
# Run - entry point

if __name__ == "__main__":
   main()
