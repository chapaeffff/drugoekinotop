# -*- coding: utf-8 -*-

import os,sys

#путь к проекту
sys.path.insert(0, '/home/d/drimspbru/drugoekinotop/public_html')
#путь к фреймворку
sys.path.insert(0, '/home/d/drimspbru/drugoekinotop')
#путь к виртуальному окружению
sys.path.insert(0, '/home/d/drimspbru/.djangovenv/lib64/python2.7/site-packages/')
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()