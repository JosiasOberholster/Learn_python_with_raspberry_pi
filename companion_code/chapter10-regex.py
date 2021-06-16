import subprocess
from optparse import OptionParser
import re

parser = OptionParser()

parser.add_option("-f", "--file", dest="filename",
                  help="The file to display")
parser.add_option("-r", "--regex", dest="regex",
                  help="The regular expression to search for")

options, arguments = parser.parse_args()

if options.filename:
   p = subprocess.Popen(["cat", options.filename ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

   text = p.stdout.read().decode()
   error = p.stderr.read().decode()
else:
   test = ""
   error = "Filename not given"
      
if len(error) > 0:
   print("*****ERROR*****")
   print(error)
else:
   for line in text.splitlines():
      if not options.regex or (options.regex and re.search(options.regex, line)):
         print(line)


