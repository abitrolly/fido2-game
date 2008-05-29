# -*- coding: utf-8 -*-

#===============================================================================
# FIDO2 project models declarations file
# 2008-05-14: Sergeyev V.V.
# http://pythondevside.com
#===============================================================================

# Идеи для игры:
# Можно: Написать полезную программу, Создать сайт, Завести блог 
# От опыта будет зависеть доход от этого
#
# Файлообмен
#
# Хакинг
# Приналичии некоторого опыта и если есть спец. софт для взлома (можо добыть на файлообменниках),
# можно взламывать других игроков (список доступных игроков - рандомно, 4-5 чел.).
# Чем выше опыт, тем больше шансов на взлом. Успешный взлом открывает возможности:
# - перевести деньги
# - снести софт
# - наслать вирусы
# !? - фаервол

from google.appengine.ext import db

import string 
from random import randint

#------------------------------------------------------------------------------ 
class Anekdot(db.Model):
    "Компьютерные анекдоты"
    text = db.StringProperty()
    
    def __unicode__(self):
        return self.title

#------------------------------------------------------------------------------ 
class Status(db.Model):
    "Статус: Чайник, Юзер, Программист, Хакер"
    title = db.StringProperty()

#------------------------------------------------------------------------------ 
class P2P(db.Model):
    "Файлообменная сеть класса Peer 2 Peer"
    title = db.StringProperty()

#------------------------------------------------------------------------------ 
class Job(db.Model):
    "Работа"
    title = db.StringProperty()
    salary = db.IntegerProperty(default=0)
    need_xp = db.IntegerProperty(default=0) # требуемый опыт для этой работы

#------------------------------------------------------------------------------ 
class Hardware(db.Model):
    "Железо"
    title = db.StringProperty()
    cost = db.IntegerProperty(default=10)
    what = db.StringProperty(choices=set(["pc", "hdd", "lan"])) # "ram", 
    size = db.IntegerProperty(default=100) # HDD - Gb, RAM - Mb, PC - MHz, LAN - Kbps
    
    xp = db.IntegerProperty(default=1) # на сколько увеличивается опыт Игрока при покупке этого железа 
    
    def __unicode__(self):
        return self.title

#------------------------------------------------------------------------------ 
class Software(db.Model):
    "Программы"
    title = db.StringProperty()
    cost = db.IntegerProperty(default=10)
    what = db.StringProperty(choices=set(["os", "soft", "games", "antivirus", "firewall"]))
    
    need_xp = db.IntegerProperty(default=10) # требуемый уровень опыта
    need_power = db.IntegerProperty(default=100) # требуемая мощность PC для установки этого софта
    size = db.IntegerProperty(default=100) # размер софта в Mb
    #install_time = db.IntegerProperty(default=5) #в Минутах
    
    xp = db.IntegerProperty(default=1) # на сколько увеличивается опыт Игрока при установке этого софта
    
    def __unicode__(self):
        return self.title

#------------------------------------------------------------------------------ 
class Relax(db.Model):
    "Развлечения"
    title = db.StringProperty()
    cost = db.IntegerProperty(default=5)

#------------------------------------------------------------------------------ 
class Game(db.Model):
    "Game instance"
    game_day = db.IntegerProperty(default=1) # День игры
    user = db.UserProperty()
    xp = db.IntegerProperty(default=11) # Опыт
    message = db.StringProperty(required=False)
    
    status = db.StringProperty(default=u'Юзер')
    reputation = db.IntegerProperty(default=0)
    fun = db.IntegerProperty(default=70)
    
    job = db.StringProperty(required=False)
    job_salary = db.IntegerProperty(default=0)
    
    money = db.IntegerProperty(default=200)
    
    os = db.StringProperty(default="---") #"MSDOS 6.22")
    os_size = db.IntegerProperty(default=0) # Мб
    soft = db.StringProperty(default="---")
    soft_size = db.IntegerProperty(default=0) # Мб
    games = db.StringProperty(required=False)
    games_size = db.IntegerProperty(default=0) # Мб
    antivirus = db.StringProperty(required=False)
    firewall = db.StringProperty(required=False)
    firewall_power = db.IntegerProperty(default=0) # Эффективность фаервола в %
    
    cool_soft = db.IntegerProperty(default=0) # Мб, сколько у нас есть КРУТОГО СОФТА :) 

    pc = db.StringProperty(default="---") #default="486DX4")
    pc_power = db.IntegerProperty(default=0) # мощность компьютера
    hdd = db.StringProperty(default="---")
    hdd_power = db.IntegerProperty(default=0) # размер винчестера
    lan = db.StringProperty(default=u'---') #'Модем на 2400')
    lan_power = db.IntegerProperty(default=0) # Kbps
    
    tik_tac = db.DateTimeProperty(auto_now=True)
    file_exchange = db.IntegerProperty(default=0)
    
    def __str__(self):
        return "%s - Опыт=%i; Репутация=%i" % (self.user, self.xp, self.reputation)
    
    def __unicode__(self):
        return "%s - Опыт=%i; Репутация=%i" % (self.user, self.xp, self.reputation)
    
    def status_str(self):
        if self.xp > 1024:
            return u"Сетевой Координатор"
        elif self.xp > 256:
            return u"Системный Программист"
        elif self.xp > 128:
            return u"Программист"
        elif self.xp > 64:
            return u"Младший Программист"
        elif self.xp > 32:
            return u"Продвинутый Юзер"
        else:
            return u"Юзер"

    def fun_str(self):
        if self.fun > 90:
            return "%i%%, отличное ;-)" % self.fun
        elif self.fun > 80:
            return "%i%%, отличное :-)" % self.fun
        elif self.fun > 60:
            return "%i%%, хорошее :-I" % self.fun
        elif self.fun > 50:
            return "%i%%, нормальное :-/" % self.fun
        elif self.fun > 40:
            return "%i%%, скверное :-|" % self.fun
        else:
            return "%i%%, депрессия :-(" % self.fun
    
    def hdd_free(self):
        #return  "%iMb free" % (self.hdd_power * 1024 - self.cool_soft - self.os_size)
        if self.hdd_power == 0:
            return "0"
        else:
            return  self.hdd_power * 1024 - self.cool_soft - self.os_size - self.soft_size - self.games_size
    
    def cool_soft_str(self):
        return "%iMb" % (self.cool_soft / 10)
    
    def job_str(self):
        if self.job:
            return self.job
        else:
            return '---'
    
    def get_ip(self):
        return "%i.%i.%i.%i" % (randint(170, 254), randint(0, 254), randint(0, 254), randint(0, 254))
    
    def reputation_color(self):
        if self.reputation > 0:
            return "green"
        elif self.reputation < 0:
            return "red"
        else:
            return "white"
    
    def reputation_str(self):
        if self.reputation > 0:
            return "+%i" % self.reputation
        else:
            return "%i" % self.reputation
        
#------------------------------------------------------------------------------ 
