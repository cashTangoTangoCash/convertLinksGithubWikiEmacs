# 20161021 finding that wiki pages that link to each other in emacs do not work as desired on github
# the links that work in emacs do not work in github, and vice versa
# use python to transform from one to the other, since want to edit wiki on desktop instead of on github

import sys
import getopt
import os
import re
import glob
import pudb
import logging
import datetime

# testing a copy of a wiki in ~/Documents/Computer/Software/GithubNotes/PyConvertLinksInWikiEmacs2Github/tempDir20161022

#TODO logging is only set up when __name__=="__main__"; if want to test via unittest in convert..Test.py, need to change this 
#TODO caution with default value of folder1=os.getcwd(); this gets evaluated at start of script

#head
def remove_md_from_links_in_line(line,folder1=os.getcwd(),testLinks=False):
    '''
    [description](link.md) is replaced with [description](link) in line
    '''
    linkRegex=re.compile(r"(\[.+?\]\(.+?\.md\))")
    linkRegexNamedG=re.compile(r"(\[.+?\]\((?P<targetFile>.+?\.md)\))")
    modRegex=re.compile(r"\.md\)$")

    # pudb.set_trace()

    os.chdir(folder1)

    assert line,'No line to operate on'

    linePieces=linkRegex.split(line)
    newLinePieces=[]
    for piece in linePieces:
        if linkRegex.match(piece):
            assert linkRegexNamedG.match(piece), 'linkRegexNamedG is not matching %s' % piece
            filenameInPiece=linkRegexNamedG.match(piece).groupdict()['targetFile']
            assert filenameInPiece.endswith('.md'), 'filenameInPiece does not end with .md'
            if testLinks:
                logging.debug('Testing link %s; is it on disk?  is it in current working dir?' % filenameInPiece)
                if not os.path.exists(filenameInPiece):
                    logging.warning('%s does not exist by os.path.exists' % filenameInPiece)
                mdFiles=glob.glob("*.md")
                if not (filenameInPiece in mdFiles):
                    logging.warning('%s not found in current directory via glob.glob("*.md")' % filenameInPiece)
            redoneLink=modRegex.sub(')',piece)  # [descr](filename) where .md extension has been removed from filename
            newLinePieces.append(redoneLink)
        else:
            newLinePieces.append(piece)

    newLine=''.join(newLinePieces)
    return newLine

def convert_md_files_to_github_online_wiki_fmt(folder1=os.getcwd(),testLinks=False):
    '''
    [description](link.md) is replaced with [description](link) in all .md files in folder1 
    '''

    os.chdir(folder1)

    mdFiles=glob.glob("*.md")
    for mdFile in mdFiles:
        f1=open(mdFile,'r')
        oldLines=f1.readlines()
        f1.close()

        newLines=[]
        for line in oldLines:
            newLine=remove_md_from_links_in_line(line,folder1=folder1,testLinks=testLinks)
            newLines.append(newLine)

        f1=open(mdFile,'w')
        f1.writelines(newLines)
        f1.close()

        logging.debug('rewrote %s' % os.path.join(folder1,mdFile))

#head
def add_md_to_links_in_line(line,folder1=os.getcwd(),testLinks=False):
    '''
    [description](link) is replaced with [description](link.md) in line.
    '''

    #TODO only convert a link from [descr](link) to [descr](link.md) if link.md exists in folder1
    #TODO do not convert [descr](link.ext) to [descr](link.ext.md)

    os.chdir(folder1)

    linkRegex=re.compile(r"(\[.+?\]\(.+?\))")
    linkRegexNamedG=re.compile(r"(\[.+?\]\((?P<targetFile>.+?)\))")
    modRegex=re.compile(r"\)$")
    fileExtRegex=re.compile(r"\.\w{2,4}$")
    # http://daringfireball.net/misc/2010/07/url-matching-regex-test-data.text
    weblinkRegex=re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

    assert line,'No line to operate on'

    linePieces=linkRegex.split(line)
    newLinePieces=[]
    for piece in linePieces:
        if linkRegex.match(piece):
            assert linkRegexNamedG.match(piece), 'linkRegexNamedG is not matching %s' % piece
            filenameInPiece=linkRegexNamedG.match(piece).groupdict()['targetFile']
            if filenameInPiece.endswith('.md') or fileExtRegex.search(filenameInPiece) or weblinkRegex.match(filenameInPiece):
                newLinePieces.append(piece)
            else:
                newLinePieces.append(modRegex.sub('.md)',piece))
                filenameInPiece+='.md'
            if testLinks and filenameInPiece.endswith('.md'):
                #TODO rewrite code so that if link with .md added is not in current directory, do not add .md
                logging.debug('Testing link %s; is it on disk?  is it in current working dir?' % filenameInPiece)
                if not os.path.exists(filenameInPiece):
                    logging.warning('%s does not exist by os.path.exists' % filenameInPiece)
                mdFiles=glob.glob("*.md")
                if not (filenameInPiece in mdFiles):
                    logging.warning('%s not found in current directory via glob.glob("*.md")' % filenameInPiece)

        else:
            newLinePieces.append(piece)

        
    newLine=''.join(newLinePieces)
    return newLine

