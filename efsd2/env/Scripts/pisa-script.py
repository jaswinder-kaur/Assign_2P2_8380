#!c:\users\jaswi\pycharmprojects\efsd2\env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pisa==3.0.33','console_scripts','pisa'
__requires__ = 'pisa==3.0.33'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pisa==3.0.33', 'console_scripts', 'pisa')()
    )
