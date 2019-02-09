#-*- coding: utf-8 -*-

import os, sys

#project directory
sys.path.append('/home/d/drimspb/.local/lib/python2.7/site-packages')
sys.path.append('/home/d/drimspb/drugoekino.top/public_html/mysite')

#project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

#start server

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()




#
# import os, sys
#
# #project directory
#
# sys.path.insert(0, '<полный_путь_до_каталога_с_проектом>')
# sys.path.insert(1, '<полный_путь_до_Django>')
#
# sys.path.append('/home/d/drimspb/.local/lib/python2.7/site-packages')
# sys.path.append('/home/d/drimspb/drugoekino.top/public_html/mysite')
#
# #project settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#
# #start server
#
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
#


#==это работало но не обновлялось

# import os, sys
#
# #project directory
# sys.path.append('/home/d/drimspb/.local/lib/python2.7/site-packages')
# sys.path.append('/home/d/drimspb/drugoekino.top/public_html/mysite')
#
# #project settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#
# #start server
#
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
#
