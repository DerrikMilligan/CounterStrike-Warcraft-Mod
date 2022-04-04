from ...tools import BaseClasses
from ...tools import DatabaseManager
import es
import playerlib

class Wisdom(BaseClasses.baseItem):
	def __init__( self ):
		self.Name          = 'Tome of Wisdom'
		self.Description   = 'Grants 1000 Experience.'
		self.Price         = 15000
		self.Requiredlevel = 0
		self.Persistent    = 0

		self.XP            = 1000
	
	def item_purchase( self, event_var ):
		player    = playerlib.getPlayer( event_var['userid'] )
		wcsPlayer = self.helper.getPlayer( player )

		wcsPlayer.roundXP += self.XP

		es.tell( player, '#multi', '#lightgreenTome of Wisdom #greengrants you #lightgreen%i #greenXP!' % self.XP )