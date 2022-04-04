from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint, choice

class Tester( baseRace ):
	def __init__( self ):
		self.RaceName         = 'Tester'
		self.isPrivate        = 1
		self.Coder            = 'Mini Dude'
		self.PlayerLimit      = 0
		self.RequiredLevel    = 1
		self.ChangeRaceIndex  = 30

		self.UltimateCooldown = 5
		self.AbilityCooldown  = 5

		self.StartingUltimateCooldown = 1
		self.StartingAbilityCooldown = 1

		self.SkillList = [
			Skill( 'testUlt', '[Ultimate] Test ults are cool eh?', 1, 0 )
		]

	def player_hurt( self, ev, skills ):
		player         = playerlib.getPlayer( ev['userid'] )
		player.health += ev['dmg_health']

	def player_spawn( self, ev, skills ):
		player = playerlib.getPlayer( ev['userid'] )


		# player.speed = 2
		# self.RaceTools.setGravity( player, 0.5 )

		wcsPlayer = self.helper.getPlayer( player )
		wcsPlayer.infoTesterDoubleJumpState = 0

	def player_ultimate( self, ev, skills ):
		player = playerlib.getPlayer( ev['userid'] )

		player.health = 500

	def player_jump( self, ev, skills ):
		player    = playerlib.getPlayer( ev['userid'] )
		wcsPlayer = self.helper.getPlayer( player )

		wcsPlayer.infoTesterDoubleJumpState = 1

	def player_air( self, ev, skills ):
		player    = playerlib.getPlayer( ev['userid'] )
		wcsPlayer = self.helper.getPlayer( player )

		gamethread.delayed( 0.1, setattr, ( wcsPlayer, 'infoTesterDoubleJumpState', 2 ) )
		# wcsPlayer.infoTesterDoubleJumpState = 2

	def client_keypress( self, ev, skills ):
		player    = playerlib.getPlayer( ev['userid'] )
		wcsPlayer = self.helper.getPlayer( player )

		if ( ev['keyname'] == 'jump' ):

			# after you finish the first jump
			# if ( wcsPlayer.infoTesterDoubleJumpState == 1 and ev['status'] == '0' ):
			# 	wcsPlayer.infoTesterDoubleJumpState = 2

			if ( wcsPlayer.infoTesterDoubleJumpState >= 2 and ev['status'] == '1' ):

				wcsPlayer.infoTesterDoubleJumpState = 0

				zVel = es.getplayerprop( player.userid, 'CBasePlayer.localdata.m_vecVelocity[2]' )

				# if you're falling, negate the falling to jump from right there
				if ( zVel < 0 ):

					self.RaceTools.pushToPoint( player, 0, 0, 300 + -zVel )

				else:

					self.RaceTools.pushToPoint( player, 0, 0, 300 )