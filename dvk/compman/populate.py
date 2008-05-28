# -*- coding: utf-8 -*-

#===============================================================================
# FIDO2 project - database fixtures
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

from dvk.compman.models import Game, Hardware, Software, Job, Status, Anekdot, P2P, Relax

#------------------------------------------------------------------------------ 
def prepopulate(request):
    "Prepopulate DB with some data :-)"
    Status(title=u'Юзер').put()
    Status(title=u'Продвинутый Юзер').put()
    Status(title=u'Младший Программист').put()
    Status(title=u'Программист').put()
    Status(title=u'Системный Программист').put()
    Status(title=u'Сетевой Координатор').put()
    
    Job(title=u'Дворник', salary=10, need_xp=0).put()
    Job(title=u'Курьер', salary=10, need_xp=0).put()
    Job(title=u'Сборщик компов', salary=20, need_xp=32).put()
    Job(title=u'Админ в интернет-кафе', salary=50, need_xp=64).put()
    Job(title=u'Сотрудник тех. поддержки', salary=60, need_xp=64).put()
    Job(title=u'Программист в бухгалтерии', salary=80, need_xp=127).put()
    Job(title=u'Админ в АСУ завода им.Ленина', salary=80, need_xp=127).put()
    Job(title=u'Программист в банке', salary=100, need_xp=256).put()
    Job(title=u'Фрилансер', salary=120, need_xp=256).put()
    Job(title=u'Тим-лидер', salary=150, need_xp=300).put()
    Job(title=u'Свой дата-ресторе центр', salary=200, need_xp=512).put()
    Job(title=u'Своя студия веб-дизайна', salary=200, need_xp=512).put()
    Job(title=u'Своя фирма по аутсорсингу', salary=200, need_xp=512).put()
    Job(title=u'Успешный стартап', salary=1000, need_xp=1024).put()
    
    Hardware(title=u'ДВК-4', cost=150, what='pc', size=5, xp=10).put()
    Hardware(title=u'Apple IIc', cost=30000, what='pc', size=10, xp=30).put()
    Hardware(title=u'486DX4', cost=20, what='pc', size=100, xp=2).put()
    Hardware(title=u'P166MMX', cost=50, what='pc', size=166, xp=1).put()
    Hardware(title=u'Celeron 633', cost=150, what='pc', size=633, xp=2).put()
    Hardware(title=u'Pentium IV 1.5GHz', cost=300, what='pc', size=1500, xp=2).put()
    Hardware(title=u'Core 2 Duo', cost=600, what='pc', size=2000, xp=1).put()
    Hardware(title=u'Core 2 Quad', cost=950, what='pc', size=3000, xp=1).put()
    Hardware(title=u'Asus EeePC', cost=600, what='pc', size=800, xp=3).put()
    Hardware(title=u'Apple iMac', cost=1500, what='pc', size=2000, xp=1).put()
    Hardware(title=u'CRAY', cost=10000, what='pc', size=10000, xp=10).put()
    
    Hardware(title=u'2х500Mb', cost=18, what='hdd', size=1, xp=5).put()
    Hardware(title=u'IDE 20Gb', cost=30, what='hdd', size=20, xp=1).put()
    Hardware(title=u'IDE 40Gb', cost=54, what='hdd', size=40, xp=1).put()
    Hardware(title=u'SATA 160Gb', cost=89, what='hdd', size=160, xp=1).put()
    Hardware(title=u'SATA 500Gb', cost=140, what='hdd', size=500, xp=1).put()
    Hardware(title=u'RAID-5 1Tb', cost=300, what='hdd', size=1000, xp=3).put()
    
    Hardware(title=u'Модем 14.4K', cost=15, what='lan', size=15, xp=2).put()
    Hardware(title=u'Модем 28.8K', cost=30, what='lan', size=29, xp=1).put()
    Hardware(title=u'Модем 56K', cost=50, what='lan', size=56, xp=1).put()
    Hardware(title=u'ADSL модем', cost=80, what='lan', size=100, xp=1).put()
    Hardware(title=u'CDMA модем', cost=160, what='lan', size=160, xp=1).put()
    Hardware(title=u'Оптоволокно T-1', cost=400, what='lan', size=10000, xp=3).put()
    
    Software(title=u'ДЕМОС 2.10', cost=2, what='os', need_xp=100, need_power=2, size=30, xp=10).put()
    Software(title=u'MSDOS 6.22 + Win3.11', cost=30, what='os', need_xp=10, need_power=50, size=150, xp=3).put()
    Software(title=u'Windows 95', cost=70, what='os', need_xp=30, need_power=100, size=300, xp=0).put()
    Software(title=u'Windows 2000 Server', cost=250, what='os', need_xp=80, need_power=600, size=1500, xp=0).put()
    Software(title=u'Windows Vista', cost=150, what='os',  need_xp=40, need_power=1500, size=5000, xp=0).put()
    Software(title=u'Linux Slackware 3.0', cost=10, what='os', need_xp=128, need_power=100, size=3000, xp=5).put()
    Software(title=u'Linux Ubuntu', cost=30, what='os', need_xp=180, need_power=300, size=3000, xp=2).put()
    Software(title=u'Linux CENTOS 5.1', cost=50, what='os', need_xp=150, need_power=500, size=4000, xp=2).put()
    Software(title=u'Mac OS 9.0', cost=80, what='os', need_xp=80, need_power=400, size=1500, xp=1).put()
    Software(title=u'Mac OS X', cost=150, what='os', need_xp=180, need_power=2000, size=5000, xp=5).put()
    Software(title=u'OS/2 Warp', cost=20, what='os', need_xp=128, need_power=166, size=200, xp=5).put()
    Software(title=u'OS/2 Server', cost=100, what='os', need_xp=256, need_power=500, size=500, xp=5).put()
    Software(title=u'FreeBSD 8.0', cost=10, what='os', need_xp=300, need_power=1000, size=2500, xp=5).put()
    
    Software(title=u'РАПИРА', cost=2, what='soft', need_xp=100, need_power=2, size=10, xp=5).put()
    Software(title=u'Assembler', cost=15, what='soft', need_xp=20, need_power=5, size=10, xp=5).put()
    Software(title=u'Паскаль', cost=25, what='soft', need_xp=10, need_power=50, size=20, xp=1).put()
    Software(title=u'Delphi 7.0', cost=80, what='soft', need_xp=64, need_power=100, size=350, xp=2).put()
    Software(title=u'Eclipse + Java', cost=10, what='soft', need_xp=128, need_power=1000, size=500, xp=3).put()
    Software(title=u'Visual Studio NET', cost=300, what='soft', need_xp=128, need_power=1500, size=2000, xp=3).put()
    Software(title=u'Python 2.5 + Django', cost=10, what='soft', need_xp=256, need_power=1000, size=50, xp=5).put()
    Software(title=u'Google App Engine Toolkit', cost=0, what='soft', need_xp=300, need_power=1500, size=120, xp=5).put()
    
    Software(title=u'Digger', cost=3, what='games', need_power=3, size=5, xp=5).put()
    Software(title=u'Dune II', cost=20, what='games', need_power=5, size=20, xp=2).put()
    Software(title=u'Doom - Hell on the Earth', cost=50, what='games', need_power=20, size=50, xp=2).put()
    Software(title=u'StartCraft', cost=100, what='games', need_power=100, size=500, xp=3).put()
    Software(title=u'S.T.A.L.K.E.R.', cost=30, what='games', need_power=1800, size=7000, xp=3).put()
    Software(title=u'Half-Life 2', cost=60, what='games', need_power=2000, size=10000, xp=2).put()
    
    Software(title=u'Aidstest', cost=15, what='antivirus', need_power=1, size=10, xp=2).put()
    Software(title=u'Dr.Web', cost=50, what='antivirus', need_power=100, size=40, xp=1).put()
    Software(title=u'Касперский', cost=78, what='antivirus', need_power=1000, size=80, xp=0).put()
    Software(title=u'NOD 32', cost=140, what='antivirus', need_power=1000, size=100, xp=0).put()
    
    Software(title=u'Защитник Windows', cost=50, what='firewall', need_power=100, size=10, xp=1).put()
    Software(title=u'Norton Security', cost=150, what='firewall', need_power=300, size=30, xp=1).put()
    Software(title=u'Outpost Firewall', cost=230, what='firewall', need_power=600, size=50, xp=1).put()
    Software(title=u'Watch Cat', cost=500, what='firewall', need_power=1000, size=70, xp=1).put()
    
    P2P(title=u'FTP-сервер провайдера').put()
    P2P(title=u'Torrents.ru').put()
    P2P(title=u'Rapidshare.de').put()
    P2P(title=u'Яндекс.Диск').put()
    P2P(title=u'Lamer Hunter BBS').put()
    P2P(title=u"Mailoman BBS").put()
    P2P(title=u"Team #37 BBS").put()
    
    Relax(title=u'Сходить в гости', cost=5).put()
    Relax(title=u'Поганять кваку по сети', cost=10).put()
    Relax(title=u'Пойти на чатовку', cost=20).put()
    Relax(title=u'Поискать девушку', cost=30).put()
    Relax(title=u'Сходить в сауну с девушками', cost=50).put()
    Relax(title=u'Сходить в гости к знакомой девушке переустановить Windows', cost=100).put()
    
    return HttpResponse('OK!')

#------------------------------------------------------------------------------
