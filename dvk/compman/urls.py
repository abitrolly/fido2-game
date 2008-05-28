# -*- coding: utf-8 -*-

#===============================================================================
# FIDO2 project URLs dispatcher
# 2008-05-14: Sergeyev V.V.
# http://pythondevside.com
#===============================================================================

from django.conf.urls.defaults import *

#------------------------------------------------------------------------------ 
urlpatterns = patterns('dvk.compman.views',
    (r"^$", "index"),
    (r'^new_game/$', 'new_game'),
    (r'^game/$', 'play_game'),
    (r'^top/$', 'top_users'),
    
    (r'^ajax_query/(?P<query_id>\w+)/$', 'ajax_query'),
    
    (r'^populate/$', 'populate'),
    
    (r'^torrents/$', 'files_exchange'),
    (r'^hacking/$', 'hacking'),
    (r'^attack/(?P<target_id>\w+)/$', 'attack_it'),
    (r'^relax/$', 'relax'),
    
)
