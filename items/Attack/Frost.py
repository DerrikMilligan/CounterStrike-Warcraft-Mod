from ...tools import BaseClasses
from ...tools import RaceTools
from random import randint

import es
import playerlib

class Frost(BaseClasses.baseItem):
	Chance      = 30
	slowPercent = 25
	duration    = 0.5

	def __init__( self ):
		self.Name          = 'Orb of Frost'
		self.Description   = 'Chance to slow people when you damage them.'
		self.Price         = 2500
		self.Requiredlevel = 0
		self.Persistent    = 1

	def player_attack( self, event_var ):
		victim = event_var['userid']
		attacker = playerlib.getPlayer( event_var['attacker'] )
		rand = randint( 1, 100 )
		if ( self.Chance >= rand ):
			player = playerlib.getPlayer( victim )
			speed = player.speed * ( self.slowPercent / 100.0 )
			RaceTools.slowPlayer( victim, speed, self.duration )
			es.tell( victim, '#multi', '#lightgreen%s #greenslowed you for #lightgreen%i #greenseconds' % ( attacker.name, self.duration ) )
	
	def item_purchase( self, event_var ):
		userid = event_var['userid']
		self.messageInformation( userid )
		
	def player_spawn( self, event_var ):
		userid = event_var['userid']
		self.messageInformation( userid )
	
	def messageInformation( self, userid ):
		es.tell( userid, '#multi', '#lightgreen%s #greengrants a #lightgreen%i%% #greenchance to slow a player for #lightgreen%s #greenseconds on attack.' % ( self.Name, self.Chance, str( self.duration ) ) )