# -*- coding: utf-8 -*-

#===============================================================================
# FIDO2 project
# 2008-05-14: Sergeyev V.V.
# http://pythondevside.com
#===============================================================================

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'', include('dvk.compman.urls')),
)
