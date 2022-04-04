from ..tools import BaseClasses
from ..tools.events import wcs_event
from ..tools.Skills import Skill
from ..tools import RaceTools
from ..tools import DatabaseManager

import es
import playerlib
import usermsg
import gamethread
from random import randint
from random import choice
import weaponlib

class TheProfessional( BaseClasses.baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse = 'knife,flashbang,smokegrenade,hegrenade, fiveseven'
		#self.WeaponsCantUse =
		#self.ItemsCanOnlyUse =
		#self.ItemsCantUse =
		self.RaceName      = "The Professional"
		self.Coder         = "MrCoolness"
		self.PlayerLimit   = 2
		self.RequiredLevel = 0
		# self.UltimateCooldown  = 20
		# self.AbilityCooldown   = 0
		
		self.ChangeRaceIndex   = 100
		# self.isSubscriber      = 0
		# self.isPrivate         = 0
		# self.UltimateTriggered = {}
		# self.AbilityTriggered  = {}
		# self.UltimateCooldownAtRoundStart = 1
		# self.AbilityCooldownAtRoundStart  = 1
		
		self.Skill_1 = Skill(  "Infamous Tricks", "[Passive] Infamy provides connections",                     0,  0, wcs_event['None']   )
		self.Skill_2 = Skill( "Powerful Enemies", "[Attack] More powerful opponents earn you more infamy", 25,  0, wcs_event['Attack'] )
		self.Skill_3 = Skill(  "Powerful Allies", "[Spawn] Your allies provide you various protection",     5,  0, wcs_event['Spawn']  )
		self.Skill_4 = Skill(    "Shoot to Kill", "[Attack] Your shots must be deadly and accurate",        5,  0, wcs_event['Attack'] )
		self.Skill_5 = Skill(         "Contract", "[Spawn] Fulfill your contract to earn more infamy",      5, 15, wcs_event['Spawn']  )
		
		self.SkillList = [ self.Skill_1, self.Skill_2, self.Skill_3, self.Skill_4, self.Skill_5 ]
		
		self.Function = [ self.blankSkill, self.Powerful_Enemies, self.Powerful_Allies, self.Shoot_to_Kill, self.Contract ]
	
	_playerInfamy = {}
	_playerDamageReduction = {}
	_playerShield = {}
	_enemyPosition = {}
	_userSpeed = {}
	def Powerful_Enemies( self, event_var, lvl ) :
		userid = event_var['attacker']
		victim = event_var['userid']
		enemy = playerlib.getPlayer( victim )
		enemykills = enemy.kills
		enemydeaths = enemy.deaths
		enemyisdead = enemy.isdead
		if ( enemyisdead == 1 ) :
			enemykd = ( enemykills / enemydeaths )
			if ( enemykd <= 0 ) :
				enemykd = 0.1
			if ( enemykd >= 4 ) :
				enemykd = 4
			self._playerInfamy[ str(userid) ] += enemykd * lvl * 0.5
			
	def Powerful_Allies( self, event_var, lvl ) :
		userid = event_var['userid']
		player = playerlib.getPlayer( userid )
		chance = randint( lvl * 2, lvl * 4 )
		if ( chance >= randint( 1, 15 ) :
			player.armor += lvl * 20
			self._playerShield[ str(userid) ] = lvl * 10
			if ( chance >= randint( 5, 25 )
				es.tell( userid, '#multi', '#lightgreenPowerful Allies #greenprovide you with a #lightgreen%i #greenpower shield.' % self._playerShield[ str(userid) ] )
				self._playerDamageReduction[ str(userid) ] = True
			if ( chance < randint( 5, 25 )
				self._playerDamageReduction[ str(userid) ] = False
		if ( chance >= randint( 7, 17 ) and self._playerInfamy[ str(userid) ] >= 30 ) :
			speedboost = randint( (self._playerInfamy[ str(userid) ] / 6), ( lvl * 8 ) )
			if ( speedboost >= 40 ) :
				speedboost = 40
			player.setSpeed( self._userspeed[ str(userid) ] + ( speedboost / 100 ) )
			es.tell( userid, '#multi', '#lightgreenPowerful Allies #greenprovide you with lighter gear. You move #lightgreen%i%% #greenfaster.' % speedboost )
		if ( chance >= randint( 5, 20 ) :
			bonushp = randint( lvl * 2, lvl * 12 )
			es.tell( userid, '#multi' '#lightgreenPowerful Allies #greenprovide you with #lightgreen%i #greenbonus hp.' % bonushp )
		
	def player_spawn( self, event_var, skills ) :
		userid = event_var['userid']
		player = playerlib.getPlayer( userid )
		self._userspeed[ str(userid) ] = player.speed
		es.give( userid, "weapon_fiveseven" )
		player.setSecondaryClip( 20 + int(self._playerInfamy[ str(userid) ]) )
		es.tell( userid, '#multi', '#lightgreenInfamy: #green%i' % self._playerInfamy[ str(userid) ] )
		if ( self._playerInfamy[ str(userid) ] >= 60 ) :
			chanceformole = randint( (self._playerInfamy[ str(userid) ] / 10), (self._playerInfamy[ str(userid) ] / 4) )
			if ( chanceformole >= 50 ) :
				chanceformole = 50
			if ( chanceformole >= randint( 1, 100 ) ) :
				if ( player.team == 2 ) :
					randplayer = choice( playerlib.getPlayerList('#ct,#alive') )
				if ( player.team == 3 ) :
					randplayer = choice( playerlib.getPlayerList('#t,#alive') )
				self._enemyPosition[ str(userid) ] = randplayer.location
				duration = randint( 13, 17 )
				es.tell( userid, '#multi', '#lightgreenInfamy: #greenyou infiltrate the enemy ranks in #lightgreen%i #greenseconds.' % duration )
				gamethread.delayed( duration, self.mole, userid )
		if ( self._playerInfamy[ str(userid) ] >= 50 ) :
			invis = self._playerInfamy[ str(userid) ] / 400
			if ( invis >= 0.7 ) :
				invis = 0.7
			RaceTools.setColor( userid, 1, 1, 1, (1 - invis), 1 )
			es.tell( userid, '#multi', '#lightgreenInfamy: #greencamoflauge provides #lightgreen%i%% #greeninvisibility.' % ( invis * 100 ) )
			
		def player_death( self, event_var, skills) :
			userid = event_var['userid']
			if ( self._playerInfamy[ str(userid) ] >= 100 ) :
				dmg = self._playerInfamy[ str(userid) ] - 99
				if ( self._playerInfamy[ str(userid) ] >= 200 ) :
					dmg = 100
				range = 200 + ( self._playerInfamy[ str(userid) ] )
				if ( self._playerInfamy[ str(userid) ] >= 200 ) :
					range = 400
				team = es.getplayerteam( userid )
				if ( team == 3 ):
					targets = '#t,#alive'
				if ( team == 2 ):
					targets = '#ct,#alive'
				targets = RaceTools.getplayersinrange( userid, targets, range )
				for player in targets:
					es.server.queuecmd( 'damage %s %i %i %s' % ( str(player.userid), dmg, 32, str(userid) ) )
		
	def mole( self, event_var, skills ) :
		userid = event_var['userid']
		player = playerlib.getPlayer( userid )
		player.setLocation( self._enemyPosition[ str(userid) ] )
	
	def player_hurt( self, event_var, skills ) :
		userid = event_var['userid']
		player = playerlib.getPlayer( userid )
		damage = int(event_var['dmg_health'])
		if ( self._playerDamageReduction[ str(userid) ] == True ) :
			if ( self._playerShield[ str(userid) ] >= 0 ) :
				damagereduction = damage * 0.2 + ( self._playerInfamy[ str(userid) ] / 1250 )
				player.health += damagereduction
				self._playerShield[ str(userid) ] -= damagereduction
	
	def player_connect( self, event_var, skills ) :
		self._playerInfamy[ str(userid) ] = 0
		self._playerDamageReduction[ str(userid) ] = False
		self._playerShield[ str(userid) ] = 0
		self._enemyPosition[ str(userid) ] = 0
	
	def race_changed( self, event_var, skills ) :
		self._playerInfamy[ str(userid) ] = 0
		self._playerDamageReduction[ str(userid) ] = False
		self._playerShield[ str(userid) ] = 0
		self._enemyPosition[ str(userid) ] = 0
		
	def es_map_start( self, event_var, skills) :
		self._playerInfamy[ str(userid) ] = 0
		self._playerDamageReduction[ str(userid) ] = False
		self._playerShield[ str(userid) ] = 0
		self._enemyPosition[ str(userid) ] = 0
		