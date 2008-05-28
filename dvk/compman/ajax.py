# -*- coding: utf-8 -*-

#===============================================================================
# FIDO2 project AJAX handlers file
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

from dvk.compman.models import Game, Hardware, Software, Job, Status, Anekdot, Relax

from random import randint

#------------------------------------------------------------------------------ 
def menu_data(request):
    return render_to_response("ajax/menu_data.html", {})

#------------------------------------------------------------------------------
def hard_data(request):
    "Покупка и апгрейд железа"
    hard_pc = Hardware.all().filter('what =','pc').order("cost")
    hard_hdd = Hardware.all().filter('what =','hdd').order("cost")
    hard_lan = Hardware.all().filter('what =','lan').order("cost")
    
    content = {
                "hard_pc": hard_pc,
                "hard_hdd": hard_hdd,
                "hard_lan": hard_lan,
               }
    
    return render_to_response("ajax/hard_data.html", content)

#------------------------------------------------------------------------------
def soft_data(request):
    "Установка ОС и софта"
    user = users.get_current_user()
    game = Game.all().filter('user =', user)[0]
    
    soft_os = Software.all().filter('what =','os').filter("need_xp <", game.xp) #.order("size")
    soft_soft = Software.all().filter('what =','soft').filter("need_xp <", game.xp) #.order("size")
    soft_games = Software.all().filter('what =','games').order("cost")
    soft_antivirus = Software.all().filter('what =','antivirus').order("cost")
    soft_firewall = Software.all().filter('what =','firewall').order("cost")
    
    content = {
                "soft_os": soft_os,
                "soft_soft": soft_soft,
                "soft_games": soft_games,
                "soft_antivirus": soft_antivirus,
                "soft_firewall": soft_firewall,
               }
    
    return render_to_response("ajax/soft_data.html", content)

#------------------------------------------------------------------------------
def job_data(request):
    "Работа, работа..."
    user = users.get_current_user()
    game = Game.all().filter('user =', user)[0]
    
    job_all = Job.all().filter("need_xp <", game.xp)
    
    content = {
                "job_all": job_all,
               }
    
    return render_to_response("ajax/job_data.html", content)

#------------------------------------------------------------------------------ 
def upgrade_data(request):
    "Апгрейд железа"
    user = users.get_current_user()
    game = Game.all().filter('user =', user)[0]
    
    item_id = request.POST['id']
    item = Hardware.get(item_id)

#    eval("game." + item.what + " = item.title")
#    eval("game." + item.what + "_power = item.size")
    
    if item.what == "pc":
        game.pc = item.title
        game.pc_power = item.size
    elif item.what == "hdd":
        game.hdd = item.title
        game.hdd_power = item.size
    elif item.what == "lan":
        game.lan = item.title
        game.lan_power = item.size

    game.money -= item.cost
    game.xp += item.xp
    game.put()
    
    content = {
                "user": user,
                "game": game,
               }
    
    return render_to_response("ajax/about_user.html", content)

#------------------------------------------------------------------------------ 
def install_data(request):
    "Установка ОС и софта"
    user = users.get_current_user()
    game = Game.all().filter('user =', user)[0]
    
    item_id = request.POST['id']
    item = Software.get(item_id)
    
    if item.what == "os":
        game.os = item.title
        game.os_size = item.size
    elif item.what == "soft":
        game.soft = item.title
        game.soft_size = item.size
    elif item.what == "games":
        game.games = item.title
        game.games_size = item.size
    elif item.what == "antivirus":
        game.antivirus = item.title
    elif item.what == "firewall":
        game.firewall = item.title
        game.firewall_power = item.size

    game.money -= item.cost
    game.xp += item.xp
    game.put()
    
    content = {
                "user": user,
                "game": game,
               }
    
    return render_to_response("ajax/about_user.html", content)

#------------------------------------------------------------------------------ 
def apply_job_data(request):
    "Устройство на работу"
    user = users.get_current_user()
    game = Game.all().filter('user =', user)[0]
    
    item_id = request.POST['id']
    item = Job.get(item_id)
    game.job = item.title
    game.job_salary = item.salary
    game.put()
    
    content = {
                "user": user,
                "game": game,
               }
    
    return render_to_response("ajax/about_user.html", content)

#------------------------------------------------------------------------------ 
def get_p2p_text_data(request):
    "Произвольный текст для диалога P2P"
    user = users.get_current_user()
    game = Game.all().filter('user =', user)[0]
    
    if randint(1,10) > 7:
        text = "error" 
        return HttpResponse(text)
    
    direction = request.POST['direction']
    soft_size = randint(1, game.cool_soft/10)
    if direction == "download":
        game.cool_soft += soft_size
        if randint(1,10) > 7:
            game.xp += 2
        game.put()
    else:
        if randint(1,10) > 7:
            game.xp += 1
            game.reputation += 1
            game.put()
    
    text = u"%i файл(а) размером %iMb" % (randint(1,100), soft_size) 

    return HttpResponse(text)

#------------------------------------------------------------------------------ 
def relax_data(request):
    "Поехали в сауну!"
    user = users.get_current_user()
    game = Game.all().filter('user =', user)[0]
    cost = int(request.POST['cost'])
    game.fun += randint(1, cost)
    game.money -= cost
    game.put()
    
    return render_to_response("ajax/relax_data.html", {"game": game})

#------------------------------------------------------------------------------ 
def hacking_data(request):
    ""
    user = users.get_current_user()
    game = Game.all().filter('user =', user)[0]
    
    target_id = request.POST['id']
    what = request.POST['what']
    target = Game.get(target_id)
    
    message = u""
    
    attack = game.xp
    defence = target.xp + target.firewall_power
    if randint(1, attack) > randint(1, defence):
        if what == 'money':
            target.message = u"Ваш банковский счет был атакован неизвестным хакером!"
            if target.money > 0:
                got_money = randint(1, target.money/2)
                target.money -= got_money
                game.money += got_money
                message = u"УРА!!! На вас счет успешно перекачано $%i." % got_money
            else:
                message = u"Доступ к счету получен, но там пусто. Может перекинете ему немного ;-)"
        elif what == 'os':
            target.os = u"С дискетки загрузил MSDOS 6.22"
            target.antivirus = None
            target.firewall = None
            target.firewall_power = 0
            target.message = u"Неизвестный хакер снес вашу ОС! Грузимся с дискетки..."
            message = u"УРА!!! Удалил пару системных DLL, теперь его ждёт приятный процесс загрузки с дискеты :-D"
        elif what == 'troyan':
            target.pc = "IBM 286"
            target.pc_power = 5
            target.message = u"Вирус сжег вам материнку! Прийдется пока поработать на старом IBM 286"
            message = u"10%...25%...100% Вирус загружен. Интересно, что у него полетит первым - материнка или винт?"
        target.xp -= randint(1, 3)
        target.put()
        game.fun += randint(1, 5)
        up_xp = randint(1, 3)
        game.xp += up_xp
        game.reputation -= 1
        game.put()
        message += u" Плюс %i к опыту." % up_xp
    else:
        message = u"%s отбил атаку :-(" % target.user.nickname
    
    return HttpResponse(message)

#------------------------------------------------------------------------------ 
