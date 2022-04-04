import es,playerlib,gamethread,random,spe,math
from spe.games import cstrike

weapons = {
"all": ["m249","aug","sg550","ak47","m4a1","mp5navy","ump45","tmp","g3sg1","sg552","scout","awp","mac10","p90","m3","xm1014","galil","famas","glock","usp","p228","fiveseven","elite","deagle"],
"primary": ["m249","aug","sg550","ak47","m4a1","mp5navy","ump45","tmp","g3sg1","sg552","scout","awp","mac10","p90","m3","xm1014","galil","famas"],
"secondary": ["glock","usp","p228","fiveseven","elite","deagle"],
"grenades": ["smokegrenade","flashbang","hegrenade"],
"other": ["c4","knife"] }
percent = "%"

def load():
  if not es.exists('command', '_skills_reload'):es.regcmd('_skills_reload', 'wcs/wcsskills/reload')
  reload()

def reload():
  global skills,est,wcs,wcs_races,wcsusers
  import wcs.skills.skills as skills
  import wcs.est.est as est
  import wcs.wcs as wcs
  from wcs.wcsraces import RacesDB as wcs_races
  from wcs.wcsusers import userdata as wcsusers

def item_pickup(event_var):
  item = str(event_var['item']).replace("weapon_","")
  if item not in weapons["all"]:
    return
  user = int(event_var["userid"])
  player = playerlib.getPlayer(user)
  player.Color
  invisp = wcsusers.get(user,"guninvisp")
  alpha = int(255-2.55*invisp)
  gamethread.delayed(1,player.setWeaponColor(255,255,255,alpha))

def madsci_end(user,match):
  from wcs.wcs import server
  if server["round"] != match:
    return
  if es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
    return
  speed = wcsusers.get(user,"speed")
  player = playerlib.getPlayer(user)
  player.setSpeed(float(speed))
  colour = player.Color
  player.setColor(255,255,255,colour[3])
  est.slow_immune(user,0)
  est.freeze_immune(user,0)
  skills.fade(user,0,1,1,255,55,5,20)
  x,y,z = es.getplayerlocation(user)
  est.csay(user,"The Elixir of Madness wears off!")
  es.server.queuecmd("est_Effect 3 #a 0 sprites/halo01.vmt %s %s %s %s %s %s 1 20 50 200 20 20 255" % (x,y,z,x,y,z+60) )

def neve_end(user,match):
  from wcs.wcs import server
  if server["round"] != match:
    return
  if es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
    return
  est.invis_reset(user)
  skills.fade(user,0,1,1,5,55,255,20)
  x,y,z = es.getplayerlocation(user)
  est.csay(user,"No longer Invisible!")
  es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 50 10 1.5 10 50 1 50 0 255 255 3" % (x,y,z+30) )

def archimonde_end(user,match):
  from wcs.wcs import server
  if server["round"] != match:
    return
  if es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
    return
  wcs.allowed(user,"awpknifec4")
  gamethread.delayed(0.1,cstrike.giveNamedItem,(user,"weapon_awp"))
  gamethread.delayed(0.2,cstrike.giveNamedItem,(user,"weapon_knife"))
  gamethread.delayed(0.5,est.invis_reset,user)
  skills.fade(user,0,1,1,5,55,255,20)
  x,y,z = es.getplayerlocation(user)
  est.csay(user,"No longer Invisible!")
  es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 100 1 20 100 1 20 100 20 120 10" % (x,y,z+30) )

def lilith_end(user,match):
  from wcs.wcs import server
  if server["round"] != match:
    return
  if es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
    return
  level = wcsusers.get(user,"PhaseWalk")
  if not level:
    return
  wcsusers._set(user,"Phasewalk",0)
  wcsusers._set(user,"primary",0)
  wcsusers._set(user,"secondary",0)
  speed = wcsusers.get(user,"speed")
  if not speed:speed = 1.0
  player = playerlib.getPlayer(user)
  player.setSpeed(float(speed))
  wcs.allowed(user,"mp5navypistolsknifegrenades")
  gamethread.delayed(0.1,cstrike.giveNamedItem,(user,"weapon_mp5navy"))
  secondary = wcsusers.get(user,"secondary")
  gamethread.delayed(0.2,cstrike.giveNamedItem,(user,secondary))
  gamethread.delayed(0.5,est.invis_reset,user)
  gamethread.delayed(0.75,est.god,(user,0))
  gamethread.delayed(0.5,wcsusers._set(user,"regeneration",0))
  x,y,z = es.getplayerlocation(user)
  est.csay(user,"No longer Invisible!")
  es.server.queuecmd("est_effect 10 #a 0.5 sprites/lgtning.vmt %s %s %s 20 200 1 20 100 1 50 50 120 120 10" % (x,y,z+30) )

def akasha_cloud(user,match):
  from wcs.wcs import server
  if server["round"] != match:
    return
  if es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
    return
  gamethread.delayed(0.05,akasha_cloud,(user,match))
  jetpack = wcsusers.get(user,"jetpack")
  if not jetpack:
    return
  x,y,z = es.getplayerlocation(user)
  es.server.queuecmd("est_effect 7 #a 0 sprites/smoke.vmt %s %s %s 5 3" % (x,y,z) )

def shield_restore(user,value,regen):
  if es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
    return
  shield = wcsusers.get(user,"lilith")
  if shield != value:
    return
  wcsusers._set(user,"armorregeneration",regen)

def necro_revive(user,nt,x,y,z):
  es.server.queuecmd("es_xsetpos %s %s %s %s" % (user,x,y,z) )
  maxhp = wcsusers.get(user,"HPmaximum")
  maxhp *= (0.2*nt)
  player = playerlib.getPlayer(user)
  player.health = maxhp
  wcsusers._set(user,"HPmaximum",maxhp)
  es.setplayerprop(user,"CBaseEntity.m_CollisionGroup",2)
  est.god(user,0)

def circu_lobotomy(target,match,charges,user):
  from wcs.wcs import server
  if server["round"] != match:
    return
  if es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
    return
  skills.drug(target,0.2)
  es.tell(target,"#multi","#greenHit by Lobotomy")
  if charges > 1:
    gamethread.delayed(2,circu_lobotomy,(target,server["round"],charges-1,user))
  else:
    es.tell(user,"#multi","#greenThe surgery #lightgreenis complete.")
    es.tell(target,"#multi","#greenThe surgery #lightgreenis complete.")

class BaseClass(object):
  def spawn(self,event_var,entry,server):
    pass
  def death(self,event_var,entry,server):
    pass
  def player_death(self,event_var,entry,server):
    pass
  def kill(self,event_var,entry,server):
    pass
  def attack(self,event_var,entry,server):
    pass
  def hurt(self,event_var,entry,server):
    pass
  def shoot(self,event_var,entry,server):
    pass
  def jump(self,event_var,entry,server):
    pass
  def smoke(self,event_var,entry,server):
    pass
  def flash(self,event_var,entry,server):
    pass
  def grenade(self,event_var,entry,server):
    pass
  def evade(self,event_var,entry,server):
    pass
  def ultimate(self,user,entry,server):
    return False
  def ability(self,user,entry,server):
    return False

class mimicfake(object):
    def __init__(self, race, races={}):
        self.__dict__ = races

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            raise AttributeError(key)

class Undead(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"ultravision",1)
    wcsusers._set(user,"undead",1)
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill2")
    if level:
      speed = 1.06+0.03*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenUnholy Aura#lightgreen allows you to run#green %i%s #lightgreenfaster!" % (int((speed-1)*100),percent) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z) )
    level = getattr(entry,"skill3")
    if level:
      gravity = 1.0-0.07*level
      wcsusers.set(user,"gravity",gravity)
      es.tell(user,"#multi", "#greenLevitation#lightgreen allows you to jump#green %i%s #lightgreenhigher!" % (int((1-gravity)*100),percent) )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
  
  def attack(self,event_var,entry,server):
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill1")
    if level == 0: return
    dice = random.randint(1,5)
    if dice <= 3:
      return
    dmg = float(event_var["dmg_health"])
    tlevel = getattr(entry,"level")
    if tlevel >= 100:
      leech = 0.3+0.002*float(tlevel-100)
      if leech > 0.4433333333333333333333:
        leech = 0.443333333333333333333333333
      hp = int(dmg*leech)
    else:
      hp = int(dmg*(float(level)/24+0.01))
    if hp:
      user = int(event_var["userid"])
      alpha = 30+level*20
      x1,y1,z1 = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 255 0 0 %i" % (x1,y1,z1,x2,y2,z2,alpha) )
      es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 255 0 0 %i" % (x1,y1,z1+40,x2,y2,z2+40,alpha) )
      playerlib.getPlayer(attacker).health += hp
      est.csay(attacker,"Drained %i hitpoints" % hp)
  
  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill4")
    if getattr(entry,"level") > 400:
      dice = 1
    else:
      dice = random.randint(1,10)
    if level < dice:
      return
    skills.suicidebomb(user,150+10*level,65+15*level)

class Human(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill1")
    if level:
      tlevel = getattr(entry,"level")
      if tlevel >= 100:
        invisp = 65+1*int((tlevel-100)/11)
        if invisp > 70:
          invisp = 70
      else:
        invisp = 20+level*5
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#greenInvisibility #lightgreengrants you#green %i #lightgreenpercent invisibility" % invisp )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
    level = getattr(entry,"skill2")
    if level:
      hp = level*5+10
      es.tell(user,"#multi", "#greenDevotion Aura#lightgreen provides a#green %i #lightgreenhealth bonus!" % hp )
      wcsusers.set(user,"HPmaximum",hp+100)
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill3")
    dice = random.randint(1,36)
    if dice > level:
      return
    attacker = int(event_var["attacker"])
    user = int(event_var["userid"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    if skills.freeze(user,1):
      est.csay(user,"frozen by %s" % attackername)
      est.csay(attacker,"froze %s" % username)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 11 #a 0 sprites/lgtning.vmt %s %s %s 1 2.3 90" % (x,y,z) )
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if level == 0:return
    wcs.evasion_set(user,"fallresist",95,None)
    skills.fade(user,0,2,1.5,0,0,0,247)
    gamethread.delayed(3,wcs.evasion_set,(user,"fallresist",0,None))
    skills.teleport(user,600+75*level)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 7 #a 0 sprites/smoke.vmt %s %s %s 40 3" % (x,y,z) )

class Orc(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    if not server["gamestarted"]:
      dice = random.randint(1,10)
      level = getattr(entry,"skill3")
      if level >= dice:
        wcsusers._set(user,"vengeance",1)
        es.tell(user,"#multi", "#greenReincarnation#lightgreen will respawn you this round!")
      else:
        wcsusers._set(user,"vengeance",0)
        es.tell(user,"#multi", "#greenReincarnation#lightgreen failed and#green won't#lightgreen respawn you!")
    else:
      wcsusers._set(user,"vengeance",0)
    tlevel = getattr(entry,"level")
    if tlevel < 100:
      return
    speed = 1.1+0.002*(tlevel-100)
    if speed > 1.2:
      speed = 1.2
    wcsusers.set(user,"speed",speed)

  def attack(self,event_var,entry,server):
    weapon = event_var["weapon"]
    if weapon in weapons["grenades"]:
      level = getattr(entry,"skill3")
      if not level:
        return
      user = int(event_var["userid"])
      attacker = int(event_var["attacker"])
      dmg = float(event_var["dmg_health"])
      #damage = int(dmg/3.2*level)
      damage = int((40 + dmg)*(level/3.2))
      dmg = skills.dealdamage(attacker,user,damage)
      if dmg < 0:
        es.tell(user,"#multi", "#green%s#lightgreenhas resisted your crit nade")
        return
      if dmg < damage:
        es.tell(user,"#multi", "#green%s#lightgreenhas resisted your crit nade")
      dice = random.randint(1,6)
      if dice == 1:est.playplayer(user,"weapons\explode3.wav")
      elif dice == 2:est.playplayer(user,"weapons\explode4.wav")
      elif dice == 3:est.playplayer(user,"weapons\explode5.wav")
      elif dice == 4:est.playplayer(user,"weapons\mortar\mortar_explode1.wav")
      elif dice == 5:est.playplayer(user,"weapons\mortar\mortar_explode2.wav")
      elif dice == 6:est.playplayer(user,"weapons\mortar\mortar_explode3.wav")
      attackername = event_var["es_attackername"]
      username = event_var["es_username"]
      es.tell(user,"#multi", "#greenCritical Grenade#lightgreen from#green %s #lightgreenunleashes#green %i + %i #lightgreendamage unto you!" % (attackername,dmg,damage) )
      es.tell(attacker,"#multi", "#greenCritical Grenade#lightgreen unleashes#green %i + %i #lightgreendamage to#green %s #lightgreen!" % (dmg,damage,username) )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 11 #a 0 sprites/crystal_beam1.vmt %s %s %s 0.7 3 200" % (x,y,z+20) )
      return
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,6)
    if dice != 1:
      return
    level = getattr(entry,"skill1")
    if not level:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = float(event_var["dmg_health"])
    damage = int(dmg*(0.2*float(level)+0.4))
    dmg = skills.dealdamage(attacker,user,damage)
    if not dmg:
      return
    est.csay(user,"Took +%i damage!" % dmg)
    est.csay(attacker,"+%i damage!" % dmg)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 20 200 20 255" % (x1,y1,z1+40,x2,y2,z2+40) )

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    respawn = wcsusers.get(user,"vengeance")
    if respawn == 0:
      return
    tlevel = getattr(entry,"level")
    if tlevel < 125:
      hp = 100
    else:
      hp = 100+int((tlevel-125)/2.46)
    if hp > 125:
      hp = 125
    skills.respawn(user,1,hp)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if level == 0:return
    if not skills.chainlightning(user,32,200+50*level,int(2+level/4)):
      return False

class NightElf(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"ultravision",2)
    level = getattr(entry,"skill1")
    if level:
      chance = 6+3*level
      wcs.evasion_set(user,"dodge",chance,None)
      es.tell(user,"#multi", "#greenEvasion#lightgreen gives you#green %i%s #lightgreenchance to evade." % (chance,percent) )
    tlevel = getattr(entry,"level")
    if tlevel < 100:
      return
    chance = 10+10*int((tlevel-100)/11)
    if chance > 60:
      chance = 60
    wcsusers._set(user,"trueshot",chance)
    wcsusers._set(user,"pierceshot",chance)

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,3)
    if dice != 1:
      return
    level = getattr(entry,"skill1")
    if not level:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = float(event_var["dmg_health"])
    damage = int(dmg*(0.05*float(level)+0.2))
    dmg = skills.dealdamage(attacker,user,damage)
    if dmg > 0:
      est.csay(user,"Took +%i damage" % dmg)
      est.csay(attacker,"+%i damage" % dmg)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 200 20 20 255" % (x1,y1,z1+40,x2,y2,z2+40) )


  def hurt(self,event_var,entry,server):
    level = getattr(entry,"skill2")
    dice = random.randint(1,13)
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = float(event_var["dmg_health"])
    damage = int(dmg/3)
    dmg = skills.dealdamage(user,attacker,damage)
    est.csay(user,"Dealt %i Mirror Damage!" % dmg)
    est.csay(attacker,"Took %i Mirror Damage!" % dmg)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/purpleglow1.vmt %s %s %s %s %s %s 1 10 10 20 200 200 255" % (x1,y1,z1+20,x2,y2,z2+20) )
  
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if level:
      skills.entanglingroots(user,200+50*level,5,int(1+level/4))

class BloodMage(BaseClass):
  def spawn(self,event_var,entry,server):
    if server["gamestarted"]:
      return
    level = getattr(entry,"skill1")
    dice = random.randint(1,7)
    num = 0
    if level < dice:
      return
    if level == 6 and dice > 4:
      num += 1
    num += 1
    user = int(event_var["userid"])
    userteam = int(event_var["es_userteam"])
    wcs.phoenix_add(userteam,num)
    es.tell(user,"#multi", "#greenPhoenix#lightgreen can now ressurect#green %i #lightgreenplayers."%num)
      
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    dice = random.randint(1,3)
    if dice == 1:
      level = getattr(entry,"skill2")
      if level:
        time = 0.25*level
        skills.drug(user,time)
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 20 0 50 255 255 150" % (x1,y1,z1+20,x2,y2,z2+60) )
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 20 0 50 255 255 150" % (x1,y1,z1+60,x2,y2,z2+20) )
        es.tell(user,"#multi", "#greenBanished#lightgreen by#green %s#lightgreen!" % attackername )
        es.tell(attacker,"#multi", "#greenBanished %s #lightgreenfor#green %s seconds#lightgreen!" % (username,time) )
    dice = random.randint(1,3)
    if dice == 1:
      level = getattr(entry,"skill3")
      if level:
        cash = 20+level*30
        Person = playerlib.getPlayer(user)
        Player = playerlib.getPlayer(attacker)
        money = int(Person.cash)
        if money > 0:
          if cash > money:
            cash = money
          Player.cash += cash
          Person.cash -= cash
          x1,y1,z1 = es.getplayerlocation(user)
          x2,y2,z2 = es.getplayerlocation(attacker)
          es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 255 255 0 255" % (x1,y1,z1+40,x2,y2,z2+40) )
          es.tell(user,"#multi", "#lightgreenLost#green $%i #lightgreento#green %s" % (cash,attackername) )
          es.tell(attacker,"#multi", "#greenSiphon Mana#lightgreen robs#green $%i #lightgreenoff#green %s" % (cash,username) )
    dice = random.randint(1,20)
    level = getattr(entry,"skill4")
    if level < dice:
      return
    time = 0.5+0.5*level
    skills.burn(attacker,user,time)
    dmg = skills.dealdamage(attacker,user,int(time*5))
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 30 30 255 0 0 150" % (x1,y1,z1+10,x2,y2,z2+10) )
    es.tell(user,"#multi", "#green %s #lightgreenhits you with#green Flame Strike#lightgreen!" % attackername )
    es.tell(attacker,"#multi", "#green Flame Strike#lightgreen burns#green %s" % username )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level == 0:
      return
    player = playerlib.getPlayer(user)
    money = int(player.cash)
    if money < 100:
      es.tell(user,"#multi", "#lightgreenNot enough mana, need #green$100#lightgreen to cast Curing Ritual")
      return False
    hp = 13+level*2
    player.cash -=  100
    player.health += hp
    es.tell(user,"#multi", "#greenCuring Ritual: #lightgreenSacrificed#green 100 Mana#lightgreen to gain#green %i HP." % hp )
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/purpleglow1.vmt %s %s %s 4 2 255" % (x,y,z+50) )

class Archmage(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"jetpack",0)
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill2")
    if level:
      speed = 1+level*0.05
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenBroom of Velocity#lightgreen allows you to run#green %i percent#lightgreen faster!" % int((speed-1)*100) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z) )
    dice = random.randint(1,3)
    level = getattr(entry,"skill3")
    if level < dice:
      return
    player = playerlib.getPlayer(user)
    est.removeweapon(user,2)
    gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_deagle"))
    gamethread.delayed(2,player.setClip,("weapon_deagle",28))
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )
    if server["round"] < 3:
      es.tell(user,"#multi", "#greenWeapon of the Sorcerer#lightgreen provides enchanted#green Deagle")
      return
    es.tell(user,"#multi", "#greenWeapon of the Sorcerer#lightgreen provides enchanted#green M4A1#lightgreen and #greenDeagle")
    gamethread.delayed(0,cstrike.giveNamedItem,args=(user,"weapon_m4a1"))
    if level > 3:
      ammo = 5*level+15
    else:
      ammo = 30
    gamethread.delayed(2,player.setClip,("weapon_m4a1",ammo))

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,4)
    if dice != 1:
      return
    level = getattr(entry,"skill1")
    if not level:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    time = 3+0.5*level
    skills.shake(user,time,20,100)
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    est.csay(user,"%s shook you!" % attackername)
    est.csay(attacker,"Shook %s!" % username)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 0 255 0 255" % (x1,y1,z1,x2,y2,z2) )
    
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if not level:
      return
    player = playerlib.getPlayer(user)
    frozen = player.freeze
    if frozen:
      est.csay(user,"You are frozen!")
      return False
    hp = 4+level
    jetpack = wcsusers.get(user,"jetpack")
    if not jetpack:
      wcsusers.set(user,"jetpack",1)
      player.health += hp
      est.csay(user,"Flying with +%i health!" % hp )
    else:
      wcsusers.set(user,"jetpack",0)
      est.csay(user,"No longer flying, lost the +%i health!" % hp)
      if player.health > hp:
        player.health -= hp
      else:
        player.health = 1
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 60 100 0.8 0 255 255 255 1" % (x,y,z) )

