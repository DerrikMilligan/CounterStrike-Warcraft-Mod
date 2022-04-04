from ...tools import BaseClasses
from random import randint

import es
import playerlib

class Mask(BaseClasses.baseItem):
	Chance     = 20
	Percentage = 0.4
	def __init__( self ):
		self.Name          = 'Mask of Death'
		self.Description   = 'Gain health when you deal damage.'
		self.Price         = 3500
		self.Requiredlevel = 0
		self.Persistent    = 1

	def player_attack( self, event_var ):
		# victim = event_var['userid']
		player = event_var['attacker']
		damage = int( event_var['dmg_health'] )
		rand = randint( 1, 100 )
		if ( self.Chance >= rand ):
			leech = damage * self.Percentage
			player = playerlib.getPlayer( player )
			player.health += leech
			# es.server.queuecmd( 'damage %s %i %i %s' % ( str(victim), extraDamage, 32, str(userid) ) )
	
	def item_purchase( self, event_var ):
		userid = event_var['userid']
		self.messageInformation( userid )
		
	def player_spawn( self, event_var ):
		userid = event_var['userid']
		self.messageInformation( userid )
	
	def messageInformation( self, userid ):
		es.tell( userid, '#multi', '#lightgreen%s #greengrants a #lightgreen%i%% #greenchance to leech #lightgreen%i%% #greenof damage back in health.' % ( self.Name, self.Chance, int(self.Percentage*100) ) )