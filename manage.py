#!/usr/bin/env python
import os
import sys

from updateLogin import *

if __name__ == "__main__":
    updateLogin()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