class Warden(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill2")
    dice = random.randint(1,5)
    if level >= dice:
      wcsusers._set(user,"ulti_immunity",1)
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 40 2 10 10 1 0 255 100 255 1" % (x,y,z) )
      es.tell(user,"#multi", "#greenBlink#lightgreen grants#green Ultimate Immunity#lightgreen.")
    if server["gamestarted"]:
      wcsusers._set(user,"vengeance",0)
      return
    wcsusers._set(user,"vengeance",1)
    level = getattr(entry,"skill1")
    dice = random.randint(1,10)
    if level < dice:
      es.tell(user,"#multi", "#greenMole Failed#lightgreen!")
      return
    gamethread.delayed(1,skills.infiltrate,(user,1))
    es.server.queuecmd("est_effect 11 #a 0 sprites/glow.vmt %s %s %s 2 1 100" % (x,y,z) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill3")
    dice = random.randint(1,10)
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = skills.dealdamage(attacker,user,10)
    est.csay(user,"Took %i dmg from Shadow Strike" % dmg )
    est.csay(attacker,"Shadow Strike deals +%i dmg!" % dmg )
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_effect 3 #a 0 sprites/glow.vmt %s %s %s %s %s %s 0.5 10 10 255 255 0 255" % (x1,y1,z1+20,x2,y2,z2+20) )

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    respawn = wcsusers.get(user,"vengeance")
    if not respawn:
      return
    level = getattr(entry,"skill4")
    hp = random.randint(1,25)+75+level*5
    wcs.reincarnation(user)
    wcs.respawning(user)
    es.delayed(2,"est_respawn %s" % user)
    es.delayed(2.1,"est_god %s 1" % user)
    es.delayed(2.1,"est_health %s = %i" % (user,hp) )
    es.delayed(2.1,"est_armor %s = 100 1" % user)
    es.delayed(2.75,"est_god %s 0" % user)
    x,y,z = es.getplayerlocation(user)
    es.tell(user,"#multi", "#greenVengeance#lightgreen respawns you with#green %i hitpoints#lightgreen!" % hp)
    es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 2 40 10 200 255 5 255" % (x,y,z,x,y,z+150) )
    
class Crypt(BaseClass):
  def spawn(self,event_var,entry,server):
    level = getattr(entry,"skill2")
    if not level:
      return
    user = int(event_var["userid"])
    armour = 100+20*level
    est.armor(user,"=",armour,1)
    es.tell(user,"#multi", "#greenSpiked Carapace#lightgreen provided you with#green %i Armor#lightgreen!" % armour)

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    dice = random.randint(1,20)
    level = getattr(entry,"skill1")
    if level >= dice:
      skills.shake(user,1,10,100)
      est.physpush(user,0,0,350)
      es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 5 10 25 0 255 200" % (x1,y1,z1+20,x2,y2,z2+20) )
      es.tell(attacker,"#multi", "#greenImpaled %s" % username )
      es.tell(user,"#multi", "#greenImpaled#lightgreen by#green %s" % attackername )
    dice = random.randint(1,15)
    level = getattr(entry,"skill3")
    if level >= dice:
      dmg = skills.dealdamage(attacker,user,level*3)
      es.tell(attacker,"#multi", "#lightgreenYour#green Carrion Beetles#lightgreen hit#green %s #lightgreenfor#green %i #lightgreendamage!" % (username,dmg) )
      es.tell(user,"#multi", "#green%s's Carrion Beetles#lightgreen hit you for#green %i #lightgreendamage!" % (attackername,dmg) )
      es.server.queuecmd("est_effect 3 #a 0 sprites/yellowflare.vmt %s %s %s %s %s %s 1 5 5 55 90 255 100" % (x1,y1,z1,x2,y2,z2) )

  def hurt(self,event_var,entry,server):
    level = getattr(entry,"skill2")
    dice = random.randint(1,12)
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = float(event_var["dmg_health"])
    damage = int(dmg/5)
    dmg = skills.dealdamage(user,attacker,damage)
    est.csay(user,"Dealt %i Mirror Damage!" % dmg)
    est.csay(attacker,"Took %i Mirror Damage!" % dmg)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/yellowflare.vmt %s %s %s %s %s %s 1 5 5 50 0 255 200" % (x1,y1,z1+20,x2,y2,z2+20) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if not level:
      return
    users = []
    myteam = es.getplayerteam(user)
    for person in es.getUseridList():
      if es.getplayerprop(person, 'CBasePlayer.pl.deadflag'):
        continue
      team = es.getplayerteam(person)
      if team == myteam:
        continue
      users.append(person)
  
    if len(users) == 0:
      es.tell(user,"#multi","#greenLocust Swarm#lightgreen has nobody to target!")
      return False
    target = random.choice(users)
    hisname = es.getplayername(target)
    immune = wcsusers.get(target,"ulti_immunity")
    if immune:
      es.tell(user,"#multi","#greenLocust Swarm#lightgreen is blocked by #green%s#lightgreen!" % hisname)
      return
    damage = 5+5*level
    dmg = skills.dealdamage(user,target,damage)
    skills.shake(target,1,10,10)
    player = playerlib.getPlayer(user)
    hp = player.health
    maxhp = wcsusers.get(user,"HPmaximum")+100
    heal = hp+dmg
    if heal > maxhp:
      heal = maxhp
    player.health = heal
    myname = es.getplayername(user)
    es.tell(user,"#multi","#greenLocust Swarm#lightgreen hits#green %s #lightgreenfor#green %i damage#lightgreen and you heal#green %i hitpoints#lightgreen!" % (hisname,dmg,dmg) )
    es.tell(target,"#multi","#lightgreenLost#green %i hp#lightgreen to #greenLocust Swarm#lightgreen from#green %s" % (dmg,myname) )
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 3 60 100 0.8 0 200 100 200 1" % (x,y,z+40) )
    
class Succubus(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    skulls = wcsusers.get(user,"skulls")
    if skulls:
      es.tell(user,"#multi","#lightgreenYou have colleceted#green %i#lightgreen skulls!" % skulls)
      level = getattr(entry,"skill3")
      if level:
        hp = skulls*(level+1)
        if hp > 80:
          hp = 80
        dice = random.randint(1,5)
        cash = skulls*(level*5+dice)
        player = playerlib.getPlayer(user)
        player.health += hp
        player.cash += cash
        es.tell(user,"#multi", "#greenTotem Incantation#lightgreen provides#green +%iHP#lightgreen and#green $%i #lightgreen!" % (hp,cash) )
        wcsusers.set(user,"HPmaximum",hp+100)
        x,y,z = es.getplayerlocation(user)
        es.server.queuecmd("est_Effect 11 #a 0 sprites/xfireball3.vmt %s %s %s 4 2 255" % (x,y,z+15) )
    level = getattr(entry,"skill4")
    if not level:
      return
    longjump = 0.5*float(level)
    wcsusers._set(user,"longjump",longjump)
    es.tell(user,"#multi","#greenAssault Tackle#lightgreen grants you#green %i percent#lightgreen longer jumps." % (int(longjump*100) ) )
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 30 100 0.8 255 100 100 255 1" % (x,y,z) )
  
  def attack(self,event_var,entry,server):
    damage = float(event_var["dmg_health"])
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dice = random.randint(1,3)
    dmg = 0
    if dice == 1:
      level = getattr(entry,"skill2")
      if level:
        skulls = wcsusers.get(attacker,"skulls")+1
        wcsusers._set(attacker,"skulls",skulls)
        dmg = int(damage*(float(level)*0.1+0.4))
        if event_var["es_userhealth"] > 0:
          dmg = skills.dealdamage(attacker,user,dmg)
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 255 200 0 255" % (x1,y1,z1+10,x2,y2,z2+10) )
        es.tell(attacker,"#multi", "#greenFlame Strike#lightgreen deals #green+%i DMG#lightgreen and you gain a #greenSkull#lightgreen!" % dmg )
    if event_var["es_userhealth"] < dmg:
      return
    if event_var["weapon"] != "knife":
      return
    level = getattr(entry,"skill1")
    if not level:
      return
    dmg = int(damage*(float(level)*0.1+0.4))
    dmg = skills.dealdamage(attacker,user,dmg)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/purpleglow1.vmt %s %s %s 2 4 255" % (x,y,z+50) )
    es.tell(attacker,"#multi", "#greenDaemonic Knife#lightgreen deals#green +%i #lightgreendamage!" % dmg )
    es.tell(user,"#multi", "#greenDaemonic Knife#lightgreen hits you with#green +%i #lightgreendamage!" % dmg )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    skulls = wcsusers.get(user,"skulls")
    if skulls < level:
      es.tell(user,"#multi", "#lightgreenNot enough skulls#green need #green%i#lightgreen more" % (level-skulls) )
      return False
    skulls -= level
    wcsusers._set(user,"skulls",skulls)
    heal = level*10
    player = playerlib.getPlayer(user)
    hp = player.health
    maxhp = wcsusers.get(user,"HPmaximum")+100
    health = hp+heal
    if health > maxhp:
      health = maxhp
    player.health = health
    gravity = 0.9-float(level)*0.1
    wcsusers.set(user,"gravity",gravity)
    invisp = 20*level
    player.setColor(140,140,140,invisp)
    wcsusers._set(user,"invisp",invisp)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/yelflare1.vmt %s %s %s 2 2 255" % (x,y,z+40) )
    es.tell(user,"#multi", "#lightgreenYou have#green Transformed#lightgreen at the cost of#green %i #lightgreenskulls! You have#green %i #lightgreenskulls remaining." % (level,skulls) )
    
class FlamePred(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"ultravision",1)
    level = getattr(entry,"skill1")
    if level:
      hp = level*5+20
      wcsusers.set(user,"HPmaximum",hp+100)
      speed = 1.1+0.075*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenBerserk#lightgreen provides#green %i #lightgreenhitpoints and#green %i%s #lightgreenfaster speed." % (hp,int((speed-1)*100),percent) )
    level = getattr(entry,"skill2")
    if level:
      invisp = 40+10*level
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#greenCloak of Invisibility#lightgreen grants you#green %s%s #lightgreeninvisibility." % (invisp,percent) )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
    level = getattr(entry,"skill3")
    if level:
      gravity = 0.8-0.1*level
      wcsusers.set(user,"gravity",gravity)
      es.tell(user,"#multi", "#greenLevitation#lightgreen allows you to jump#green %i%s #lightgreenhigher!" % (int((1-gravity)*100),percent) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] != "knife":
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    level = getattr(entry,"skill4")
    dice = random.randint(1,11)
    if level > dice:
      est.dropweapon(user,1)
      es.tell(user,"#multi","#greenDisarmed#lightgreen by#green %s" % attackername)
      es.tell(attacker,"#multi","#greenDisarmed %s" % username)
    level = getattr(entry,"skill5")
    dice = random.randint(1,12)
    if level > dice:
      time = 1.5+0.5*level
      damage = int(time*5)
      dmg = skills.dealdamage(attacker,user,damage)
      skills.burn(attacker,user,time)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 11 #a 0 sprites/purpleglow1.vmt %s %s %s 2 2 255" % (x,y,z+50) )
      es.tell(attacker,"#multi","#greenBurning Blade#lightgreen strikes#green %s" % username)
      es.tell(user,"#multi", "#greenBurning Blade#lightgreen from#green %s #lightgreenstrikes you!" % attackername)

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill6")
    dice = random.randint(1,6)
    if level < dice:
      return
    skills.suicidebomb(user,200+10*level,125+15*level)
      
class ElvishEnchanter(BaseClass):
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)    
    dice = random.randint(1,3)
    if dice == 1:
      level = getattr(entry,"skill1")
      if level:
        dmg = float(event_var["dmg_health"])
        damage = int(dmg*(0.1*float(level)))
        dmg = skills.dealdamage(attacker,user,damage)
        if dmg:
          est.csay(user,"Took +%i damage!" % dmg)
          est.csay(attacker,"+%i damage!" % dmg)
          es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 20 200 20 255" % (x1,y1,z1+40,x2,y2,z2+40) )
    dice = random.randint(1,12)
    level = getattr(entry,"skill3")
    if level >= dice:
      dmg = int(float(level+1)/2)
      if skills.poisonstart(attacker,user,dmg,5):
        es.tell(attacker,"#multi","#LightgreenYou have poisoned#green %s #Lightgreendealing#Green %i #Lightgreendamage over 5s seconds!" % (event_var["es_username"],dmg*5))
        es.tell(user,"#multi","#LightgreenYou have poisoned by#green %s #Lightgreen!" % event_var["es_attackername"] )
        es.server.queuecmd("est_Effect 3 #a 0 sprites/greenspit1.vmt %s %s %s %s %s %s 3 5 9 155 155 155 255" % (x1,y1,z1+35,x2,y2,z2+35) )
      else:
        es.tell(attacker,"#multi","#LightgreenYou have refreshed poison on#green %s #Lightgreen." % event_var["es_username"])

  def hurt(self,event_var,entry,server):
    level = getattr(entry,"skill2")
    dice = random.randint(1,12)
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = float(event_var["dmg_health"])
    damage = int(dmg/4)
    team = int(event_var["es_userteam"])
    if team == 2:
      est.health("#t","+",damage)
    elif team == 3:
      est.health("#ct","+",damage)
    est.csay(user,"All teammates got %i hitpoints!" % damage)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if level == 0:return
    skills.chainhealing(user,150+50*level,5,3*level)
    
class Keeper(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    player = playerlib.getPlayer(user)
    gamethread.delayed(2,est.clip_set,(user,2,40))
    est.armor(user,"=",100,1)
    es.tell(user,"#multi", "#lightgreenYou spawned with #green100 Armor#lightgreen and with #green40 bullets#lightgreen in your pistol!")
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill3")
    if level:
      longjump = 0.2*float(level)
      wcsusers._set(user,"longjump",longjump)
      es.tell(user,"#multi","#greenNature's Gift#lightgreen grants you#green %i%s #lightgreenlonger jumps." % (int(longjump*100),percent ) )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 30 100 0.8 255 100 100 255 1" % (x,y,z) )
    level = getattr(entry,"skill4")
    if level:
      hp = 2+level
      maxhp = 95+level*5
      wcsusers.set(user,"HPmaximum",hp+100)
      skills.regenerationstart(user,hp,6,0,150,400,1.0)
    if server["round"] < 3:
      return
    dice = random.randint(1,4)
    level = getattr(entry,"skill1")
    if level < dice:
      return
    gamethread.delayed(0,cstrike.giveNamedItem,args=(user,"weapon_m4a1"))
    if level > 5:
      ammo = 5*level+5
    else:
      ammo = 30
    es.tell(user,"#multi", "#greenForce of nature#lightgreen provides#green %i clip M4A1#lightgreen." % ammo)
    gamethread.delayed(2,player.setClip,("weapon_m4a1",ammo))

  def hurt(self,event_var,entry,server):
    level = getattr(entry,"skill2")
    dice = random.randint(1,13)
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = float(event_var["dmg_health"])
    damage = int(dmg/3)
    dmg = skills.dealdamage(user,attacker,damage)
    est.csay(user,"Dealt %i Mirror Damage!" % dmg)
    est.csay(attacker,"Took %i Mirror Damage!" % dmg)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/purpleglow1.vmt %s %s %s %s %s %s 1 10 10 20 200 150 255" % (x1,y1,z1+20,x2,y2,z2+20) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level == 0:return
    if not skills.hinderingroots(user,550,5,0.8-float(level)*0.025,float(level)/4+1):
      return False

class MadSci(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill2")
    if level:
      hp = level*10
      es.tell(user,"#multi", "#greenElixir of Life#lightgreen provides a#green %i #lightgreenhealth bonus!" % hp )
      wcsusers.set(user,"HPmaximum",hp+100)
    level = getattr(entry,"skill4")
    if level:
      gravity = 1.0-0.1*level
      wcsusers.set(user,"gravity",gravity)
      es.tell(user,"#multi", "#greenElixir of Feathers#lightgreen allows you to jump#green %i%s #lightgreenhigher!" % (int((1-gravity)*100),percent) )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 200 200 1" % (x,y,z) )
    level = getattr(entry,"skill6")
    if level:
      if level == 5:
        count = 3
      if level < 5:
        count = 2
      if level < 3:
        count = 1
      wcsusers._set(user,"potions",count)
      es.tell(user,"#multi", "#lightgreenYou have brewed#green %i Elixirs of Rejuvination#lightgreen to use!" % count )
    else:
      wcsusers._set(user,"potions",0)
  
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    username = event_var["es_username"]
    attackername = event_var["es_attackername"]
    dice = random.randint(1,4)
    if dice == 1:
      level = getattr(entry,"skill1")
      if level:
        time = 0.5+0.5*float(level)
        skills.drug(user,time)
        dmg = skills.dealdamage(attacker,user,int(time*5))
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 30 30 255 0 0 150" % (x1,y1,z1+10,x2,y2,z2+10) )
        es.tell(user,"#multi", "#green%s #lightgreenhits you with#green Flame Strike#lightgreen!" % attackername )
        es.tell(attacker,"#multi", "#greenFlame Strike#lightgreen burns#green %s" % username )
    dice = random.randint(1,3)
    if dice == 1:
      level = getattr(entry,"skill3")
      if level:
        time = 3+0.5*float(level)
        skills.shake(user,time,20,100)
        attackername = event_var["es_attackername"]
        username = event_var["es_username"]
        est.csay(user,"%s shook you!" % attackername)
        est.csay(attacker,"Shook %s!" % username)
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 0 255 0 255" % (x1,y1,z1,x2,y2,z2) )

  def ability(self,user,entry,server):
    level = getattr(entry,"skill6")
    if not level:
      return
    potions = wcsusers.get(user,"potions")
    if not potions:
      es.tell(user,"#multi", "#green#lightgreenYou have no more potions!")
      return False
    potions -= 1
    wcsusers._set(user,"potions",potions)  
    player = playerlib.getPlayer(user)
    hp = player.health
    maxhp = wcsusers.get(user,"HPmaximum")
    dmg = int(float(maxhp-hp)/4)
    if (hp >= maxhp) or (dmg <= 0):
      es.tell(user,"#multi", "#lightgreenThe#green Elixir of Rejuvination#lightgreen had no effect; you have#green %i#lightgreen potions left!" % potions)
      return
    heal = hp+dmg
    if heal > maxhp:
      heal = maxhp
    player.health = heal
    es.tell(user,"#multi", "#lightgreenThe#green Elixir of Rejuvination#lightgreen heals #green%i#lightgreenHP,;you have#green %i#lightgreen potions left!" % (dmg,potions) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    time = 2+level
    gamethread.delayed(time,madsci_end,(user,server["round"]))
    speed = wcsusers.get(user,"speed")
    player = playerlib.getPlayer(user)
    player.setSpeed(speed*2)
    colour = player.Color
    player.setColor(255,0,0,colour[3])
    skills.fade(user,5,2,0,255,1,1,20)
    est.slow_immune(user,1)
    est.freeze_immune(user,1)
    x,y,z = es.getplayerlocation(user)
    es.tell(user,"#multi", "#lightgreenEnraged by the#green Elixir of Madness#lightgreen you run #green200%s #lightgreenfaster for#green %i#lightgreenseconds!" % (percent,time) )
    es.server.queuecmd("est_Effect 3 #a 0 sprites/halo01.vmt %s %s %s %s %s %s 1 20 50 200 20 20 255" % (x,y,z,x,y,z+60) )

class RPGrace(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill1")
    if level:
      hp = level*5
      es.tell(user,"#multi", "#greenGreater Health#lightgreen provides a#green %i #lightgreenhealth bonus!" % hp )
      wcsusers.set(user,"HPmaximum",hp+100)
    level = getattr(entry,"skill2")
    if level:
      longjump = 0.1*float(level)+0.4
      wcsusers._set(user,"longjump",longjump)
      es.tell(user,"#multi","#greenLongjump#lightgreen grants you#green %i%s #lightgreenlonger jumps." % (int(longjump*100),percent ) )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 30 100 0.8 255 100 100 255 1" % (x,y,z) )
    level = getattr(entry,"skill5")
    if level:
      invisp = 20+level*5
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#greenInvisibility #lightgreengrants you#green %i #lightgreenpercent invisibility" % invisp )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 100 1 20 100 1 20 100 20 120 10" % (x,y,z) )
  
  def attack(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    username = event_var["es_username"]
    attackername = event_var["es_attackername"]
    level = getattr(entry,"skill3")
    if level:
      dmg = float(event_var["dmg_health"])
      player = playerlib.getPlayer(attacker)
      health = player.health
      maxhp = wcsusers.get(attacker,"HPmaximum")
      if (health < maxhp):
        hp = int(dmg*(float(level)/32))
        diff = maxhp-health
        if hp > diff:
          hp = diff
      else:
        hp = int(dmg*(float(level)/64))
        if hp > 10:
          hp = 10
      if hp:
        user = int(event_var["userid"])
        alpha = 30*hp
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        if alpha > 255:
          es.server.queuecmd("est_effect 10 #a 0 sprites/tp_beam001.vmt %s %s %s 120 0.5 1.00 10 50 0 255 0 0 255 80" % (x1,y1,z1+30) )
          es.server.queuecmd("est_effect 10 #a 0 sprites/tp_beam001.vmt %s %s %s 0.5 120 1.00 10 50 0 255 0 0 255 80" % (x2,y2,z2+30) )
        es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 255 0 0 %i" % (x1,y1,z1+30,x2,y2,z2+30,alpha) )
        player.health += hp
        est.csay(attacker,"Drained %i hitpoints" % hp)
    if event_var["es_userhealth"] < 0:
      return
    weapon = event_var["weapon"]
    if weapon not in weapons["secondary"]:
      return
    level = getattr(entry,"skill4")
    if level:
      slow = 0.98-0.03*float(level)
      skills.slow(user,1.5,slow)
      slow = int(slow*100)
      est.csay(user,"Slowed to %i%s" % (slow,percent) )
      est.csay(attacker,"Slowed to %i%s" % (slow,percent) )

class Nubbernaut(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    player = playerlib.getPlayer(user)
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill1")
    if level:
      hp = level*5+10
      player.health += hp
      es.tell(user,"#multi", "#greenDevotion to God#lightgreen provides a#green %i #lightgreenhealth bonus!" % hp )
      wcsusers.set(user,"HPmaximum",hp+100)
    level = getattr(entry,"skill3")
    if level:
      est.removeweapon(user,2)
      gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_deagle"))
      ammo = 10*level
      gamethread.delayed(2,player.setClip,("weapon_deagle",ammo))
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )
      es.tell(user,"#multi", "#greenHoly Hand Cannon!")
    if server["round"] < 3:
      return
    dice = random.randint(1,3)
    level = getattr(entry,"skill2")
    if level < dice:
      es.tell(user,"#multi", "#lightgreenYou are not holy enough to wield the #greenHoly Cannon#lightgreen!")
      return
    gamethread.delayed(0,cstrike.giveNamedItem,args=(user,"weapon_xm1014"))
    ammo = 5*level+10
    es.tell(user,"#multi", "#greenHoly Cannon#lightgreen grants a#green %i clip XM 1014#lightgreen." % ammo)
    gamethread.delayed(2,player.setClip,("weapon_xm1014",ammo))

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if level == 0:return
    wcs.evasion_set(user,"fallresist",95,None)
    gamethread.delayed(3,wcs.evasion_set,(user,"fallresist",0,None))
    skills.teleport(user,540+60*level)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 7 #a 0 sprites/smoke.vmt %s %s %s 40 3" % (x,y,z) )

class Neve(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill4")
    if level:
      speed = 1.1+0.08*level
      wcsusers.set(user,"speed",speed)
      gravity = 0.76-0.08*level
      wcsusers.set(user,"gravity",gravity)
      es.tell(user,"#multi", "#lightgreenPower of the #greenAvalanche#lightgreen provides#green %i %s#lightgreen faster speed and#green %i %s#lightgreen lower gravity." % (int((speed-1)*100),percent,int((1-gravity)*100),percent) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z) )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
      
  def attack(self,event_var,entry,server):
    weapon = event_var["weapon"]
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    if weapon in weapons["grenades"]:
      level = getattr(entry,"skill3")
      if not level:
        return
      dmg = float(event_var["dmg_health"])
      damage = int(dmg/3.2*level)
      dmg = skills.dealdamage(attacker,user,damage)
      if dmg < 0:
        es.tell(user,"#multi", "#green%s#lightgreenhas resisted some of your crit nade")
        return
      dice = random.randint(1,6)
      if dice == 1:est.playplayer(user,"physics/glass/glass_largesheet_break1.wav")
      elif dice == 2:est.playplayer(user,"physics/glass/glass_largesheet_break2.wav")
      elif dice == 3:est.playplayer(user,"physics/glass/glass_largesheet_break3.wav")
      elif dice == 4:est.playplayer(user,"physics/glass/glass_sheet_break1.wav")
      elif dice == 5:est.playplayer(user,"physics/glass/glass_sheet_break2.wav")
      elif dice == 6:est.playplayer(user,"physics/glass/glass_sheet_break3.wav")
      attackername = event_var["es_attackername"]
      username = event_var["es_username"]
      es.tell(user,"#multi", "#greenCritical Grenade#lightgreen from#green %s #lightgreenunleashes#green %i + %i #lightgreendamage unto you!" % (attackername,dmg,damage) )
      es.tell(attacker,"#multi", "#greenCritical Grenade#lightgreen unleashes#green %i + %i #lightgreendamage to#green %s #lightgreen!" % (dmg,damage,username) )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 11 #a 0 sprites/crystal_beam1.vmt %s %s %s 0.7 3 200" % (x,y,z+20) )
      return
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,3)
    if dice == 1:
      level = getattr(entry,"skill2")
      if level:
        time = 1+level
        skills.shake(user,time,20,100)
        attackername = event_var["es_attackername"]
        username = event_var["es_username"]
        est.csay(user,"%s shook you!" % attackername)
        est.csay(attacker,"Shook %s!" % username)
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 0 255 0 255" % (x1,y1,z1,x2,y2,z2) )
    dice = random.randint(1,2)
    if dice == 1:
      level = getattr(entry,"skill1")
      if level:
        slow = 0.90-0.05*float(level)
        time = 1+0.5*float(level)
        skills.slow(user,time,slow)
        slow = int(slow*100)
        est.csay(user,"Slowed to %i%s" % (slow,percent) )
        est.csay(attacker,"Slowed to %i%s" % (slow,percent) )
      
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    time = level
    gamethread.delayed(time,neve_end,(user,server["round"]))
    player = playerlib.getPlayer(user)
    player.setColor(100,100,255,1)
    player.setWeaponColor(100,100,255,50)
    skills.fade(user,time,2,0,1,1,150,20)
    x,y,z = es.getplayerlocation(user)
    es.tell(user,"#multi", "#greenMist#lightgreen shrouds you for#green %i#lightgreenseconds!" % time )
    
class Tatsu(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill1")
    if level:
      invisp = 35+level*5
      gamethread.delayed(1.5,playerlib.getPlayer(user).setColor,(100,100,255,invisp))
      wcsusers._set(user,"invisp",invisp)
      es.tell(user,"#multi", "#greenClear Ice #lightgreengrants you#green %i%%#lightgreen invisibility" % invisp )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
    level = getattr(entry,"skill4")
    if not level:return
    time = 8-level
    wcsusers._set(user,"stealthtime",time)
  
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    x,y,z = es.getplayerlocation(user)
    dice = random.randint(1,10)
    level = getattr(entry,"skill2")
    if level >= dice:
      time = 1+level
      skills.fade(user,1,2,0,100,220,235,75)
      est.csay(user,"%s blinded you!" % attackername)
      est.csay(attacker,"Blinded %s!" % username)
      es.server.queuecmd("est_effect 4 #a 0 sprites/tp_beam001.vmt %s 2 5 10 20 100 155 255 255" % (user) )
      es.server.queuecmd("est_effect 11 #a 0 sprites/lgtning.vmt %s %s %s 1 2.3 90" % (x,y,z) )
    level = getattr(entry,"skill3")
    dice = random.randint(1,21)
    if level < dice:
      return
    if skills.freeze(user,1):
      est.csay(user,"Frozen by %s" % attackername)
      est.csay(attacker,"Froze %s" % username)
      es.server.queuecmd("est_effect 11 #a 0 sprites/lgtning.vmt %s %s %s 1 2.3 90" % (x,y,z) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level == 0:return
    wcs.evasion_set(user,"fallresist",95,None)
    gamethread.delayed(3,wcs.evasion_set,(user,"fallresist",0,None))
    skills.teleport(user,300+100*level)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 500 3 100 100 0 0 0 255 255 10" % (x,y,z) )
    
class HumanGen(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill1")
    if level:
      hp = level*5+20
      es.tell(user,"#multi", "#greenDevotion Aura#lightgreen provides a#green %i #lightgreenhealth bonus!" % hp )
      wcsusers.set(user,"HPmaximum",hp+100)
    tlevel = getattr(entry,"level")
    if tlevel < 40:
      return
    invisp = 20+int(tlevel-40)
    if invisp > 60:
      invisp = 60
    else:
      invisp = 20+level*5
    gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
    es.tell(user,"#multi", "#greenHuman General Expertise#lightgreen grants you#green %i%%#lightgreen invisibility"%invisp)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    if "invisp" in wcsusers.get(user):
      alpha = 255-wcsusers.get(attacker,"invisp")*4
    else:
      alpha = 255
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    level = getattr(entry,"skill2")
    dice = random.randint(1,40)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    if level >= dice:
      if skills.freeze(user,1.25):
        est.csay(user,"Frozen by %s" % attackername)
        est.csay(attacker,"Froze %s" % username)
        es.server.queuecmd("est_effect 11 #a 0 sprites/lgtning.vmt %s %s %s 1 2.3 90" % (x1,y1,z1) )
    level = getattr(entry,"skill3")
    dice = random.randint(1,50)
    if level >= dice:
      player = playerlib.getPlayer(user)
      ammo = int(player.clip.primary)-3
      if ammo < 0:
        ammo = 0
      player.clip.primary = ammo
      es.tell(user,"#multi", "#greenPacifism#lightgreen from#green %s#lightgreen hits you!" % attackername )
      es.tell(attacker,"#multi", "#greenPacifism#lightgreen affects#green  %s" % username )
      es.server.queuecmd("est_effect 3 #a 0 sprites/tp_beam001.vmt %s %s %s %s %s %s 3 4 2 15 11 167 %s" % (x1,y1,z1+40,x2,y2,z2+40,alpha) )
      es.server.queuecmd("est_effect 11 #a 0 sprites/lgtning_noz.vmt %s %s %s 3 1 %s" % (x1,y1,z1+40,alpha) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/physring1.vmt %s %s %s 100 300 3 40 20 0 14 0 41 %s" % (x1,y1,z1+40,alpha) )
    dice = random.randint(1,3)
    if dice != 1:
      return
    level = getattr(entry,"skill4")
    if not level:
      return
    cash = 10+level*30
    Person = playerlib.getPlayer(user)
    Player = playerlib.getPlayer(attacker)
    money = int(Person.cash)
    if money <= 0:
      return
    if cash > money:
      cash = money
    Player.cash += cash
    Person.cash -= cash
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 255 255 0 %s" % (x1,y1,z1+40,x2,y2,z2+40,alpha) )
    es.tell(user,"#multi", "#lightgreenLost#green $%i #lightgreento#green %s" % (cash,attackername) )
    es.tell(attacker,"#multi", "#greenStole $%i #lightgreenoff#green %s" % (cash,username) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level == 0:return
    wcs.evasion_set(user,"fallresist",95,None)
    gamethread.delayed(3,wcs.evasion_set,(user,"fallresist",0,None))
    skills.teleport(user,600+100*level)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 7 #a 0 sprites/smoke.vmt %s %s %s 40 3" % (x,y,z) )
    
class UndeadLord(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    wcsusers._set(user,"ultravision",1)
    wcsusers._set(user,"undead",1)
    skulls = wcsusers.get(user,"skulls")
    if skulls:
      es.tell(user,"#multi","#lightgreenYou have colleceted#green %i#lightgreen skulls!" % skulls)
    level = getattr(entry,"skill3")
    if level:
      gravity = 0.9-0.05*level
      wcsusers.set(user,"gravity",gravity)
      es.tell(user,"#multi", "#greenGravity Inhibitor#lightgreen allows you to jump#green %i%s #lightgreenhigher!" % (int((1-gravity)*100),percent) )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 150 20 20 255 1" % (x,y,z) )
    dice = random.randint(1,16)
    level = getattr(entry,"skill4")
    if level >= dice:
      wcsusers._set(user,"vengeance",1)
      es.tell(user,"#multi", "#greenUndead Vengeance#lightgreen will respawn you this round!")
    else:
      wcsusers._set(user,"vengeance",0)
      es.tell(user,"#multi", "#greenUndead Vengeance#lightgreen failed and#green wont#lightgreen respawn you!")
    tlevel = getattr(entry,"level")
    if tlevel < 60:
      return
    speed = 1.1+(tlevel-60)*0.005
    if speed > 1.3:speed = 1.3
    wcsusers.set(user,"speed",speed)
    es.tell(user,"#multi", "#greenUndead Lord Expertise#lightgreen allows you to run#green %i%s #lightgreenfaster!" % (int((speed-1)*100),percent) )

  def attack(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    damage = float(event_var["dmg_health"])
    dice = random.randint(1,3)
    if dice == 1:
      level = getattr(entry,"skill2")
      if level:
        skulls = wcsusers.get(attacker,"skulls")+1
        wcsusers._set(attacker,"skulls",skulls)
        dmg = int(damage*(float(level)*0.025+0.1))
        if event_var["es_userhealth"] > 0:
          dmg = skills.dealdamage(attacker,user,dmg)
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 150 0 0 255" % (x1,y1,z1+10,x2,y2,z2+10) )
        es.tell(attacker,"#multi", "#greenSkull Harvest#lightgreen deals #green+%i DMG#lightgreen and you gain a #greenSkull#lightgreen!" % dmg )
    dice = random.randint(1,2)
    if dice == 2:
      return
    level = getattr(entry,"skill1")
    hp = int(damage*(float(level)/24+0.01))
    if hp:
      user = int(event_var["userid"])
      alpha = 30+level*20
      x1,y1,z1 = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 255 0 0 %i" % (x1,y1,z1+20,x2,y2,z2+20,alpha) )
      playerlib.getPlayer(attacker).health += hp
      est.csay(attacker,"Drained %i hitpoints" % hp)

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill5")
    dice = random.randint(1,20)
    if level >= dice:
      skills.suicidebomb(user,55+15*level,90+5*level)
    respawn = wcsusers.get(user,"vengeance")
    if respawn == 0:
      return
    skills.respawn(user,3,100)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill6")
    if not level:
      return
    skulls = wcsusers.get(user,"skulls")
    cost = int(level/3)
    if cost == 0:cost = 1
    if skulls < cost:
      es.tell(user,"#multi", "#lightgreenNot enough skulls#green need #green%i#lightgreen more" % (cost-skulls) )
      return False
    skulls -= cost
    wcsusers._set(user,"skulls",skulls)
    heal = level*2+4
    player = playerlib.getPlayer(user)
    hp = player.health
    maxhp = wcsusers.get(user,"HPmaximum")+100
    health = hp+heal
    if health > maxhp:
      health = maxhp
    player.health = health
    speed = wcsusers.get(user,"speed")
    player = playerlib.getPlayer(user)
    gamethread.delayed(5,player.setSpeed,speed)
    speed *= (1.0+0.05*level)
    if speed > 1.6:
      speed = 1.6
    player.setSpeed(speed)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/yelflare1.vmt %s %s %s 4 2 255" % (x,y,z+40) )
    es.tell(user,"#multi", "#greenBloodlust#lightgreen grants you#green %i #lightgreenhealth and#green +%i%s#lightgreen speed for#green 5s#lightgreen! You have#green %i #lightgreenskulls remaining." % (level*2+4,int((speed-1)*100),percent,skulls) )

class Kirin(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"jetpack",0)
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill3")
    if level:
      invisp = 30+level*5
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#greenInvisibility #lightgreengrants you#green %i%%#lightgreen invisibility"%invisp)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
    level = getattr(entry,"skill4")
    if level:
      speed = 1+level*0.05
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenHaste#lightgreen allows you to run#green %i percent#lightgreen faster!" % int((speed-1)*100) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z) )
    tlevel = getattr(entry,"level")
    if tlevel >= 40:
      level = (tlevel-10)*2
      if level > 100:
        level = 100
      wcs.evasion_set(user,"fallresist",level,None)  
      es.tell(user,"#multi", "#greenKirin-Tor Expertise#lightgreen grants#green %s #lightgreenfall resistance." % level)

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    dice = random.randint(1,4)
    if dice == 1:
      level = getattr(entry,"skill1")
      if level:
        skills.shake(user,level+2,20,80)
        est.csay(user,"%s shook you!" % attackername)
        est.csay(attacker,"Shook %s!" % username)
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 0 255 0 255" % (x1,y1,z1,x2,y2,z2) )
    if dice == 2:
      level = getattr(entry,"skill4")
      if not level:
        return
      time = random.randint(2,4)
      skills.burn(attacker,user,time)
      dmg = skills.dealdamage(attacker,user,int(time*level/5))
      x1,y1,z1 = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 30 30 255 0 0 150" % (x1,y1,z1+10,x2,y2,z2+10) )
      es.tell(user,"#multi", "#green %s #lightgreenhits you with#green Flame Strike#lightgreen!" % attackername )
      es.tell(attacker,"#multi", "#green Flame Strike#lightgreen burns#green %s" % username )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    player = playerlib.getPlayer(user)
    frozen = player.freeze
    if frozen:
      est.csay(user,"You are frozen!")
      return False
    jetpack = wcsusers.get(user,"jetpack")
    if not jetpack:
      wcsusers.set(user,"jetpack",1)
      playerlib.getPlayer(user).setSpeed(1.5)
      est.csay(user,"Flying with speed boost!")
      es.setplayerprop(user,"CBasePlayer.m_fFlags",8)
      player.jetpack(1)
    else:
      wcsusers.set(user,"jetpack",0)
      speed = wcsusers.get(user,"speed")
      playerlib.getPlayer(user).setSpeed(speed)
      est.csay(user,"No longer flying, lost the speed boost!")
      es.setplayerprop(user,"CBasePlayer.m_fFlags",1)
      player.jetpack(0)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 60 100 0.8 0 255 255 255 1" % (x,y,z) )
    
class Akasha(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    player = playerlib.getPlayer(user)
    player.setModel("player/slow/akasha/slow")
    if int(event_var["es_userteam"]) == 3:
      player.setColor(175,175,254,255)
    else:
      player.setColor(254,175,175,255)
    akasha_cloud(user,server["round"])
    wcsusers._set(user,"jetpack",0)
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill2")
    dice = random.randint(1,8)
    if level >= dice:
      wcsusers._set(user,"ulti_immunity",1)
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 40 2 10 10 1 0 255 100 255 1" % (x,y,z) )
      es.tell(user,"#multi", "#lightgreenYou are now attuned to#green Block Ultimates#lightgreen!")
    level = getattr(entry,"skill5")
    if level:
      hp = 1+int(level/2)
      skills.regenerationstart(user,hp,3,0,400,0,1.0)
      es.tell(user,"#multi", "#greenHealing Gift#lightgreen provides#green %s #lightgreenhitpoints every#green 3s#lightgreen!" % hp)

  def attack(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill1")
    if level:
      dmg = float(event_var["dmg_health"])
      hp = int(dmg*(float(level+2)/100))
      hpmax = wcsusers.get(attacker,"HPmaximum")
      hpmax += hp
      if hpmax > 150:
        hpmax = 150
      wcsusers._set(attacker,"HPmaximum",hpmax)
      skills.transfusestart(attacker,user,hp)
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,24)
    level = getattr(entry,"skill3")
    if level >= dice:
      time = 1.0+0.5*level
      skills.burn(attacker,user,time)
      dmg = skills.dealdamage(attacker,user,int(time*2))
      x1,y1,z1 = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 7 #a 0 sprites/smoke.vmt %s %s %s 5 3" % (x1,y1,z1+20) )
    dice = random.randint(1,24)
    level = getattr(entry,"skill4")
    if level < dice:
      return
    die = 1+0.49*float(level)
    try:
      charges = int(wcsusers.get(user,"wounded"))
    except:
      charges = 0
    wcsusers._set(user,"wounded",die)
    if not charges:
      es.server.queuecmd("es wcs_wound %s %s 1 3 server_var(wcs_roundcounter)" % (user,attacker) )  
      es.tell(user,"#multi","#lightgreenYou have been#green wounded#lightgreen by#green %s #lightgreen!!" % event_var["es_attacername"])
      es.tell(attacker,"#multi","#lightgreenYou have #greenwounded %s #lightgreen!!" % event_var["es_username"])

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    player = playerlib.getPlayer(user)
    frozen = player.freeze
    if frozen:
      est.csay(user,"You are frozen!")
      return False
    jetpack = wcsusers.get(user,"jetpack")
    if not jetpack:
      wcsusers.set(user,"jetpack",1)
      playerlib.getPlayer(user).setSpeed(1.5)
      est.csay(user,"Flying with speed boost!")
      est.freeze_immune(user,1)
      es.setplayerprop(user,"CBasePlayer.m_fFlags",8)
      player.jetpack(1)
    else:
      wcsusers.set(user,"jetpack",0)
      speed = wcsusers.get(user,"speed")
      playerlib.getPlayer(user).setSpeed(speed)
      est.csay(user,"No longer flying, lost the speed boost!")
      est.freeze_immune(user,0)
      es.setplayerprop(user,"CBasePlayer.m_fFlags",1)
      player.jetpack(0)

class Rakdos(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"jetpack",0)
    wcsusers._set(user,"demon",1)
    est.armor(user,"=",100,1)
    x,y,z = es.getplayerlocation(user)
    dice = random.randint(1,3)
    level = getattr(entry,"skill3")
    if level < dice:
      return
    if server["round"] < 2:
      return
    if level > 3:
      ammo = 8+16*(level-3)
    else:
      ammo = 8
    es.tell(user,"#multi", "#greenHell Cannon#lightgreen provides a#green %s#lightgreen shot#green M3 Shotgun!" % ammo)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )
    gamethread.delayed(0,cstrike.giveNamedItem,args=(user,"weapon_m3"))
    gamethread.delayed(2,playerlib.getPlayer(user).setClip,("weapon_m3",ammo))

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dice = random.randint(1,2)
    if dice == 1:
      level = getattr(entry,"skill1")
      if level:
        skills.shake(user,0.5*level,20,100)
        est.csay(user,"%s shook you!" % event_var["es_attackername"])
        est.csay(attacker,"Shook %s!" % event_var["es_username"])
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    dice = random.randint(1,2)
    level = getattr(entry,"skill2")
    if level >= dice:
      es.server.queuecmd("est_effect 10 #a 0 sprites/flatflame.vmt %s %s %s 50 350 2 90 200 0 155 155 155 155 2" % (x1,y1,z1) )
      es.server.queuecmd("est_effect 11 #a 0 sprites/flatflame.vmt %s %s %s 3 3 255" % (x1,y1,z1) )
      es.server.queuecmd("est_effect 3 #a 0 sprites/flatflame.vmt %s %s %s %s %s %s 1 3 6 100 255 55 255" % (x1,y1,z1,x2,y2,z2) )
      skills.dragonslave(user,x1,y1,z1,es.getplayerteam(attacker),level,5,300,server["round"])
    dice = random.randint(1,100)
    level = getattr(entry,"skill2")
    chance = 4+level
    if x2 >= x1-10:chance *= 2
    if x2 > x1+200:chance *= 2
    if chance < dice:
      return
    if skills.freeze(user,1):
      attackername = event_var["es_attackername"]
      username = event_var["es_username"]
      est.csay(user,"Stunned by %s" % attackername)
      est.csay(attacker,"Stunned %s" % username)
      x,y,z = es.getplayerlocation(user) 
      es.server.queuecmd("est_effect 10 #a 0 sprites/tp_beam001.vmt %s %s %s 30 0 0.2000 10 1 10 255 150 150 255 1" % (x,y,z+10) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/tp_beam001.vmt %s %s %s 30 0 0.2000 10 1 10 255 150 150 255 1" % (x,y,z+20) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    player = playerlib.getPlayer(user)
    frozen = player.freeze
    if frozen:
      est.csay(user,"You are frozen!")
      return False
    hp = 2+3*level
    jetpack = wcsusers.get(user,"jetpack")
    if not jetpack:
      wcsusers.set(user,"jetpack",1)
      player.health += hp
      speed = wcsusers.get(user,"speed")
      if speed < 1.3:
        playerlib.getPlayer(user).setSpeed(1.3)
        est.csay(user,"Flying with +%i health and speed boost!" % hp)
      else:
        est.csay(user,"Flying with +%i health!" % hp)
      es.setplayerprop(user,"CBasePlayer.m_fFlags",8)
      player.jetpack(1)
    else:
      wcsusers.set(user,"jetpack",0)
      if player.health > hp:
        player.health -= hp
      else:
        player.health = 1
      wcsusers.set(user,"jetpack",0)
      speed = wcsusers.get(user,"speed")
      if speed < 1.3:
        playerlib.getPlayer(user).setSpeed(speed)
        est.csay(user,"No longer flying, lost the +%i health and speed boost!" % hp)
      else:
        est.csay(user,"No longer flying, lost the +%i health!" % hp)
      es.setplayerprop(user,"CBasePlayer.m_fFlags",1)
      player.jetpack(0)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 60 100 0.8 255 20 20 255 1" % (x,y,z) )
    
class Zeratul(BaseClass):
  def spawn(self,event_var,entry,server):
    gamethread.delayed(1, playerlib.getPlayer(int(event_var["userid"])).setDefuser,(0))
    user = int(event_var["userid"])
    team = es.getplayerteam(user)
    if team == 2:
      es.server.queuecmd("wcs_ztelite1 %s x;py_keysetvalue WCSuserdata %s elite1 server_var(x);es wcs_setindexcolour server_var(x) 255 150 150 255 400 550" % (user,user) )
      es.server.queuecmd("wcs_ztelite2 %s y;py_keysetvalue WCSuserdata %s elite2 server_var(y);es wcs_setindexcolour server_var(y) 255 150 150 255 400 550" % (user,user) )
    else:
      es.server.queuecmd("wcs_ztelite1 %s x;py_keysetvalue WCSuserdata %s elite1 server_var(x);es wcs_setindexcolour server_var(x) 150 150 255 255 400 550" % (user,user) )
      es.server.queuecmd("wcs_ztelite2 %s y;py_keysetvalue WCSuserdata %s elite2 server_var(y);es wcs_setindexcolour server_var(y) 150 150 255 255 400 550" % (user,user) )
    es.doblock("wcs/shell/WCSskills/Zeratul/player_spawn")
    wcsusers._set(user,"hidden",0)
    level = getattr(entry,"skill2")
    if level:
      est.armor(user,"=",100,1)
      wcs.evasion_set(user,"shield",100,None)
      shield = int(level/2.5)
      skills.armoraurastart(user,shield,2,100,200,0)
      es.tell(user,"#multi", "#greenPlasma Shield#lightgreen is#green active#lightgreen and will resist#green 100%#lightgreen damage if you have armor.")
    level = getattr(entry,"skill4")
    invisp = 50+2*level
    gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
    es.tell(user,"#multi", "#greenCloaking#lightgreen provides#green %s percent#lightgreen invisibility." % invisp)

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    x = wcsusers.get(user,"elite1")
    if not x:
      return
    skills.setindexcolour(x,[255,150,150,1],400,550)
    y = wcsusers.get(user,"elite2")
    if not y:
      return
    skills.setindexcolour(y,[255,150,150,1],400,550)
    
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] != "knife":
      return
    level = getattr(entry,"skill3")
    if not level:
      return
    if event_var["dmg_health"] < 30:
      level = int(level*0.6)
    if not level:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = skills.dealdamage(attacker,user,level)
    if not dmg:
      return
    est.csay(attacker,"Dealt + %s damage with psi blades!" % level)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if not level:
      return
    skills.suicidebomb(user,250,5+level)

  def ability(self,user,entry,server):
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 server_var(wcs_userid) 0 sprites/lgtning.vmt %s %s %s 20 40 2 10 10 1 0 255 100 255 1" % (x,y,z) )
    hidden = wcsusers.get(user,"hidden")
    team = es.getplayerteam(user)
    if not hidden:
      wcsusers._set(user,"hidden",1)
      initialgrav = wcsusers.get(user,"gravity")
      wcsusers.set(user,"gravity",0.01)
      est.physpush(user,0,0,250)
      x = wcsusers.get(user,"elite1")
      if x:
        if team == 2:
          gamethread.delayed(0.25,skills.setindexcolour,(x,[255,150,150,200],400,550))
          gamethread.delayed(0.50,skills.setindexcolour,(x,[255,150,150,150],400,550))
          gamethread.delayed(0.75,skills.setindexcolour,(x,[255,150,150,100],400,550))
          gamethread.delayed(1.00,skills.setindexcolour,(x,[255,150,150,1],400,550))
        else:
          gamethread.delayed(0.25,skills.setindexcolour,(x,[150,150,255,200],400,550))
          gamethread.delayed(0.50,skills.setindexcolour,(x,[150,150,255,150],400,550))
          gamethread.delayed(0.75,skills.setindexcolour,(x,[150,150,255,100],400,550))
          gamethread.delayed(1.00,skills.setindexcolour,(x,[150,150,255,1],400,550))
      x = wcsusers.get(user,"elite2")

      if x:
        if team == 2:
          gamethread.delayed(0.25,skills.setindexcolour,(x,[255,150,150,200],400,550))
          gamethread.delayed(0.50,skills.setindexcolour,(x,[255,150,150,150],400,550))
          gamethread.delayed(0.75,skills.setindexcolour,(x,[255,150,150,100],400,550))
          gamethread.delayed(1.00,skills.setindexcolour,(x,[255,150,150,1],400,550))
        else:
          gamethread.delayed(0.25,skills.setindexcolour,(x,[150,150,255,200],400,550))
          gamethread.delayed(0.50,skills.setindexcolour,(x,[150,150,255,150],400,550))
          gamethread.delayed(0.75,skills.setindexcolour,(x,[150,150,255,100],400,550))
          gamethread.delayed(1.00,skills.setindexcolour,(x,[150,150,255,1],400,550))
      player = playerlib.getPlayer(user)
      gamethread.delayed(1,player.freeze,1)
      gamethread.delayed(1.1,est.freeze_immune,(user,1))
      gamethread.delayed(2,est.physpush,(user,0,0,0))
      gamethread.delayed(2,wcsusers.set,(user,"gravity",initialgrav))
      player = playerlib.getPlayer(user)
      gamethread.delayed(0.5,player.setColor,(240,240,240,0))
      return
    wcsusers._set(user,"hidden",0)
    player = playerlib.getPlayer(user)
    est.freeze_immune(user,0)
    player.freeze(0)
    gamethread.delayed(0.6,est.physpush,(user,0,0,0))
    est.invis_reset(user)
    x = wcsusers.get(user,"elite1")
    if x:
      if team == 2:
        gamethread.delayed(0.25,skills.setindexcolour,(x,[255,150,150,100],400,550))
        gamethread.delayed(0.50,skills.setindexcolour,(x,[255,150,150,150],400,550))
        gamethread.delayed(0.75,skills.setindexcolour,(x,[255,150,150,200],400,550))
        gamethread.delayed(1.00,skills.setindexcolour,(x,[255,150,150,255],400,550))
      else:
        gamethread.delayed(0.25,skills.setindexcolour,(x,[150,150,255,100],400,550))
        gamethread.delayed(0.50,skills.setindexcolour,(x,[150,150,255,150],400,550))
        gamethread.delayed(0.75,skills.setindexcolour,(x,[150,150,255,200],400,550))
        gamethread.delayed(1.00,skills.setindexcolour,(x,[150,150,255,255],400,550))
    x = wcsusers.get(user,"elite2")
    if x:
      if team == 2:
        gamethread.delayed(0.25,skills.setindexcolour,(x,[255,150,150,100],400,550))
        gamethread.delayed(0.50,skills.setindexcolour,(x,[255,150,150,150],400,550))
        gamethread.delayed(0.75,skills.setindexcolour,(x,[255,150,150,200],400,550))
        gamethread.delayed(1.00,skills.setindexcolour,(x,[255,150,150,255],400,550))
      else:
        gamethread.delayed(0.25,skills.setindexcolour,(x,[150,150,255,100],400,550))
        gamethread.delayed(0.50,skills.setindexcolour,(x,[150,150,255,150],400,550))
        gamethread.delayed(0.75,skills.setindexcolour,(x,[150,150,255,200],400,550))
        gamethread.delayed(1.00,skills.setindexcolour,(x,[150,150,255,255],400,550))
        
class Zeus(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill1")
    if level:
      speed = 1.05+0.05*level
      wcsusers.set(user,"speed",speed)
      gravity = 0.8-0.04*level
      wcsusers.set(user,"gravity",gravity)
      es.tell(user,"#multi", "#greenLightning Dash#lightgreen provides#green %i %s#lightgreen faster speed and#green %i %s#lightgreen lower gravity." % (int((speed-1)*100),percent,int((1-gravity)*100),percent) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,6)
    if dice != 1:
      return
    level = getattr(entry,"skill2")
    if not level:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = float(event_var["dmg_health"])
    damage = int(dmg*(0.25*float(level)+0.25))
    dmg = skills.dealdamage(attacker,user,damage)
    if not dmg:

      return
    est.csay(user,"Took +%i damage!" % dmg)
    est.csay(attacker,"+%i damage!" % dmg)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 255 255 255 100" % (x1,y1,z1+40,x2,y2,z2+40) )

  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill3")
    dice = random.randint(1,13)
    if level < dice:
      return
    user = int(event_var["userid"])
    est.playplayer(user,"weapons/physcannon/energy_sing_flyby2.wav")
    player = playerlib.getPlayer(user)
    gamethread.delayed(0.5,player.setColor,(15,0,255,10))
    gamethread.delayed(1.0,player.setColor,(15,0,255,25))
    gamethread.delayed(1.5,player.setColor,(15,0,255,35))
    gamethread.delayed(2.0,player.setColor,(15,0,255,60))
    gamethread.delayed(2.5,player.setColor,(15,0,255,80))
    gamethread.delayed(3.0,player.setColor,(15,0,255,115))
    gamethread.delayed(3.5,player.setColor,(15,0,255,135))
    gamethread.delayed(4.0,player.setColor,(15,0,255,165))
    gamethread.delayed(4.5,player.setColor,(15,0,255,185))
    gamethread.delayed(5.0,est.invis_reset,user)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if level == 0:return
    if not skills.chainlightning(user,30,300+100*level,2+level):
      return False

class Magician(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"spell",1)
    wcsusers._set(user,"trueshot",100)
    es.server.queuecmd("wcs_nerf %s percent 75" % user)
    gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_scout"))
    gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_usp"))
    
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    targetP = playerlib.getPlayer(user)
    if targetP.health > 5:
      targetP.health -= 5
    else:
      es.delayed(0,"sm_damage %s %s %s"% (attacker,user,5))
    spell = wcsusers.get(attacker,"spell")
    if spell == 1:
      level = getattr(entry,"skill2")
      if level == 0:return
      skills.magicmissilestart(attacker,user,level*5+15)
      es.tell(attacker,"Magic Missile!")
    elif spell == 2:
      ss
    elif spell == 3:
      ss

  def shoot(self,event_var,entry,server):
    user = int(event_var["userid"])
    weapon = event_var["weapon"]
    player = playerlib.getPlayer(user)
    if weapon in weapons["primary"]:
      ammo = int(player.clip.primary)
      ammo -= 1
      if ammo < 0:ammo = 0
      player.clip.primary = ammo
    elif weapon in weapons["secondary"]:
      ammo = int(player.clip.secondary)
      ammo -= 1
      if ammo < 0:ammo = 0
      player.clip.secondary = ammo
  
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level == 0:return
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 7 #a 0 sprites/smoke.vmt %s %s %s 40 3" % (x,y,z+40) )
    es.server.queuecmd("est_effect 7 #a 0.10 sprites/smoke.vmt %s %s %s 40 3" % (x,y,z+40) )
    es.server.queuecmd("est_effect 7 #a 0.20 sprites/smoke.vmt %s %s %s 40 3" % (x,y,z+40) )
    es.server.queuecmd("est_effect 7 #a 0.30 sprites/smoke.vmt %s %s %s 40 3" % (x,y,z+40) )
    es.server.queuecmd("est_effect 7 #a 0.40 sprites/smoke.vmt %s %s %s 40 3" % (x,y,z+40) )
    es.server.queuecmd("est_viewcoords %s x;es wcs_blink %s server_var(x) %s" % (user,user,150+level*50) )

class Link(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill2")
    wcsusers._set(user,"bottle",1)
    if level:
      wcs.evasion_set(user,"dmgimmune",level*2,None)
      es.tell(user,"#multi","#greenHylian Shield#lightgreen blocks#green %s#lightgreen of all damage"%(level*2))
    level = getattr(entry,"skill3")
    if level:
      garb = wcsusers.get(user,"garb")
      hp = level
      skills.regenerationstart(user,hp,6,0,150,0,1.0)
      if garb == 1:
        invisp = 10+5*level
        alpha = 255-2.55*invisp
        wcsusers._set(user,"invisp",invisp)
        gamethread.delayed(1.5,playerlib.getPlayer(user).setColor,(150,255,150,alpha))
        gamethread.delayed(0.5,wcsusers._set(user,"regeneration",0))
        es.tell(user,"#multi","#lightgreenGreen #greenLegendary Hero's Garbs#lightgreen equipped!")
      elif garb == 2:
        es.tell(user,"#multi","#lightgreenRed #greenLegendary Hero's Garbs#lightgreen equipped!")
      elif garb == 3:
        es.tell(user,"#multi","#lightgreenBlue #greenLegendary Hero's Garbs#lightgreen equipped!")
        gamethread.delayed(0.5,wcsusers._set(user,"regeneration",0))
      else:
        es.tell(user,"#multi","#greenLegendary Hero's Garbs#lightgreen now available from Ability")
        gamethread.delayed(0.5,wcsusers._set(user,"regeneration",0))
    else:
      wcsusers._set(user,"garb",0)
    level = getattr(entry,"skill5")
    if level:
      bow = wcsusers.get(user,"bow")
      if bow == 1:
        es.tell(user,"#multi","#greenFlame Arrows#lightgreen equipped!")
      elif bow == 2:
        es.tell(user,"#multi","#greenIce Arrows#lightgreen equipped!")
      elif bow == 3:
        es.tell(user,"#multi","#greenLight Arrows#lightgreen equipped!")
      else:
        es.tell(user,"#multi","#greenQuivers#lightgreen now available from Ability")
    else:
      wcsusers._set(user,"bow",0)
    level = getattr(entry,"skill6")
    if level:
      inventory = wcsusers.get(user,"inventory")
      if inventory == 1:
        es.tell(user,"#multi","#greenSlingshot#lightgreen equipped!")
      elif inventory == 2:
        es.tell(user,"#multi","#greenBoomerang#lightgreen equipped!")
      elif inventory == 3:
        es.tell(user,"#multi","#greenBombs#lightgreen equipped!")
      elif inventory == 4:
        es.tell(user,"#multi","#greenHookshot#lightgreen equipped!")
      else:
        es.tell(user,"#multi","#greenNew Inventory#lightgreen now available from Ability")
    else:
      wcsusers._set(user,"inventory",0)
    level = getattr(entry,"skill8")
    if level:
      wcs.evasion_set(user,"resist",50,None)
      x = 12-level
      es.tell(user,"#multi","#greenRoll#lightgreen will block #green50%% damage of a single hit every#green %s #lightgreenseconds!" % x)

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    x,y,z = es.getplayerlocation(user)
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill2")
    if level:
      dmg = skills.dealdamage(attacker,user,level*2)
      if dmg:
        est.csay(user,"Took +%i damage!" % dmg)
        est.csay(attacker,"+%i damage!" % dmg)
    else:damage = 0
    garb = wcsusers.get(attacker,"garb")
    inventory = wcsusers.get(attacker,"inventory")
    level = getattr(entry,"skill6")
    if inventory == 1:
      dice = random.randint(1,30)
      if level >= dice:
        if skills.freeze(user,1.0):
          est.csay(user,"Frozen by %s" % attackername)
          est.csay(attacker,"Froze %s" % username)
          es.server.queuecmd("est_effect 11 #a 0 sprites/lgtning.vmt %s %s %s 1 2.3 90" % (x,y,z) )
    elif inventory == 2:
      dice = random.randint(1,25)
      if level >= dice:
        est.csay(attacker,"Pushed %s" % username)
        ##es.setplayerprop(user,"CBasePlayer.m_fFlags",64.0)
        ##gamethread.delayed(0.1,es.setplayerprop,(user,"CBasePlayer.m_fFlags",64.0))
        skills.forcepush(attacker,user,500) 
    level = getattr(entry,"skill5")
    if not level:
      return
    bow = wcsusers.get(attacker,"bow")
    dice = random.randint(1,30)
    if level >= dice:
      if not bow:
        bow = 0
      if bow == 1:
        skills.burn(attacker,user,2,5)
      elif bow == 2:
        skills.slow(user,2,0.7)
      elif bow == 3:
        skills.fade(user,1,2,0,255,255,255,100)

  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    #roll
    if wcsusers.get(user,"resist") > 40:
      wcs.evasion_set(user,"resist",0)
      gamethread.delayed(12-getattr(entry,"skill8"),hyrule_evasion,(user,server["round"]))
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 11 #a 0 sprites/strider_blackball.vmt %s %s %s 2 0.5 255" % (x,y,z+40))
    if int(event_var["es_userhealth"]) < 40:
      recall = wcsusers.get(user,"bottle")
      if recall:
        wcsusers._set(user,"bottle",0)
        level = getattr(entry,"level")-40
        if level < 0:level = 0
        if level > 60:level = 60
        hp = 40+int(level*1.33)
        playerlib.getPlayer(user).health = hp
        gamethread.delayed(1,skills.infiltrate,(user,0))
        es.tell(user,"#multi","#greenFaerie Bottle#lightgreen pulls you back from death with#green %sHP#lightgreen!" % hp)
    garb = wcsusers.get(user,"garb")
    if garb != 3:return
    level = getattr(entry,"skill3")
    if not level:return
    duration = 1.1-level*0.1
    gamethread.delayed(duration,skills.slow,(user,1,0.0))
    gamethread.delayed(duration,skills.freeze,(user,0.0))
    gamethread.delayed(duration,skills.drug,(user,0.0))
    gamethread.delayed(duration,skills.burn,(attacker,user,0.0))
    gamethread.delayed(duration,skills.fade,(user,0.1,2,100,100,100,1))
  
  def shoot(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill4")
    if level:
      x,y,z = es.getplayerlocation(user)
      team = es.getplayerteam(user)
      if random.randint(1,10) < level:
          skills.spinattack(user,level,(x,y,z),team,150)
  
  def ability(self,user,entry,server):
    wcs.linkmenu(user)
  
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill6")
    if level == 0:return
    inventory = wcsusers.get(user,"inventory")
    if inventory == 3:
      radius = 150
      damage = 10+level*3
      es.server.queuecmd("est_viewcoords %s x;es wcs_explodeviewcoords %s server_var(x) %s %s" % (user,user,damage,radius))
    elif inventory == 4:
      wcs.evasion_set(user,"fallresist",60,None)
      gamethread.delayed(3,wcs.evasion_set,(user,"fallresist",0,None))
      skills.teleport(user,100+50*level)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 7 #a 0 sprites/smoke.vmt %s %s %s 40 3" % (x,y,z) )
def hyrule_evasion(user,round):
  from wcs.wcs import server
  if round != server["round"]:
    return
  wcs.evasion_set(user,"resist",50)

class Calthron(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"jetpack",0)
    level = getattr(entry,"skill2")
    if level:
      chance = 7+3*level
      wcs.evasion_set(user,"dodge",chance,None)
      es.tell(user,"#multi", "#lightgreenYour #greenOwl Eye#lightgreen will let you evade#green %s%s #lightgreenof attacks!" % (chance,percent) )
    level = getattr(entry,"skill3")
    if level:
      hp = 4+level
      delay = 8-level
      skills.regenerationstart(user,hp,delay,0,500,400,0.5)
      es.tell(user,"#multi", "#greenFirst Aid#lightgreen will heal for#green %sHP #lightgreenper#green %ss #lightgreenand half to yourself!" % (hp,delay) )
    level = getattr(entry,"skill4")
    if level:
      speed = 1.0+0.05*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenMobility#lightgreen allows you to run and fly#green %i%s #lightgreenfaster!" % (int((speed-1)*100),percent) )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,6)
    if dice != 1:
      return
    level = getattr(entry,"skill1")
    if not level:
      return      
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    x,y,z = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    distance = int( float( ((x-x2)**2 + (y-y2)**2 + (z-z2)**2)**(0.5) ) )
    damage = distance*level*0.0015
    if damage > 50:
      damage = 50
    dmg = skills.dealdamage(attacker,user,damage)
    if dmg:
      es.tell(attacker,"#multi", "#lightgreenYour #greenVulture Eye#lightgreen dealt an extra#green %s #lightgreendamage!" % int(dmg) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    player = playerlib.getPlayer(user)
    frozen = player.freeze
    if frozen:
      est.csay(user,"You are frozen!")
      return False
    jetpack = wcsusers.get(user,"jetpack")
    if not jetpack:
      wcsusers.set(user,"jetpack",1)
      est.csay(user,"Flying!")
      es.setplayerprop(user,"CBasePlayer.m_fFlags",8)
      player.jetpack(1)
    else:
      wcsusers.set(user,"jetpack",0)
      est.csay(user,"No longer flying!")
      es.setplayerprop(user,"CBasePlayer.m_fFlags",1)
      player.jetpack(0)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 60 100 0.8 0 255 255 255 1" % (x,y,z) )
 
class Harlute(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    es.server.queuecmd("est_setmodel %s player/pietro/yiyas/yiyas.mdl" % user)
    player = playerlib.getPlayer(user)
    if int(event_var["es_userteam"]) == 2:
      gamethread.delayed(0.5,player.setColor,(255,100,100,255))
    else:
      gamethread.delayed(0.5,player.setColor,(100,100,255,255))
    wcsusers._set(user,"ultravision",3)
    wcsusers._set(user,"lilith",0)
    level = getattr(entry,"skill1")
    if level:
      hp = level*5+10
      wcsusers.set(user,"HPmaximum",hp+100)
      es.tell(user,"#multi", "#greenHardware#lightgreen provides#green %i #lightgreenhitpoints." % hp )
    level = getattr(entry,"skill2")
    if level:
      est.armor(user,"=",100,1)
      wcs.evasion_set(user,"shield",100,None)
      skills.armoraurastart(user,level+2,1,150,200,0)
      es.tell(user,"#multi", "#greenForce Shield#lightgreen is#green active#lightgreen and will resist#green 100%%#lightgreen damage if you have armor.")
    level = getattr(entry,"skill5")
    if level:
      gravity = 0.8-0.05*level
      wcsusers.set(user,"gravity",gravity)
      speed = 1.1+0.05*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenMatter Hoverboots#lightgreen allows you to jump#green %i%s #lightgreenhigher and run#green %i%s#lightgreen faster.!" % (int((1-gravity)*100),percent,int((speed-1)*100),percent) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] != "knife":
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    level = getattr(entry,"skill4")
    dice = random.randint(1,12)
    if level > dice:
      index = es.getindexfromhandle(es.getplayerhandle(user))
      gravity = wcsusers.get(user,"gravity")
      gamethread.delayed(3,wcsusers.set(user,"gravity",gravity))
      gravity *= (1.0-0.1*level)
      if gravity < 0.2:
        gravity = 0.2
      wcsusers.set(user,"gravity",gravity)
      gravity = int((1.0-gravity)*100)
      es.tell(attacker,"#multi", "#greenGravity Distortion#lightgreen reduces #green%s's#lightgreen gravity to #green%s%s#lightgreen!" % (username,gravity,percent) )
    level = getattr(entry,"skill6")
    dice = random.randint(1,20)
    if level >= dice:
      skills.shake(user,1,10,100)
      damage = skills.dealdamage(attacker,user,level*5+20)
      est.physpush(user,0,0,350)
      es.tell(attacker,"#multi", "#greenForce Pulsar#lightgreen hit #green%s#lightgreen and dealt #green+%i#lightgreen damage!" % (username,damage) )

  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    shield = wcsusers.get(user,"lilith")
    shield += 1
    wcsusers._set(user,"lilith",shield)
    wcsusers._set(user,"armorregeneration",0)
    gamethread.delayed(3,shield_restore,(user,shield,1.0))
    level = getattr(entry,"skill3")
    dice = random.randint(1,10)
    if level >= dice:
      x1,y1,z1 = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      x,y,z = skills.distancecalc(x1-x2,y1-y2,z1-z2,100)
      est.physpush(attacker,x*level*100,y*level*100,z*level*100)
  
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill7")
    if not level:
      return
    x,y,z = es.getplayerlocation(user)
    team = es.getplayerteam(user)      
    skills.gravitywardstart(user,x,y,z,team,1+level/4,350,400)

class Marlute(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    es.server.queuecmd("est_setmodel %s player/pietro/yiyas/yiyas.mdl" % user)
    player = playerlib.getPlayer(user)
    wcsusers._set(user,"ultravision",3)
    level = getattr(entry,"skill1")
    if level:
      hp = level*5+10
      wcsusers.set(user,"HPmaximum",hp+100)
      es.tell(user,"#multi", "#greenHardware#lightgreen provides#green %i #lightgreenhitpoints." % hp )
    level = getattr(entry,"skill3")
    alpha = 255
    if level:
      est.armor(user,"=",100,1)
      wcs.evasion_set(user,"resist",level-1,None)
      invisp = 40+5*level
      gamethread.delayed(1.5,wcsusers._set,(user,"invisp",invisp))
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
      es.tell(user,"#multi", "#greenAngel's Veil#lightgreen grants you#green %s%% #lightgreeninvisibility and will resist #green%s#lightgreen damage per hit." % (invisp,level-1) )
    if int(event_var["es_userteam"]) == 2:
      gamethread.delayed(0.5,player.setColor,(255,100,100,alpha))
    else:
      gamethread.delayed(0.5,player.setColor,(100,100,255,alpha))
 
    level = getattr(entry,"skill5")
    if level:
      gravity = 0.8-0.05*level
      wcsusers.set(user,"gravity",gravity)
      speed = 1.1+0.05*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenMatter Hoverboots#lightgreen allows you to jump#green %i%s #lightgreenhigher and run#green %i%s#lightgreen faster.!" % (int((1-gravity)*100),percent,int((speed-1)*100),percent) )

  def attack(self,event_var,entry,server):
    if event_var["weapon"] != "knife":
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    damage = float(event_var["dmg_health"])
    level = getattr(entry,"skill4")
    if damage > 70:hp = int(damage*(float(level)/24))
    elif damage > 50:hp = int(damage*(float(level)/16))
    elif damage > 20:hp = int(damage*(float(level)/12))
    else: hp = int(damage*(float(level)/10))
    if hp:
      user = int(event_var["userid"])
      alpha = 30+level*20
      x1,y1,z1 = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 255 0 0 %i" % (x1,y1,z1+20,x2,y2,z2+20,alpha) )
      playerlib.getPlayer(attacker).health += hp
      est.csay(attacker,"Drained %i hitpoints" % hp)
    if event_var["es_userhealth"] < 0:
      return
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    dice = random.randint(1,3)
    if dice == 1:
      level = getattr(entry,"skill2")
      if level:
        cash = 20+level*30
        Person = playerlib.getPlayer(user)
        Player = playerlib.getPlayer(attacker)
        money = int(Person.cash)
        if money > 0:
          if cash > money:
            cash = money
          Player.cash += cash
          Person.cash -= cash
          x1,y1,z1 = es.getplayerlocation(user)
          x2,y2,z2 = es.getplayerlocation(attacker)
          es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 255 255 0 255" % (x1,y1,z1+40,x2,y2,z2+40) )
          es.tell(user,"#multi", "#lightgreenLost#green $%i #lightgreento#green %s" % (cash,attackername) )
          es.tell(attacker,"#multi", "#greenMana Drain#lightgreen robs#green $%i #lightgreenoff#green %s" % (cash,username) )
    dice = random.randint(1,3)
    if dice == 1:
      level = getattr(entry,"skill6")
      if level:
        es.server.queuecmd("lordpit_bury %s %s %s %s %s" % (user,attacker,1+level/4,username,attackername) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill7")
    dice = random.randint(1,20)
    if 9-level >= dice:
      es.tell(user,"#multi","#greenSoul Conversion#lightgreen failed!")
      return
    if not level:
      return
    users = []
    myteam = es.getplayerteam(user)
    for person in es.getUseridList():
      if es.getplayerprop(person, 'CBasePlayer.pl.deadflag'):
        continue
      team = es.getplayerteam(person)
      if team == myteam:
        continue
      users.append(person)
  
    if len(users) == 0:
      es.tell(user,"#multi","#greenLocust Swarm#lightgreen has nobody to target!")
      return False
    target = random.choice(users)
    hisname = es.getplayername(target)
    immune = wcsusers.get(target,"ulti_immunity")
    if immune:
      es.tell(user,"#multi","#greenSoul Conversion#lightgreen is blocked by #green%s#lightgreen!" % hisname)
      return
    player = playerlib.getPlayer(user)
    Player = playerlib.getPlayer(target)
    mymaxhp = wcsusers.get(user,"HPmaximum")
    myhpbefore = float(player.health)
    myperc = float(myhpbefore/mymaxhp)
    hismaxhp = wcsusers.get(target,"HPmaximum")
    hishpbefore = float(Player.health)
    hisperc = float(hishpbefore/hismaxhp)
    myhp = int(hisperc*mymaxhp*(level/32+0.75))
    if myhp < 1:myhp = 1
    hishp = int(myperc*hismaxhp)
    if hishp <1:hishp = 1
    player.health = myhp
    Player.health = hishp
    myname = es.getplayername(user)
    if myhpbefore < myhp:
      es.tell(user,"#multi","#greenSoul Conversion#lightgreen increased you to #green%sHP#lightgreen with #green%sHP#lightgreen to#green %s#lightgreen!" % (myhp,hishp,hisname) )
    else:
      es.tell(user,"#multi","#greenSoul Conversion#lightgreen reduced you to #green%sHP#lightgreen with #green%sHP#lightgreen to#green %s#lightgreen!" % (myhp,hishp,hisname) )
    if hishpbefore > hishp:
      es.tell(target,"#multi","#greenSoul Conversion#lightgreen from#green %s#lightgreen reduced you to#green %sHP#lightgreen!" % (myname,hishp) )
    else:
      es.tell(target,"#multi","#greenSoul Conversion#lightgreen from#green %s#lightgreen increased you to#green %sHP#lightgreen!" % (myname,hishp) )

class Agent(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"jetpack",0)
    est.removeweapon(user,2)
    gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_fiveseven"))
    if not server["gamestarted"]:
      wcsusers._set(user,"vengeance",2)
    dice = random.randint(1,20)
    level = getattr(entry,"skill3")
    if level >= dice:
      es.tell(user,"#multi", "#lightgreenWill#green Respawn #lightgreenthis round!")
    else:
      wcsusers._set(user,"vengeance",0)

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] != "fiveseven":
      return
    user = int(event_var["userid"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    x,y,z = es.getplayerlocation(user)
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill2")
    dice = random.randint(1,10)
    dmg = 0
    if level >= dice:
      ammo = int(playerlib.getPlayer(attacker).clip.secondary)
      if ammo < 20:
        dmg = skills.dealdamage(attacker,user,2*(20-ammo))
    level = getattr(entry,"skill1")
    dice = random.randint(1,33)
    if level >= dice:
      skills.drug(user,1.0+level*0.1)
      est.playplayer(attacker,"weapons/shotgun/shotgun_dbl_fire7.wav")
      es.setplayerprop(user,"CBasePlayer.m_fFlags",64.0)
      gamethread.delayed(0.1,es.setplayerprop,(user,"CBasePlayer.m_fFlags",1))
      skills.forcepush(attacker,user,500) 
      if dmg:
        est.csay(attacker,"Dealt +%s dmg and hit Concussive Shot!" % dmg)
      else:
        est.csay(attacker,"Concussive Shot!")
      return
    if dmg:
      est.csay(attacker,"Dealt +%s dmg!" % dmg)

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    respawn = wcsusers.get(user,"vengeance")
    if respawn == 0:
      return
    skills.respawn(user,1,100)
    level = getattr(entry,"skill3")
    skills.forcebomb(user,100+level*10,level*3,400+level*50)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if not level:
      return
    player = playerlib.getPlayer(user)
    frozen = player.freeze
    if frozen:
      est.csay(user,"You are frozen!")
      return False
    jetpack = wcsusers.get(user,"jetpack")
    if not jetpack:
      wcsusers.set(user,"jetpack",1)
      est.csay(user,"Flying!")
      es.setplayerprop(user,"CBasePlayer.m_fFlags",8)
      player.jetpack(1)
    else:
      wcsusers.set(user,"jetpack",0)
      est.csay(user,"No longer flying!")
      es.setplayerprop(user,"CBasePlayer.m_fFlags",1)
      player.jetpack(0)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 60 100 0.8 0 255 255 255 1" % (x,y,z) )
  
class Siren(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill1")
    if level:
      if level < 4:hp = 1
      elif level < 8:hp = 2
      elif level == 8:hp = 3
      bonus=level*3+6
      radius = 300+50*level
    else:
      return
    level = getattr(entry,"skill2")
    if level:
      cash = 1+level*3
      lowest = 4050-level*500
    else:
      cash = 4
      lowest = 3550
    level = getattr(entry,"skill3")
    if level:
      amount = level*0.01+0.02
      slowest = 1.0-level*0.1
    else:
      amount = 0.03
      slowest = 0.9
    level = getattr(entry,"skill4")
    if level:
      speed = level*0.03+1.01
    else:
      speed = 1.04
    level = getattr(entry,"skill5")
    if level:
      damage = int(level/2)
    else:
      damage = 1
    skills.siren_start(user,"heal",1,radius,hp,bonus,cash,lowest,amount,slowest,speed,damage)
    es.tell(user,"#multi","#greenSoothing#lightgreen Song!")

  def ultimate(self,user,entry,server):
    wcs.sirenmenu(user)

class Takeno(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill1")
    if level:
      gravity = 1.0-0.125*level
      wcsusers.set(user,"gravity",gravity)
      es.tell(user,"#multi", "#greenBuddha#lightgreen allows you to jump#green %i%s #lightgreenhigher!" % (int((1-gravity)*100),percent) )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) ) 
    level = getattr(entry,"skill2")
    if level:
      cash = level*500
      playerlib.getPlayer(user).cash += cash
      es.tell(user,"#multi","#greenWar Monger#lightgreen steals#green $%s#lightgreen from the local populace!" % cash)
    level = getattr(entry,"skill4")
    if level:
      hp = level*5+20
      wcsusers.set(user,"HPmaximum",hp+100)
      speed = 1.2+0.05*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenSnakes Arts#lightgreen provides#green %i #lightgreenhitpoints and#green %i%s #lightgreenfaster speed." % (hp,int((speed-1)*100),percent) )
    level = getattr(entry,"skill5")
    if level:
      invisp = 35+level*10
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#greenHiding Tactics #lightgreengrants you#green %i #lightgreenpercent invisibility" % invisp )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] != "knife":
      return
    user = int(event_var["userid"])    
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill3")
    dice = random.randint(1,6)
    if level >= dice:
      est.playplayer(user,"common/bass.wav")
      est.dropweapon(user,1)
      es.tell(user,"#multi","#green%s#lightgreen disarmed you!" % event_var["es_attackername"])
      es.tell(attacker,"#multi","#lightgreenYou disarmed #green%s#lightgreen!" % event_var["es_username"])
    dice = random.randint(1,3)
    if dice != 1:
      return
    level = getattr(entry,"skill6")
    if not level:
      return
    dmg = int(event_var["dmg_health"])
    dmg = skills.dealdamage(attacker,user,int(dmg*(1.0+0.25*level)))
    if dmg:
      est.csay(attacker,"Dealt +%s damage!" % dmg)
      est.csay(user,"Took +%s damage!" % dmg)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill7")
    if not level:
      return
    time = level*0.50+2
    gamethread.delayed(time,neve_end,(user,server["round"]))
    player = playerlib.getPlayer(user)
    player.setColor(100,100,255,1)
    player.setWeaponColor(100,100,255,1)
    skills.fade(user,time,2,0,1,1,150,20)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 7 #a 0 sprites/smoke.vmt %s %s %s 40 1" % (x,y,z) )
    es.tell(user,"#multi", "#lightgreenYou #greenMeditate#lightgreen to conceal yourself for#green %i#lightgreenseconds!" % time )

class Outlaw(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    est.removeweapon(user,2)
    gamethread.delayed(0.05,cstrike.giveNamedItem,args=(user,"weapon_elite"))
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill3")
    if level:
      speed = 1.1+0.08*level
      wcsusers.set(user,"speed",speed)
      gravity = 0.76-0.08*level
      wcsusers.set(user,"gravity",gravity)
      es.tell(user,"#multi", "#greenOutlaw Escape#lightgreen provides#green %i %s#lightgreen faster speed and#green %i %s#lightgreen lower gravity." % (int((speed-1)*100),percent,int((1-gravity)*100),percent) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z) )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
    level = getattr(entry,"skill4")
    if level:
      chance = level*5
      wcs.evasion_set(user,"dodge",chance)
      es.tell(user,"#multi","#greenOutlaw Charm#lightgreen allows you to evade#green %s%s#lightgreen of shots" % (chance,percent) )
    if server["round"] < 2:
      return
    gamethread.delayed(0.5,cstrike.giveNamedItem,(user,"weapon_m3"))

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])    
    attacker = int(event_var["attacker"])
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    level = getattr(entry,"skill1")
    dice = random.randint(1,10)
    if level >= dice:
      if skills.freeze(user,1):
        est.csay(user,"Frozen by %s" % event_var["es_attackername"])
        est.csay(attacker,"Froze %s" % event_var["es_username"])
        es.server.queuecmd("est_effect 11 #a 0 sprites/lgtning.vmt %s %s %s 1 2.3 90" % (x1,y1,z1) )
    level = getattr(entry,"skill2")
    dice = random.randint(1,30)
    if level >= dice:
      player = playerlib.getPlayer(user)
      ammo = int(player.clip.primary)-3
      if ammo < 0:
        ammo = 0
      player.clip.primary = ammo
      es.tell(user,"#multi", "#greenSharpshooter#lightgreen from#green %s#lightgreen hits you!" % event_var["es_username"] )
      es.tell(attacker,"#multi", "#greenSharpshooter#lightgreen affects#green  %s" % event_var["es_attackername"] )
      es.server.queuecmd("est_effect 3 #a 0 sprites/tp_beam001.vmt %s %s %s %s %s %s 3 4 2 15 11 167 255" % (x1,y1,z1+40,x2,y2,z2+40) )
      es.server.queuecmd("est_effect 11 #a 0 sprites/lgtning_noz.vmt %s %s %s 3 1 255" % (x1,y1,z1+40) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/physring1.vmt %s %s %s 100 300 3 40 20 0 14 0 41 255" % (x1,y1,z1+40) )    

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level:
      skills.showdown(user,277+100*level,2+level)
    es.tell(user,"#multi","fuckin bork come back later")

class MasterSniper(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"ultravision",2)
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill1")
    dice = random.randint(1,10)
    if (level+5) >= dice:
      est.removeweapon(user,1)
      est.removeweapon(user,2)
      gamethread.delayed(0.5,cstrike.giveNamedItem,(user,"weapon_deagle"))
      if server["round"] > 2:
        gamethread.delayed(0.5,cstrike.giveNamedItem,(user,"weapon_scout"))
        es.tell(user,"#multi","#greenSupplies#lightgreen have arrived giving you a Deagle and Scout!")
      else:
        es.tell(user,"#multi","#greenSupplies#lightgreen have arrived giving you a Deagle!")
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )
    level = getattr(entry,"skill2")
    if level:
      longjump = 0.2*float(level)+0.2
      wcsusers._set(user,"longjump",longjump)
      es.tell(user,"#multi","#lightgreenBy #greenTravelling Light#lightgreen you get#green %i%s #lightgreenlonger jumps." % (int(longjump*100),percent ) )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 30 100 0.8 255 100 100 255 1" % (x,y,z) )
    level = getattr(entry,"skill3")
    if level:
      time = 10-level
      tlevel = getattr(entry,"level")
      if tlevel > 70:
        time - .5*(math.floor((tlevel-70)/5))
        if tlevel > 105:
          time = 1.5
      wcsusers._set(user,"fadetime",time)
      wcsusers._set(user,"fadecount",0)
      es.tell(user,"#multi","#lightgreenYou are granted#green 75%%#lightgreen invis but shooting someone will remove it for#green %ss#lightgreen."%time)
      wcsusers.set(user,"invisp",75)

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] != "scout":
      return
    level = getattr(entry,"skill4")
    dice = random.randint(1,7)
    if (level+2) < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = float(event_var["dmg_health"])
    dmg = skills.dealdamage(attacker,user,int(dmg/5*level))
    if not dmg:
      return
    es.tell(attacker,"#multi","#greenPrecision Strike#lightgreen strikes for#green %s#lightgreen damage!" % dmg)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/laser.vmt %s %s %s %s %s %s 5 5 5 5 5 255 255" % (x1,y1,z1+45,x2,y2,z2+45) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    player = playerlib.getPlayer(user)
    hp = level*4+5
    player.health += hp
    es.tell(user,"#multi", "#greenFirst Aid#lightgreen heals#green %i HP." % hp )
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/purpleglow1.vmt %s %s %s 4 2 255" % (x,y,z+50) )

class Troll(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill1")
    if level:
      hp = 2+level
      maxhp = 110+level*10
      wcsusers.set(user,"HPmaximum",maxhp)
      skills.regenerationstart(user,hp,2,0,150,0,1.0)
    level = getattr(entry,"skill2")
    if level:
      longjump = 0.25*float(level)+0.25
      wcsusers._set(user,"longjump",longjump)
      es.tell(user,"#multi","#greenLong Leap#lightgreen grants you#green %i%% #lightgreenlonger jumps." %int(longjump*100) )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 30 100 0.8 255 100 100 255 1" % (x,y,z) )  
    level = getattr(entry,"skill3")
    if level:
      invisp = 30+10*level
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#greenChameleon Cloak#lightgreen grants you#green %s%s #lightgreeninvisibility." % (invisp,percent) )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] != "knife":
      return
    dice = random.randint(1,4)
    if dice != 4:
      return
    level = getattr(entry,"skill4")
    if not level:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = int(event_var["dmg_health"])
    dmg = int(dmg*(0.4+level*0.3))
    dmg = skills.dealdamage(attacker,user,dmg)
    if dmg > 0:
      es.tell(attacker,"#multi","#greenLoxodon Warhammer#lightgreen deals #green%s Damage!" % dmg)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    immune = skills.ultimatecheck(user)
    if immune:
      es.tell(user,"#multi","#green%s#lightgreen prevented your ultimate!" % es.getplayername(immune) )      
      return
    est.god(user,1)
    time = 1.0+0.25*level
    gamethread.delayed(time,est.god,(user,0))
    level = getattr(entry,"level")
    if level >= 100:
      dmg = level-90
      if dmg > 50:dmg = 50
      wcs.evasion_set(user,"resist",dmg)
      gamethread.delayed(5,wcs.evasion_set,(user,"resist",10))
      es.tell(user,"#multi","#greenImmortal#lightgreen for#green %ss#lightgreen!" % time)
      gamethread.delayed(time,es.tell,(user,"#multi","#green%s%s Immortal#lightgreen for#green 3s#lightgreen!" % (dmg,percent) ))
      gamethread.delayed(5,es.tell,(user,"#multi","#greenNo longer immortal!"))
    else:
      es.tell(user,"#multi","#greenImmortal#lightgreen for#green %ss#lightgreen!" % time)
      gamethread.delayed(time,es.tell,(user,"#multi","#greenNo longer immortal!"))
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 4 #a 0 sprites/lgtning.vmt %s 1 10 10 10 255 0 25 255" % user )

class Molecule(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill1")
    if level:
      speed = 1.10+0.04*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenCharged Suit#lightgreen allows you to run#green %i%s #lightgreenfaster!" % (int((speed-1)*100),percent) )
      es.server.queuecmd("est_effect 11 #a 0 sprites/physring1.vmt %s %s %s 3 10 255" % (x,y,z+15) )
    level = getattr(entry,"skill3")
    if level:
      dodge = 7*level
      wcs.evasion_set(user,"dodge",dodge)
      es.tell(user,"#multi","#greenStatic Field#lightgreen allows you to dodge#green %s%s#lightgreen of shots" % (dodge,percent) )
  
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,6)
    if dice != 1:
      return
    level = getattr(entry,"skill2")
    if not level:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = float(event_var["dmg_health"])
    damage = int(dmg*(0.2*float(level)+0.4))
    dmg = skills.dealdamage(attacker,user,damage)
    if not dmg:
      return
    est.csay(user,"Took +%i damage!" % dmg)
    est.csay(attacker,"+%i damage!" % dmg)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 255 255 255 255" % (x1,y1,z1+40,x2,y2,z2+40) )

  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] != "knife":
      return
    level = getattr(entry,"skill4")
    dice = random.randint(1,8)
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    if not es.getplayerprop(attacker, 'CBasePlayer.pl.deadflag'):
        return
    est.rocket(attacker,user)
    x,y,z = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.tell(attacker,"#multi","#greenMolecule's Suit#lightgreen electrocutes you as you knife him#lightgreen!!!")
    es.server.queuecmd("est_effect 3 #a 0 sprites/halo01.vmt %s %s %s %s %s %s 1 20 50 200 20 20 255" % (x,y,z+40,x2,y2,z2+40) )

  def evade(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    x,y,z = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_effect 3 #a 0 sprites/blueshaft1.vmt %s %s %s %s %s %s 1 5 5 255 255 255 255" % (x,y,z+40,x2,y2,z2+40) )
    if event_var["weapon"] != "knife":
      return
    level = getattr(entry,"skill4")
    dice = random.randint(1,8)
    if level < dice:
      return
    est.rocket(attacker,user)
    es.tell(attacker,"#multi","#greenMolecule's Suit#lightgreen electrocutes you as you knife him#lightgreen!!!")
    x,y,z = es.getplayerlocation(event_var["userid"])
    x2,y2,z2 = es.getplayerlocation(event_var["attacker"])
    es.server.queuecmd("est_effect 3 #a 0 sprites/halo01.vmt %s %s %s %s %s %s 1 20 50 200 20 20 255" % (x,y,z+40,x2,y2,z2+40) )

class Keldon(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"ultravision",1)
    wcsusers._set(user,"damage",0)
    tlevel = getattr(entry,"level")
    level = getattr(entry,"skill3")
    if level:
      dice = random.randint(1,4)
      if level >= dice:
        wcsusers._set(user,"ulti_immunity",1)
        est.armor(user,"=",200,1)
        es.tell(user,"#multi","#lightgreenThe#green Whispersilk Cloak#lightgreen will protect you from all#green ultimates#lightgreen this round as well as granting#green 200 Armor#lightgreen!")
      else:
        es.tell(user,"#multi","#lightgreenThe#green Whispersilk Cloak#lightgreen grants#green 200 Armor#lightgreen.")
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 40 2 10 10 1 0 255 100 255 1" % (x,y,z) )
      if tlevel >= 100:
        dmg = tlevel-75
        if dmg > 50:
          dmg = 50
        wcsusers._set(user,"bdmg_immune",dmg)
        es.tell(user,"#multi","#lightgreenThe#green Whispersilk Cloak#lightgreen grants#green %s%% #lightgreenbonus damage immunity."%dmg)
    if server["round"] < 3:
      return
    level = getattr(entry,"skill5")
    dice = random.randint(2,5)
    if (level+1) >= dice:
      gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_sg552"))
      if tlevel >= 50:
        dmg = dice+int((tlevel-50)/5)
        if dmg > 8:
          dmg = 8
        es.tell(user,"#multi","#greenAdvanced Weaponry#lightgreen and#green Keldon Expertise#lightgreen provides a #green+%s SG-552#lightgreen!" % dmg)
      else:
        dmg = dice
        es.tell(user,"#multi","#greenAdvanced Weaponry#lightgreen provides a #green+%s SG-552#lightgreen!" % dmg)
      wcsusers._set(user,"damage",dmg)

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    if event_var["weapon"] == "sg552":
      dmg = wcsusers.get(attacker,"dmg")
      if dmg:
        skills.dealdamage(attacker,user,dmg)
        est.csay(attacker,"+%s Dmg!" % dmg)
    strike = wcsusers.get(attacker,"firststrike")
    if strike:
      level = getattr(entry,"skill2")
      if level:
        dmg = level+2
        skills.dealdamage(attacker,user,dmg)
        est.csay(attacker,"Second Strike hits for %s damage!" % dmg)
        wcsusers._set(user,"firststrike",0)
    else:
      dice = random.randint(1,3)
      level = getattr(entry,"skill1")
      if dice != 1:
        level = 0
      if level:
        wcsusers._set(user,"firststrike",1)
        time = 0.5+level*0.5
        speed = 0.90-level*0.05
        skills.slow(user,time,speed)
        gamethread.delayed(time,wcsusers._set(user,"firststrike",0))
        x,y,z = es.getplayerlocation(user)
        es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 100 20 1 20 100 1 20 20 200 150 10" % (x,y,z+20))
        est.csay(attacker,"First Strike slows for %ss!" % time)
        est.csay(user,"First Strike slowed you for %ss!" % time)
    level = getattr(entry,"skill4")
    dice = random.randint(1,12)
    if level >= dice:
      cash = 250
      Person = playerlib.getPlayer(user)
      Player = playerlib.getPlayer(attacker)
      money = int(Person.cash)
      if money > 0:
        if cash > money:
          cash = money
        Player.cash += cash
        Person.cash -= cash
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 155 255 0 255" % (x1,y1,z1+40,x2,y2,z2+40) )
        es.tell(user,"#multi", "#lightgreenLost#green $%i #lightgreento#green %s" % (cash,event_var["es_attackername"]) )
        es.tell(attacker,"#multi", "#lightgreenYarr, ye #greenPlundered $%s #lightgreenswags off#green %s #lightgreen." % (cash,event_var["es_username"]) )

class Crusader(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill1")
    if level:
      skills.detectstart(user,0.25,100+40*level,1000+200*level)
      wcsusers._set(user,"detect",1)
      es.tell(user,"#multi","#greenGuiding Light#lightgreen reveals nearby enemies")
    level = getattr(entry,"skill3")
    if level:
      dodge = 2*level+10
      wcs.evasion_set(user,"resist",dodge)
      es.tell(user,"#multi","#greenShield of Faith#lightgreen blocks#green %s%s#lightgreen damage!" %(dodge,percent) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dice = random.randint(1,3)
    if dice != 1:
      return
    level = getattr(entry,"skill2")
    if not level:
      return
    time = 1.0+0.2*level
    skills.drug(user,time)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 20 0 50 255 255 150" % (x1,y1,z1+20,x2,y2,z2+60) )
    es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 20 0 50 255 255 150" % (x1,y1,z1+60,x2,y2,z2+20) )
    es.tell(user,"#multi", "#greenBanished#lightgreen by#green %s#lightgreen!" % event_var["es_attackername"] )
    es.tell(attacker,"#multi", "#greenBanished %s #lightgreenfor#green %s seconds#lightgreen!" % (event_var["es_username"],time) )

  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dice = random.randint(1,2)
    if dice != 1:
      return
    level = getattr(entry,"skill4")
    if not level:
      return
    skills.slow(attacker,0.90-level*0.03,1)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 20 0 150 150 150 150" % (x1,y1,z1+10,x2,y2,z2+60) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    skills.prayer(user,2*level+5,25+5*level)

class Necromancer(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    nt = getattr(entry,"skill1")
    if nt:
      wcsusers._set(user,"necromancer",nt)
    level = getattr(entry,"skill2")
    if level:
      delay = 6-level
      if nt == 5:hp = 3
      elif nt < 3: hp = 1
      else: hp = 2
      skills.regenerationstart(user,hp,delay,0,400,0,1.0)
      es.tell(user,"#multi","#greenUnholy Regeneration#lightgreen restores#green %sHP#lightgreen per#green %ss#lightgreen!" % (hp,delay) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    nt = wcsusers.get(attacker,"necromancer")
    dice = random.randint(1,15)
    level = getattr(entry,"skill3")
    if level >= dice:
      skills.slow(user,1.0-nt*0.05,2)
    level = getattr(entry,"skill4")
    dice = random.randint(1,5)
    if level >= dice:
      skills.dealdamage(attacker,user,nt*2)
      player = playerlib.getPlayer(attacker)
      health = player.health
      health -= nt
      if health < 1:
        health = 1
      player.health = health
      est.csay(attacker,"Frenzy deals +%s dmg for %s hp" % (nt*2,nt) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    nt = wcsusers.get(user,"necromancer")
    if nt < 2:
      es.tell(user,"#multi","#greenRaise Skeleton#lightgreen failed because you are too weak!")
      return
    users = []
    myteam = es.getplayerteam(user)
    for person in es.getUseridList():
      if not es.getplayerprop(person, 'CBasePlayer.pl.deadflag'):
        continue
      team = es.getplayerteam(person)
      if team != myteam:
        continue
      users.append(person)

    if len(users) == 0:
      es.tell(user,"#multi","#greenRaise Skeleton#lightgreen has nobody to target!")
      return False
    target = random.choice(users)
    hisname = es.getplayername(target)
    es.tell(user,"#multi","#greenRaise Skeleton#lightgreen chooses#green %s#lightgreen to be brought from the dead!" % hisname)
    es.tell(target,"#multi","#lightgreen Your teams#green Necromancer#lightgreen brings you back from the dead!")
    es.server.queuecmd("est_respawn %s" % target)
    x,y,z = es.getplayerlocation(user)
    gamethread.delayed(1,necro_revive,(target,nt,x,y,z))
    wcsusers._set(user,"necromancer",nt-2)
    if nt == 5:wcsusers._set(user,"regeneration",0.66)
    elif nt < 3:wcsusers._set(user,"regeneration",0)
    else:wcsusers._set(user,"regeneration",0.5)

class Beast(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    gamethread.delayed(1.5,est.invis_set,(user,[255,55,0,191],25))
    level = getattr(entry,"skill2")
    dice = random.randint(1,10)
    if level >= dice:
      wcsusers._set(user,"vengeance",1)
      es.tell(user,"#multi","#greenResurrect#lightgreen will respawn you this round!")
    else:
      wcsusers._set(user,"vengeance",0)
      es.tell(user,"#multi","#greenResurrect#lightgreen wont respawn you this round!")

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill1")
    dice = random.randint(1,10)
    if level >= dice:
      dmg = skills.dealdamage(attacker,user,10)
      if dmg > 0:
        est.csay(attacker,"Wrath dealt +%s damage!" % dmg)
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_Effect 3 #a 0 sprites/glow.vmt %s %s %s %s %s %s 0.5 20 60 255 50 0 255" % (x1,y1,z1+20,x2,y2,z2+20) )
    level = getattr(entry,"skill3")
    dice = random.randint(1,12)
    if level < dice:
      return
    skills.burn(attacker,user,3,level)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 30 30 255 0 0 150" % (x1,y1,z1+20,x2,y2,z2+20) )
    es.tell(user,"#multi","#lightgreenYou were burned by#green %s#lightgreen!" % event_var["es_attackername"])
    es.tell(attacker,"#multi","#greenInferno#lightgreen burns#green %s#lightgreen with #green%s#lightgreen damage for 3s!" % (event_var["es_username"],level) )

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    respawn = wcsusers.get(user,"vengeance")
    if respawn == 0:
      return
    skills.respawn(user,1,100)
    est.playplayer(user,"npc/antlion/attack_singl4.wav")
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/flamelet4.vmt %s %s %s 1 3.5 150" % (x,y,z) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if level == 0:return
    wcs.evasion_set(user,"fallresist",95,None)
    gamethread.delayed(4,wcs.evasion_set,(user,"fallresist",0,None))
    skills.teleport(user,600+100*level)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 500 3 100 100 0 255 55 0 255 10" % (x,y,z) )

class LordPit(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"demon",1)
    skulls = wcsusers.get(user,"skulls")
    if skulls:
      es.tell(user,"#multi","#lightgreenYou have colleceted#green %i#lightgreen skulls!" % skulls)
    level = getattr(entry,"skill4")
    dice = random.randint(1,25)
    if level >= dice:
      wcsusers._set(user,"vengeance",-1)
      es.tell(user,"#multi","#greenRitual of Rebirth#lightgreen has been prepared!")
    else:
      wcsusers._set(user,"vengeance",0)
      es.tell(user,"#multi","#greenRitual of Rebirth#lightgreen is not prepared!")
    level = getattr(entry,"skill3")
    if not level:
      return
    longjump = 0.2*float(level+1)
    wcsusers._set(user,"longjump",longjump)
    es.tell(user,"#multi","#greenDemon Wings#lightgreen grants you#green %i percent#lightgreen longer jumps." % (int(longjump*100) ) )
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 30 100 0.8 255 100 100 255 1" % (x,y,z) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill1")
    dice = random.randint(1,10)
    if level >= dice:
      skulls = wcsusers.get(attacker,"skulls")+1
      wcsusers._set(attacker,"skulls",skulls)
      x1,y1,z1 = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s2 8 6 100 155 255 255" % (x1,y1,z1+10,x2,y2,z2+10) )
      es.server.queuecmd("est_effect 3 #a 0 sprites/halo01.vmt %s %s %s %s %s %s2 5 5 50 20 255 255" % (x1,y1,z1+10,x2,y2,z2+10) )
      es.server.queuecmd("est_effect 3 #a 0 sprites/glow.vmt %s %s %s %s %s %s 2 5 5 0 0 255 255" % (x1,y1,z1+10,x2,y2,z2+10) )
      es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 255 200 0 255" % (x1,y1+50,z1+10,x2,y2,z2+10) )
      es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 255 200 0 255" % (x1,y1-50,z1+10,x2,y2,z2+10) )
      time = 0.5*level+0.5
      skills.drug(user,time)
      es.tell(attacker,"#multi", "#greenHell Trophy#lightgreen banishes for #green%ss#lightgreen and you gain a #greenSkull#lightgreen!" % int(time) )
    level = getattr(entry,"skill2")
    dice = random.randint(1,20)
    if level < dice:
      return
    est.bury(user,attacker,2)

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    respawn = wcsusers.get(user,"vengeance")
    if respawn == 0:
      return
    skills.respawn(user,3,100)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/flamelet4.vmt %s %s %s 1 3.5 150" % (x,y,z) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    skulls = wcsusers.get(user,"skulls")
    cost = int(level/1.5)
    if skulls < cost:
      es.tell(user,"#multi", "#lightgreenNot enough skulls#green need #green%i#lightgreen more" % (cost-skulls) )
      return False
    skulls -= int(5-(level/5)*2)
    wcsusers._set(user,"skulls",skulls)
    heal = level*5
    player = playerlib.getPlayer(user)
    hp = player.health
    maxhp = wcsusers.get(user,"HPmaximum")
    health = hp+heal
    if health > maxhp:
      health = maxhp
    player.health = health
    gravity = 1.0-float(level)*0.05
    wcsusers.set(user,"gravity",gravity)
    invisp = 20+10*level
    wcsusers._set(user,"invisp",invisp)
    alpha = 255-2.55*invisp
    player.setColor(140,140,140,alpha)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/yelflare1.vmt %s %s %s 2 2 255" % (x,y,z+40) )
    es.tell(user,"#multi", "#greenSacrifice of Blood#lightgreen costs#green %i #lightgreenskulls! You have#green %i #lightgreenskulls remaining." % (cost,skulls) )

class Rebel(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    player = playerlib.getPlayer(user)
    est.armor(user,"=",100,1)
    level = getattr(entry,"skill2")
    dice = random.randint(1,3)
    if level >= dice:
      est.removeweapon(user,2)
      gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_elite"))
      if level > 3:
        ammo = 5+level*5
        gamethread.delayed(2,player.setClip,("weapon_elite",ammo*2))
        es.tell(user,"#multi","#greenDual Elites#lightgreen with #green%s#lightgreen bullets in each!" % ammo)
      else:
        es.tell(user,"#multi","#greenDual Elites#lightgreen equipped!")
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )
    level = getattr(entry,"skill3")
    dice = random.randint(1,10)
    if level >= dice:
      dice = random.randint(1,40)
      if level >= dice:
        gamethread.delayed(1,skills.infiltrate,(user,1))
        es.tell(user,"#multi","#greenInfiltration#lightgreen allows you to Mole this round!")
      else:
        if int(event_var["es_userteam"]) == 2:
          est.setmodel(user,"player/t_phoenix")
        else:
          est.setmodel(user,"player/ct_urban")
        es.tell(user,"#multi","#greenInfiltration#lightgreen allows you to look like an enemy!")
    if server["round"] < 2:
      return
    level = getattr(entry,"skill1")
    dice = random.randint(1,3)
    if level < dice:
      return
    est.removeweapon(user,1)
    gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_ak47"))
    if level > 3:
      ammo = 30+10*level
      gamethread.delayed(2,player.setClip,("weapon_ak47",ammo*2))
      es.tell(user,"#multi","#greenAK47#lightgreen with #green%s clip#lightgreen drum locked and loaded." % ammo)
    else:
      es.tell(user,"#multi","#greenAK47#lightgreen locked and loaded.")
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill4")
    dice = random.randint(1,10)
    if (level+4) < dice:
      return
    skills.suicidebomb(user,100+15*level,50+20*level)
    es.server.queuecmd("est_Effect 4 #a 0 sprites/steam1.vmt %s 0.8 10 5 1 255 100 100 200" % user )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    users = []
    myteam = es.getplayerteam(user)
    for person in es.getUseridList():
      if es.getplayerprop(person, 'CBasePlayer.pl.deadflag'):
        continue
      team = es.getplayerteam(person)
      if team == myteam:
        continue
      users.append(person)

    if len(users) == 0:
      es.tell(user,"#multi","#greenRansom Demand#lightgreen has nobody to target!")
      return False
    target = random.choice(users)
    hisname = es.getplayername(target)
    immune = wcsusers.get(target,"ulti_immunity")
    dice = random.randint(1,5)
    if dice > level:
      es.tell(user,"#multi","#lightgreenYour #greenRansdom Demand#lightgreen was denied by #green%s#lightgreen!" % hisname)
      return
    if immune:
      es.tell(user,"#multi","#green%s#lightgreen doesn't listen to terrorist demands!" % hisname)
      return
    cash = 300*level
    skills.shake(target,1,10,10)
    player = playerlib.getPlayer(target)
    money = int(player.cash)
    myname = es.getplayername(user)
    if money >= cash:
      player.cash -= cash
      playerlib.getPlayer(user).cash += cash
      es.tell(user,"#multi","#lightgreenYou collected #green$%s#lightgreen from#green %s#lightgreen!" % (cash,hisname) )
      es.tell(target,"#multi","#lightgreenYou were forced to pay#green %s $%s#lightgreen in ransom money." % (myname,cash) )
    else:
      difference = cash-money
      damage = int(float(cash-money)/50+10)
      dmg = skills.dealdamage(user,target,damage)
      player.cash == 0
      playerlib.getPlayer(user).cash += difference
      es.tell(user,"#multi","#lightgreenYou dealt#green %s#lightgreen damage to#green %s#lightgreen because they couldn't fill your demands!!" % (dmg,hisname) )
      es.tell(target,"#multi","#lightgreenYou couldn't fill#green %s's#lightgreen demands and took#green %s#lightgreen damage because of it!" % (myname,dmg) )
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 3 60 100 0.8 0 100 255 100 10" % (x,y,z+40) )

class Vigilante(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    est.armor(user,"=",120,1)
    player = playerlib.getPlayer(user)
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill4")
    if level:
      hp = level*15
      wcs.evasion_set(user,"knifedodge",hp,0)
      es.tell(user,"#multi", "#greenSelf Defence#lightgreen training allows you to block#green %s%s#lightgreen of knife attacks!" % (hp,percent) )
    level = getattr(entry,"skill2")
    if level:
      est.removeweapon(user,2)
      gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_p228"))
      ammo = 10+10*level
      gamethread.delayed(2,player.setClip,("weapon_p228",ammo))
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )
      es.tell(user,"#multi", "#lightgreenGot your #greenTrusty Sidearm#lightgreen, never leave home without it")
    level = getattr(entry,"skill3")
    dice = random.randint(1,5)
    if level >= dice:
      player = playerlib.getPlayer(user)
      ammo = player.getAmmo("weapon_flashbang")
      if not ammo:
        gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_flashbang"))
      player.setAmmo("weapon_flashbang",3)
      ammo = player.getAmmo("weapon_hegrenade")
      if not ammo:
        gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_hegrenade"))
      player.setAmmo("weapon_hegrenade",2)
      es.tell(user,"#multi", "#lightgreenPicked up three#green Flashbangs#lightgreen and two #greenHigh Explosive Grenades")
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )
    if server["round"] < 3:
      return
    dice = random.randint(1,5)
    level = getattr(entry,"skill1")
    if level < dice:
      return
    gamethread.delayed(0,cstrike.giveNamedItem,args=(user,"weapon_m4a1"))
    es.tell(user,"#multi", "#lightgreenYou went to the #greenArmory#lightgreen and picked up an#green M4A1#lightgreen.")

  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] != "knife":
      return
    level = getattr(entry,"skill4")
    dice = random.randint(1,15)
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    est.rocket(attacker,user)
    es.tell(attacker,"#multi","#lightgreenUnfortunately, a true#green Vigilante#lightgreen knows #greenkung-fu#lightgreen.")
    es.tell(user,"#multi","#lightgreenYou send#green %s #lightgreenflying with your#green Counter Nut Punch#lightgreen." % event_var["es_attackername"])
    x,y,z = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_effect 3 #a 0 sprites/halo01.vmt %s %s %s %s %s %s 1 20 50 200 20 20 255" % (x,y,z+40,x2,y2,z2+40) )
  
  def shoot(self,event_var,entry,server):
    level = getattr(entry,"skill5")
    dice = random.randint(1,10)
    if level < dice:
      return
    user = int(event_var["userid"])
    weapon = event_var["weapon"]
    player = playerlib.getPlayer(user)
    if weapon in weapons["primary"]:
      player.clip.primary += 1
    elif weapon in weapons["secondary"]:
      player.clip.secondary += 1
      
class Ahmed(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    player = playerlib.getPlayer(user)
    est.armor(user,"=",100,1)
    level = getattr(entry,"skill2")
    dice = random.randint(1,3)
    if level >= dice:
      est.removeweapon(user,2)
      gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_glock"))
      if level > 2:
        ammo = 10+level*10
        gamethread.delayed(2,player.setClip,("weapon_glock",ammo))
        es.tell(user,"#multi","#lightgreenYour#green Glock#lightgreen is ready with#green %s#lightgreen rounds!" % ammo)
      else:
        es.tell(user,"#multi","#lightgreenYour#green Glock#lightgreen is ready with#green 20#lightgreen rounds!")
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )
    level = getattr(entry,"skill1")
    dice = random.randint(1,3)
    if level < dice:
      return
    est.removeweapon(user,1)
    gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_galil"))
    if level > 2:
      ammo = 45+5*level
      gamethread.delayed(2,player.setClip,("weapon_galil",ammo))
      es.tell(user,"#multi","#lightgreenYour#green Galil#lightgreen is ready with#green %s#lightrgeen rounds!" % ammo)
    else:
      es.tell(user,"#multi","#greenGalil#lightgreen is ready with#green 35#lightgreen rounds.")
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )
    
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill4")
    dice = random.randint(1,15)
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    time = 1.5+0.5*level
    skills.burn(attacker,user,time,3)
    dmg = skills.dealdamage(attacker,user,int(time*5))
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 30 30 255 0 0 150" % (x1,y1,z1+10,x2,y2,z2+10) )
    es.tell(user,"#multi", "#green%s #lightgreenburns you with#green Fires of War#lightgreen!" % event_var["es_attackername"] )
    es.tell(attacker,"#multi", "#greenFires of War#lightgreen burns#green %s" % event_var["es_username"] )
    
  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill3")
    if not level:
      return
    user = int(event_var["userid"])
    speed = 1.3+level*0.1
    skills.slow(user,3,speed)
    
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    immune = skills.ultimatecheck(user)
    if immune:
      es.tell(user,"#multi","#green%s#lightgreen prevented your Ahmed Jihad!" % es.getplayername(immune) )      
      return False
    es.tell(user,"#multi","#greenAllah Akbar!")
    est.kills(user,"+",1)
    est.deaths(user,"-",1)
    est.slay(user,user)
    skills.suicidebomb(user,200+30*level,70+20*level)

class Archimonde(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    player = playerlib.getPlayer(user)
    est.removeweapon(user,1)
    est.removeweapon(user,2)
    gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_awp"))
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill1")
    if level:
      longjump = 0.25+0.125*float(level)
      wcsusers._set(user,"longjump",longjump)
      gravity = 1.0-0.025*level
      wcsusers.set(user,"gravity",gravity)
      es.tell(user,"#multi", "#greenThe Defiler#lightgreen has#green %s%s #lightgreenlonger and#green %s%s #lightgreenhigher jumps" % (int(longjump*100),percent,int((1-gravity)*100),percent) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z) )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
    level = getattr(entry,"skill3")
    if level:
      invisp = 10+5*level
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#greenBlend#lightgreen grants you#green %s%% #lightgreeninvisibility." %invisp )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
    level = getattr(entry,"level")
    if level < 100: return
    wcsusers.set(user,"speed",1.1)

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill2")
    dice = random.randint(1,15)
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    time = 1+0.25*level
    skills.burn(attacker,user,time,10)
    x1,y1,z1 = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/fire.vmt %s %s %s 1 1 255" % (x1,y1,z1+50) )
    es.server.queuecmd("est_effect 11 #a 0 sprites/fire.vmt %s %s %s 1 1 255" % (x1+50,y1,z1) )
    es.server.queuecmd("est_effect 11 #a 0 sprites/fire.vmt %s %s %s 1 1 255" % (x1,y1+50,z1) )
    dmg = wcsusers.get(attacker,"damage")
    if dmg:
      damage = int(float(event_var["dmg_health"])*(dmg/100))
      dmg = skills.dealdamage(attacker,user,damage)
      if dmg:
        es.tell(attacker,"#multi", "#greenHidden Strike#lightgreen hit with#green %s#lightgreen damage!" % dmg)
      wcsusers._set(attacker,"trueshot",0)
      wcsusers._set(attacker,"pierceshot",0)
      wcsusers._set(attacker,"damage",0)

  def ultimate(self,user,entry,server):
    level1 = getattr(entry,"skill5")
    if not level1:return
    level = getattr(entry,"skill4")
    if level:
      wcsusers._set(user,"trueshot",100)
      wcsusers._set(user,"pierceshot",100)
      wcsusers._set(user,"damage",level*5)
    
    time = 1+float(level1)*0.50
    est.removeweapon(user,1)
    est.removeweapon(user,2)
    est.removeweapon(user,3)
    est.removeweapon(user,4)
    wcs.allowed(user,"none")
    player = playerlib.getPlayer(user)
    player.setColor(0,0,0,0)
    es.tell(user,"#multi", "#greenCloak of the Deciever#lightgreen... #greenfully invisible#lightgreen for#green %ss" % time )
    x1,y1,z1 = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 100 20 1 20 100 1 20 100 20 120 10" % (x1,y1,z1+20) ) 
    gamethread.delayed(time,archimonde_end,(user,server["round"]))
    
class Mercenary(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    player = playerlib.getPlayer(user)
    est.armor(user,"=",100,1)
    level = getattr(entry,"skill2")
    dice = random.randint(1,3)
    if level >= dice:
      est.removeweapon(user,2)
      gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_fiveseven"))
      if level > 2:
        ammo = 15+level*5
        gamethread.delayed(2,player.setClip,("weapon_fiveseven",ammo))
        es.tell(user,"#multi","#lightgreenYour#green FiveSeven#lightgreen is ready with#green %s#lightgreen rounds!" % ammo)
      else:
        es.tell(user,"#multi","#lightgreenYour#green FiveSeven#lightgreen is ready with#green 20#lightgreen rounds!")
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 255 0 255 1" % (x,y,z) )
    level = getattr(entry,"skill3")
    if level:
      speed = 1.05+0.05*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenSwift#lightgreen allows you to run#green %i%s #lightgreenfaster!" % (int((speed-1)*100),percent) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z) )
    level = getattr(entry,"skill5")
    if level:
      dmg = 10*level
      wcsusers._set(user,"bdmg_immune",dmg)
      es.tell(user,"#multi","#greenSkirmish Suit#lightgreen grants#green %s%s #lightgreen magic and explosion damage immunity." % (dmg,percent) )
    level = getattr(entry,"skill1")
    dice = random.randint(1,3)
    if level < dice:
      return
    est.removeweapon(user,1)
    gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_tmp"))
    if level > 2:
      ammo = 20+5*level
      gamethread.delayed(2,player.setClip,("weapon_tmp",ammo))
      es.tell(user,"#multi","#lightgreenYour#green TMP#lightgreen is ready with#green %s#lightgreen rounds!" % ammo)
    else:
      es.tell(user,"#multi","#greenTMP#lightgreen is ready with#green 30#lightgreen rounds.")
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 40 60 2 20 10 1 10 0 255 255 1" % (x,y,z) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = wcsusers.get(user,"marked")
    if event_var["weapon"] == "tmp":
      level = getattr(entry,"skill1")
      if level:
        damage = level+1+dmg
        dmg = skills.dealdamage(attacker,user,damage)
        est.csay(attacker,"+ %s dmg" % dmg)
    elif event_var["weapon"] == "fiveseven":
      level = getattr(entry,"skill2")
      if level:
        damage = level*2
        armor = level*4
        dmg = skills.dealdamage(attacker,user,damage)
        wcsusers._set(user,"marked",level)
        gamethread.delayed(7,wcsusers._set(user,"marked",0))
        est.armor(user,"-",armor)
        est.csay(attacker,"Shredded %s armor with + %s dmg" % (armor,dmg) )
    dice = random.randint(1,3)
    if dice != 1:
      return
    level = getattr(entry,"skill4")
    if not level:
      return
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect #a 0 sprites/tp_beam001.vmt %s %s %s %s %s %s 1 20 30 25 10 255 255" % (x1,y1,z1+20,x2,y2,z2+1620) )
    if est.get_attr(user,"slow") < 0:
      time = 0.5+level*0.5
      slow = 0.95-0.05*level
      skills.slow(user,time,slow)
      return
    player = playerlib.getPlayer(user)
    speed = player.speed
    speed -= 0.05
    if speed < 0.25:
      speed = 0.25
    player.speed = speed

  def shoot(self,event_var,entry,server):
    level = getattr(entry,"skill1")
    dice = random.randint(1,10)
    if level < dice:
      return
    user = int(event_var["userid"])
    if event_var["weapon"] == "tmp":
      player = playerlib.getPlayer(user)
      player.clip.primary += 1

class Circu(BaseClass):
  def spawn(self,event_var,entry,server):
    level = getattr(entry,"skill3")
    if not level:
      return
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    speed = 1.08+0.04*level
    wcsusers.set(user,"speed",speed)
    gravity = 1.00-0.08*level
    wcsusers.set(user,"gravity",gravity)
    es.tell(user,"#multi", "#greenHaste#lightgreen provides#green %i %s#lightgreen faster speed and#green %i %s#lightgreen lower gravity." % (int((speed-1)*100),percent,int((1-gravity)*100),percent) )
    es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z) )
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    level = getattr(entry,"skill1")
    if level:
      invisp = wcsusers.get(user,"invisp")
      if invisp <= level*20:
        player = playerlib.getPlayer(user)
        player.setColor(75,75,255,255)
      if invisp:
        wcsusers.set(user,"invisp",0)
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_Effect 3 #a 0 sprites/orangelight1.vmt %s %s %s %s %s %s 3 3 3 155 155 155 255" % (x1,y1,z1+30,x2,y2,z2+50) )
        es.tell(attacker,"#multi", "#greenRevealed %s#lightgreen!" % username )
    dice = random.randint(1,3)
    if dice == 1:
      level = getattr(entry,"skill2")
      if level:
        time = 1.00+0.25*level
        skills.drug(user,time)
        x1,y1,z1 = es.getplayerlocation(user)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 20 0 50 255 255 150" % (x1,y1,z1+20,x2,y2,z2+60) )
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 20 0 50 255 255 150" % (x1,y1,z1+60,x2,y2,z2+20) )
        es.tell(user,"#multi", "#greenBanished#lightgreen by#green %s#lightgreen!" % attackername )
        es.tell(attacker,"#multi", "#greenMind Twist#lightgreen banishes#green %s #lightgreenfor#green %s seconds#lightgreen!" % (username,time) )
    dice = random.randint(1,10)
    level = getattr(entry,"skill3")
    if level >= dice:
      slow = 0.80-0.05*float(level)
      skills.slow(user,2,slow)
      slow = int(slow*100)
      x1,y1,z1 = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_effect 3 #a 0 sprites/tp_beam001.vmt %s %s %s %s %s %s 2 5 5 255 0 0 255" % (x1,y1,z1+50,x2,y2,z2+50) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/tp_beam001.vmt %s %s %s 50 5 1.5 10 50 0 255 0 0 255 80" % (x1,y1,z1+50) )
      est.csay(user,"Slowed to %i%s" % (slow,percent) )
      est.csay(attacker,"Slowed to %i%s" % (slow,percent) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if not level:
      return
    users = []
    myteam = es.getplayerteam(user)
    for person in es.getUseridList():
      if es.getplayerprop(person, 'CBasePlayer.pl.deadflag'):
        continue
      team = es.getplayerteam(person)
      if team == myteam:
        continue
      users.append(person)
  
    if len(users) == 0:
      es.tell(user,"#multi","#greenLobotomy#lightgreen has nobody to target!")
      return False
    target = random.choice(users)
    hisname = es.getplayername(target)
    immune = wcsusers.get(target,"ulti_immunity")
    if immune:
      es.tell(user,"#multi","#greenLobotomy#lightgreen is blocked by #green%s#lightgreen!" % hisname)
      return
    skills.shake(target,1,10,10)
    skills.drug(target,0.2)
    gamethread.delayed(2,circu_lobotomy,(target,server["round"],level+1,user))
    es.tell(user,"#multi","#greenYou lobotimized #green%s#lightgreen!" % hisname)
    es.tell(target,"#multi","#greenYou've been lobotomized!")
    
class FireDrag(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    player = playerlib.getPlayer(user)
    player.setColor(255,55,0,200)
    level = getattr(entry,"skill3")
    if not level:
      return
    gravity = 1.0-0.05*level
    wcsusers.set(user,"gravity",gravity)
    es.tell(user,"#multi", "#greenDragon Wings#lightgreen allows you to jump#green %i%s #lightgreenhigher!" % (int((1-gravity)*100),percent) )  

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,20)
    level = getattr(entry,"skill1")
    if (level+4) < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    time = 0.5+0.5*level
    skills.burn(attacker,user,time)
    dmg = skills.dealdamage(attacker,user,int(time*3))
    x1,y1,z1 = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/fire.vmt %s %s %s 1 1 255" % (x1,y1,z1+50) )
    es.server.queuecmd("est_effect 11 #a 0 sprites/fire.vmt %s %s %s 1 1 255" % (x1+50,y1,z1) )
    es.server.queuecmd("est_effect 11 #a 0 sprites/fire.vmt %s %s %s 1 1 255" % (x1,y1+50,z1) )
    es.tell(user,"#multi", "#green %s #lightgreenhits you with#green Incinerate#lightgreen!" % attackername )
    es.tell(attacker,"#multi", "#greenIncinerate#lightgreen burns#green %s" % username )

  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,15)
    level = getattr(entry,"skill2")
    if (level+4) < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    time = 0.2*level
    skills.burn(attacker,time,user)
    x1,y1,z1 = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/fire.vmt %s %s %s 1 1 255" % (x1,y1,z1+50) )
    es.server.queuecmd("est_effect 11 #a 0 sprites/fire.vmt %s %s %s 1 1 255" % (x1+50,y1,z1) )
    es.server.queuecmd("est_effect 11 #a 0 sprites/fire.vmt %s %s %s 1 1 255" % (x1,y1+50,z1) )
    es.tell(user,"#multi", "#green %s #lightgreenhits you with#green Fire Shrieker#lightgreen!" % attackername )
    es.tell(attacker,"#multi", "#greenFire Shrieker#lightgreen burns#green %s" % username )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if level == 0:return
    wcs.evasion_set(user,"fallresist",95,None)
    gamethread.delayed(4,wcs.evasion_set,(user,"fallresist",0,None))
    skills.teleport(user,400+75*level)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 60 80 3 60 100 0.8 155 20 10 155 1" % (x,y,z) )

class ElvishKnight(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    player = playerlib.getPlayer(user)
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill2")
    if level:
      hp = 2+level
      maxhp = 110+level*5
      wcsusers.set(user,"HPmaximum",maxhp)
      skills.regenerationstart(user,hp,6,0,150,0,1.0)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 200 1 20 100 1 0 40 255 200 10" % (x,y,z) )
    level = getattr(entry,"skill3")
    if level:
      longjump = 0.2+0.1*level
      speed = 1.10+0.025*level
      wcsusers.set(user,"speed",speed)      
      wcsusers._set(user,"longjump",longjump)
      es.tell(user,"#multi","#greenElvish Leap#lightgreen grants you#green %s%s#lightgreen longjump and#green +%s%s#lightgreen speed." % (int(longjump*100),percent,int((speed-1)*100),percent) )
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 30 100 0.8 255 100 100 255 1" % (x,y,z) )

  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    level = getattr(entry,"skill1")
    dice = random.randint(1,20)
    if (level+2) >= dice:
      est.playplayer(user,"weapons/physcannon/energy_sing_flyby2.wav")
      player = playerlib.getPlayer(user)
      gamethread.delayed(0.5,player.setColor,(15,0,255,100))
      gamethread.delayed(1.0,player.setColor,(15,0,255,120))
      gamethread.delayed(1.5,player.setColor,(15,0,255,140))
      gamethread.delayed(2.0,player.setColor,(15,0,255,160))
      gamethread.delayed(2.5,player.setColor,(15,0,255,180))
      gamethread.delayed(3.0,est.invis_reset,user)
    level = getattr(entry,"skill4")
    dice = random.randint(1,10)
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dmg = float(event_var["dmg_health"])
    damage = int(dmg/20*level)
    dmg = skills.dealdamage(user,attacker,damage)
    est.csay(user,"Dealt %i Mirror Damage!" % dmg)
    est.csay(attacker,"Took %i Mirror Damage!" % dmg)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/purpleglow1.vmt %s %s %s %s %s %s 1 10 10 20 200 200 255" % (x1,y1,z1+20,x2,y2,z2+20) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,12)
    level = getattr(entry,"skill5")
    if level < dice:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]          
    dmg = int(float(level)/2)
    if skills.poisonstart(attacker,user,dmg,3):
      es.tell(attacker,"#multi","#LightgreenYou have poisoned#green %s #Lightgreendealing#Green %i #Lightgreendamage over 3s seconds!" % (username,dmg*3))
      es.tell(user,"#multi","#LightgreenYou have poisoned by#green %s #Lightgreen!" % attackername )
      x1,y1,z1 = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_Effect 3 #a 0 sprites/greenspit1.vmt %s %s %s %s %s %s 3 5 9 155 155 155 255" % (x1,y1,z1+35,x2,y2,z2+35) )
    else:
      es.tell(attacker,"#multi","#LightgreenYou have refreshed poison on#green %s #Lightgreen." % username)

class GoldenTail(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcs.evasion_set(user,"fallresist",95,None)
    wcsusers._set(user,"ultravision",1)
    level = getattr(entry,"skill1")
    if level:
      invisp = 36+5*level
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#greenSpirit Cloak#lightgreen grants you#green %s%% #lightgreeninvisibility." %invisp )
    level = getattr(entry,"skill2")
    if level:
      hp = 4+level
      skills.regenerationstart(user,hp,7,50,200,100+40*level,1.0)
    level = getattr(entry,"skill3")
    if level:
      chance = 1+4*level
      wcs.evasion_set(user,"dodge",chance,None)
      es.tell(user,"#multi", "#greenEvasion#lightgreen gives you#green %i%s #lightgreenchance to evade." % (chance,percent) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    dice = random.randint(1,5)
    if dice <= 2:
      level = getattr(entry,"skill4")
      if level:
        dmg = int(float(level)/2)+2
        if skills.poisonstart(attacker,user,dmg,5):
          es.tell(attacker,"#multi","#LightgreenYou have poisoned#green %s #Lightgreendealing#Green %i #Lightgreendamage over 5s seconds!" % (username,dmg*5))
          es.tell(user,"#multi","#LightgreenYou have poisoned by#green %s #Lightgreen!" % attackername )
          es.server.queuecmd("est_Effect 3 #a 0 sprites/greenspit1.vmt %s %s %s %s %s %s 3 5 9 155 155 155 255" % (x1,y1,z1+35,x2,y2,z2+35) )
        else:
          es.tell(attacker,"#multi","#LightgreenYou have refreshed poison on#green %s #Lightgreen." % username)
    dice = random.randint(1,4)
    if dice == 1:
      level = getattr(entry,"skill5")
      if level:
        time = int(level/2)+1
        skills.shake(user,time,20,100)
        est.csay(user,"%s shook you!" % attackername)
        est.csay(attacker,"Shook %s!" % username)
    dice = random.randint(1,12)
    level = getattr(entry,"skill7")
    if level < dice:
      return
    if skills.freeze(user,1):
      est.csay(user,"Frozen by %s" % attackername)
      est.csay(attacker,"Froze %s" % username)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 11 #a 0 sprites/lgtning.vmt %s %s %s 1 2.3 90" % (x,y,z) )

  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill6")
    if not level:
      return
    user = int(event_var["userid"])
    speed = 1.2+level*0.1
    skills.slow(user,3,speed)
    es.server.queuecmd("est_effect 4 #a 0 sprites/lgtning.vmt %s 1 10 10 10 255 0 25 255" % user )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill8")
    if level == 0:return
    skills.teleport(user,300*level)
    est.playplayer(user,"weapons/357/357_spin1.wav")
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 7 #a 0 sprites/smoke.vmt %s %s %s 40 3" % (x,y,z) )
    es.server.queuecmd("est_viewcoords %s x;es es_xtoken x2 server_var(x) , 0;es es_xtoken y2 server_var(x) , 1;es es_xtoken z2 server_var(x) , 2;est_effect 3 #a 0 dev/ocean.vmt %s %s %s server_var(x2) server_var(y2) server_var(z1) 1 0.1 0.1 255 14 41 255" % (user,x,y,z) )
    
class Mimic(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    est.armor(user,"=",100,1)
    race = wcsusers.get(user,"mimic")
    if not race:
      es.tell(user,"#multi","#greenNo race mimiced!")
      return
    es.tell(user,"#multi","#greenMimic#lightgreen: %s" % (wcs_races("racebase").get(race,"name")))
    level = getattr(entry,"skill3")
    dice = random.randint(1,10)
    if dice > level:
      return
    skillcfg = wcs_races("racebase").get(race,"skillcfg")
    if "player_ultimate" in skillcfg:
      count = 0
      for skill in skillcfg:
        count += 1
        cfg = str.lower(skill)
        if "player_ultimate" in cfg:
          skilllevel = getattr(entry, "skill" + str(count))
          ultimate = skilllevel-1
          break
    else:
      ultimate = 0
    cooldown = wcs_races("racebase").get(race,"ultimate_cooldown")
    try:
      cooldown = int(cooldown[ultimate])
    except (ValueError, IndexError):
      cooldown = int(cooldown[0])
    gamethread.delayed(0.1,wcs.ultimate_cooldown,(user,cooldown))
    n1 = wcsusers.get(user,"Mimic_1")
    n2 = wcsusers.get(user,"Mimic_2")
    n3 = wcsusers.get(user,"Mimic_3")
    n4 = wcsusers.get(user,"Mimic_4")
    n5 = wcsusers.get(user,"Mimic_5")
    n6 = wcsusers.get(user,"Mimic_6")
    n7 = wcsusers.get(user,"Mimic_7")
    n8 = wcsusers.get(user,"Mimic_8")
    n9 = wcsusers.get(user,"Mimic_9")
    path = wcs_races("racebase").get(race,"nickname")
    if hasattr(wcs.wcsskills,path):
      races = {
        'level': entry.level,
        'skill1': n1,
        'skill2': n2,
        'skill3': n3,
        'skill4': n4,
        'skill5': n5,
        'skill6': n6,
        'skill7': n7,
        'skill8': n8,
        'skill9': n9
      }
      entry = mimicfake(race=race,races=races)
      player_class = getattr(wcs.wcsskills,path)()
      player_skill = getattr(player_class,"spawn")(event_var,entry,server)
      return
    wcsusers._set(user,"skill_1",n1)
    wcsusers._set(user,"skill_2",n2)
    wcsusers._set(user,"skill_3",n3)
    wcsusers._set(user,"skill_4",n4)
    wcsusers._set(user,"skill_5",n5)
    wcsusers._set(user,"skill_6",n6)
    wcsusers._set(user,"skill_7",n7)
    wcsusers._set(user,"skill_8",n8)
    wcsusers._set(user,"skill_9",n9)
    es.doblock("wcs/shell/WCSskills/%s/skills_spawn" % path )

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    race = wcsusers.get(user,"mimic")
    if not race:
      return
    level = getattr(entry,"skill5")
    dice = random.randint(1,10)
    if dice > level:
      return
    n1 = wcsusers.get(user,"Mimic_1")
    n2 = wcsusers.get(user,"Mimic_2")
    n3 = wcsusers.get(user,"Mimic_3")
    n4 = wcsusers.get(user,"Mimic_4")
    n5 = wcsusers.get(user,"Mimic_5")
    n6 = wcsusers.get(user,"Mimic_6")
    n7 = wcsusers.get(user,"Mimic_7")
    n8 = wcsusers.get(user,"Mimic_8")
    n9 = wcsusers.get(user,"Mimic_9")
    path = wcs_races("racebase").get(race,"nickname")
    if hasattr(wcs.wcsskills,path):
      races = {
        'level': entry.level,
        'skill1': n1,
        'skill2': n2,
        'skill3': n3,
        'skill4': n4,
        'skill5': n5,
        'skill6': n6,
        'skill7': n7,
        'skill8': n8,
        'skill9': n9
      }
      entry = mimicfake(race=race,races=races)
      player_class = getattr(wcs.wcsskills,path)()
      player_skill = getattr(player_class,"death")(event_var,entry,server)
      return
    wcsusers._set(user,"skill_1",n1)
    wcsusers._set(user,"skill_2",n2)
    wcsusers._set(user,"skill_3",n3)
    wcsusers._set(user,"skill_4",n4)
    wcsusers._set(user,"skill_5",n5)
    wcsusers._set(user,"skill_6",n6)
    wcsusers._set(user,"skill_7",n7)
    wcsusers._set(user,"skill_8",n8)
    wcsusers._set(user,"skill_9",n9)
    es.doblock("wcs/shell/WCSskills/%s/skills_death" % path )

  def kill(self,event_var,entry,server):
    user = int(event_var["attacker"])
    es.tell(user,"hi")
    level = getattr(entry,"skill1")
    dice = random.randint(1,5)
    if level >= dice:
      mind = wcsusers.get(user,"mind")
      if not mind:
        player = int(event_var["userid"])
        race = wcsusers.get(player,"race")
        if race:
          allow = 1
          name = wcs_races("racebase").get(race,"name")
          allowed = wcs_races("racebase").get(race,"proficiency")
          if allowed != "all":allow = 0
          allowed = wcs_races("racebase").get(race,"pistolrace")
          if allowed != "":allow = 0
          allowed = wcs_races("racebase").get(race,"kniferace")
          if allowed != 0:allow = 0
          if race == 98:allow = 0
          if allow:
            wcsusers._set(user,"mimic",race)
            n1 = wcsusers.get(player,"skill_1")
            n2 = wcsusers.get(player,"skill_2")
            n3 = wcsusers.get(player,"skill_3")
            n4 = wcsusers.get(player,"skill_4")
            n5 = wcsusers.get(player,"skill_5")
            n6 = wcsusers.get(player,"skill_6")
            n7 = wcsusers.get(player,"skill_7")
            n8 = wcsusers.get(player,"skill_8")
            n9 = wcsusers.get(player,"skill_9")
            wcsusers._set(user,"Mimic_1",n1)
            wcsusers._set(user,"Mimic_2",n2)
            wcsusers._set(user,"Mimic_3",n3)
            wcsusers._set(user,"Mimic_4",n4)
            wcsusers._set(user,"Mimic_5",n5)
            wcsusers._set(user,"Mimic_6",n6)
            wcsusers._set(user,"Mimic_7",n7)
            wcsusers._set(user,"Mimic_8",n8)
            wcsusers._set(user,"Mimic_9",n9)
            es.tell(user,"#multi","#greenMimiced#lightgreen %s" % name)
          else:
            es.tell(user,"#multi","#lightgreenNot allowed to #greenMimic#lightgreen %s!" % name)
      else:
        es.tell(user,"#multi","#greenClosed-Mind#lightgreen prevents you from changing Mimic")
    race = wcsusers.get(user,"mimic")
    if not race:
      return
    level = getattr(entry,"skill2")
    dice = random.randint(1,10)
    if dice > level:
      return
    if allow:
      n1 = wcsusers.get(user,"Mimic_1")
      n2 = wcsusers.get(user,"Mimic_2")
      n3 = wcsusers.get(user,"Mimic_3")
      n4 = wcsusers.get(user,"Mimic_4")
      n5 = wcsusers.get(user,"Mimic_5")
      n6 = wcsusers.get(user,"Mimic_6")
      n7 = wcsusers.get(user,"Mimic_7")
      n8 = wcsusers.get(user,"Mimic_8")
      n9 = wcsusers.get(user,"Mimic_9")
    path = wcs_races("racebase").get(race,"nickname")
    if hasattr(wcs.wcsskills,path):
      races = {
        'level': entry.level,
        'skill1': n1,
        'skill2': n2,
        'skill3': n3,
        'skill4': n4,
        'skill5': n5,
        'skill6': n6,
        'skill7': n7,
        'skill8': n8,
        'skill9': n9
      }
      entry = mimicfake(race=race,races=races)
      player_class = getattr(wcs.wcsskills,path)()
      player_skill = getattr(player_class,"kill")(event_var,entry,server)
      return
    wcsusers._set(user,"skill_1",n1)
    wcsusers._set(user,"skill_2",n2)
    wcsusers._set(user,"skill_3",n3)
    wcsusers._set(user,"skill_4",n4)
    wcsusers._set(user,"skill_5",n5)
    wcsusers._set(user,"skill_6",n6)
    wcsusers._set(user,"skill_7",n7)
    wcsusers._set(user,"skill_8",n8)
    wcsusers._set(user,"skill_9",n9)
    es.doblock("wcs/shell/WCSskills/%s/skills_kill" % path )

  def attack(self,event_var,entry,server):
    user = int(event_var["attacker"])
    race = wcsusers.get(user,"mimic")
    if not race:
      return
    level = getattr(entry,"skill2")
    dice = random.randint(1,10)
    if dice > level:
      return
    n1 = wcsusers.get(user,"Mimic_1")
    n2 = wcsusers.get(user,"Mimic_2")
    n3 = wcsusers.get(user,"Mimic_3")
    n4 = wcsusers.get(user,"Mimic_4")
    n5 = wcsusers.get(user,"Mimic_5")
    n6 = wcsusers.get(user,"Mimic_6")
    n7 = wcsusers.get(user,"Mimic_7")
    n8 = wcsusers.get(user,"Mimic_8")
    n9 = wcsusers.get(user,"Mimic_9")
    path = wcs_races("racebase").get(race,"nickname")
    if hasattr(wcs.wcsskills,path):
      races = {
        'level': entry.level,
        'skill1': n1,
        'skill2': n2,
        'skill3': n3,
        'skill4': n4,
        'skill5': n5,
        'skill6': n6,
        'skill7': n7,
        'skill8': n8,
        'skill9': n9
      }
      entry = mimicfake(race=race,races=races)
      player_class = getattr(wcs.wcsskills,path)()
      player_skill = getattr(player_class,"attack")(event_var,entry,server)
      return
    wcsusers._set(user,"skill_1",n1)
    wcsusers._set(user,"skill_2",n2)
    wcsusers._set(user,"skill_3",n3)
    wcsusers._set(user,"skill_4",n4)
    wcsusers._set(user,"skill_5",n5)
    wcsusers._set(user,"skill_6",n6)
    wcsusers._set(user,"skill_7",n7)
    wcsusers._set(user,"skill_8",n8)
    wcsusers._set(user,"skill_9",n9)
    es.doblock("wcs/shell/WCSskills/%s/skills_attack" % path )

  def hurt(self,event_var,entry,server):
    user = int(event_var["userid"])
    race = wcsusers.get(user,"mimic")
    if not race:
      return
    level = getattr(entry,"skill4")
    dice = random.randint(1,10)
    if dice > level:
      return
    n1 = wcsusers.get(user,"Mimic_1")
    n2 = wcsusers.get(user,"Mimic_2")
    n3 = wcsusers.get(user,"Mimic_3")
    n4 = wcsusers.get(user,"Mimic_4")
    n5 = wcsusers.get(user,"Mimic_5")
    n6 = wcsusers.get(user,"Mimic_6")
    n7 = wcsusers.get(user,"Mimic_7")
    n8 = wcsusers.get(user,"Mimic_8")
    n9 = wcsusers.get(user,"Mimic_9")
    path = wcs_races("racebase").get(race,"nickname")
    if hasattr(wcs.wcsskills,path):
      races = {
        'level': entry.level,
        'skill1': n1,
        'skill2': n2,
        'skill3': n3,
        'skill4': n4,
        'skill5': n5,
        'skill6': n6,
        'skill7': n7,
        'skill8': n8,
        'skill9': n9
      }
      entry = mimicfake(race=race,races=races)
      player_class = getattr(wcs.wcsskills,path)()
      player_skill = getattr(player_class,"hurt")(event_var,entry,server)
      return
    wcsusers._set(user,"skill_1",n1)
    wcsusers._set(user,"skill_2",n2)
    wcsusers._set(user,"skill_3",n3)
    wcsusers._set(user,"skill_4",n4)
    wcsusers._set(user,"skill_5",n5)
    wcsusers._set(user,"skill_6",n6)
    wcsusers._set(user,"skill_7",n7)
    wcsusers._set(user,"skill_8",n8)
    wcsusers._set(user,"skill_9",n9)
    es.doblock("wcs/shell/WCSskills/%s/skills_hurt" % path )

  def shoot(self,event_var,entry,server):
    user = int(event_var["userid"])
    race = wcsusers.get(user,"mimic")
    if not race:
      return
    n1 = wcsusers.get(user,"Mimic_1")
    n2 = wcsusers.get(user,"Mimic_2")
    n3 = wcsusers.get(user,"Mimic_3")
    n4 = wcsusers.get(user,"Mimic_4")
    n5 = wcsusers.get(user,"Mimic_5")
    n6 = wcsusers.get(user,"Mimic_6")
    n7 = wcsusers.get(user,"Mimic_7")
    n8 = wcsusers.get(user,"Mimic_8")
    n9 = wcsusers.get(user,"Mimic_9")
    path = wcs_races("racebase").get(race,"nickname")
    if hasattr(wcs.wcsskills,path):
      races = {
        'level': entry.level,
        'skill1': n1,
        'skill2': n2,
        'skill3': n3,
        'skill4': n4,
        'skill5': n5,
        'skill6': n6,
        'skill7': n7,
        'skill8': n8,
        'skill9': n9
      }
      entry = mimicfake(race=race,races=races)
      player_class = getattr(wcs.wcsskills,path)()
      player_skill = getattr(player_class,"shoot")(event_var,entry,server)
      return
    wcsusers._set(user,"skill_1",n1)
    wcsusers._set(user,"skill_2",n2)
    wcsusers._set(user,"skill_3",n3)
    wcsusers._set(user,"skill_4",n4)
    wcsusers._set(user,"skill_5",n5)
    wcsusers._set(user,"skill_6",n6)
    wcsusers._set(user,"skill_7",n7)
    wcsusers._set(user,"skill_8",n8)
    wcsusers._set(user,"skill_9",n9)
    es.doblock("wcs/shell/WCSskills/%s/skills_shoot" % path )

  def evade(self,event_var,entry,server):
    user = int(event_var["userid"])
    race = wcsusers.get(user,"mimic")
    if not race:
      return
    n1 = wcsusers.get(user,"Mimic_1")
    n2 = wcsusers.get(user,"Mimic_2")
    n3 = wcsusers.get(user,"Mimic_3")
    n4 = wcsusers.get(user,"Mimic_4")
    n5 = wcsusers.get(user,"Mimic_5")
    n6 = wcsusers.get(user,"Mimic_6")
    n7 = wcsusers.get(user,"Mimic_7")
    n8 = wcsusers.get(user,"Mimic_8")
    n9 = wcsusers.get(user,"Mimic_9")
    path = wcs_races("racebase").get(race,"nickname")
    if hasattr(wcs.wcsskills,path):
      races = {
        'level': entry.level,
        'skill1': n1,
        'skill2': n2,
        'skill3': n3,
        'skill4': n4,
        'skill5': n5,
        'skill6': n6,
        'skill7': n7,
        'skill8': n8,
        'skill9': n9
      }
      entry = mimicfake(race=race,races=races)
      player_class = getattr(wcs.wcsskills,path)()
      player_skill = getattr(player_class,"evade")(event_var,entry,server)
      return
    wcsusers._set(user,"skill_1",n1)
    wcsusers._set(user,"skill_2",n2)
    wcsusers._set(user,"skill_3",n3)
    wcsusers._set(user,"skill_4",n4)
    wcsusers._set(user,"skill_5",n5)
    wcsusers._set(user,"skill_6",n6)
    wcsusers._set(user,"skill_7",n7)
    wcsusers._set(user,"skill_8",n8)
    wcsusers._set(user,"skill_9",n9)
    es.doblock("wcs/shell/WCSskills/%s/skills_evade" % path )

  def ultimate(self,user,entry,server):
    race = wcsusers.get(user,"mimic")
    if not race:
      return
    level = getattr(entry,"skill6")
    dice = random.randint(1,5)
    if dice > level:
      return
    skillcfg = wcs_races("racebase").get(race,"skillcfg")
    if "player_ultimate" in skillcfg:
      count = 0
      for skill in skillcfg:
        count += 1
        cfg = str.lower(skill)
        if "player_ultimate" in cfg:
          skilllevel = getattr(entry, "skill" + str(count))
          ultimate = skilllevel-1
          break
    else:
      ultimate = 0
    cooldown = wcs_races("racebase").get(race,"ultimate_cooldown")
    try:
      cooldown = int(cooldown[ultimate])
    except (ValueError, IndexError):
      cooldown = int(cooldown[0])
    gamethread.delayed(0.1,wcs.ultimate_cooldown,(user,cooldown))
    n1 = wcsusers.get(user,"Mimic_1")
    n2 = wcsusers.get(user,"Mimic_2")
    n3 = wcsusers.get(user,"Mimic_3")
    n4 = wcsusers.get(user,"Mimic_4")
    n5 = wcsusers.get(user,"Mimic_5")
    n6 = wcsusers.get(user,"Mimic_6")
    n7 = wcsusers.get(user,"Mimic_7")
    n8 = wcsusers.get(user,"Mimic_8")
    n9 = wcsusers.get(user,"Mimic_9")
    path = wcs_races("racebase").get(race,"nickname")
    if hasattr(wcs.wcsskills,path):
      races = {
        'level': entry.level,
        'skill1': n1,
        'skill2': n2,
        'skill3': n3,
        'skill4': n4,
        'skill5': n5,
        'skill6': n6,
        'skill7': n7,
        'skill8': n8,
        'skill9': n9
      }
      entry = mimicfake(race=race,races=races)
      player_class = getattr(wcs.wcsskills,path)()
      player_skill = getattr(player_class,"ultimate")(user,entry,server)
      return player_skill
    wcsusers._set(user,"skill_1",n1)
    wcsusers._set(user,"skill_2",n2)
    wcsusers._set(user,"skill_3",n3)
    wcsusers._set(user,"skill_4",n4)
    wcsusers._set(user,"skill_5",n5)
    wcsusers._set(user,"skill_6",n6)
    wcsusers._set(user,"skill_7",n7)
    wcsusers._set(user,"skill_8",n8)
    wcsusers._set(user,"skill_9",n9)
    es.set("wcs_userid",user)
    es.doblock("wcs/shell/WCSskills/%s/skills_ultimate" % path )

  def ability(self,user,entry,server):
    level = getattr(entry,"skill6")
    mind = wcsusers.get(user,"mind")
    if not mind:
      wcsusers._set(user,"mind",1)
      es.tell(user,"#multi","#lightgreenYou are now#green Closed-Minded")
    else:
      wcsusers._set(user,"mind",0)
      es.tell(user,"#multi","#lightgreenYou are now#green Open-Minded")

class DrowQueen(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"ultravision",3)
    gamethread.delayed(1,est.invis_set,(user,[100,10,150,153],40))
    level = getattr(entry,"skill1")
    if level:
      dodge = 2*level+9
      wcs.evasion_set(user,"dodge",dodge)
      es.tell(user,"#multi","#greenForesight#lightgreen lets your evade#green %s%s#lightgreen of shots!" %(dodge,percent) )
    level = getattr(entry,"skill3")
    dice = random.randint(1,10)
    if level >= dice:
      wcsusers._set(user,"ulti_immunity",1)
      es.tell(user,"#multi", "#greenWisdom#lightgreen grants#green Ultimate Immunity#lightgreen.")
    level = getattr(entry,"skill4")
    if level:
      skills.detectstart(user,0.25,200+10*level,1000+500*level)
      wcsusers._set(user,"detect",1)
      es.tell(user,"#multi","#greenKnowledge#lightgreen discovers nearby enemies")

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    level = getattr(entry,"skill2")
    dice = random.randint(1,12)
    if level < dice:
      return
    invisp = wcsusers.get(user,"invisp")
    if invisp:
      player = playerlib.getPlayer(user)
      player.setColor(255,255,255,255)
      wcsusers.set(user,"invisp",0)
      x1,y1,z1 = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_Effect 3 #a 0 sprites/orangelight1.vmt %s %s %s %s %s %s 3 3 3 155 155 155 255" % (x1,y1,z1+30,x2,y2,z2+50) )
      es.tell(attacker,"#multi", "#greenInsight#lightgreen destroyed#green%s's#lightgreen invisibility!" % username )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    skills.darknessstart(user,2.0+level,200+50*level)
    
class Lilith(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    secondary = wcsusers.get(user,"secondary")
    if secondary:
      gamethread.delayed(0.1,cstrike.giveNamedItem,(user,secondary))
    wcsusers._set(user,"lilith",0)
    wcsusers._set(user,"PhaseWalk",0)
    wcsusers._set(user,"primary",0)
    wcsusers._set(user,"secondary",0)
    gamethread.delayed(1,est.invis_set,(user,[100,10,150,153],40))
    level = getattr(entry,"skill3")
    if level:
      armor = 100+2*level
      est.armor(user,"=",armor,1)
      shield = 20+level*3
      wcs.evasion_set(user,"shield",shield,None)
      if level < 4: dmg = 1
      elif level < 10: dmg = 2
      else: dmg = 3
      skills.armoraurastart(user,dmg,0.5,armor,1000,0)
      es.tell(user,"#multi", "#greenDiva#lightgreen gives extra#green %s#lightgreen shield and #green%s#lightgreen shield regeneration out of combat." % (armor,dmg) )
    else:
      est.armor(user,"=",100,1)
      wcs.evasion_set(user,"shield",20,None)
      skills.armoraurastart(user,1,0.5,100,1000,0)
      shield = 20
      armor = 100
      dmg = 1
    es.tell(user,"#multi", "#greenEnergy Shield#lightgreen online. Resisting#green %s%s#lightgreen damage if you have armor." % (shield,percent) )
    level = getattr(entry,"skill3")
    if level: 
      if level < 4: hp = 1
      elif level < 10: hp = 2
      else: hp = 3
      skills.regenerationstart(user,hp,0.5,0,5000,0,1.0)
      es.tell(user,"#multi","#greenInner Glow#lightgreen will regenerate#green %s #lightgreenper second during#green Ultimate!" % hp*2)
      gamethread.delayed(0.5,wcsusers._set(user,"regeneration",0))
    if server["round"] < 2:
      return
    gamethread.delayed(0.1,cstrike.giveNamedItem,(user,"weapon_mp5navy"))
    player = playerlib.getPlayer(user)
    player.setColor(200,200,255,255)
    try:gamethread.delayed(0.5,player.setWeaponColor(50,50,120,255))
    except: pass

  def attack(self,event_var,entry,server):
    attacker = int(event_var["attacker"])
    lilith_end(attacker,server["round"])
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    if int(event_var["hitgroup"]) == 1:
      level = getattr(entry,"skill7")
      if level:
        dmg = float(event_var["dmg_health"])
        damage = int(dmg/20*level)
      else: damage = 0
    else: damage = 0
    x1,y1,z1 = es.getplayerlocation(user)
    if event_var["weapon"] in "mp5navy ump45 mac10 tmp p90":
      level = getattr(entry,"skill7")
      if level:
        dmg = int(level/2)
        x2,y2,z2 = es.getplayerlocation(attacker)
        es.server.queuecmd("est_Effect 3 #a 0 sprites/heatwave.vmt %s %s %s %s %s %s 0.50 5 5 100 100 100 255" % (x1,y1,z1+20,x2,y2,z2+20) )
      else: dmg = 0
    else: dmg = 0
    mylevel = getattr(entry,"level")
    enlevel = wcsusers.get(user,"level")
    if enlevel == 0:enlevel = 1
    level = int(50-20*float(mylevel)/float(enlevel))
    dice = random.randint(1,level)
    level = getattr(entry,"skill8")
    if level > dice:
      speed = 1.0-level*0.03
      skills.slow(user,2,speed)
      es.server.queuecmd("est_Effect 3 #a 0 sprites/heatwave.vmt %s %s %s 0.5 1 150" % (x1,y1,z1+20) )
    dmg += damage
    if dmg:
      dmg = skills.dealdamage(attacker,user,dmg)
      if dmg:
        est.csay(attacker,"+%s damage!" % dmg)

  def kill(self,event_var,entry,server):
    level = getattr(entry,"skill6")
    if not level:
      return
    attacker = int(event_var["attacker"])
    level2 = getattr(entry,"skill6")
    shield = 100+level*2
    player = playerlib.getPlayer(attacker)
    armor = player.armor
    diff = shield-armor
    hp = level
    if diff < hp:
      hp = diff
    if hp > 0:
      player.armor += hp
      est.csay(attacker,"Girl Power grants %s armour!" % hp)
    
  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    shield = wcsusers.get(user,"lilith")+1
    wcsusers._set(user,"lilith",shield)
    wcsusers._set(user,"armorregeneration",0)
    gamethread.delayed(3,shield_restore,(user,shield,1.0))

  def ultimate(self,user,entry,server):
    wcsusers._set(user,"regeneration",1)
    wcsusers._set(user,"PhaseWalk",1)
    secondary = playerlib.getPlayer(user).secondary
    wcsusers._set(user,"secondary",secondary)
    time = 1.5
    speed = wcsusers.get(user,"speed")
    level = getattr(entry,"skill1")
    if level:
      speed += level*0.05
    speed += 0.5
    level = getattr(entry,"skill5")
    if level:
      time += level*0.25
    est.god(user,1)
    player = playerlib.getPlayer(user)
    player.setSpeed(speed)
    wcs.allowed(user,"knife")
    est.removeweapon(user,1)
    est.removeweapon(user,2)
    es.delayed(0.05,"est_useweapon %s 3" % user)
    gamethread.delayed(0.10,player.setColor,(50,50,120,5))
    gamethread.delayed(0.10,player.setWeaponColor,(50,50,120,50))
    gamethread.delayed(time,lilith_end,(user,server["round"]))
    x1,y1,z1 = es.getplayerlocation(user)
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 200 20 1 20 100 1 50 50 120 120 10" % (x1,y1,z1+20) )
    es.tell(user,"#multi", "#greenPhase Walk#lightgreen... #greeninvisible#lightgreen for#green %ss" % time )
    
class Sentinel(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    est.removeweapon(user,1)
    est.removeweapon(user,2)
    if server["round"] > 2:
      gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_awp"))
    gamethread.delayed(0.2,cstrike.giveNamedItem,args=(user,"weapon_deagle"))
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill1")
    if level:
      speed = 1.00+0.05*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenHaste#lightgreen allows you to run#green %i%s #lightgreenfaster!" % (int((speed-1)*100),percent) )
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z) )
    level = getattr(entry,"skill2")
    if level:
      longjump = 0.25*float(level)
      wcsusers._set(user,"longjump",longjump)
      es.tell(user,"#multi","#greenCavalry#lightgreen grants you#green %i%s #lightgreenlonger jumps." % (int(longjump*100),percent ) )
    level = getattr(entry,"skill3")
    if level:
      dodge = 2+level
      wcs.evasion_set(user,"dmgimmune",dodge)
      es.tell(user,"#multi","#greenShield of Faith#lightgreen blocks#green %s#lightgreen damage per hit!" % dodge )
    level = getattr(entry,"skill4")
    if level:
      skills.detectstart(user,0.25,100+50*level,600+150*level)
      wcsusers._set(user,"detect",1)
      es.tell(user,"#multi","#greenDetection Wards#lightgreen reveal nearby enemies")

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] != "awp":
      return
    level = getattr(entry,"skill5")
    if not level:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    est.csay(attacker,"High Caliber Shot")
    es.setplayerprop(user,"CBasePlayer.m_fFlags",64.0)
    est.playplayer(user,"weapons/shotgun/shotgun_dbl_fire7.wav")
    gamethread.delayed(0.1,es.setplayerprop,(user,"CBasePlayer.m_fFlags",1))
    skills.forcepush(attacker,user,300+100*level)

class Slyph(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"jetpack",0)
    x,y,z = es.getplayerlocation(user)
    player = playerlib.getPlayer(user)
    level = getattr(entry,"skill1")
    if level:
      ammo = player.getAmmo("weapon_hegrenade")
      if not ammo:
        gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_hegrenade"))
      if level < 2:
        ammo = 1
      elif level < 4:
        ammo = 2
      else:
        ammo = 3
      player.setAmmo("weapon_hegrenade",ammo)
      es.tell(user,"#multi", "#greenPocket Tornadoes#lightgreen account for#green %i #lightgreengrenades." % ammo)
    level = getattr(entry,"skill2")
    if level:
      invisp = 10+level*10
      gamethread.delayed(1.5,player.setColor,(100,100,255,255-2.55*invisp))
      wcsusers._set(user,"invisp",invisp)
      es.tell(user,"#multi", "#greenDispersion#lightgreen grants you#green %s%% #lightgreeninvisibility."%invisp)
    level = getattr(entry,"skill4")
    if level:
      armor = 100+10*level
      est.armor(user,"=",armor,1)
      shield = 4*level
      wcs.evasion_set(user,"resist",shield,None)
      es.tell(user,"#multi", "#greenWind Shield#lightgreen provides#green %s #lightgreenarmor and#green %s%s#lightgreendamage resistance." % (armor,shield,percent) )

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    weapon = event_var["weapon"]
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill1")
    if weapon in weapons["grenades"]:
      level *= 4
    dice = random.randint(1,20)
    if level >= dice:
      skills.shake(user,3,10,100)
      est.physpush(user,0,0,350)
      es.server.queuecmd("est_effect 10 #a 0 sprites/glow.vmt %s %s %s 0 300 0.2 200 30 0 55 55 55 255 50" % (x,y,z) )
      es.server.queuecmd("est_effect 10 #a 0.2 sprites/glow.vmt %s %s %s 0 300 0.2 200 30 0 55 55 55 255 50" % (x,y,z+30) )
      es.tell(attacker,"#multi", "#greenTornado#lightgreen sends#green %s#lightgreen into the air!" % event_var["es_username"] )
    dice = random.randint(1,10)
    level = getattr(entry,"skill3")
    if level < dice:
      return
    dice = random.randint(1,10)
    damage = dice+level*2
    dmg = skills.dealdamage(attacker,user,damage)
    if not dmg:
      return
    est.csay(user,"Took +%i damage!" % dmg)
    est.csay(attacker,"+%i damage!" % dmg)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    player = playerlib.getPlayer(user)
    frozen = player.freeze
    if frozen:
      est.csay(user,"You are frozen!")
      return False
    jetpack = wcsusers.get(user,"jetpack")
    lvl = getattr(entry,"skill2")
    if not jetpack:
      wcsusers.set(user,"jetpack",1)
      invisp = 10+lvl*10+level*4
      wcsusers.set(user,"invisp",invisp)
      est.csay(user,"Flying with %s%% invisibility!" % invisp)
      es.setplayerprop(user,"CBasePlayer.m_fFlags",8)
      player.jetpack(1)
    else:
      wcsusers.set(user,"jetpack",0)
      invisp = 10+lvl*10
      wcsusers.set(user,"invisp",invisp)
      est.csay(user,"No longer flying, now have %s%% invisibility!" % invisp)
      es.setplayerprop(user,"CBasePlayer.m_fFlags",1)
      player.jetpack(0)

class Shopkeeper(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    es.tell(user,"#multi", "#lightgreenYou are playing a#green Shopkeeper#lightgreen and as such you can not buy#green any#lightgreen shop items. #defaultThis race is based on the TOTAL race level!")
    level = getattr(entry,"level")
    if level >= 10:
      armour = int(float(level-10)/10*5+120)
      est.armor(user,"=",armour,1)
      es.tell(user,"#multi", "#greenRing of Armor#lightgreen provided you with#green %i Armor#lightgreen!" % armour)
    if level >= 20:
      resist = int(float(level-30)/30+4)
      if resist > 8:resist = 8
      wcs.evasion_set(user,"resist",resist,None)
      es.tell(user,"#multi", "#greenEnchanted Chainmail#lightgreen reduces all damage by#green %s#lightgreen!" % resist)
    if level >= 30:
      if level >= 60:speed = 1.3
      else:speed = 1.15
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi", "#greenBoots of Speed#lightgreen allows you to run#green %i%s #lightgreenfaster!" % (int((speed-1)*100),percent) )
    if level >= 40:
      if level >= 80:invisp = 60
      else:invisp = 40
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#greenCloak of Shadows#lightgreen grants you#green %s%% #lightgreeninvisibility."%invisp )
    if level >= 80:
      dice = random.randint(1,7)
      if dice == 1:
        wcsusers._set(user,"ShopManItem",1)
        es.tell(user,"#multi", "#greenPot Luck#lightgreen rewards an#green Orb of Frost")
      elif dice == 2:
        wcsusers._set(user,"ShopManItem",2)
        es.tell(user,"#multi", "#greenPot Luck#lightgreen rewards an#green Orb of Fire")
      elif dice == 3:
        wcsusers._set(user,"ShopManItem",3)
        es.tell(user,"#multi", "#greenPot Luck#lightgreen rewards a#green Mask of Death")
      elif dice == 4:
        wcsusers._set(user,"ShopManItem",4)
        hp = int (float(level-80)/10+2)
        if hp > 10:hp = 10
        es.tell(user,"#multi", "#greenPot Luck#lightgreen rewards a#green +%s Ring of Regeneration" % hp)
      elif dice == 5:
        wcsusers._set(user,"ShopManItem",5)
        longjump = float(level-80)/100+0.25
        if longjump > 1.0:longjump = 1.0
        wcsusers._set(user,"longjump",longjump)
        gravity = 1-float(level-80)/100
        if gravity < 0.5:gravity = 0.5
        wcsusers.set(user,"gravity",gravity)
        es.tell(user,"#multi", "#greenPot Luck#lightgreen rewards#green Longjump")
      elif dice == 6:
        wcsusers._set(user,"ShopManItem",6)
        es.tell(user,"#multi", "#greenPot Luck#lightgreen rewards#green Chant of Infiltration")
        if server["gamestarted"]:
          gamethread.delayed(1,skills.infiltrate,(user,1))
        else:
          dice = 7
      if dice == 7:
        wcsusers._set(user,"ShopManItem",7)
        es.tell(user,"#multi", "#greenPot Luck#lightgreen rewards#green Stolen Uniform#lightgreen and#green Sunglasses")
        if int(event_var["es_userteam"]) == 2:
          est.setmodel(user,"player/t_phoenix")
        else:
          est.setmodel(user,"player/ct_urban")
        wcsusers._set(user,"flash_target","victim")
        wcsusers._set(user,"flash_duration",0.2)
        wcsusers._set(user,"flash_alpha",175)
    else:
      wcsusers._set(user,"ShopManItem",0)
    gamethread.delayed(5,wcs.saveguns,user)
    
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"level")
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    if level > 15:
      damage = int(float(level-15)/30+4)
      if damage > 8:
        damage = 8
      dmg = skills.dealdamage(attacker,user,damage)
      if dmg:
        est.csay(attacker,"Dealt +%s damage!" % dmg)
    if level < 80:
      return
    item = wcsusers.get(attacker,"ShopManItem")
    dice = random.randint(1,100)
    if item == 1:
      if dice > 40:
        return
      speed = 1-(float(level-75)/100)
      if speed < 0.7:speed = 0.7
      skills.slow(user,2,speed)
      speed = int(speed*100)
      est.csay(user,"Slowed to %s%s for 2s!" % (speed,percent) )
      est.csay(attacker,"Slowed enemy to %s%s for 2s!" % (speed,percent) )
    elif item == 2:
      burn = level-70
      if burn > 40:burn = 40
      if dice > burn:
        return
      skills.burn(attacker,user,3)
      est.csay(user,"Burned for 3s!")
      est.csay(attacker,"Burned enemy for 3s!")
    elif item == 3:
      vamp = level-60
      if vamp > 60:vamp = 60
      if dice > vamp:
        return
      dmg = float(event_var["dmg_health"])
      hp = int(dmg/5)
      playerlib.getPlayer(attacker).health += hp
      est.csay(attacker,"Leeched %s HP with Mask of Death" % hp)

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"level")
    if level < 5:
      return
    wcs.denial(user)
    es.tell(user,"#multi","#lightgreenYour weapons have been saved by #greenCrusaders Wish!")
    wcsusers._set(user,"ShopManItem",0)

  def ultimate(self,user,entry,server):
    player = playerlib.getPlayer(user)
    cash = int(player.cash)
    if cash <= 0:
      es.tell(user,"#multi","#lightgreenYou got no $$$s, bro")
      return
    users = []
    myteam = es.getplayerteam(user)
    for person in es.getUseridList():
      team = es.getplayerteam(person)
      if team != myteam:
        continue
      if person == user:
        continue
      users.append(person)
    length = len(users)
    if not length:
      es.tell(user,"#multi","#lightgreenYou cannot share money with only yourself.")
      return
    cashshare = int(float(cash)/length)
    level = getattr(entry,"level")
    xp = int(float(cash)/64+(level*cash/4000))
    wcs.wcs_givexp(user,xp,0,1)
    for person in users:
      playerlib.getPlayer(person).cash += cashshare
      es.tell(person,"#multi","#lightgreenYour #greenShopkeeper#lightgreen shares #green$%s#lightgreen with you!" % cashshare)
    player.cash = 0
    es.tell(user,"#multi","#lightgreenYou shared#green $%s #lightgreenacross your#green %s teammates#lightgreen for#green %sXP#lightgreen!" % (cash,length,xp) )
    
class AKSniper(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"zoom",0)
    player = playerlib.getPlayer(user)
    est.removeweapon(user,2)
    gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_glock"))
    
    x,y,z = es.getplayerlocation(user)
    level = getattr(entry,"skill2")
    if level:
      invisp = 15+5*level
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#lightgreenBy following the #greenPath of the Hidden#lightgreen you gain#green %s%%#lightgreen invisibilty."%invisp )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
    if server["round"] < 2:
      return
    level = getattr(entry,"skill1")
    ammo = level*3+30
    es.tell(user,"#multi", "#greenJarmen Kell#lightgreen gets a#green %s clip AK47" % ammo)
    gamethread.delayed(0,cstrike.giveNamedItem,args=(user,"weapon_ak47"))
    gamethread.delayed(2,player.setClip,("weapon_ak47",ammo))

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill3")
    if not level:
      return
    dice = random.randint(level,17)
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    if dice == 17:
      skills.shake(user,1,10,100)
      est.physpush(user,0,0,300)
      es.tell(attacker,"#multi", "#lightgreen An#green Explosive#lightgreen bullet pushed#green %s #lightgreenupwards!" % event_var["es_username"] )
    elif dice == 16:
      if skills.freeze(user,1):
        es.tell(attacker,"#multi", "#lightgreen A#green Cryo#lightgreen bullet froze#green %s #lightgreenfor a second!" % event_var["es_username"] )
    elif dice == 15:
      skills.burn(attacker,user,2)
      es.tell(attacker,"#multi", "#lightgreen An#green Incindienary#lightgreen bullet burns#green %s #lightgreenfor 2 seconds!" % event_var["es_username"] )
    elif dice >= 12:
      est.armor(user,"-",25)
      es.tell(attacker,"#multi", "#lightgreen An#green AP#lightgreen bullet shreds 25 armor off#green %s #lightgreen!" % event_var["es_username"] )
    else:
      return
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 200 3 10 50 1 100 100 25 255 3" % (x,y,z+60) )

  def kill(self,event_var,entry,server):
    level = getattr(entry,"skill4")
    if not level:
      return
    attacker = int(event_var["attacker"])
    armor = level*4
    est.armor(attacker,"+",armor,1)
    playerlib.getPlayer(attacker).health += level
    es.tell(attacker,"#multi", "#lightgreenYou#green scavenged %s #lightgreenarmor and#green %s #lightgreenhealth." % (armor,level) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if not level:
      return
    zoom = wcsusers.get(user,"zoom")
    if not zoom:
      wcsusers._set(user,"zoom",1)
      es.setplayerprop(user,"CBasePlayer.m_iFOV",85-4*level)
    else:
      wcsusers._set(user,"zoom",0)
      es.setplayerprop(user,"CBasePlayer.m_iFOV",0)
#------------------------------- : ) ------------------------------------
class Spencer(BaseClass):
  def spawn(self,event_var,entry,server):
    level = getattr(entry,"skill1")
    if not level:
      return
    user = int(event_var["userid"])
    speed = 1.08+0.02*level
    wcsusers.set(user,"speed",speed)
    hp = level*5
    es.tell(user,"#multi", "#lightgreenYour #greenMilitary Training#lightgreen grants you#green %i%% #lightgreenspeed and #green%i #lightgreenhealth!" % (int((speed-1)*100),hp) )
    wcsusers.set(user,"HPmaximum",hp+100)
      
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill2")
    dice = random.randint(1,100)
    if dice > 3.3*level:
      return
    user = int(event_var["userid"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    attacker = int(event_var["attacker"])
    if not skills.freeze(user,1):
      return
    es.tell(user,"#multi","#greenTazed #lightgreenby #green%s#lightgreen." % attackername)
    es.tell(attacker,"#multi","#greenzapped %s#lightgreen." % username)
      
  def kill(self,event_var,entry,server):
    user = int(event_var["attacker"])
    level = getattr(entry,"skill3")
    if not level:
      return
    playerlib.getPlayer(user).health += 4+level*2    
    
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    level2 = getattr(entry,"skill5")
    if level:
        es.server.queuecmd("est_viewplayer %s x;es wcs_spencer %s server_var(x) %s %s" % (user,user,level,level2) )
  
class Isaac(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill1")
    if level:
      wcsusers._set(user,"djinn",1)
      hp = level*5+5
      wcsusers.set(user,"HPmaximum",hp+100)
      speed = 1.06+.02*level
      wcsusers.set(user,"speed",speed)
      dmg = (3*level-1)
      es.tell(user,"#multi", "#greenEarth Djinn#lightgreen empowers your body with#green %i #lightgreenhealth, #green %i%s #lightgreenspeed, #lightgreenand #green %i%% #lightgreendamage bonus!" % (hp,int((speed-1)*100),percent,dmg) )
    level = getattr(entry,"skill2")
    if level:
      skills.regenerationstart(user,3+level,5,0,150,0,1.0)
    dice = random.randint(1,14)
    level = getattr(entry,"skill4")
    if level >= dice:
      wcsusers._set(user,"vengeance",1)
      es.tell(user,"#multi", "#greenReincarnation#lightgreen will respawn you this round!")
    else:
      wcsusers._set(user,"vengeance",0)
      es.tell(user,"#multi", "#greenReincarnation#lightgreen failed and#green won't#lightgreen respawn you!")

  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill1")
    djinn = wcsusers.get(attacker,"djinn")
    if level and djinn == 1:
      attackername = event_var["es_attackername"]
      username = event_var["es_username"]
      dmg = float(event_var["dmg_health"])
      dmg = dmg*(.03*level-.01)
      damage = skills.dealdamage(attacker,user,dmg)
      if damage > 0:
        est.csay(user,"%s dealt +%i dmg!" % (attackername,damage) )
        est.csay(attacker,"Dealt +%i dmg to %s!" % (damage,username) )
    level = getattr(entry, "skill3")
    dice = random.randint(1,20)
    if dice >= level+1:
      return
    damage = skills.dealdamage(attacker,user,level+1)
    if not damage:
      return
    skills.shake(user,2,20,100)
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    est.csay(user,"%s shook you and dealt +%i dmg!" % (attackername,damage))
    est.csay(attacker,"Shook %s and dealt +%i dmg!" % (username,damage))

  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    respawn = wcsusers.get(user,"vengeance")
    if respawn == 0:
      return
    level = getattr(entry,"skill4")
    hp = 5+5*level
    skills.respawn(user,1,hp)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    users = []
    myteam = es.getplayerteam(user)
    for person in es.getUseridList():
      if es.getplayerprop(person, 'CBasePlayer.pl.deadflag'):
        continue
      team = es.getplayerteam(person)
      if team == myteam:
        continue
      users.append(person)
      
    if len(users) == 0:
      es.tell(user,"#multi","#greenJudgement#lightgreen has nobody to target!")
      return False
    target = random.choice(users)
    hisname = es.getplayername(target)
    immune = wcsusers.get(target,"ulti_immunity")
    if immune:
      es.tell(user,"#multi","#greenJudgement#lightgreen is blocked by #green%s#lightgreen!" % hisname)
      return
    wcsusers._set(user,"djinn",0)
    gamethread.delayed(30,wcsusers._set(user,"djinn",0))
    damage = 7+level*4
    dmg = skills.dealdamage(user,target,damage)
    skills.shake(target,2,20,100)
    skills.slow(target,2,.7)
    player = playerlib.getPlayer(user)
    myname = es.getplayername(user)
    es.tell(user,"#multi","#greenJudgement#lightgreen hits#green %s #lightgreenfor#green %i damage#lightgreen!" % (hisname,dmg) )
    es.tell(target,"#multi","#lightgreenLost#green %i hp#lightgreen to #greenJudgement#lightgreen from#green %s" % (dmg,myname) )
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 3 60 100 0.8 0 200 100 200 1" % (x,y,z+40) )

class Everlasting(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill1")
    dice = random.randint(1,5)
    if level >= dice:
      wcsusers._set(user,"ulti_immunity",level)
      es.tell(user,"#multi", "#greenEnergy Sphere#lightgreen grants#green Ultimate Immunity#lightgreen.")
    level = getattr(entry,"skill4")
    if level:
      hp = int(level/1.5)
      time = 8.0/level
      skills.regenerationstart(user,hp,time,0,150,0,1.0)
      es.tell(user,"#multi","#greenSoothing Waters#lightgreen provide#green %i hitpoints #lightgreenevery#green %i #lightgreenseconds!" % (hp,time) )
    level = getattr(entry,"skill5")
    if level:
      speed = 1.0-level*.02
      wcsusers.set(user,"speed",speed)
      gravity = 1.0+level*.02
      wcsusers.set(user,"gravity",gravity)
      est.armor(user,"=",100,1)
      shield = 10*level
      wcs.evasion_set(user,"shield",shield,None)
      skills.armoraurastart(user,level,2,100,60,30)
      es.tell(user,"#multi","#greenEarth Shield#lightgreen is#green active#lightgreen and will resist#green %i%s#lightgreen if you have armor and#green %i%s#lightgreen if you dont." % (shield,percent,level,percent) )

    def attack(self,event_var,entry,server):
      if event_var["es_userhealth"] < 0:
        return
      user = int(event_var["userid"])
      attacker = int(event_var["attacker"])
      attackername = event_var["es_attackername"]
      username = event_var["es_username"]      
      level = getattr(entry,"skill2")
      dice = random.randint(1,15)
      if level >= dice:
        time = 0.3*level
        skills.burn(attacker,user,time)
        dmg = skills.dealdamage(attacker,user,int(time*3))
        x1,y1,z1 = es.getplayerlocation(attacker)
        x2,y2,z2 = es.getplayerlocation(user)
        es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 30 30 255 0 0 150" % (x1,y1,z1+10,x2,y2,z2+10) )
        es.tell(attacker,"#multi","#greenFlame Strike#lightgreen burns#green %s" % username)
        es.tell(user,"#multi", "#greenFlame Strike#lightgreen from#green %s #lightgreenburns you!" % attackername)              
      level = getattr(entry,"skill3")
      dice = random.randint(1,30)
      if level >= dice:
        skills.freeze(user,1)

class GrimReaper(BaseClass):
    def spawn(self,event_var,entry,server):
        user = int(event_var["userid"])
        wcsusers._set(user,"kniferace",1)
        wcsusers._set(user,"ultravision",2)
        level = getattr(entry,"skill1")
        if level:
            speed = 1.0+0.1*level
            wcsusers.set(user,"speed",speed)
            gravity = 1.0-.05*level
            wcsusers.set(user,"gravity",gravity)
        level = getattr(entry,"skill3")
        if level:
            dmg = 5*level
            wcs.evasion_set(user,"resist",dmg)
            es.tell(user,"#multi","#greenReaper Perserverence#lightgreen lets you resist #green%i%% #lightgreenof all damage!" % dmg)
    def attack(self,event_var,entry,server):
        if event_var["es_userhealth"] < 0:
            return
        if event_var["weapon"] != "knife":
            return
        user = int(event_var["userid"])
        attacker = int(event_var["attacker"])
        level = getattr(entry,"skill4")
        if level:
            dmg = float(event_var["dmg_health"])
            dmg = .05*level*dmg
            damage = skills.dealdamage(attacker,user,dmg)
            if damage:
                es.tell(attacker,"#multi","#greenDeath Scythe#lightgreen deals#green %i #lighgreendamage" % dmg)
            
    def hurt(self,event_var,entry,server):
        user = int(event_var["userid"])
        if event_var["es_userhealth"]:
            level = getattr(entry,"skill2")
            if level:
                time = 0.55-0.05*level
                gamethread.delayed(time,skills.unslow,(user))
                gamethread.delayed(time,skills.unfreeze,(user))
    
class KilJaeden(BaseClass):
    def spawn(self,event_var,entry,server):
        user = int(event_var["userid"])
        wcsusers._set(user,"ultravision",2)
        wcsusers._set(user,"kjscout",1)
        
        level = getattr(entry,"skill1")
        if level:
            invisp = 80+level*5
            gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
            team = es.getplayerteam(user)
            if team == 2:
                es.server.queuecmd("es_xset kjs 0;wcs_kjscout %s kjs;es wcs_setindexcolour server_var(kjs) 255 150 150 255 350 450;py_keysetvalue WCSuserdata %s kjscout server_var(kjs)" % (user,user) )
            else:
                es.server.queuecmd("es_xset kjs 0;wcs_kjscout %s kjs;es wcs_setindexcolour server_var(kjs) 150 150 255 255 350 450;py_keysetvalue WCSuserdata %s kjscout server_var(kjs)" % (user,user) )            
            es.delayed(1,"est_useweapon %s 3" % user)
            es.tell(user,"#multi", "#greenThe Deciever is#green %d%% #lightgreen invisible." % invisp )
        
        level = getattr(entry,"skill2")
        if level:
            lowgrav = .7-level*.1
            wcsusers.set(user,"gravity",lowgrav)
            
            speed = 1.1+level*.05
            wcsusers.set(user,"speed",speed)
            
            x,y,z = es.getplayerlocation(user)
            es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0" % (x,y,z))
            es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 3 10 0 0 0 200 25 255 0" % (x,y,z+50))
            
    def death(self,event_var,entry,server):
        user = int(event_var["userid"])
        kjscout = wcsusers.get(user,"kjscout")
        es.server.queuecmd("es wcs_setindexcolour %s 150 150 255 0 0 0" % kjscout)
       
    def attack(self,event_var,entry,server):
        level = getattr(entry,"skill3")
        if level:
            dice = random.randint(1,10)
            if level >= dice:
                user = int(event_var["userid"])
                attacker = int(event_var["attacker"])
                est.playplayer(user,"common/bass.wav")
                est.dropweapon(user,1)
                attackername = event_var["es_attackername"]
                username = event_var["es_username"] 
                es.tell(user,"#multi","#green%s #lightgreen forced you to #green drop #lightgreenyour primary weapon!" % attackername)
                es.tell(attacker,"#multi","#greenClaw Strike#lightgreen forces#green %s #lightgreento drop his #greenprimary weapon" % username)
    def ultimate(self,user,entry,server):
        level = getattr(entry,"skill4")
        if level:
            dice = random.randint(1,200)
            steamID = str(playerlib.getPlayer(user).steamid)
            if steamID == "STEAM_0:1:19477547":
                level = 1000
            if dice <= level:
                es.msg("#multi","#lightgreenThe #greenEye of Sargeras#lightgreen has awoken#green Zombie Yiyas#lightgreen only #greenshooting him#lightgreen can defeat it!!")
                player = playerlib.getPlayer(user)
               
                player.health = 300
                wcs.evasion_set(user,"resist",75,None)
                
                wcsusers._set(user,"bdmg_immune",100)
                wcsusers._set(user,"NoHeal",1)
                wcsusers._set(user,"regeneration",0)
                wcsusers.set(user,"gravity",1.5)
                
                team = es.getplayerteam(user)
                if team == 2:
                    player.setModel("player/ics/t_guerilla_z/t_guerilla")
                else:
                    player.setModel("player/ics/zombielunatic/urban")
                
                player.setColor(255,0,0,255)
            else:
                level = int(level) + 4
                es.msg("#multi","#lightgreenThe #greenEye of Sargeras#lightgreen has been activated for#green %s #lightgreenseconds!" % level)

class Pistoleer(BaseClass):
    def spawn(self,event_var,entry,server):
        user = int(event_var["userid"])
        
        level = getattr(entry,"skill2")
        if level:
            chance = 1+3*level
            wcs.evasion_set(user,"fallresist",95,None)
            wcs.evasion_set(user,"dodge",chance,None)
            es.tell(user,"#multi","#greenAlertness#lightgreen gives you#green %s#lightgreen%% chance to evade." % chance)
        
        level = getattr(entry,"skill3")
        if level:
            invisp = 5*level+30
            gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
            es.tell(user,"#multi","#lightgreenYou are granted#green %s#lightgreen%% invis!" % invisp)
        
        if getattr(entry,"level") > 50:
            es.tell(user,"#multi","#lightgreen Aim for the #greenhead!")     
    def attack(self,event_var,entry,server):
        level = getattr(entry,"skill1")
        attacker = int(event_var["attacker"])
        user = int(event_var["userid"])
        if level:
            damage = level
            tlevel = getattr(entry,"level")
            if tlevel > 50:
                dmgdealt = float(event_var["dmg_health"])
                if dmgdealt > 66:
                    if tlevel < 70:
                        damage = dmgdealt*((level-50)/20)
                    else:
                        damage = dmgdealt
            dmg = skills.dealdamage(attacker,user,damage)
            attackername = event_var["es_attackername"]
            if dmg > 50:
                est.csay(attacker,"Dealt +%s damage to the head!" % dmg)
            elif dmg > 0:
                est.csay(attacker,"Dealt +%s damage!" % dmg)
    def ultimate(self,user,entry,server):  
        level = getattr(entry,"skill4")
        if level:
            skills.teleport(user,100+50*level)

class Selune(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"moonbridge",1)
    
    level = getattr(entry,"skill1")
    if level:
      longjump = 0.1*float(level)+0.3
      wcsusers._set(user,"longjump",longjump)
      es.tell(user,"#multi","#greenMoon Bridge#lightgreen grants you#green %i%s #lightgreenlonger jumps." % (int(longjump*100),percent ) )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 30 100 0.8 255 100 100 255 1" % (x,y,z) ) 
    level = getattr(entry,"skill3")
    if level:
      skills.trackstart(user,.2)        
    level = getattr(entry,"skill4")
    if level:
      wcsusers._set(user,"ulti_immunity",1)
      es.tell(user,"#multi", "#greenSpell Resistance#lightgreen grants you ultimate immunity.")
    level = getattr(entry,"skill5")
    if level:
      wcs.evasion_set(user,"dodge",100,None)
    level = getattr(entry,"skill6")
    if level:
      level = int(level/2.5)
      es.tell(user,"#multi","#greenPhase Door#lightgreen has#green %s #lightgreenuses this round." % level)
      wcsusers._set(user,"phase",level)
    else:
      wcsusers._set(user,"phase",0)
                
  def evade(self,event_var,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    wcs.evasion_set(user,"dodge",0,None)
    time = 9-level
    gamethread.delayed(time,wcs.evasion_set,(user,"dodge",100,None))
    gamethread.delayed(time,est.csay,(user,"Prismatic Barrier ready!"))
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 11 #a 0 sprites/strider_blackball.vmt %s %s %s 2 0.5 255" % (x,y,z+40))
    
  def attack(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill2")
    dice = random.randint(1,7)
    if level >= dice:
      skills.drug(user,0.5)
    
    level = getattr(entry,"skill3")
    dice = random.randint(1,8)
    if level >= dice:
      skills.trackadd(user,attacker)
      es.tell(attacker,"#multi","#lightgreenYou have #greenremoved 10 of %s's armor#lightgreen!" % es.getplayername(user))
      es.tell(user,"#multi","#lightgreenYou have #greenlost 10 of your armor to %s's attack!" % es.getplayername(attacker))
      es.server.queuecmd("est_effect 4 #a 0 sprites/lgtning.vmt %s 1 10 10 10 255 50 50 255" % user)
      es.delayed(2,"est_effect 4 #a 0 sprites/lgtning.vmt %s 1 10 10 10 200 50 50 200" % user)
    phase = wcsusers.get(attacker,"phase")
    if not phase:
      return
    level = getattr(entry,"skill6")
    damage = int(event_var["dmg_health"])
    damage = int(3*level/100*damage*phase)
    dmg = skills.dealdamage(attacker,user,damage)
    if not dmg:
      return
    est.csay(attacker,"Phase Existance: Dealt +%s Damage" % dmg)
    est.csay(user,"Took +%s Damage" % dmg)

  def jump(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 100 1 20 100 1 255 255 255 200 10" % (x,y,z) )
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 150 1 20 100 1 0 0 0 200 10" % (x,y,z) )
    es.server.queuecmd("est_effect 4 #a 0 sprites/lgtning.vmt %s 1 0.01 5 5 200 200 225 150" % (user) )

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill6")
    if not level:
      return
    phase = wcsusers.get(user,"phase")
    if phase == 0:
      return
    skills.infiltrate(user,0)
    wcsusers._set(user,"phase",phase+1)
    hp = level*10+50-(2-(phase-1))*15
    x,y,z = es.getplayerlocation(user)
    i = 0
    while (i < 7):
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 150 10 1 20 100 1 255 255 255 200 10" % (x,y,z+i*10) )
      i = i+1
    dmg = 3*level
    es.tell(user,"#multi","#lightgreenYou come through the#green Phase Door#lightgreen with#green %s hp#lightgreen and#green %s%%#lightgreen bonus dmg." % (hp,dmg))
    wcsusers.set(user,"HPmaximum",hp)
            
class Reptile(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"Shed_Skin",1)
    wcsusers.set(user,"speed",1.3)
    
    level = getattr(entry,"skill2")
    if not level:
      return
    wcsusers.set(user,"HPmaximum",100+10*level)
    armor = 10*level+100
    est.armor(user,"=",armor,1)
               
  def attack(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    username = event_var["es_username"]
    
    level = getattr(entry,"skill3")
    if level:
      dice = random.randint(1,10)
      if dice < 5:
        time = .25+float(level*.05)
        skills.freeze(user,time)
        es.tell(user,"#multi","#lightgreenYou have been#green frozen#lightgreen by#green %s #lightgreen!!" % attackername)
        es.tell(attacker,"#multi","#lightgreenYou have #green frozen %s #lightgreen!!" % username)
            
    level = getattr(entry,"skill4")
    dice = random.randint(1,10)
    if level < dice:
      return
    skills.poisonstart(attacker,user,3,level)

  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    skin = wcsusers.get(user,"Shed_Skin")
    if not skin:
      es.tell(user,"#multi","#lightgreenYou have no more skin to shed!!")
      return
    dice = random.randint(1,5)
    if dice > level:
      return
    wcsusers._set(user,"Shed_Skin",0)
    skills.freeze(user,0)
    playerlib.getPlayer(user).health = 150
    
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 7 #a 0 sprites/smoke.vmt %s %s %s 40 1" % (x,y,z) )
    team = es.getplayerteam(user)
    if team == 2:
      usermodel = "models/player/t_phoenix.mdl"
    else:
      usermodel = "models/player/ct_urban.mdl"
    es.server.queuecmd("est_effect 11 #a 0 %s %s %s %s 0.5 1 100" % (usermodel,x,y,z) )
    i = 0
    while i < 4:
      time = .5 + .5*i
      gamethread.delayed(time,es.server.queuecmd,("est_effect 11 #a 0 %s %s %s %s 0.5 1 %s" % (usermodel,x,y,z,80-(i*20)) ) )
      i += 1
    es.tell(user,"#multi","#lightgreenYou have shed your skin to restore your HP to#green 150!")

class Shinobi(BaseClass):
    def spawn(self,event_var,entry,server):
        user = int(event_var["userid"])
        wcsusers._set(user,"ultravision",1)
        level = getattr(entry,"skill2")
        if level:
            time = 12-int(level/2)
            wcsusers._set(user,"fadecount",0)
            wcsusers._set(user,"fadetime",4)
            es.tell(user,"#multi","#lightgreenYou are granted#green 75#lightgreen percent invis but shooting someone will remove it for#green %s #lightgreenseconds" % time)
            gamethread.delayed(1.5,wcsusers.set,(user,"invisp",75))
    def attack(self,event_var,entry,server):
        level = getattr(entry,"skill1")
        if not level:
            return
        if int(event_var["es_userhealth"]) > 0:
            dice = random.randint(1,3)
            if dice == 1:
                dmg = 1+int(level/2)
                user = int(event_var["userid"])
                attacker = int(event_var["attacker"])
                skills.poisonstart(attacker,user,dmg,3)
                x2,y2,z2 = es.getplayerlocation(user)
                x1,y1,z1 = es.getplayerlocation(attacker)
                es.server.queuecmd("est_effect 3 #a 0 sprites/greenspit1.vmt %s %s %s %s %s %s 3 5 9 155 155 155 255" % (x1,y1,z1+40,x2,y2,z2+40) )
    def hurt(self,event_var,entry,server):
        user = int(event_var["userid"])
        level = getattr(entry,"skill3")
        if not level:
            return
        if int(event_var["es_userhealth"]) > 0:
            chance = 15+level*5
            dice = random.randint(1,100)
            if chance >= dice:
                est.playplayer(user,"weapons/pyscannon/energy_sing_flyby2.wav")
    def ultimate(self,user,entry,server):
        level = getattr(entry,"skill4")
        if level:
            skills.teleport(user,500+150*level)
            est.playplayer(user,"weapons/357/357_spin1.wav")
            x,y,z = es.getplayerlocation(user)
            es.server.queuecmd("est_viewcoords %s x;est_effect 3 #a 0 dev/ocean.vmt server_var(x) %s %s %s 2 0.5 0.5 255 14 41 255" % (user,x,y,z) )
            
class Duskian(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"ultravision",3)
    wcsusers._set(user,"DefensiveSpur",1)
    level = getattr(entry,"skill2")
    if not level:
      return
    speed = 1.00+.03*level
    wcsusers.set(user,"speed",speed)
    es.tell(user,"#multi","#greenDexterity#lightgreen allows you to move#green %s%% #lightgreenfaster!" %((speed-1)*100))

  def attack(self,event_var,entry,server):
    if int(event_var["es_userhealth"]) < 0:
      return
    level = getattr(entry,"skill1")
    dice = random.randint(1,10)
    if level < dice:
      return
    attacker = int(event_var["attacker"])
    user = int(event_var["userid"])
    invisp = wcsusers.get(user,"invisp")
    if not invisp:
      return
    wcsusers.set(user,"invisp",0)
    es.tell(attacker,"#multi","#lightgreenYou #greenTarnished#green %s #lightgreen, making them #green100%%#lightgreen visible!" % event_var["es_username"])
    es.tell(user,"#multi","#greenTarnished#lightgreen by#green %s #lightgreen. Now #green100%%#lightgreen visible!!" % event_var["es_attackername"])
  
  def hurt(self,event_var,entry,server):
    health = int(event_var["es_userhealth"])
    if health < 0 or health > 40:
      return
    level = getattr(entry,"skill3")
    dice = random.randint(1,13)
    if level < dice:
      return
    user = int(event_var["userid"])
    if not wcsusers.get(user,"DefensiveSpur"):
      return
    est.god(user,1)
    gamethread.delayed(2,est.god,(user,0))
    gamethread.delayed(.6,skills.infiltrate,(user,0))
    playerlib.getPlayer(user).health = 40+6*level
    wcsusers._set(user,"DefensiveSpur",0)
  
  def death(self,event_var,entry,server):
    level = getattr(entry,"skill4")
    dice = random.randint(1,10)
    if level < dice:
      return
    attacker = int(event_var["attacker"])
    attackername = event_var["es_attackername"]
    user = int(event_var["userid"])
    username = event_var["es_username"]
    dmg = int(25+level*2.5)
    if skills.dealdamage(user,attacker,dmg) > 0:
      es.tell(attacker,"#multi","#lightgreen You were infected by#green %s#lightgreen and take#green %s #lightgreendamage!" % (username,dmg))
      es.tell(user,"#multi","#lightgreen You infected#green %s #lightgreenwith a parasite, dealing#green %s #lightgreendamage!" % (attackername,dmg))
          
  def ultimate(self,user,entry,server):
      level = getattr(entry,"skill5")
      if not level:
          return
      users = []
      team = es.getplayerteam(user)
      for target in es.getUseridList():
          targetteam = es.getplayerteam(target)
          if targetteam == team or es.getplayerprop(target, 'CBasePlayer.pl.deadflag'):
              continue
          users.append(target)
      
      if len(users) == 0:
          es.tell(user,"#multi","#greenDuststorm#lightgreen has nobody to target!")
          return
      tlevel = getattr(entry,"level")-50
      target = random.choice(users)
      i = 0
      if tlevel > 5:
        users.remove(target)
        time = 7
        while tlevel > 0:
          if i >= len(users):
            break
          target2 = users[i]
          hisname = es.getplayername(target2)
          immune = wcsusers.get(target2,"ulti_immunity")
          if immune:
            es.tell(user,"#multi","#greenDuststorm#lightgreen is blocked by #green%s#lightgreen!" % hisname)
            i += 1
            continue
          skills.shake(target2,1,10,10)
          skills.fade(target2,0,1,6,0,0,0,200)
          es.tell(target2,"#multi","#greenDuststorm#green blinds you for#green 7 #lightgreenseconds!")
          tlevel -= 5
          i += 1
      else:
        time = int(.5*level)
      hisname = es.getplayername(target)
      immune = wcsusers.get(target,"ulti_immunity")
      if immune:
        es.tell(user,"#multi","#greenDuststorm#lightgreen is blocked by #green%s#lightgreen!" % hisname)
        es.tell(user,"#multi","#greenDuststorm#lightgreen has blinded #green%s #lightgreenenemies!"% i)
        return        
      skills.shake(target,1,10,10)
      dmg = skills.dealdamage(user,target,level*2)
      if i > 0:
        es.tell(user,"#multi","#greenDuststorm#lightgreen has blinded #green%s #lightgreenenemies and dealt #green%s #lightgreendamage to #green%s#lightgreen!"%(i+1,level*2,target) )
      else:
        es.tell(user,"#multi","#greenDuststorm#lightgreen hit#green %s #lightgreenblinding for#green %s #lightgreenand dealing#green %s #lightgreendamage." % (es.getplayername(target),time,dmg) )
      es.tell(target,"#multi","#greenDuststorm#green blinds you for#green %s #lightgreenseconds!" % time)
      skills.fade(target,0,1,time,0,0,0,220)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 3 60 100 0.8 0 200 100 200 1" % (x,y,z))
          
class Gryphon(BaseClass):
    def spawn(self,event_var,entry,server):
        user = int(event_var["userid"])
        es.tell(user,"#multi","#lightgreenYou ride a fucking #greenGryphon!")
        tlevel = getattr(entry,"level")
        if tlevel > 50:
            es.tell(user,"#multi","#lightgreenYou're passion for #greenGryphons#lightgreen has taught you that your #greenbeast#lightgreen needs a rest once in awhile.")
        es.tell(user,"#multi","#greenGryphon Riders#lightgreen can only use the#green M3 Pump Action Shotgun#lightgreen!")
        wcs.evasion_set(user,"fallresist",100,None)
        wcsusers.set(user,"jetpack",1)
        est.removeweapon(user,1)
        est.removeweapon(user,2)
        gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_m3"))
        level = getattr(entry,"skill1")
        if level:
            hp = 100+5*(level+1)
            wcsusers.set(user,"HPmaximum",hp)
            playerlib.getPlayer(user).health = hp
            speed = 1.00+.04*level
            wcsusers.set(user,"speed",speed)
        level = getattr(entry,"skill3")
        if level:
            es.tell(user,"#multi","#greenIspiration#lightgreen has been activated, granting your team #greenspeed#lightgreen!")
            wcsusers.set(user,"speed",wcsusers.get(user,"speed")+(.01*level))
            team = es.getplayerteam(user)
            if team == 2:
              targets = "#t!d"
            elif team == 3:
              targets = "#ct!d"
            
            people = skills.playersnearplayer(user,1231231,targets)
            for entry in people:
              person = entry[0]
              wcsusers._set(person,"speed",wcsusers.get(person,"speed")+(.02+.01*level))
              es.tell(person,"#multi","#greenInspiration#lightgreen from#green%s #lightgreen grants you extra #greenspeed#lightgreen!"%event_var["es_username"])

    def attacker(self,event_var,entry,server):
        if int(event_var["es_userhealth"]) < 0:
            return
        if event_var["weapon"] != "m3":
            return
        level = getattr(entry,"skill2")
        if not level:
            return
        dmg = int(level*.45)
        attacker = event_var["attacker"]
        user = event_var["userid"]
        if skills.dealdamage(attacker,user,dmg):
            est.csay(attacker,"+%s damage!"%dmg)
    def hurt(self,event_var,entry,server):
        user = int(event_var["userid"])
        if int(event_var["es_userhealth"]) < 0:
            return
        level = getattr(entry,"skill4")
        dice = random.randint(1,32)
        resolve = wcsusers.get(user,"resolve")
        if level >= dice and resolve:
            skills.fade(user,1,3,1,55,0,0,100)
            wcsusers._set(user,"resolve",1)
            wcs.evasion_set(user,"resist",33,None)
            es.tell(user,"#multi","#greenSteel Resolve#lightgreen activated!!")
            gamethread.delayed(2,wcs.evasion_set,(user,"resist",0,None))
            gamethread.delayed(4,wcsusers._set,(user,"resolve",0))
                
    def ultimate(self,user,entry,server):
        tlevel = getattr(entry,"level")
        if tlevel < 50:
            return
        flight = wcsusers.get(user,"jetpack")
        if flight:
            est.csay(user,"Gryphon nap Zzz")
            wcsusers._set(user,"jetpack", 0)
        else:
            est.csay(user,"Back to adventuring!")
            wcsusers._set(user,"jetpack", 1)

class Infected(BaseClass):
    def spawn(self,event_var,entry,server):
        user = int(event_var["userid"])
        player = playerlib.getPlayer(user)
        team = int(event_var["es_userteam"])
        if team == 3:
            player.setModel("player/ics/zombielunatic/urban")
        else:
            player.setModel("player/ics/t_guerilla_z/t_guerilla")
        level = getattr(entry,"skill1")
        if level:
            hp = 100+50*level
            wcsusers.set(user,"HPmaximum",hp)
            wcs.evasion_set(user,"resist",60,None)
            wcsusers._set(user,"bdmg_immune",60)
            es.tell(user,"#multi","#greenInfected Flesh#lightgreen grants you #green60%% resistance#lightgreen to all damage and #green%s Hitpoints#lightgreen!"%hp)
        level = getattr(entry,"skill2")
        if level:
            regenhp = 2+3*level
            es.tell(user,"#multi","#greenRegeneration#lightgreen provides#green %s hitpoints#lightgreen every#green 3#lightgreen seconds."%regenhp)
            skills.regenerationstart(user,regenhp,3,0,150,0,1.0)
    
    def hurt(self,event_var,entry,server):
      user = int(event_var["userid"])
      if int(event_var["es_userhealth"]) < 0:
          return
      if wcsusers.get(user,"regeneration") == 1:
        wcsusers._set(user,"regeneration",.2)
        gamethread.delayed(3,wcsusers._set,(user,"regeneration",1))
      
    def attack(self,event_var,entry,server):
      if int(event_var["es_userhealth"]) < 0:
        return
      if event_var["weapon"] != "knife":
        return
      user = int(event_var["userid"])
      if wcsusers.get(user,"infected"):
        return
      level = getattr(entry,"skill4") 
      die = random.randint(1,12)
      if level < die:
        return
      dmg = level*2
      wcsusers._set(user,"infected",1)
      attacker = int(event_var["attacker"])
      es.tell(user,"#multi","#lightgreenYou were infected by#green %s #lightgreenand are taking#green %s #Lightgreendamage per second!" % (event_var["es_attackername"],dmg) )
      es.tell(attacker,"#multi","#lightgreenYou infected#green %s #lightgreenand are deal#green %s #Lightgreendamage per second!" % (event_var["es_username"],dmg) )
      gamethread.delayed(1,skills.dealdamage,(attacker,user,dmg))
      gamethread.delayed(2,skills.dealdamage,(attacker,user,dmg))
      gamethread.delayed(3,skills.dealdamage,(attacker,user,dmg))
      gamethread.delayed(5,wcsusers._set,(user,"infected",0))
        
    def kill(self,event_var,entry,server):
      user = int(event_var["userid"])
      if wcsusers.get(user,"zombie")+wcsusers.get(user,"undead"):
        return
      attacker = int(event_var["attacker"])
      level = getattr(entry,"skill2") 
      regen = wcsusers.get(attacker,"regeneration")
      hp = regen+(0.04*level+0.01)
      wcsusers._set(attacker,"regeneration",hp)
      hp = int(hp*100-100)
      es.tell(attacker,"#multi","#lightgreenYour#green Infectious Bite#lightgreen consumes#green %s #lightgreenand you now regenerate#green %s%% #lightgreenfaster" % (event_var["es_username"],hp) )
      
    def ultimate(self,user,entry,server):
        level = getattr(entry,"skill5")
        if not level:
            return
        speed = wcsusers.get(user,"speed")
        wcsusers.set(user,"speed",speed+.09+.06*level)
        es.tell(user,"#multi","#greenFerocious Dash#lightgreen grants you #greenspeed#lightgreen for #green5#lightgreen seconds!")
        gamethread.delayed(5,wcsusers.set,(user,"speed",1.0))
        gamethread.delayed(5,es.tell,(user,"#multi","#greenFerocious Dash#lightgreen has worn off."))

class Adventurer(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill2")
    if level:
      speed = 1.0+0.02*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi","#multi","#greenAgility#lightgreen grants#green %s%% #lightgreenmore speed." % (speed*100-100))
    level = getattr(entry,"skill3")
    if level:
      hp = level*2
      wcsusers.set(user,"HPmaximum",hp+100)
      es.tell(user,"#multi","#multi","#greenEndurance#lightgreen grants#green %shp#lightgreen." % hp)
    level = getattr(entry,"skill4")
    if level:
      invisp = 20+level*2
      wcsusers.set(user,"invisp",invisp)
      es.tell(user,"#multi","#multi","#greenCunning#lightgreen grants#green %s%%#lightgreen invisibility." % invisp)
    level = getattr(entry,"skill7")
    if level:
      wcs.evasion_set(user,"dodge",level)
      es.tell(user,"#multi","#multi","#greenRogue Cloak#lightgreen grants#green %s%% #lightgreenevasion." % level)
    level = getattr(entry,"skill8")
    if level:
      dmg = int(level/2)
      wcs.evasion_set(user,"dmgimmune",dmg)
      es.tell(user,"#multi","#multi","#greenGolem Armour#lightgreen absorbs#green %s #lightgreendamage each hit." % dmg)

  def attack(self,event_var,entry,server):
    if int(event_var["es_userhealth"]) < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill1")
    dmg = 0
    if level:
      dmg = int(2+level/2.5)
      dmg = skills.dealdamage(attacker,user,dmg)
    level = getattr(entry,"skill6")
    die = random.randint(1,60)
    if level >= die:
      skills.freeze(user,1)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 11 #a 0 sprites/lgtning.vmt %s %s %s 1 2.3 90" % (x,y,z) )
    level = getattr(entry,"skill5")
    if level:
      hp = float(event_var["dmg_health"])
      hp = int(level/200*hp)
      if hp:
        playerlib.getPlayer(attacker).health += hp
        if dmg:
          est.csay(attacker,"Dealt + %s damage and leeched %s hitpoints!" % (dmg,hp) )
        else:
          est.csay(attacker,"Leeched %s hitpoints!" % hp )
    elif dmg:
      est.csay(attacker,"Dealt + %s damage!" % dmg )

class Priest(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"skulls",0)
    level = getattr(entry,"skill3")
    if level:
      dice = random.randint(1,7)
      if level >= dice:
        wcsusers._set(user,"ulti_immunity",1)
        es.tell(user,"#multi","#greenLex Divina: #lightgreenUltimate Immune")
        x,y,z = es.getplayerlocation(user)
        es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 40 2 10 10 1 0 255 100 255 1"%(x,y,z))
    level = getattr(entry,"skill2")
    if level:
      chance = 5*level
      wcs.evasion_set(user,"dodge",chance,None)
      es.tell(user,"#multi","#greenKyrie Eleison #lightgreenwill block#green %s #lightgreenof attacks."%chance)
    level = getattr(entry,"skill4")
    if level and not server["gamestarted"]:
      dice = random.randint(1,10)
      if level >= dice:
        num = int(level/3)
        if num == 1:
          es.tell(user,"#multi","#greenResurrection#lightgreen will resurrect the first player to die on your team.")
        else:
          es.tell(user,"#multi","#greenResurrection#lightgreen will resurrect the first#green %s #lightgreenplayers to die on your team."%num)
        userteam = int(event_var["es_userteam"])
        wcs.phoenix_add(userteam,num)
  def attack(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    if int(event_var["es_userhealth"]) < 0:
      return
    dice = random.randint(1,10)
    level = getattr(entry,"skill1")
    if dice < 8 and level > 0:
      if wcsusers.get(user,"undead") or wcsusers.get(user,"demon") or wcsusers.get(user,"shadow"):
        dmg = int(event_var["dmg_health"])
        dmg = int(dmg*level*.11)
        dmg = skills.dealdamage(attacker,user,dmg)
        if dmg > 0:
          es.tell(attacker,"#multi","#greenAspersio#lightgreen deals %s more damage"%dmg)
  def kill(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    tlevel = getattr(entry,"level")
    if tlevel > 100:
      if wcsusers.get(user,"undead") or wcsusers.get(user,"demon") or wcsusers.get(user,"shadow"):
        wcsusers._set(attacker,"skulls",wcsusers.get(attacker,"skulls")+1)
  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill5")
    dice = random.randint(1,80)
    if level > dice:
      est.rocket(attacker,user)
      es.tell(attacker,"#multi","#lightgreenYou have been sent to #greenHeaven#lightgreen to be judged.")
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill6")
    if level:
      skulls = wcsusers.get(user,"skulls")
      if skulls:
        es.tell(user,"#multi","#lightgreenYour #greenangelic #lightgreenendeavors enchant the #greenSanctuary#lightgreen.")
      duration = 9+level
      health = int((level*2+1)/3)+skulls*2
      radius = level*10+230
      x,y,z = es.getplayerlocation(user)
      z += 45
      skills.healingwardstart(user,duration,health,50,radius)
      es.tell(user,"#multi","#greenHealing Ward down.")
      
class RPGgen(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    #crusaders
    level = getattr(entry,"skill7")
    dice = random.randint(1,5)
    if level > dice:
      wcsusers._set(user,"crusaders",1)
      gamethread.delayed(1,es.tell,(user,"#multi","#greenDenial#lightgreen will save your #green current loadout#lightgreen in #green3#lightgreen seconds."))
      gamethread.delayed(3,wcs.saveguns,(user))
      gamethread.delayed(3,es.tell,(user,"#multi","#lightgreenYour #greenguns#lightgreen have been #greensaved#lightgreen."))
    else:
      es.tell(user,"#multi","#lightgreenYour guns have #greennot#lightgreen been saved this round.")
    level = getattr(entry,"skill1")
    if level:
      skills.regenerationstart(user,level,5,0,100,0,1.0)
      es.tell(user,"#multi","#greenRegeneration#lightgreen will restore#green %s #lightgreenhitpoints every#green 5 #lightgreenseconds!"%level)
    level = getattr(entry,"skill2")
    if level:
      hp = int(level*2.5)
      wcsusers.set(user,"HPmaximum",100+hp)
      es.tell(user,"#multi","#lightgreenSpawned with#green %s #lightgreenextra hitpoints!"%hp)
    level = getattr(entry,"skill3")
    if level:
      ammo = int(level*4/5)
      skills.resupplystart(user,ammo,0,5)
      es.tell(user,"#multi","#greenResupply#lightgreen will refill your primary weapon with#green %s #lightgreenbullets every#green 5 #lightgreenseconds!"% ammo)
    level = getattr(entry,"skill5")
    if level:
      longjump = level*.8
      wcsusers._set(user,"longjump",longjump)
      es.tell(user,"#multi","#greenLongjump #lightgreen allows you to jump#green %s%%#lightgreen farther than normal!"%(longjump*100))
    level = getattr(entry,"skill6")
    if level:
      invisp = level*5
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi","#greenInvisibility #lightgreengrants you#green %s #lightgreenpercent invisibility."%invisp)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 100 1 20 100 1 20 100 20 120 10"%(x,y,z))
  def attack(self,event_var,entry,server):
    level = getattr(entry,"skill4")
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    player = playerlib.getPlayer(attacker)
    
    if int(event_var["es_userhealth"]) < 0:
      return
    if level:
      dmg = int(event_var["dmg_health"])
      dmg = int(dmg*level/40)
      maxhp = wcsusers.get(user,"HPmaximum")+25
      if (player.health+dmg) > maxhp:
        player.health = maxhp
      else:
        player.health += dmg
      es.tell(attacker,"#multi","#greenVampirism#lightgreen leeches#green %s #lightgreenhitpoints."%dmg)
      x1,y1,z1 = es.getplayerlocation(attacker)
      x2,y2,z2 = es.getplayerlocation(user)
      alpha = int(255-2.55*int(wcsusers.get(user,"invisp")))
      es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 25 25 255 0 0 %s"%(x1,y1,z1+20,x2,y2,z2+20,alpha))
  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    if wcsusers.get(user,"crusaders"):
      wcs.denial(user)
      es.tell(user,"#multi","#greenDenial#lightgreen will save your weapons!")
      
class PsychoMantis(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill4")
    if level:
      lowgrav = 1.00-level*.1
      wcsusers.set(user,"gravity",lowgrav)
      lowgrav = int(100-100*lowgrav)
      es.tell(user,"#multi","#greenLevitation#lightgreen provides#green %s%% #lightgreenlower gravity."%lowgrav)
  def attack(self,event_var,entry,server):
    user = int(event_var["userid"])
    username = event_var["es_username"]
    attacker = int(event_var["attacker"])
    if int(event_var["es_userhealth"]) < 0:
      return
    level = getattr(entry,"skill1")
    if level:
      dice = random.randint(1,100)
      if (5+5*level) > dice:
        x = random.randint(-200,200)
        y = random.randint(-200,200)
        est.physpush(user,x,y,300)
        x,y,z = es.getplayerlocation(attacker)
        x2,y2,z2 = es.getplayerlocation(user)
        es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 5 10 25 0 255 200"%(x,y,z+20,x2,y2,z2+20))
    level = getattr(entry,"skill2")
    if level:
      dice = random.randint(1,100)
      if (1+4*level) > dice:
        skills.freeze(user,1)
        es.tell(attacker,"#multi","#greenPsionic Blast#lightgreen stuns#green %s."%username)
    level = getattr(entry,"skill3")
    if level:
      dice = random.randint(1,100)
      if (5*level) > dice:
        skills.burn(attacker,user,1.5)
        es.tell(attacker,"#multi","#greenPyrokensis#lightgreen burns#green %s."%username)
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level:
      es.tell(user,"#multi","#greenPsionic Barrier#lightgreen activated for#green 10#lightgreen seconds.")
      shield = int(level*12.5)
      immune = skills.ultimatecheck(user)
      if immune:
        es.tell(user,"#multi","#greenYour Ultimate was blocked!")
        return
      wcs.evasion_set(user,"resist",shield,None)
      gamethread.delayed(10,wcs.evasion_set,(user,"resist",0,None))
      gamethread.delayed(10,es.tell,(user,"#multi","#greenPsionic Barrier#lightgreen has #greenworn off#lightgreen."))

class Antlion(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    player = playerlib.getPlayer(user)
    player.setModel("player/techknow/antlion/antlion.mdl")
    team = int(event_var["es_userteam"])
    wcs.evasion_set(user,"hitgroups",1,50)
    if team == 2:
      R = 255
      B = 170
    else:
      R = 170
      B = 255
    G = 200
    player.setColor(R,G,B,255)
    wcsusers._set(user,"burrow",0)
    level = getattr(entry,"skill2")
    if level:
      hp = 100+5*level
      wcsusers.set(user,"HPmaximum",hp)
      dmg = 5+level*5
      wcs.evasion_set(user,"resist",dmg,None)
    level = getattr(entry,"skill3")
    if level:
      speed = 1.0+.15*level
      lowgrav = 1-.075*level
      wcsusers.set(user,"speed",speed)
      wcsusers.set(user,"gravity",lowgrav)
    level = getattr(entry,"skill4")
    if level:
      skills.regenerationstart(user,level,2,0,300,0,1.0)
  def attack(self,event_var,entry,server):
    if int(event_var["es_userhealth"]) <= 0:
      return
    level = getattr(entry,"skill1")
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    if level:
      time = int(level*.5+2)
      dmg = level*5
      skills.shake(user,time,20,100)
      dmg = skills.dealdamage(attacker,user,dmg)
      attackername = event_var["es_attackername"]
      username = event_var["es_username"]
      est.csay(user,"%s shook you!"%attackername)
      if dmg > 0:
        est.csay(attacker,"Shook %s and dealt %s damage!"%(username,dmg))
      x,y,z = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 0 255 0 255"%(x,y,z,x2,y2,z2))
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill6")
    if level:
      x,y,z = es.getplayerlocation(user)
      if wcsusers.get(user,"burrow") == 0:
        wcsusers._set(user,"burrow",1)
        z -= 200
        est.god(user,1)
        es.server.queuecmd("es_xsetpos %s %s %s %s" % (user,x,y,z) )
        gamethread.delayed(.1,es.server.queuecmd,("es_xsetpos %s %s %s %s" % (user,x,y,z) ))
        gamethread.delayed(.2,es.server.queuecmd,("es_xsetpos %s %s %s %s" % (user,x,y,z) ))
        gamethread.delayed(.3,es.server.queuecmd,("es_xsetpos %s %s %s %s" % (user,x,y,z) ))
        gamethread.delayed(.4,es.server.queuecmd,("es_xsetpos %s %s %s %s" % (user,x,y,z) ))
        gamethread.delayed(.5,es.server.queuecmd,("es_xsetpos %s %s %s %s" % (user,x,y,z) ))
        gamethread.delayed(1,est.god,(user,0))
        wcsusers._set(user,"regeneration",0.5)
        skills.freeze(user)
        wcsusers._set(user,"freeze_immune",1)
      else:
        wcsusers._set(user,"burrow",0)
        z += 200
        es.server.queuecmd("es_xsetpos %s %s %s %s" % (user,x,y,z) )
        wcsusers._set(user,"regeneration",1)
        skills.unfreeze(user)
        wcsusers._set(user,"freeze_immune",0)
  def ability(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level:
      skills.teleport(user,200+level*40)
      
class Malevolent(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"shadow",1)
    est.armor(user,"=",100,1)
    es.tell(user,"#multi","#lightgreenYou spawned with#green 100 armor.")
    
    level = getattr(entry,"skill6")
    dice = random.randint(1,12)
    if (level >= dice) and not server["gamestarted"]:
      wcsusers._set(user,"vengeance",1)
      es.tell(user,"#multi","#greenDefiance#lightgreen will respawn you this round!")
    else:
      wcsusers._set(user,"vengeance",0)
      es.tell(user,"#multi","#greenDefiance#lightgreen failed and #greenwon't#lightgreen respawn you!")
    level = getattr(entry,"skill1")
    if level:
      invisp = 35+level*5
      wcsusers.set(user,"invisp",invisp)
      es.tell(user,"#multi","#greenEthereality #lightgreengrants you#green %s #lightgreenpercent invisibility"%invisp)
    level = getattr(entry,"skill4")
    if level:
      speed = level*.05+1.00
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi","#greenSwift Step#lightgreen allows you to move#green %s%%#lightgreen faster than usual!"%(100*speed-100))
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 255 100 0 255 0"%(x,y,z))
    level = getattr(entry,"skill5")
    dice = random.randint(1,6)
    if level >= dice:
      gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_mp5navy"))
      player = playerlib.getPlayer(user)
      gamethread.delayed(5,player.setClip,("weapon_mp5navy",60))
      es.tell(user,"#multi","#greenMalevolent Weaponry#lightgreen provides a#green 60#lightgreen clip#green MP5 Navy!")
  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    if wcsusers.get(user,"vengeance") == 1:
      skills.respawn(user,3,100) 
  def attack(self,event_var,entry,server):
    attacker = int(event_var["attacker"])
    user = int(event_var["userid"])
    level = getattr(entry,"skill2")
    dice = random.randint(1,8)
    if level and (dice > 3):
      dmg = float(event_var["dmg_health"])
      dmg = skills.dealdamage(attacker,user,int(dmg*(.10+level*.05)))
      if dmg > 0:
        x,y,z = es.getplayerlocation(attacker)
        x2,y2,z2 = es.getplayerlocation(user)
        es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 255 255 255 100"%(x,y,z+40,x2,y2,z2+40))
        est.csay(attacker,"+ %s Damage"%dmg)
        est.csay(user,"Took + %s Damage!"%dmg)
  def hurt(self,event_var,entry,server):
    user = int(event_var["userid"])
    team = es.getplayerteam(user)
    level = getattr(entry,"skill2")
    dice = random.randint(1,15)
    if level >= dice:
      dmg = int(event_var["dmg_health"])
      hp = int(dmg/(9-level))
      if team == 2:
        teammates = skills.selectplayers(user,"#t")
      else:
        teammates = skills.selectplayers(user,"#c")
      for player in teammates:
        playerlib.getPlayer(user).health += hp
      est.csay(user,"All teammates got %s hitpoints!"%hp)
      
class Lurker(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    x,y,z = es.getplayerlocation(user)
    
    wcsusers._set(user,"NoHeal",1)
    wcsusers._set(user,"ultravision",5)
    gamethread.delayed(3,est.removeweapon,(user,3))
    gamethread.delayed(.9,est.removeweapon,(user,2))
    gamethread.delayed(1,cstrike.giveNamedItem,(user,"weapon_usp"))
    gamethread.delayed(4,wcsusers.set,(user,"guninvisp",0))
    level = getattr(entry,"skill1")
    if level:
      speed = level*.025+1.05
      dmg = 3+int(level/2)
      wcsusers.set(user,"speed",speed)
      wcsusers._set(user,"bdmg_immune",dmg)
      es.tell(user,"#multi","#greenEnchanting Shadows#lightgreen allow you to run#green %s%%#lightgreen faster, with#green %s #lightgreenmagical resistance."%(speed,dmg))
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 20 60 1 4 2 0 0 255 0 50 0"%(x,y,z))
    level = getattr(entry,"skill2")
    if level:
      invisp = 45+level*5.5
      wcsusers.set(user,"invisp",invisp)
      wcsusers.set(user,"guninvisp",0)
      es.tell(user,"#multi","#greenShadow Meld #lightgreengrants you#green %s #lightgreenpercent invisibility"%invisp)
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 3 10 0 0 0 255 0 255 0"%(x,y,z))
    tlevel = getattr(entry,"level")
    hp = 0
    if tlevel > 60:
      hp = int((tlevel-60)*.625)
      if hp > 30:
        hp = 30
      es.tell(user,"#mutli","#greenLurker#lightgreen expertise grants you#green %s #lightgreenbonus hitpoints."%hp)
    wcsusers.set(user,"HPmaximum",90-8*level+hp)
  def attack(self,event_var,entry,server):
    if int(event_var["es_userhealth"]) <= 0:
      return
    user = int(event_var["userid"])
    username = event_var["es_username"]
    attacker = int(event_var["attacker"])
    x = 0
    y = 0
    dmg = int(event_var["dmg_health"])
    level = getattr(entry,"skill3")
    if level:
      damage = random.randint(1,int(level*.4)+1)
      x = dmg*.1+damage
    level = getattr(entry,"skill4")
    if level:
      y = dmg*.1+level*.75
    dmg = int(x+y)
    if dmg:
      dmg = skills.dealdamage(attacker,user,dmg)
      if dmg:
        es.tell(attacker,"#multi","#lightgreenDealt #green%s #lightgreenDamage to #green%s#lightgreen."%(dmg,username))

class Duelist(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    gamethread.delayed(2,est.removeweapon,(user,2))
    tlevel = getattr(entry,"level")
    if tlevel > 70:
      lowgrav = 1-((tlevel-70)/100)
      wcsusers.set(user,"gravity",lowgrav)
      es.tell(user,"#multi","#lightgreenYour gravity has been lowered by #greenDuelist's expertise#lightgreen.")    
    level = getattr(entry,"skill2")
    if level:
      chance = level*10
      wcs.evasion_set(user,"knifedodge",chance,0)
      es.tell(user,"#multi","#lightgreenYour#green Parrying#lightgreen will block#green %s%% #lightgreen of frontal knife attacks."%chance)
    level = getattr(entry,"skill3")
    if level:
      wcsusers._set(user,"bdmg_immune",level)
      wcs.evasion_set(user,"dmgimmune",level)
      es.tell(user,"#multi","#greenChainmail Armor#lightgreen will resist#green %s #lightgreenpoints of all damage."%level)
    level = getattr(entry,"skill4")
    if level == 10:
      wcsusers._set(user,"freeze_immune",1)
      wcsusers._set(user,"slow_immune",1)
      es.tell(user,"#multi","#greenQuick Step#lightgreen lets you run#green 30%%#lightgreen faster and are#green immune#lightgreen to #greenslows and stuns#lightgreen.")
      wcsusers.set(user,"speed",1.30)
    elif level:
      speed = 1.0+.03*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi","#greenQuick Step#lightgreen lets you run#green %s #lightgreen%% faster."%speed)
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0 or event_var["weapon"] != "weapon_knife":
      return
    userid = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill1")
    if level:
      dmg = level
      if event_var["dmg_health"] > 50:
        dmg = level*4
      skills.dealdamage(attacker,user,dmg)
      est.csay(user,"Rapier deals +%s damage!"%dmg)
  def evade(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["userid"])
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill1")
    if level:
      if event_var["dmg_health"] > 50:
        level = level*5
      skills.dealdamage(user,attacker,level)
      est.csay(user,"Rapier Parry deals %s damage!"%level)
      est.csay(attacker,"Rapier Parry deals %s damage!"%level)
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level:
      skills.teleport(user,100+level*40)
      wcsusers._set(user,"fallresist",95)
      gamethread.delayed(3,wcsusers._set,(user,"fallresist",0))

class calI(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    tlevel = getattr(entry,"level")
    #trueshot expertise lvl 50-150 50%->100% chance
    if tlevel > 50:
      chance = tlevel
      wcsusers._set(user,"trueshot",chance)
      wcsusers._set(user,"pierceshot",chance)      
    #deagle expertise      420
    #aura that decreases everyones speeds, LJ, grav, invis, jetpack              
    #starts at x   200-300-500?? ? ?    
    
    #autobuy - crusaders+nades
    level = getattr(entry,"skill1")
    if level:
      wcsusers._set(user,"crusaders",1)
      gamethread.delayed(1,es.tell,(user,"#multi","#greenAUTO-BUY#lightgreen will save your #green current loadout#lightgreen in #green3#lightgreen seconds."))
      gamethread.delayed(3,wcs.saveguns,(user))
      gamethread.delayed(3,es.tell,(user,"#multi","#lightgreenYour #greenguns#lightgreen have been #greensaved#lightgreen."))
      if level > 1:
        gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_hegrenade"))
      if level > 2:
        gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_flashbang"))
      if level > 3:
        gamethread.delayed(.2,playerlib.getPlayer(user).setAmmo,("weapon_flashbang",2))
      if level > 4:
        gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_smokegrenade"))
    #OBJECTIVE
    level = getattr(entry,"skill4")
    dice = random.randint(1,20)
    if level >= dice:
      if es.getplayerteam(user) == 2:
        gamethread.delayed(.1,skills.bombswap,(user))
        es.tell(user,"#multi","#lightgreenYou have recieved the #greenbomb.")
      elif es.getplayerteam(user) == 3:
        es.setplayerprop(user,"CCSPlayer.m_bHasDefuser",1)
        
    else:
      gamethread.delayed(.1,checkbomb,(user))
    #ulti immu
    dice = random.randint(1,10)
    level = getattr(entry,"skill3")
    if level >= dice:
      wcsusers._set(user,"ulti_immunity",8)
      es.tell(user,"#multi","#lightgreenYou have spawned with #greenUltimate Immunity")
    #spell resistance
    level = getattr(entry,"skill2")
    if level:
      #dmg immunity
      wcsusers._set(user,"bdmg_immune",60+level*2)
      #slow immune
      if level > 5:
        wcsusers._set(user,"slow_immune",1)
      #drunk immune
      if level > 8:
        wcsusers._set(user,"drunk_immune",1)
      #shake immune
      if level > 11:
        wcsusers._set(user,"shake_immune",1)
      #fade resist
      if level > 12:
        wcsusers._set(user,"fade_immune",1)
      #drug/banish immune
      if level > 14:
        wcsusers._set(user,"drug_immune",1)
      #burn immune
      if level > 16:
        wcsusers._set(user,"burn_immune",1)
      #freeze immune
      if level > 18:
        wcsusers._set(user,"freeze_immune",1)
      #poison immune
      if level > 19:
        wcsusers._set(user,"poison_immune",1)
      #paralyze immune
      if level > 20:
        wcsusers._set(user,"para_immune",1)
    #b-6-2
    level = getattr(entry,"skill8")
    if level:
      if level >= 30:
        wcs.evasion_set(user,"hitgroups",1,100)
      wcs.evasion_set(user,"resist",level)
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    tlevel = getattr(entry,"level")
    #vision
    level = getattr(entry,"skill5")
    dice = random.randint(1,10)
    if level >= dice:
      if wcsusers.get(attacker,"invisp") > 20:
        wcsusers.set(attacker,"invisp",0)
        x,y,z = es.getplayerlocation(user)
        red = 120
        green = 245
        blue = 255
        es.server.queuecmd("est_Effect 3 %s 0 sprites/laser.vmt %s %s %s %s %s %s 5 5 5 %s %s %s 255"%(user,x,y,z+50,x,y,z+70,red,green,blue))
    #destruction
    level = getattr(entry,"skill6")
    if tlevel > 135:
      level = 50
    dice = random.randint(1,70)
    if level < dice:
      wcsusers.set(user,"speed",1.0)
      wcsusers._set(user,"longjump",0)
      
    #percent dmg expertise
    dice = random.randint(1,155)
    if tlevel+25 < dice:
      return
    if wcsusers.get(user,"HPmaximum") <= 100:
      return
    dmg = (float(event_var["dmg_health"])/100)*wcsusers.get(user,"HPmaximum")-float(event_var["dmg_health"])
    if wcsusers.get(user,"infected"):
      freq = []
      i = 0
      while i < 20: #20% chance to get a 1-9 dmg
        freq[i] = random.randint(1,9)
        i += 1
      while i < 92: #72% chance to get 10-26 dmg
        freq[i] = random.randint(10,26)
        i += 1
      while i < 100: #8% chance to get 27-42
        freq[i] = random.randint(27,42)
        i += 1
      dice = random.choice(freq)
      dmg = dmg*.25 + dice
    skills.dealdamage(attacker,user,dmg)
    
  def kill(self,event_var,entry,server):
    level = getattr(entry,"skill7")
    if level:
      user = int(event_var["userid"])
      attacker = int(event_var["userid"])
      delay = 2.000/float(level)
      #play hl2 armor suit charge sound !?
      skills.regenerationstart(attacker,1,delay,25,500,0,1.0)
      gamethread.delayed(1.99,wcsusers._set,(attacker,"regeneration",0))
  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    #reveal ppl who shoot u
    level = getattr(entry,"skill5")
    dice = random.randint(1,10)
    if level-10 >= dice:
      if wcsusers.get(attacker,"invisp") > 20:
        wcsusers.set(attacker,"invisp",0)
      x,y,z = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      red = 120
      green = 245
      blue = 255
      alpha = 200
      es.server.queuecmd("est_effect 10 %s 0 sprites/tp_beam001.vmt %s %s %s 50 80 %s 10 50 0 %s %s %s %s 200"%(user,x2,y2,z2+20,.5,red,green,blue,alpha))
      es.server.queuecmd("est_Effect 3 %s 0 sprites/laser.vmt %s %s %s %s %s %s 5 5 5 %s %s %s 140"%(user,x,y,z+45,x2,y2,z2+45,red,green,blue))
  def bomb_begindefuse(event_var,entry):
    user = int(event_var["userid"])
    level = gettattr(entry,"skill4")
    if level:
      cw_c4index = es.getentityindex("planted_c4")
      es.setindexprop(cw_c4index,"CPlantedC4.m_flDefuseCountDown",1.0)
  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    if wcsusers.get(user,"crusaders"):
      wcs.denial(user)
def checkbomb(user):
  if playerlib.getPlayer(user).getWeaponIndex("weapon_c4"):
    es.tell(user,"#multi","#lightgreenYou have recieved the #greenbomb.")
    
class headcrab(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    player = playerlib.getPlayer(user)
    player.setModel("player/slow/babycrab_v2/slow_babycrab")
    wcsusers.set(user,"guninvisp",100)
    level = getattr(entry,"skill1")
    if level:
      speed = .5*level
      wcsusers.set(user,"speed",speed)
      lowgrav = 1.0-.04*level
      wcsusers.set(user,"gravity",lowgrav)
    level = getattr(entry,"skill2")
    if level:
      lj = .3*float(level)-.1
      wcsusers._set(user,"longjump",lj)
        
  def attack(self,event_var,entry,server):
    dmg = float(event_var["es_userhealth"])
    if dmg < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill3")
    level2 = getattr(entry,"skill4")
    level3 = getattr(entry,"skill5")
    if level:
      if level3:
        if dmg > 100:
          dmg = 3
        elif dmg > 40:
          dmg = 2
        else:
          dmg = .3+level*.1
      else:
          dmg = .3+level*.1
      slow_amount = 0
      if level2:
        slow_amount = float(level2)/100.00
      skills.hcpoisonstart(attacker,user,dmg,slow_amount)
  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill6")
    dice = random.randint(0,14)
    if level > dice:
      dice = 4
      
      
class OrcChief(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"rush",0)
    level = getattr(entry,"skill3")
    if level:
      hp = level*2
      time = 11-level
      skills.regenerationstart(user,hp,time,50,100,0,1.0)
      es.tell(user,"#multi","#greenRing of Resilience#lightgreen provides#green %s hitpoints#lightgreen every#green %s #lightgreenseconds."%(hp,time))
    level = getattr(entry,"skill4")
    dice = random.randint(1,13)
    if not server["gamestarted"]:
      if level >= dice:
        wcsusers._set(user,"vengeance",1)
        es.tell(user,"#multi","#greenRing of Rebirth#lightgreen has charged!")
      else:
        wcsusers._set(user,"vengeance",0)
        es.tell(user,"#multi","#greenRing of Rebirth#lightgreen has failed!")
    else:
        wcsusers._set(user,"vengeance",0)
    tlevel = getattr(entry,"level")
    if tlevel >= 40:
      dmg = (tlevel-30)*3
      if dmg > 200:
        dmg = 200
      if tlevel >= 60:
        player = playerlib.getPlayer(user)
        ammo = player.getAmmo("weapon_hegrenade")
        if not ammo:
          cstrike.giveNamedItem(user,"weapon_hegrenade")
          ammo = 1
        if tlevel >= 80:
          ammo = 2
        es.tell(user,"#multi","#greenOrc Chieftain lvl %s Expertise#lightgreen gives you#green %s%%#lightgreen strong grenades"%(tlevel,dmg))
        player.setAmmo("weapon_hegrenade",ammo)
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    weapon = event_var["weapon"]
    user = int(event_var["userid"])
    if weapon in weapons["grenades"]: #crit nade
      tlevel = getattr(entry,"level")
      if tlevel >= 40:
        attacker = int(event_var["attacker"])
        dmg = float(event_var["dmg_health"])
        damage = int((tlevel-30)*.03)
        if damage > 2:
          damage = 2
        damage = damage*dmg
        dmg = skills.dealdamage(attacker,user,damage)
        if dmg < 0:
          es.tell(user,"#multi", "#green%s#lightgreenhas resisted some of your crit nade")
          return
        dice = random.randint(1,6)
        if dice == 1:est.playplayer(user,"weapons\explode3.wav")
        elif dice == 2:est.playplayer(user,"weapons\explode4.wav")
        elif dice == 3:est.playplayer(user,"weapons\explode5.wav")
        elif dice == 4:est.playplayer(user,"weapons\mortar\mortar_explode1.wav")
        elif dice == 5:est.playplayer(user,"weapons\mortar\mortar_explode2.wav")
        elif dice == 6:est.playplayer(user,"weapons\mortar\mortar_explode3.wav")
        attackername = event_var["es_attackername"]
        username = event_var["es_username"]
        es.tell(user,"#multi", "#greenCritical Grenade#lightgreen from#green %s #lightgreenunleashes#green %i + %i #lightgreendamage unto you!" % (attackername,dmg,damage) )
        es.tell(attacker,"#multi", "#greenCritical Grenade#lightgreen unleashes#green %i + %i #lightgreendamage to#green %s #lightgreen!" % (dmg,damage,username) )
        x,y,z = es.getplayerlocation(user)
        es.server.queuecmd("est_effect 11 #a 0 sprites/crystal_beam1.vmt %s %s %s 0.7 3 200" % (x,y,z+20) )
        return
    else: #crit dmg
      dice = random.randint(1,5)
      if dice != 1:
        return
      level = getattr(entry,"skill1")
      if not level:
        return
      attacker = int(event_var["attacker"])
      dmg = float(event_var["dmg_health"])
      damage = int(dmg*(0.2*float(level)+0.4))
      dmg = skills.dealdamage(attacker,user,damage)
      if not dmg:
        return
      est.csay(user,"Took +%i damage!" % dmg)
      est.csay(attacker,"+%i damage!" % dmg)
      x1,y1,z1 = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 20 200 20 255" % (x1,y1,z1+40,x2,y2,z2+40) )
    #slow
    level = getattr(entry,"skill2")
    dice = random.randint(1,10)
    if level > dice:
      skills.slow(user,2,.9)
      attackername = event_var["es_attackername"]
      username = event_var["es_username"]
      es.tell(user,"#multi","#lightgreenYou have slowed#green %s"%username)
      es.tell(user,"#multi","#green%s #lightgreenhas slowed you down!"%attackername)
      time = .7
      skills.fade(user,time,.7,29,29,29,215)
      skills.fade(user,time,.7,29,29,29,140)
      skills.shake(user,.6,10,50)
      x,y,z = es.getplayerlocation(attacker)
      x2,y2,z2 = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 10 #a 0 sprites/glow.vmt %s %s %s 100 950 0.2 200 30 0 55 55 55 255 50"%(x2,y2,z2))
      es.server.queuecmd("est_effect 10 #a 0.2 sprites/glow.vmt %s %s %s 950 100 0.2 200 30 0 55 55 55 255 50"%(x2,y2,z2))
      z += 40
      z2 += 40
      es.server.queuecmd("est_Effect 3 #a 0 sprites/glow.vmt %s %s %s %s %s %s 0.1 3 3 55 55 55 255"%(x,y,z,x2,y2,z2))
      es.server.queuecmd("est_Effect 3 #a 0.2 sprites/glow.vmt %s %s %s %s %s %s 0.1 3 3 55 55 55 255"%(x,y,z,x2,y2,z2))
      es.server.queuecmd("est_Effect 3 #a 0.4 sprites/glow.vmt %s %s %s %s %s %s 0.1 3 3 55 55 55 255"%(x,y,z,x2,y2,z2))
  def hurt(self,event_var,entry,server):
    user = int(event_var["userid"])
    if event_var["es_userhealth"] < 0 or wcsusers.get(user,"rush"):
      return
    level = getattr(entry,"skill5")
    if level:
      speed = 1.1+level*.1
      oldspeed = wcsusers.get(user,"speed")
      wcsusers.set(user,"speed",speed)
      wcsusers._set(user,"rush",1)
      gamethread.delayed(2,rush,(user,oldspeed,server["round"]))
  def death(self,event_var,entry,server):
    user = int(event_var["userid"])
    vengeance = wcsusers.get(user,"vengeance")
    if vengeance > 0:
      skills.respawn(user,2.8,100)
      x,y,z = es.getplayerlocation(user)
      gamethread.delayed(3,es.server.queuecmd,("est_effect 11 #a 0 sprites/flamelet4.vmt %s %s %s 1 3.5 150"%(x,y,z)) ) 
def rush(user,oldspeed,match):
  from wcs.wcs import server
  if server["round"] != match or es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
    return
  wcsusers.set(user,"speed",oldspeed)
  wcsusers._set(user,"rush",0)
  
class Savage(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    #skulls
    skulls = wcsusers.get(user,"skulls")
    es.tell(user,"#multi","#lightgreenSkulls: #green%s"%skulls)
    #longjump
    level = getattr(entry,"skill3")
    if level:
      longjump = 1+.05*level
      wcsusers._set(user,"longjump",longjump)
      es.tell(user,"#multi","#greenLongjump#lightgreen grants you#green %s%%#lightgreen longer jumps."%(longjump*100-100))
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 30 100 0.8 255 100 100 255 1"%(x,y,z))
    #lowgrav
    level = getattr(entry,"skill5")
    if level:
      lowgrav = 1.0-.08*level
      wcsusers.set(user,"gravity",lowgrav)
      es.tell(user,"#multi","#lightgreenYour gravity is now#green %s%%#lightgreen lower."%(int(100-lowgrav*100)))
    #evade
    tlevel = getattr(entry,"level")
    level = getattr(entry,"skill4")
    if level:
      tmp = 0
      if tlevel > 50:
        tmp = tlevel - 50
        if tmp > 50:
          tmp = 50
      chance = int(12*level+tmp/5)
      wcs.evasion_set(user,"dodge",chance,None)
      es.tell(user,"#multi","#greenSurvivalist#lightgreen gives you#green %s%% #lightgreenchance to evade."%chance)
    #magical dmg immune
    if tlevel > 50:
      dmg = int((tlevel-40)/5)
      if dmg > 12:
        dmg = 15
      wcsusers._set(user,"bdmg_immune",dmg)
      es.tell(user,"#multi","#lightgreenYour experience as #greenSavage#lightgreen grants#green %s #lightgreenmagic damage immunity"%dmg)
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    #dmg
    if event_var["weapon"] == "knife":
      level = getattr(entry,"skill1")
      if level:
        dmg = float(event_var["dmg_health"])
        dice = random.randint(1,3)
        dmg = int(dmg*(level*(.4+dice/10)/3))
        if skills.dealdamage(attacker,user,dmg) > 0:
          es.tell(attacker,"#multi","#lightgreenYou dealt an extra #green%s#lightgreen damage!"%dmg)
        x,y,z = es.getplayerlocation(user)
        es.server.queuecmd("est_effect 11 #a 0 sprites/purpleglow1.vmt %s %s %s 2 4 255"%(x,y,z+50))
    #skulls
    level = getattr(entry,"skill2")
    if level:
      dice = random.randint(1,100)
      chance = 15*level
      if event_var["es_userhealth"] <= 0:
        chance = 100
      if chance >= dice:
        es.tell(attacker,"#multi","#lightgreenYou collect a #greenskull#lightgreen off your foe")
        wcsusers._set(attacker,"skulls",wcsusers.get(attacker,"skulls")+1)
        x,y,z = es.getplayerlocation(attacker)
        x2,y2,z2 = es.getplayerlocation(user)
        es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 255 200 0 255"%(x,y,z,x2,y2,z2))
  def ultimate(self,user,entry,server):
    skulls = wcsusers.get(user,"skulls")
    level = getattr(entry,"skill6")
    if not level:
      return
    skullcost = int(level/2)
    if skulls > skullcost:
      wcsusers._set(user,"skulls",skulls-skullcost)
      es.tell(user,"#multi","#greenRage #lightgreen is felt all threwout you")
      current_hp = playerlib.getPlayer(user).health
      heal = level*4
      hp = 150-current_hp
      if hp > heal:
        hp = heal
      if hp < 0:
        hp = 0
      if hp > 0:
        playerlib.getPlayer(user).health += hp
      oldspeed = wcsusers.get(user,"speed")
      wcsusers.set(user,"speed",1.0+level*.15)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 11 #a 0 sprites/yelflare1.vmt %s %s %s 4 2 255"%(x,y,z+30))
      gamethread.delayed(7,savage_end,(user,oldspeed,server["round"]))
    else:
      skulls *= -1
      es.tell(user,"#multi","#greenRage#lightgreenfailed. Need #green%s#lightgreen more skulls."%skulls)
      
def savage_end(user,speed,match):
  from wcs.wcs import server
  if server["round"] != match or es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
    return
  wcsusers.set(user,"speed",speed)
  es.tell(user,"multi","#greenRage#lightgreen has ended.")
  
class Gunner(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"trench",0)
    #m249
    level = getattr(entry,"skill1")
    if level and server["round"] > 2:
      gamethread.delayed(0.1,cstrike.giveNamedItem,(user,"weapon_m249"))
    #HP/armor
    level = getattr(entry,"skill2")
    if level:
      armor = 100+10*level
      est.armor(user,"=",armor,1)
      hp = 100+level*5
      wcsusers.set(user,"HPmaximum",hp)
      es.tell(user,"#multi","#greenArmored Suit#lightgreen provides#green %s #lightgreenextra health and#green %s #lightgreenarmor."%(hp,armor))
    #Mixxed Murder print
    level = getattr(entry,"skill3")
    if level:
      wcsusers._set(user,"MM",1)
      es.tell(user,"#multi","#greenMixed Murder#lightgreen - #greenSilver#lightgreen Bullets - deal more damage to#green Undead#lightgreen!")
  def attack(self,event_var,entry,server):
    level = getattr(entry,"skill3")
    if level:
      user = int(event_var["userid"])
      attacker = int(event_var["attacker"])
      MM = wcsusers.get(attacker,"MM")
      if MM == 1 and wcsusers.get(user,"undead"):
        dmg = int(event_var["dmg_health"])
        dmg *= (level*.05)
        skills.dealdamage(attacker,user,dmg)
      elif MM == 2:
        speed = .90-.02*level
        skills.slow(user,speed,.5)
      elif MM == 3:
        skills.freeze(user,.025*level)
      elif MM == 4:
        skills.burn(attacker,user,.025*level)
      elif MM == 0:
        skills.dealdamage(attacker,user,level)
        team = es.getplayerteam(user)
        if team == 2:
          targets = "#ct!d"
        elif team == 3:
          targets = "#t!d"
        people = skills.playersnearplayer(user,150,targets)
        for user in people:
          skills.dealdamage(attacker,user,level)
  def ability(self,user,entry,server):
    level = getattr(entry,"skill3")
    if level:
      MM = wcsusers.get(user,"MM")
      MM = (MM+1)%5
      wcsusers._set(user,"MM",MM)
      if MM == 1:
        amount = 5*level
        es.tell(user,"#multi","#greenMixed Murder#lightgreen - #greenSilver#lightgreen Bullets - deal#green %s%%#lightgreen more damage to#green Undead#lightgreen!"%amount)
      elif MM == 2:
        amount = 90-level*2
        es.tell(user,"#multi","#greenMixed Murder#lightgreen - #greenSlow#lightgreen Bullets - to slow to#green %s%%#lightgreen speed."%amount)
      elif MM == 3:
        amount = .05*level
        es.tell(user,"#multi","#greenMixed Murder#lightgreen - #greenFreeze#lightgreen Bullets - freeze for#green %s#lightgreen seconds"%amount)
      elif MM == 4:
        amount = .05*level
        es.tell(user,"#multi","#greenMixed Murder#lightgreen - #greenFire#lightgreen Bullets - burn for #green%s#lightgreen seconds"%amount)
      elif MM == 0:
        amount = level
        es.tell(user,"#multi","#greenMixed Murder#lightgreen - Explosive Bullets - deal #green+%s#lightgreen dmg each shot"%amount) 
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if level:
      trench = wcsusers.get(user,"trench")
      if trench == 0:
        wcsusers._set(user,"trench",1)
        skills.freeze(user)
        wcsusers._set(user,"freeze_immune",1)
        resist = int(level*12.5)
        wcs.evasion_set(user,"resist",resist,None)
        es.tell(user,"#multi","#greenEntrenched#lightgreen with#green %s #lightgreenpercent damage resistance."%resist)
      else:
        wcsusers._set(user,"trench",0)
        wcsusers._set(user,"freeze_immune",0)
        skills.freeze(user)
        wcs.evasion_set(user,"resist",0,None)
        es.tell(user,"#multi","#lightgreenYou are no longer #greenentrenched.")
        
class Tyrande(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"ultravision",2)
    level = getattr(entry,"skill1")
    if level:
      chance = 9+level*3
      wcs.evasion_set(user,"dodge",chance,None)
      es.tell(user,"#multi", "#greenEvasion#lightgreen gives you#green %i%% #lightgreenchance to evade." % chance )
    level = getattr(entry,"skill2")
    if level:
      time = 7-level/2
      wcsusers._set(user,"fadetime",time)
      wcsusers._set(user,"fadecount",0)
      es.tell(user,"#multi","#lightgreenYou are granted#green 75%%#lightgreen invis but shooting someone will remove it for#green %ss#lightgreen."%time)
      wcsusers.set(user,"invisp",75)
    dice = random.randint(1,10)
    level = getattr(entry,"skill3")
    if level < dice:
      return
    wcsusers._set(user,"ulti_immunity",1)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 40 2 10 10 1 0 255 100 255 1" % (x,y,z) )
    es.tell(user,"#multi", "#greenMoon Armour#lightgreen grants#green Ultimate Immunity#lightgreen.")  
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill4")
    if not level:
      return
    attacker = int(event_var["attacker"])
    user = int(event_var["userid"])
    dmg = float(event_var["dmg_health"])
    percent = (float(level)*2-1)/100
    damage = int(dmg*percent)
    dmg = skills.dealdamage(attacker,user,damage)
    if not dmg:
      return
    est.csay(user,"Took +%i damage!" % dmg)
    est.csay(attacker,"+%i damage!" % dmg)
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 1 3 6 255 255 255 50" % (x1,y1,z1+40,x2,y2,z2+40) )
  def evade(self,event_var,entry,server):
    attacker = int(event_var["attacker"])
    user = int(event_var["userid"])
    x1,y1,z1 = es.getplayerlocation(user)
    x2,y2,z2 = es.getplayerlocation(attacker)
    es.server.queuecmd("est_Effect 3 #a 0 sprites/yellowflare.vmt %s %s %s %s %s %s 1 5 5 255 255 255 255" % (x1,y1,z1+10,x2,y2,z2+10) )        
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    dmg = level+2
    radius = 280+level*40
    time = 1+int(level/2)
    if "assault" in server["map"]:
      radius /= 1.5
    if "crackhouse" in server["map"]:
      dmg /= 2
    skills.starfallstart(user,time,dmg,radius)
    
class Boreas(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"slow_immune",1)
    wcsusers._set(user,"freeze_immune",1)
    es.tell(user,"#multi","#greenBoreas#lightgreen is both#green Freeze#lightgreen and #greenSlow#lightgreen immune!")
    level = getattr(entry,"skill1")
    if level:
      armor = 100+level*2
      est.armor(user,"=",armor,1)
      shield = 5*level
      wcs.evasion_set(user,"shield",shield,None)
      es.tell(user,"#multi","#greenFrozen Armor#lightgreen grants you#green %s #lightgreenarmor and#green %s%%#lightgreen armor absorbsion."%(armor,shield))
    level = getattr(entry,"skill3")
    if level:
      invisp = 15+level*5
      wcsusers.set(user,"invisp",invisp)
      es.tell(user,"#multi","#greenFrost Shroud#lightgreen provides#green %s%%#lightgreen invisibility."%invisp)
  def attack(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill4")
    dice = random.randint(1,40)
    if level >= dice:
      skills.freeze(user,1)
      x,y,z = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_effect 10 #a 0 sprites/smoke.vmt %s %s %s 2 16 1.3 100 200 0 25 25 255 255 0"%(x,y,z+30))
      es.server.queuecmd("est_effect 3 #a 0 sprites/orangelight1.vmt %s %s %s %s %s %s 1 3 19 15 25 255 255"%(x,y,z+45,x2,y2,z2+45))
      es.server.queuecmd("est_effect 3 #a 0 sprites/tp_beam001.vmt %s %s %s %s %s %s 1 3 19 25 25 255 255"%(x,y,z+45,x2,y2,z2+45))
    level = getattr(entry,"skill2")
    dice = random.randint(1,20)
    if level >= dice:
      speed = 1.00-.03*level
      skills.slow(user,2,speed)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 200 1 20 100 1 0 40 255 200 10"%(x,y,z+20))
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 200 1 20 100 1 0 40 255 200 10"%(x,y,z+20))
      est.csay(attacker,"slowed %s"%event_var["es_username"])
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level:
      speed = 1-(.025*level)
      time = 2+level/5
      maxtargets = int((len(wcsusers.get())/2)*(float(level)/10.00))
      skills.blizzard(user,time,maxtargets)

class Ranger(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"ultravision",2)
    level = getattr(entry,"skill1")
    if level:
      invisp = 20+10*level
      gamethread.delayed(1.5,wcsusers.set,(user,"invisp",invisp))
      es.tell(user,"#multi", "#greenTrackless Step#lightgreen grants you#green %s%s #lightgreeninvisibility." % (invisp,percent) )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 2 60 100 0.8 0 20 100 255 1" % (x,y,z) )
    level = getattr(entry,"skill2")
    if level:
      armor = 95+5*level
      est.armor(user,"=",armor,1)
      wcs.evasion_set(user,"shield",75)
      skills.armoraurastart(user,5,3,armor,1000,0)
      es.tell(user,"#multi", "#greenBarkskin #lightgreenprovides you with#green %s #lightgreenarmor which protects you from#green 75%%#lightgreen of damage!" % armor)       
    if server["round"] < 3:
      return
    dice = random.randint(1,4)
    level = getattr(entry,"skil3")
    if level < dice:
      return
    player = playerlib.getPlayer(user)
    weapon = player.primary
    if weapon != "weapon_m4a1":
      gamethread.delayed(.1,cstrike.giveNamedItem,args=(user,"weapon_m4a1"))
      es.tell(user,"#multi", "#greenCraft Weapon#lightgreen provides#green 45 clip M4A1#lightgreen.")
      ammo = 45
    else:
      es.tell(user,"#multi", "#greenCraft Weapon#lightgreen provides#green 60 clip M4A1#lightgreen.")
      ammo = 60
    gamethread.delayed(2,player.setClip,("weapon_m4a1",ammo)) 
    if level > 4:
      gamethread.delayed(.1,cstrike.giveNamedItem,args=(user,"weapon_m4a1"))
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    dice = random.randint(1,3)
    if dice > 1:
      return
    level = getattr(entry,"skill4")
    if not level:
      return
    attacker = int(event_var["attacker"])
    user = int(event_var["userid"])
    if skills.poisonstart(attacker,user,5,level):
      x1,y1,z1 = es.getplayerlocation(user)
      x1,y1,z1 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_effect 3 #a 0 sprites/greenspit1.vmt %s %s %s %s %s %s 3 5 9 155 155 155 255" % (x1,y1,z1,x2,y2,z2) )
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if not level:
      return
    try:x = float(es.getplayerprop(user,"CCSPlayer.baseclass.localdata.m_vecVelocity[0]"))
    except TypeError:x = 0
    try:y = float(es.getplayerprop(user,"CCSPlayer.baseclass.localdata.m_vecVelocity[1]"))
    except TypeError:y = 0
    try:z = float(es.getplayerprop(user,"CCSPlayer.baseclass.localdata.m_vecVelocity[2]"))
    except TypeError:z = 0
    if abs(x+y+z) > 0.05:
      es.tell(user,"#multi","#greenYou must be standing still to patch yourself up!")
      return False
    heal = level*5
    player = playerlib.getPlayer(user)
    hp = player.health
    maxhp = wcsusers.get(user,"HPmaximum")
    if hp >= maxhp:
      es.tell(user,"#multi","#greenYou are already at full health!")
      return False
    health = hp+heal
    if health > maxhp:
      health = maxhp
    es.tell(user,"#multi","#lightgreenYou heal yourself up to#green %s #lightgreenhitpoints." % health)
    player.health = health
    skills.freeze(user,1)
    x,y,z = es.getplayerlocation(user)
    es.server.queuecmd("est_effect 10 #a 0 sprites/tp_beam001.vmt %s %s %s 30 60 1.5 10 50 0 10 150 10 255 80" % (x,y,z+10) )
    es.server.queuecmd("est_effect 10 #a 0.1 sprites/tp_beam001.vmt %s %s %s 30 60 1.5 10 50 0 10 150 10 255 80" % (x,y,z+20) )
    es.server.queuecmd("est_effect 10 #a 0.2 sprites/tp_beam001.vmt %s %s %s 30 60 1.5 10 50 0 10 150 10 255 80" % (x,y,z+30) )
    es.server.queuecmd("est_effect 10 #a 0.3 sprites/tp_beam001.vmt %s %s %s 30 60 1.5 10 50 0 10 150 10 255 80" % (x,y,z+40) )
    es.server.queuecmd("est_effect 10 #a 0.4 sprites/tp_beam001.vmt %s %s %s 30 60 1.5 10 50 0 10 150 10 255 80" % (x,y,z+50) )
    es.server.queuecmd("est_effect 10 #a 0.5 sprites/tp_beam001.vmt %s %s %s 30 60 1.5 10 50 0 10 150 10 255 80" % (x,y,z+60) )

class Judge(object):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    level = getattr(entry,"skill3")
    if level:
      dice = level*20
      wcs.evasion_set(user,"knifedodge",dice)
      es.tell(user,"#multi","#lightgreenYour#green Judges Immunity#lightgreen will block#green %s%% #lightgreen of knife attacks."%dice)
    playerlib.getPlayer(user).setColor(66,66,99,255)
    if server["round"] > 2:
      level = getattr(entry,"skill1")
      if level:
        clip = int(25*(1+level*.2))
        gamethread.delayed(.2,cstrike.giveNamedItem,(user,"weapon_ump45"))
        gamethread.delayed(1,playerlib.getPlayer(user).setClip,("weapon_ump45",clip))
        es.tell(user,"#multi","#greenJudge's Hammer#lightgreen has granted you a #green%s #lightgreenclip UMP45!"%clip)
    level = getattr(entry,"skill5")
    if level:
      hp = level*5+100
      wcsusers.set(user,"HPmaximum",hp)
      est.armor(user,"=",hp,1)
      es.tell(user,"#multi","#greenGift of Altana#lightgreen brings your health and armor to#green %s"%hp)
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 3 10 0 0 175 175 175 255 0"%(x,y,z+20))
    else:
      est.armor(user,"=",100,1)
      es.tell(user,"#multi","#lightgreenYou have spawned with #green100#lightgreen armor.")
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0 or event_var["weapon"] != "ump45":
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill2")
    dice = random.randint(1,8)
    if level >= dice:
      dmg = int(level*1.6)
      dmg = skills.dealdamage(attacker,user,dmg)
      if dmg:
        es.tell(attacker,"#multi","#greenJudge's Wrath#lightgreen deals#green %s #lightgreen extra damage"%dmg)
        es.tell(user,"#multi","#lightgreenYou received an additional#green %s #lightgreendamage due to#green Judge %s#lightgreen's wrath!"%(dmg,event_var["es_attackername"]))
        x,y,z = es.getplayerlocation(attacker)
        x2,y2,z2 = es.getplayerlocation(user)
        es.server.queuecmd("est_effect 3 #a 0 sprites/yellowflare.vmt %s %s %s %s %s %s 1 5 5 55 90 255 100"%(x,y,z,x2,y2,z2))
  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill4")
    if level:
      hp = float(event_var["dmg_health"])
      hp = int(hp/(24-level*3))
      player = playerlib.getPlayer(user)
      skills.regenerationstart(user,hp,1,0,150,0,1.0)
      gamethread.delayed(2.5,wcsusers._set,(user,"regeration",0))
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_Effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 200 1 20 100 1 0 40 255 200 10"%(x,y,z))
      es.server.queuecmd("est_Effect 10 #a 0.2 sprites/lgtning.vmt %s %s %s 20 300 1 20 100 1 0 40 255 200 10"%(x,y,z))
      es.tell(user,"#multi","#greenRegeneration#lightgreen heals#green %s #lightgreenover time."%hp)
      es.tell(attacker,"#multi","#lightgreenSome of your attack was resisted")   
  def evade(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill3")
    if level:
      time = 1+.2*level
      skills.freeze(attacker,1)
      x,y,z = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_effect 3 #a 0 sprites/yellowflare.vmt %s %s %s %s %s %s 1 5 5 255 255 255 255"%(x,y,z,x2,y2,z2))
      es.tell(user,"#multi","#green Judge's Immunity: %s #lightgreen attacks you with no results"%(event_var["es_attackername"]))
      es.tell(attacker,"#multi","#green Judge's Immunity: %s #lightgreen is immune to your attack"%(event_var["es_username"]))
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill6")
    if level:
      radius = 100+50*level
      time = 1.5+.25*level
      skills.entanglingroots(user,radius,5,time)

class Stalker(object):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    wcsusers._set(user,"ultravision",2)
    level = getattr(entry,"skill1")
    if level:
      invisp = 40+5*level
      wcsusers._set(user,"fadetime",2)
      wcsusers._set(user,"fadecount",0)
      wcsusers.set(user,"invisp",invisp)
      es.tell(user,"#multi","#greenStealth Field#lightgreen grants you #green%s%%#lightgreen invisibility!"%invisp)
    level = getattr(entry,"skill3")
    if level:
      speed = 1.0+.03*level
      wcsusers.set(user,"speed",speed)
      es.tell(user,"#multi","#lightgreenYou are quick on your feet: #green%s%% faster!"%((speed-1)*100))
    level = getattr(entry,"skill4")
    if level:
      radius = 200+level*50
      skills.targetaurastart(user,.25,radius)
      es.tell(user,"#multi","#greenHightened Senses#lightgreen will find enemies within a #green%s#lightgreen radius."%radius)
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    level = getattr(entry,"skill2")
    dice = random.randint(1,4)
    if level and dice > 3:
      dmg = int(event_var["dmg_health"])
      dmg = int(dmg*((level/2)*.1+.5)) + random.randint(1,36)
      dmg = skills.dealdamage(attacker,user,dmg)
      if dmg:
        est.csay(attacker, "+ %s damage"%dmg)
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill5")
    if level:
      immune = skills.ultimatecheck(user)
      if immune:
        es.tell(user,"#multi","#green%s#lightgreen prevented your ultimate!" % es.getplayername(immune) )      
        return
      radius = 100+level*20
      dmg = 75+level*10
      es.server.queuecmd("est_effect 4 #a 0 sprites/steam1.vmt %s 0.8 10 5 1 255 100 100 200"%user)
      #playplayer ambient/explosions/explode_6.wav
      skills.suicidebomb(user,radius,dmg)
      est.slay(user)
      est.kills(user,"+",1)
      est.deaths(user,"-",1)

class Trickster(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    gamethread.delayed(0.4,est.removeweapon,(user,2))
    gamethread.delayed(0.5,cstrike.giveNamedItem,(user,"weapon_elite"))
    level = getattr(entry,"skill4")
    if level:
      c = level*2
      wcsusers._set(user,"Barrels",c)
      es.tell(user,"#multi","#lightgreenYou can call upon#green %s#lightgreen bretheren this round!" %c)
    else:
      wcsusers._set(user,"Barrels",0)
    level = getattr(entry,"skill1")
    dice = random.randint(1,5)
    if level >= dice:
      gamethread.delayed(0.85,wcsusers.set,("invis",[255,255,255,255]))
      if "de_cbble" == server["map"] or "westwood" in server["map"]:
        gamethread.delayed(0.7,est.setmodel,(user,"props_c17/woodbarrel001"))
        es.tell(user,"#multi","#greenBarreficiation#lightgreen has turned you into a#green Wooden Barrel#lightgreen!!")
      elif server["map"] == "cs_desperados":
        gamethread.delayed(0.7,est.setmodel,(user,"props/de_inferno/wine_barrel"))
        es.tell(user,"#multi","#greenBarreficiation#lightgreen has turned you into a#green Wine Barrel#lightgreen!!")
      else:
        gamethread.delayed(0.7,est.setmodel,(user,"props_c17/oildrum001"))
        es.tell(user,"#multi","#greenBarreficiation#lightgreen has turned you into a#green Oil Barrel#lightgreen!!")
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 11 #a 0 sprites/yelflare1.vmt %s %s %s 2 2 255" % (x,y,z) )
    level = getattr(entry,"skill2")
    if level:
      wcs.evasion_set(user,"dmgimmune",level)
      es.tell(user,"#multi","#greenIron Skin#lightgreen will absorb#green %s#lightgreen damage per hit" % level)
    level = getattr(entry,"level")
    if level < 80:
      return
    barrels = int((level-40)/10)
    if barrels > 5:
      barrels = 5
    wcsusers._set(user,"ExBarrels",barrels)
    es.tell(user,"#multi","#greenTrickster Assassin#lightgreen expertise gives#green %s Explosive Bretheren#lightgreen, use#green Ability#lightgreen to call them."% barrels)  
    grenades = 1+int((level-50)/25)
    if grenades > 3:
      grenades = 3
    player = playerlib.getPlayer(user)
    ammo = player.getAmmo("weapon_hegrenade")
    if not ammo:
      gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_hegrenade"))
    gamethread.delayed(0.5,player.setAmmo,("weapon_hegrenade",grenades))
    es.tell(user,"#multi","#greenTrickster Assassin#lightgreen expertise gives#green %s #lightgreennapalm grenades." % grenades)
  def attack(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    if event_var["weapon"] in weapons["grenades"]:
      level = getattr(entry,"level")
      if level < 80:
        return
      user = int(event_var["userid"])
      attacker = int(event_var["attacker"])
      dmg = float(event_var["dmg_health"])
      damage = int((40 + dmg)/4)
      dmg = skills.dealdamage(attacker,user,damage)
      est.burn(user,5,attacker)
      dice = random.randint(1,6)
      if dice == 1:est.playplayer(user,"weapons\explode3.wav")
      elif dice == 2:est.playplayer(user,"weapons\explode4.wav")
      elif dice == 3:est.playplayer(user,"weapons\explode5.wav")
      elif dice == 4:est.playplayer(user,"weapons\mortar\mortar_explode1.wav")
      elif dice == 5:est.playplayer(user,"weapons\mortar\mortar_explode2.wav")
      elif dice == 6:est.playplayer(user,"weapons\mortar\mortar_explode3.wav")
      attackername = event_var["es_attackername"]
      username = event_var["es_username"]
      es.tell(user,"#multi", "#greenNapalm Grenade#lightgreen from#green %s #lightgreenunleashes#green %i + %i #lightgreendamage unto you and burns you for 5s!" % (attackername,dmg,damage) )
      es.tell(attacker,"#multi", "#greenNapalm Grenade#lightgreen unleashes#green %i + %i #lightgreendamage to#green %s #lightgreenand burns for 5s!" % (dmg,damage,username) )
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 11 #a 0 sprites/crystal_beam1.vmt %s %s %s 0.7 3 200" % (x,y,z+20) )
    else:
      level = getattr(entry,"skill3")
      if not level:
        return
      die = random.randint(1,4)
      if die != 1:
        return
      time = level/2
      user = int(event_var["userid"])
      attacker = int(event_var["attacker"])
      est.burn(user,time,attacker)
      es.tell(attacker,"#multi","#greenOil Spill#lightgreen sets#green %s #lightgreenalight for#green %s #lightgreenseconds." % (event_var["es_username"],int(time)) )
  def hurt(self,event_var,entry,server):
    if event_var["es_userhealth"] < 0:
      return
    level = getattr(entry,"skill3")
    if not level:
      return
    die = random.randint(1,4)
    if die != 1:
      return
    time = level/2
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    est.burn(attacker,time,user)
    es.tell(user,"#multi","#greenOil Spill#lightgreen sets#green %s #lightgreenalight for#green %s #lightgreenseconds." % (event_var["es_attackername"],int(time)) )
  def ultimate(self,user,entry,server):
    level = getattr(user,"skill4")
    if not level:
      return
    barrels = wcsusers.get(user,"Barrels")
    if not barrels:
      es.tell(user,"#multi","#lightgreenYou have no#green Bretheren#lightgreen left to call upon!")
      return
    barrels -= 1
    wcsusers._set(user,"Barrels",barrels)
    if server["map"] == "de_cbble":
      es.prop_physics_create(user,"props_c17/woodbarrel001")
    elif server["map"] == "cs_desperados":
      es.prop_physics_create(user,"props/de_inferno/wine_barrel")
    elif "westwood" in server["map"]:
      es.prop_physics_create(user,"props_c17/woodbarrel001")
    else:
      es.prop_physics_create(user,"props_c17/oildrum001")
    es.tell(user,"#multi","#greenBackup arrived#lightgreen! You have#green %s Bretheren#lightgreen remaining to call upon!" % barrels)
  def ability(self,user,entry,server):
    level = getattr(user,"level")
    if level < 80:
      return
    barrels = wcsusers.get(user,"ExBarrels")
    if not barrels:
      es.tell(user,"#multi","#lightgreenYou have no#green Explosive Bretheren#lightgreen left to call upon!")
      return
    barrels -= 1
    wcsusers._set(user,"ExBarrels",barrels)
    es.prop_physics_create(user,"props_c17/oildrum001_explosive.mdl")
    es.tell(user,"#multi","#greenBackup arrived#lightgreen! You have#green %s Explosive Bretheren#lightgreen remaining to call upon!" % barrels)
    
class Cheiron(BaseClass):
  def spawn(self,event_var,entry,server):
    user = int(event_var["userid"])
    ak_print = ""
    if server["round"] > 2:
      gamethread.delayed(0.1,cstrike.giveNamedItem,args=(user,"weapon_ak47"))
      ak_print = "#lightgreen and a free #green AK47"
    est.armor(user,"=",100,1)
    es.tell(user,"#multi","#lightgreenYou spawned with #green100 Armor%s!"%(ak_print))
    level = getattr(entry,"skill3")
    if level:
      lj = 1+level*.05
      wcsusers._set(user,"longjump",lj)
      es.tell(user,"#multi","#greenHorde Jump#lightgreen grants you#green %s%%#lightgreen longer jumps."%(lj*100-100))
      x,y,z = es.getplayerlocation(user)
      es.server.queuecmd("est_effect 10 #a 0 sprites/lgtning.vmt %s %s %s 20 50 1 60 100 0.8 0 255 255 255 1"%(x,y,z))
  def attack(self,event_var,entry,server):
    user = int(event_var["userid"])
    attacker = int(event_var["attacker"])
    dice = random.randint(1,2)
    level = getattr(entry,"skill1")
    if dice and level:
      hp = float(event_var["dmg_health"])
      hp = int(hp*(.08+level*.02))
      if hp:
        playerlib.getPlayer(attacker).health += hp
        est.csay(attacker,"Drained %s hitpoints!" % hp )
        x,y,z = es.getplayerlocation(attacker)
        x2,y2,z2 = es.getplayerlocation(user)
        es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 0 255 0 200"%(x,y,z,x2,y2,z2))
        es.server.queuecmd("est_Effect 3 #a 0 sprites/lgtning.vmt %s %s %s %s %s %s 0.5 40 40 0 255 0 200"%(x,y,z+20,x2,y2,z2+20))
  def hurt(self,event_var,entry,server):
    attacker = int(event_var["attacker"])
    user = int(event_var["userid"])
    level = getattr(entry,"skill2")
    dice = random.randint(1,12)
    if level >= dice:
      dmg = float(event_var["dmg_health"])
      dmg = int(dmg/(11-level))
      skills.dealdamage(user,attacker,dmg)
      x,y,z = es.getplayerlocation(user)
      x2,y2,z2 = es.getplayerlocation(attacker)
      es.server.queuecmd("est_effect 3 #a 0 sprites/purpleglow1.vmt %s %s %s %s %s %s 1 10 10 20 200 200 255"%(x,y,z,x2,y2,z2))
      est.csay(user,"%s Mirror Damage!"%dmg)
      est.csay(attacker,"Hit by %s Mirror Damage!"%dmg)
  def ultimate(self,user,entry,server):
    level = getattr(entry,"skill4")
    if level:
      radius = 50+level*50
      time = 1.0+level*.25
      skills.entanglingroots(user,radius,3,time)