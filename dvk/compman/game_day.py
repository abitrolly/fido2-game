# -*- coding: utf-8 -*-

#===============================================================================
# FIDO2 project game day's routines file
# 2008-05-14: Sergeyev V.V.
# http://pythondevside.com
#===============================================================================

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden

from dvk.compman.models import Game, Hardware, Software, Job, Status, Anekdot

from random import randint
import datetime
import time

#------------------------------------------------------------------------------ 
def game_day_data(request):
    "Прошел еще один игровой день..."
    user = users.get_current_user()
    game = Game.all().filter('user =', user)[0]
    
    game_day = int(request.POST['today_is'])
    game.game_day = game_day
    game.file_exchange -= 1
    
    if game.job:
        game.fun += randint(-7, 0)
        game.money += game.job_salary
    
    game.fun += randint(-4, 4)
    if game.games:
        game.fun += 3
    if game.fun > 150:
        game.fun = 150
    game.cool_soft = game.cool_soft + randint(10, 20)
    
    message = None
    if game.status != game.status_str():
        game.status = game.status_str()
        message = u'Поздравляем! Вас повысили до статуса "%s"' % game.status
    
    if game.message:
        message = game.message
        game.message = None
    
    viruses = False
    viruses_title = u"По диску прошло стадо слонов!"
    viruses_text = u"И вот что они сказали: где твой антивирус, чувак? ;)"
    if not game.antivirus:
        # Может - Напали вирусы? ;-)
        if randint(0, 10) > 7:
            viruses = True
            viruses_title = u"По диску прошло стадо слонов!"
            viruses_text = u"И вот что они сказали: где твой антивирус, чувак? ;)"
    else:
        pass # Может мы от них отбились...
    
    cur_time = datetime.datetime.now()
    delta = cur_time - game.tik_tac
    if delta.seconds < 10:
        viruses_title = u"Внимание! Обнаружен Читер"
        viruses_text = u"А сейчас мы тебе, злостный читер, винт отформатируем! Возможно даже циркулем :-D"
        game = Game.all().filter('user =', user)[0]
        game.status = u"Читер"
    game.put()
    
    content = {
                "user": user,
                "game": game,
                "viruses": viruses,
                "viruses_title": viruses_title,
                "viruses_text": viruses_text,
                "message": message,
               }
    
    return render_to_response("ajax/about_user.html", content)

#------------------------------------------------------------------------------ 
