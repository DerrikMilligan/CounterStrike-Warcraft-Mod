# Flashbang stuff
es.setplayerprop(userid, 'CCSPlayer.m_flFlashDuration', 10)
es.setplayerprop(userid, 'CCSPlayer.m_flFlashMaxAlpha', 255)

# remove watching these for banning.
kac_removecvar sv_cheats
kac_removecvar r_drawothermodels

# re add teh kac watching
kac_addcvar sv_cheats equal ban 0
kac_addcvar r_drawothermodels equal ban 1

# make player crouched
es_setplayerprop event_var(userid) CBasePlayer.m_fFlags 2
1 -- FL_ONGROUND -- On the ground 
2 -- FL_DUCKING -- Player is fully crouched 
4 -- FL_WATERJUMP -- Player jumping out of water 
8 -- FL_ONTRAIN -- Player is controlling a train, so movement commands should be ignored on client during prediction. 
16 -- FL_INRAIN -- Indicates the entity is standing in rain 
32 -- FL_FROZEN -- Player is frozen for 3rd person camera 
64 -- FL_ATCONTROLS -- Player can't move, but keeps key inputs for controlling another entity 
128 -- FL_CLIENT -- Is a player 
256 -- FL_FAKECLIENT -- Fake client, simulated server side; don't send network messages to them 

# Post on how to get players view coords Trust Super Dave
http://forums.eventscripts.com/viewtopic.php?p=391976#p391976

# make it so when you move your curser over a player their name wont show up
es.setplayerprop(player, "CBaseAnimating.m_nHitboxSet", 2)

# muting people for players
http://forums.eventscripts.com/viewtopic.php?f=125&t=46569

# Drug effect - must execture on clinet
es.server.queuecmd( 'es_xcexec %i "r_screenoverlay effects/tp_eyefx/tp_eyefx"' % ( player ) )