def convert_md_files_to_emacs_gfm_fmt(folder1=os.getcwd(),testLinks=False):
    '''
    [description](link) is replaced with [description](link.md) in all .md files in folder1
    '''

    os.chdir(folder1)

    mdFiles=glob.glob("*.md")
    for mdFile in mdFiles:
        f1=open(mdFile,'r')
        oldLines=f1.readlines()
        f1.close()

        newLines=[]
        for line in oldLines:
            newLine=add_md_to_links_in_line(line,folder1=folder1,testLinks=testLinks)
            newLines.append(newLine)

        f1=open(mdFile,'w')
        f1.writelines(newLines)
        f1.close()

        logging.debug('rewrote %s' % os.path.join(folder1,mdFile))

#head
#head
class CallCounted(object):
    """
    Decorator to determine number of calls for a method
    http://stackoverflow.com/questions/812477/how-many-times-was-logging-error-called
    answer by Mark Roddy 20090501
    """

    def __init__(self,method):
        self.method=method
        self.counter=0

    def __call__(self,*args,**kwargs):
        self.counter+=1
        return self.method(*args,**kwargs)

def set_up_logging(loggingLevel=None):
    global logFilename

    logLevelsDict={None:None,'debug':logging.DEBUG,'info':logging.INFO,'warning':logging.WARNING,'error':logging.ERROR,'critical':logging.CRITICAL}
    try:
        doNotLogAtOrBelow=logLevelsDict[loggingLevel]
    except:
        doNotLogAtOrBelow=None

    #http://stackoverflow.com/questions/9135936/want-datetime-in-logfile-name
    #TODO how to tell logging module to put the log file in a particular folder?
    # logFilename=datetime.datetime.now().strftime('%Y%m%d_%H%MConvertLinksMarkdownEmacsGithub.log')
    logFilename=os.path.join(origFolder,datetime.datetime.now().strftime('%Y%m%d_%H%MConvertLinksMarkdownEmacsGithub.log'))

    print 'Log file is %s' % logFilename

    logging.basicConfig(filename=logFilename,filemode="w",level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')

    logging.error=CallCounted(logging.error)
    logging.warning=CallCounted(logging.warning)

    if doNotLogAtOrBelow:
        logging.disable(doNotLogAtOrBelow) #quickly disable logging below a chosen level; see sweigart

def remove_old_logs(globPattern,N_to_keep=1):
    "Remove old .log files that match globPattern"

    try:
        prevLogL=None
        prevLogL=sorted(glob.iglob(globPattern),key=os.path.getctime)
        prevLogL.reverse()  #make sure logs are sorted newest to oldest DONE
        NOldLogs=len(prevLogL)

    except ValueError:
        logging.debug('No previous log file found (%s)' % globPattern)
        return None

    logsToDelete=prevLogL[N_to_keep:]

    if logsToDelete:
        for oldLog in logsToDelete:
            os.remove(oldLog)
            logging.debug('Deleted old log %s' % oldLog) 
    else:
        logging.debug('Number of old logs (%s) does not exceed %i; nothing deleted' % (NOldLogs,N_to_keep))

#head
def usage():

    messg1='''
    use case: using emacs to work on .md files which are for a github wiki
    script rewrites all .md files in a local folder so that links to other .md files match a format.
    default is to change from emacs github flavored format (description)[filename.md] to github website format (description)[filename]

    flags with no input argument:
    -h, --help: show this help blurb
    -e, --emacsLinks: convert .md files so that links to other .md files match emacs github flavored wiki format (add .md)
    -t, --testLinks: test if links are working; output goes in log file

    flags with input argument:
    -f, --folder:  give the folder where there are .md files to be converted
    -L, --loggingLevel: do not log at or below.  None, debug, info, warning, error, or critical.

    example call:
    python convertLinksInWikiEmacs2Github.py -e -f /home/userName/Documents
    '''
    print messg1

#head module level stuff (global)
origFolder=os.getcwd()
#head MAIN
if __name__=="__main__":

    #initialize variables that could be changed via command line inputs
    # localFolderWithWiki='/home/dad84/Documents/Computer/Software/OrgModeNotes/MyOrgModeScripts/OrgModeFileCrawler/githubWikiStart20161013'
    #this is a copy of a github wiki for testing
    localFolderWithWiki='/home/dad84/Documents/Computer/Software/GithubNotes/PyConvertLinksInWikiEmacs2Github/tempDir20161022'
    assert os.path.exists(localFolderWithWiki), 'folder %s written into script as default does not exist on filesystem' % localFolderWithWiki
    convertFun=convert_md_files_to_github_online_wiki_fmt

    loggingLevel=None
    testLinks=False
    # ---------------------------------------------------------
    #process command line inputs
    #dive into python 10.6
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hetf:L:", ["help","emacsLinks","testLinks","folder=","loggingLevel="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt,arg in opts:
        if opt in ("-h","--help"):
            usage()
            sys.exit()

        elif opt in ("-e","--emacsLinks"):
            convertFun=convert_md_files_to_emacs_gfm_fmt

        elif opt in ("-t","--testLinks"):
            testLinks=True

        elif opt in ("-f","--folder"):
            localFolderWithWiki=arg
            assert os.path.exists(localFolderWithWiki), 'folder %s supplied via command line input does not exist on filesystem' % arg

        elif opt in ("-L","--loggingLevel"):
            #user has supplied a logging level; logging will take place above this level
            loggingLevel=arg

    # pudb.set_trace()

    os.chdir(localFolderWithWiki)

    set_up_logging(loggingLevel)

    convertFun(folder1=localFolderWithWiki,testLinks=testLinks)

    print 'Run completed: log file %s contains %s errors and %s warnings\n' % (logFilename,logging.error.counter,logging.warning.counter)

    remove_old_logs(os.path.join(origFolder,'*.log'))
