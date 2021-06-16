import os
import tarfile
from optparse import OptionParser
from time import localtime
import datetime
import subprocess
import re

parser = OptionParser()

parser.add_option("-f", "--file", dest="filename",
                  help="filename to write backup to (if no option is given, backup will be used)", metavar="FILE")
parser.add_option("-p", "--path", dest="path",
                  help="path to backup (if no option is given, ~ will be used)")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                  help="print status messages to stdout")
parser.add_option("-i", "--images", action="store_true", dest="images", default=False,
                  help="backup image files")
parser.add_option("-c", "--code", action="store_true", dest="code", default=False,
                  help="backup code files")
parser.add_option("-d", "--documents", action="store_true", dest="documents", default=False,
                  help="backup document files")
parser.add_option("-a", "--all", action="store_true", dest="all", default=False,
                  help="backup all filetypes (this overrides c, d & i)")
parser.add_option("-m", "--mtime", dest="mtime", default=False,
                  help="backup files modified less than this many days ago")
parser.add_option("-r", "--regex", dest="regex",
                  help="only back up filenames that match this regex")
parser.add_option("-s", "--server", dest="server", default=False,
                  help="copy backup file to this remote point (should be an scp location)")

options, arguments = parser.parse_args()

if options.filename:
    backup_file_name = options.filename + '.tar.gz'
else:
    backup_file_name = "backup.tar.gz"

backup_tar = tarfile.open(backup_file_name, "w:gz")

file_types = {"code":[".py"], 
              "image":[".jpeg", ".jpg", ".png", ".gif"], 
              "document":[".doc", "docx", ".odt", ".rtf"]}

backup_types = []
all_types = False

if options.images:
	backup_types.extend(file_types["image"])
if options.code:
	backup_types.extend(file_types["code"])
if options.documents:
	backup_types.extend(file_types["document"])

if len(backup_types) == 0 or options.all:
	all_types = True

if options.mtime:
   try:
       mtime_option = int(options.mtime)
   except ValueError:
       print("mtime option is not a valid integar. Ignoring option")
       mtime_option = -1
else:
    mtime_option = -1

if options.path:
    if os.path.isdir(options.path):
        directory = options.path
    else:
        print("Directory not found. Using ~")
        directory = os.getenv("HOME")
else:
    directory = os.getenv("HOME")

for root, dirs, files in os.walk(directory):
    for file_name in files:
        if not options.regex or re.match(options.regex, file_name):
            name, extension = os.path.splitext(file_name)
            if (extension in backup_types) or all_types:
                modified_days = (datetime.datetime.now() - 
                                 datetime.datetime.fromtimestamp(
                                 os.path.getmtime(
                                 os.path.join(root,file_name)))).days
                if mtime_option < 0 or modified_days < mtime_option:
                    if options.verbose:
                        print("Adding ", os.path.join(root,file_name), 
                               "last modified", modified_days, "days ago")
                    backup_tar.add(os.path.join(root,file_name))

if options.server:
   subprocess.call(["scp", backup_file_name, options.server])

