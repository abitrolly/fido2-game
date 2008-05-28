# -*- coding: utf-8 -*-

#===============================================================================
# FIDO2 project views (controllers) file
# 2008-05-14: Sergeyev V.V.
# http://pythondevside.com
#===============================================================================

from google.appengine.api import users
from google.appengine.api.users import User
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
#from django.template import RequestContext

from dvk.compman.models import Game, Hardware, Software, Job, Status, Anekdot, P2P, Relax
from dvk.compman.game_day import *
from dvk.compman.ajax import *
from dvk.compman.populate import *

import time
from random import randint

#------------------------------------------------------------------------------ 
def index(request):
    "Main page"
    user = users.get_current_user()
    if user:
        return HttpResponseRedirect("/game/")
    
    content = {"user": user,}
    return render_to_response("index.html", content)

#------------------------------------------------------------------------------ 
def top_users(request):
    top = Game.all().order("-xp").fetch(50)
    content = {"top": top,}
    return render_to_response("top_users.html", content)

#------------------------------------------------------------------------------
def new_game(request):
    "Create new Game instance"
    user = users.get_current_user()
    if not user:
        auth_url = users.create_login_url("/new_game/")
        return HttpResponseRedirect(auth_url)
    
    games = Game.gql("WHERE user = :1", user)
    for game in games:
        game.delete()
    
    game = Game(user=user)
    game.put()
    
    return HttpResponseRedirect("/game/")

#------------------------------------------------------------------------------ 
def play_game(request):
    "Play game"
    user = users.get_current_user()
    if not user:
        auth_url = users.create_login_url("/game/")
        return HttpResponseRedirect(auth_url)
    
    logout_url = users.create_logout_url("/")
    
    try:
        game = Game.all().filter('user =', user)[0] #Game.gql("WHERE game.user = :1", user).fetch(1)[:0]
    except:
        game = Game(user=user)
        game.put()
    
    message = None
    if game.message:
        message = game.message
        game.message = None
        game.put()
    
    content = {
                "user": user,
                "game": game,
                "logout_url": logout_url,
                "message": message,
               }
    
    return render_to_response("game.html", content)

#------------------------------------------------------------------------------ 
def ajax_query(request, query_id):
    "Диспетчер АЯКС-запросов"
    user = users.get_current_user()
    if not user:
        return HttpResponseRedirect("/")
    
    return eval(query_id + '_data(request)')

#------------------------------------------------------------------------------ 
def populate(request):
    "Prepopulate DB with some data :-)"
    return prepopulate(request)

#------------------------------------------------------------------------------ 
def relax(request):
    "Расслабляемся"
    user = users.get_current_user()
    if not user:
        return HttpResponseRedirect("/")
    
    logout_url = users.create_logout_url("/")
    game = Game.all().filter('user =', user)[0] #Game.gql("WHERE game.user = :1", user).fetch(1)[:0]
    
    items = Relax.all().order("cost")
    
    content = {
                "user": user,
                "game": game,
                "logout_url": logout_url,
                "items": items,
               }
    
    return render_to_response("relax.html", content)

#------------------------------------------------------------------------------ 
def files_exchange(request):
    "Файлообмен"
    user = users.get_current_user()
    if not user:
        return HttpResponseRedirect("/")
    
    logout_url = users.create_logout_url("/")
    game = Game.all().filter('user =', user)[0] #Game.gql("WHERE game.user = :1", user).fetch(1)[:0]
    
    p2p = P2P.all()
    
    content = {
                "user": user,
                "game": game,
                "p2p": p2p,
                "logout_url": logout_url,
               }
    
    return render_to_response("files_exchange.html", content)

#------------------------------------------------------------------------------ 
def hacking(request):
    user = users.get_current_user()
    if not user:
        return HttpResponseRedirect("/")
    
    logout_url = users.create_logout_url("/")
    game = Game.all().filter('user =', user)[0]
    
    content = {
                "user": user,
                "game": game,
                "logout_url": logout_url,
               }
    
    if game.xp < 64:
        content["denied"]=True
    else:
        count = Game.all().count()
        targets = []
        if count > 7:
            offset = randint(0, count-7)
            items = Game.all().fetch(offset+7, offset)
        else:
            items = Game.all()
        
        for item in items:
            if item.user != game.user:
                targets.append(item)
        content["targets"] = targets

    return render_to_response("hacking.html", content)

#------------------------------------------------------------------------------ 
def attack_it(request, target_id):
    "Атакуем другого игрока"
    time.sleep(3)
    target = Game.get(target_id)
    
    content = {
            "target": target,
            }
    
    return render_to_response("ajax/attack_it.html", content)
    
#------------------------------------------------------------------------------ 
