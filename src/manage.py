#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise RuntimeError('Django is not installed or not available in this environment') from exc
    execute_from_command_line(sys.argv)
