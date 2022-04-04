from ...tools import BaseClasses
import es

class Claws(BaseClasses.baseItem):
	extraDamage = 6
	def __init__( self ):
		self.Name          = 'Claws of Attack'
		self.Description   = 'Deals %i bonus damage when you attack.' % self.extraDamage
		self.Price         = 2000
		self.Requiredlevel = 0
		self.Persistent    = 1

	def pre_player_attack( self, event_var ):
		userid = event_var['attacker']
		damage = event_var['dmg_health']
		es.tell( userid, '#multi', '#lightgreenClaws of Attack #greendeal #lightgreen%s #greenbonus damage.' % ( self.extraDamage ) )
		return (damage + self.extraDamage)
		
	def item_purchase( self, event_var ):
		userid = event_var['userid']
		self.messageInformation( userid )
		
	def player_spawn( self, event_var ):
		userid = event_var['userid']
		self.messageInformation( userid )
	
	def messageInformation( self, userid ):
		es.tell( userid, '#multi', '#lightgreen%s #greengrants #lightgreen%i #greenbonus damage on attack.' % ( self.Name, self.extraDamage ) )