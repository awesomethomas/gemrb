# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003-2004 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# $Header: /data/gemrb/cvs2svn/gemrb/gemrb/gemrb/GUIScripts/bg2/GUIREC.py,v 1.23 2005/11/22 18:50:54 avenger_teambg Exp $


# GUIREC.py - scripts to control stats/records windows from GUIREC winpack

###################################################
import string
import GemRB
import GUICommonWindows
from GUIDefines import *
from ie_stats import *
from GUICommon import CloseOtherWindow
from GUICommonWindows import *
from GUIWORLD import OpenReformPartyWindow

###################################################
RecordsWindow = None
InformationWindow = None
BiographyWindow = None

###################################################
def OpenRecordsWindow ():
	global RecordsWindow, OptionsWindow, PortraitWindow
	global OldPortraitWindow

	if CloseOtherWindow (OpenRecordsWindow):
		if InformationWindow: OpenInformationWindow ()
		
		GemRB.UnloadWindow (RecordsWindow)
		GemRB.UnloadWindow (OptionsWindow)
		GemRB.UnloadWindow (PortraitWindow)

		RecordsWindow = None
		GemRB.SetVar ("OtherWindow", -1)
		GemRB.SetVisible (0,1)
		GemRB.UnhideGUI ()
		GUICommonWindows.PortraitWindow = OldPortraitWindow
		OldPortraitWindow = None
		SetSelectionChangeHandler (None)
		return	

	GemRB.HideGUI ()
	GemRB.SetVisible (0,0)

	GemRB.LoadWindowPack ("GUIREC", 640, 480)
	RecordsWindow = Window = GemRB.LoadWindow (2)
	GemRB.SetVar ("OtherWindow", RecordsWindow)
	#saving the original portrait window
	OldPortraitWindow = GUICommonWindows.PortraitWindow
	PortraitWindow = OpenPortraitWindow(0)
	OptionsWindow = GemRB.LoadWindow(0)
	SetupMenuWindowControls (OptionsWindow, 0, "OpenRecordsWindow")
	GemRB.SetWindowFrame (OptionsWindow)

	# dual class
	Button = GemRB.GetControl (Window, 0)
	GemRB.SetText (Window, Button, 7174)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "DualClassWindow")

	# levelup
	Button = GemRB.GetControl (Window, 37)
	GemRB.SetText (Window, Button, 7175)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "LevelupWindow")

	# information
	Button = GemRB.GetControl (Window, 1)
	GemRB.SetText (Window, Button, 11946)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenInformationWindow")

	# reform party
	Button = GemRB.GetControl (Window, 51)
	GemRB.SetText (Window, Button, 16559)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenReformPartyWindow")

	# customize
	Button = GemRB.GetControl (Window, 50)
	GemRB.SetText (Window, Button, 10645)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "CustomizeWindow")

	# export
	Button = GemRB.GetControl (Window, 36)
	GemRB.SetText (Window, Button, 13956)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "ExportWindow")

	# kit info
	Button = GemRB.GetControl (Window, 52)
	GemRB.SetText (Window, Button, 61265)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "KitInfoWindow")

	SetSelectionChangeHandler (UpdateRecordsWindow)
	UpdateRecordsWindow ()
	GemRB.SetVisible (OptionsWindow, 1)
	GemRB.SetVisible (Window, 3)
	GemRB.SetVisible (PortraitWindow, 1)
	return


def UpdateRecordsWindow ():
	global stats_overview, alignment_help
	
	Window = RecordsWindow
	if not RecordsWindow:
		print "SelectionChange handler points to non existing window\n"
		return

	pc = GemRB.GameGetSelectedPCSingle ()
	
	# name
	Label = GemRB.GetControl (Window, 0x1000000e)
	GemRB.SetText (Window, Label, GemRB.GetPlayerName (pc, 0))

	# portrait
	Button = GemRB.GetControl (Window, 2)
	GemRB.SetButtonState (Window, Button, IE_GUI_BUTTON_LOCKED)
	GemRB.SetButtonFlags (Window, Button, IE_GUI_BUTTON_NO_IMAGE | IE_GUI_BUTTON_PICTURE, OP_SET)
	GemRB.SetButtonPicture (Window, Button, GemRB.GetPlayerPortrait (pc,0))

	# armorclass
	Label = GemRB.GetControl (Window, 0x10000028)
	GemRB.SetText (Window, Label, str (GemRB.GetPlayerStat (pc, IE_ARMORCLASS)))
	GemRB.SetTooltip (Window, Label, 17183)

	# hp now
	Label = GemRB.GetControl (Window, 0x10000029)
	GemRB.SetText (Window, Label, str (GemRB.GetPlayerStat (pc, IE_HITPOINTS)))
	GemRB.SetTooltip (Window, Label, 17184)

	# hp max
	Label = GemRB.GetControl (Window, 0x1000002a)
	GemRB.SetText (Window, Label, str (GemRB.GetPlayerStat (pc, IE_MAXHITPOINTS)))
	GemRB.SetTooltip (Window, Label, 17378)

	# stats

	sstr = GemRB.GetPlayerStat (pc, IE_STR)
	sstrx = GemRB.GetPlayerStat (pc, IE_STREXTRA)
	
	if sstrx > 0 and sstr==18:
		sstr = "%d/%02d" %(sstr, sstrx % 100)
	else:
		sstr = str(sstr)
	sint = str(GemRB.GetPlayerStat (pc, IE_INT))
	swis = str(GemRB.GetPlayerStat (pc, IE_WIS))
	sdex = str(GemRB.GetPlayerStat (pc, IE_DEX))
	scon = str(GemRB.GetPlayerStat (pc, IE_CON))
	schr = str(GemRB.GetPlayerStat (pc, IE_CHR))

	Label = GemRB.GetControl (Window, 0x1000002f)
	GemRB.SetText (Window, Label, sstr)

	Label = GemRB.GetControl (Window, 0x10000009)
	GemRB.SetText (Window, Label, sdex)

	Label = GemRB.GetControl (Window, 0x1000000a)
	GemRB.SetText (Window, Label, scon)

	Label = GemRB.GetControl (Window, 0x1000000b)
	GemRB.SetText (Window, Label, sint)

	Label = GemRB.GetControl (Window, 0x1000000c)
	GemRB.SetText (Window, Label, swis)

	Label = GemRB.GetControl (Window, 0x1000000d)
	GemRB.SetText (Window, Label, schr)

	# class
	ClassTitle = GetActorClassTitle (pc)
	Label = GemRB.GetControl (Window, 0x10000030)
	GemRB.SetText (Window, Label, ClassTitle)

	# race
	Table = GemRB.LoadTable ("races")
	text = GemRB.GetTableValue (Table, GemRB.GetPlayerStat (pc, IE_RACE) - 1, 0)
	GemRB.UnloadTable (Table)
	
	Label = GemRB.GetControl (Window, 0x1000000f)
	GemRB.SetText (Window, Label, text)

	Table = GemRB.LoadTable ("aligns")

	text = GemRB.GetTableValue (Table, GemRB.FindTableValue ( Table, 3, GemRB.GetPlayerStat (pc, IE_ALIGNMENT) ), 0)
	GemRB.UnloadTable (Table)
	Label = GemRB.GetControl (Window, 0x10000010)
	GemRB.SetText (Window, Label, text)

	Label = GemRB.GetControl (Window, 0x10000011)
	if GemRB.GetPlayerStat (pc, IE_SEX) ==  1:
		GemRB.SetText (Window, Label, 7198)
	else:
		GemRB.SetText (Window, Label, 7199)

	#collecting tokens for stat overview
	ClassTitle = GemRB.GetString (GetActorClassTitle (pc) )

	GemRB.SetToken("CLASS", ClassTitle)
	GemRB.SetToken("LEVEL", str (GemRB.GetPlayerStat (pc, IE_LEVEL) ) )
	GemRB.SetToken("EXPERIENCE", str (GemRB.GetPlayerStat (pc, IE_XP) ) )

	# help, info textarea
	stats_overview = GetStatOverview (pc)
	Text = GemRB.GetControl (Window, 45)
	GemRB.SetText (Window, Text, stats_overview)
	#making window visible/shaded depending on the pc's state
	GemRB.SetVisible (Window, 1)
	return

def GetStatOverview (pc):
	#dunno if bg2 has colour highlights
	#won = "[color=FFFFFF]"
	#woff = "[/color]"
	won = ""
	woff = ""
	str_None = GemRB.GetString (61560)
	
	GS = lambda s, pc=pc: GemRB.GetPlayerStat (pc, s)

	stats = []
	# 16480 <CLASS>: Level <LEVEL>
	# Experience: <EXPERIENCE>
	# Next Level: <NEXTLEVEL>

	Main = GemRB.GetString (16480)
	stats.append (None)

	stats.append (8442)
	stats.append ( (61932, GS (IE_THAC0), '') )
	stats.append ( (9457, GS (IE_THAC0), '') )
	stats.append ( (9458, GS (IE_NUMBEROFATTACKS), '') )
	stats.append ( (9459, GS (IE_LORE), '') )
	reptxt = GetReputation (GemRB.GameGetReputation()/10)
	stats.append ( (9465, reptxt, '') )
	stats.append ( (9460, GS (IE_LOCKPICKING), '') )
	stats.append ( (9462, GS (IE_TRAPS), '') )
	stats.append ( (9463, GS (IE_PICKPOCKET), '') )
	stats.append ( (9461, GS (IE_STEALTH), '') )
	stats.append ( (34120, GS (IE_HIDEINSHADOWS), '') )
	stats.append ( (34121, GS (IE_DETECTILLUSIONS), '') )
	stats.append ( (34122, GS (IE_SETTRAPS), '') )
	stats.append ( (12128, GS (IE_BACKSTABDAMAGEMULTIPLIER), 'x') )
	stats.append ( (12126, GS (IE_TURNUNDEADLEVEL), '') )
	stats.append ( (12127, GS (IE_LAYONHANDSAMOUNT), '') )
	stats.append (2078)
	stats.append (None)


	#   17379 Saving Throws
	stats.append (17379)
	#   17380 Death
	stats.append ( (17380, GS (IE_SAVEVSDEATH), '') )
	#   17381 
	stats.append ( (17381, GS (IE_SAVEVSWANDS), '') )
	#   17382 AC vs. Crushing
	stats.append ( (17382, GS (IE_SAVEVSPOLY), '') )
	#   17383 Rod
	stats.append ( (17383, GS (IE_SAVEVSBREATH), '') )
	#   17384 Spells
	stats.append ( (17384, GS (IE_SAVEVSSPELL), '') )
	stats.append (None)

	# 9466 Weapon profs
	stats.append (9466)
	table = GemRB.LoadTable("weapprof")
	RowCount = GemRB.GetTableRowCount (table)
	# the first 7 profs are foobared
	for i in range(8,RowCount):
		text = GemRB.GetTableValue (table, i, 1)
		stat = GemRB.GetTableValue (table, i, 0)
		stats.append ( (text, GS(stat), '+') )
	stats.append (None)

	# 11766 AC Bonuses
	stats.append (11766)
	#   11770 AC vs. Crushing
	stats.append ((11770, GS (IE_ACCRUSHINGMOD), ''))
	#   11767 AC vs. Missile
	stats.append ((11767, GS (IE_ACMISSILEMOD), ''))
	#   11769 AC vs. Piercing
	stats.append ((11769, GS (IE_ACPIERCINGMOD), ''))
	#   11768 AC vs. Slashing
	stats.append ((11768, GS (IE_ACSLASHINGMOD), ''))
	stats.append (None)

	# 10315 Ability bonuses
	stats.append (10315)
	value = GemRB.GetPlayerStat (pc, IE_STR)
	ex = GemRB.GetPlayerStat (pc, IE_STREXTRA)
	# 10332 to hit
	stats.append ( (10332, GemRB.GetAbilityBonus(IE_STR,0,value,ex), '') )
	# 10336 damage
	stats.append ( (10336, GemRB.GetAbilityBonus(IE_STR,1,value,ex), '') )
	# 10337 open doors (bend bars lift gates)
	stats.append ( (10337, GemRB.GetAbilityBonus(IE_STR,2,value,ex), '') )
	# 10338 weight allowance
	stats.append ( (10338, GemRB.GetAbilityBonus(IE_STR,3,value,ex), '') )
	# 10339 AC
	value = GemRB.GetPlayerStat (pc, IE_DEX)
	stats.append ( (10339, GemRB.GetAbilityBonus(IE_DEX,2,value), '') )
	# 10340 Missile
	stats.append ( (10340, GemRB.GetAbilityBonus(IE_DEX,1,value), '') )
	# 10341 Reaction
	stats.append ( (10341, GemRB.GetAbilityBonus(IE_DEX,0,value), '') )
	value = GemRB.GetPlayerStat (pc, IE_CON)
	# 10342 Hp/Level
	stats.append ( (10342, GemRB.GetAbilityBonus(IE_CON,0,value), '') )
	value = GemRB.GetPlayerStat (pc, IE_CHR)
	stats.append ( (10347, GemRB.GetAbilityBonus(IE_CHR,0,value), '') )
	stats.append (0)

	stats.append (10344)
	stats.append (10345)

	# 32204 Resistances
	stats.append (32204)
	#   32213 Normal Fire
	stats.append ((32213, GS (IE_RESISTFIRE), '%'))
	#   32222 Magic Fire
	stats.append ((32222, GS (IE_RESISTMAGICFIRE), '%'))
	#   32214 Normal Cold
	stats.append ((32214, GS (IE_RESISTCOLD), '%'))
	#   32223 Magic Cold
	stats.append ((32223, GS (IE_RESISTMAGICCOLD), '%'))
	#   32220 Electricity
	stats.append ((32220, GS (IE_RESISTELECTRICITY), '%'))
	#   32221 Acid
	stats.append ((32221, GS (IE_RESISTACID), '%'))
	#   32233 Magic Damage
	stats.append ((32233, GS (IE_RESISTMAGIC), '%'))
	#   67216 Slashing Attacks
	stats.append ((67216, GS (IE_RESISTSLASHING), '%'))
	#   67217 Piercing Attacks
	stats.append ((67217, GS (IE_RESISTPIERCING), '%'))
	#   67218 Crushing Attacks
	stats.append ((67218, GS (IE_RESISTCRUSHING), '%'))
	#   67219 Missile Attacks
	stats.append ((67219, GS (IE_RESISTMISSILE), '%'))
	stats.append (None)

	stats.append (32131)
	#stats.append (10340)

	res = []
	lines = 0
	for s in stats:
		try:
			strref, val, type = s
			if val == 0 and type != '0':
				continue
			if type == '+':
				res.append (GemRB.GetString (strref) + ' '+ '+'
* val)
			elif type == 'x':
				res.append (GemRB.GetString (strref)+': x' + str (val) )
			else:
				res.append (GemRB.GetString (strref) + ': ' + str (val) + type)
			lines = 1
		except:
			if s != None:
				res.append (won + GemRB.GetString (s) + woff)
				lines = 0
			else:
				if not lines:
					res.append (str_None)
				res.append ("")
				lines = 0

	return Main + string.join (res, "\n")


def GetReputation (repvalue):
	table = GemRB.LoadTable ("reptxt")
	if repvalue>20:
		repvalue=20
	txt = GemRB.GetString (GemRB.GetTableValue (table, repvalue, 0) )
	GemRB.UnloadTable (table)
	return txt+"("+str(repvalue)+")"


def OpenInformationWindow ():
	global InformationWindow
	
	if InformationWindow != None:
		if BiographyWindow: OpenBiographyWindow ()

		GemRB.UnloadWindow (InformationWindow)
		GemRB.SetVisible (OptionsWindow, 3)
		GemRB.SetVisible (RecordsWindow, 3)
		GemRB.SetVisible (PortraitWindow, 3)
		InformationWindow = None
		
		return

	InformationWindow = Window = GemRB.LoadWindow (4)

	# Biography
	Button = GemRB.GetControl (Window, 26)
	GemRB.SetText (Window, Button, 18003)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenBiographyWindow")

	# Done
	Button = GemRB.GetControl (Window, 24)
	GemRB.SetText (Window, Button, 11973)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenInformationWindow")

	TotalPartyExp = 0
	ChapterPartyExp = 0
	TotalCount = 0
	ChapterCount = 0
	for i in range (1, GemRB.GetPartySize() + 1):
		stat = GemRB.GetPCStats(i)
		TotalPartyExp = TotalPartyExp + stat['KillsChapterXP']
		ChapterPartyExp = ChapterPartyExp + stat['KillsTotalXP']
		TotalCount = TotalCount + stat['KillsChapterCount']
		ChapterCount = ChapterCount + stat['KillsTotalCount']

	# These are used to get the stats
	pc = GemRB.GameGetSelectedPCSingle ()
	stat = GemRB.GetPCStats (pc)

	Label = GemRB.GetControl (Window, 0x10000000)
	GemRB.SetText (Window, Label, GemRB.GetPlayerName (pc, 1))
	# class
	ClassTitle = GetActorClassTitle(pc)
	Label = GemRB.GetControl (Window, 0x10000018)
	GemRB.SetText (Window, Label, ClassTitle)

	#most powerful vanquished
	Label = GemRB.GetControl (Window, 0x10000005)
	#we need getstring, so -1 will translate to empty string
	GemRB.SetText (Window, Label, GemRB.GetString (stat['BestKilledName']))

	# NOTE: currentTime is in seconds, joinTime is in seconds * 15
	#   (script updates???). In each case, there are 60 seconds
	#   in a minute, 24 hours in a day, but ONLY 5 minutes in an hour!!
	# Hence currentTime (and joinTime after div by 15) has
	#   7200 secs a day (60 * 5 * 24)
	currentTime = GemRB.GetGameTime()
	joinTime = stat['JoinDate'] - stat['AwayTime']

	party_time = currentTime - (joinTime / 15)
	days = party_time / 7200
	hours = (party_time % 7200) / 300

	GemRB.SetToken ('GAMEDAYS', str (days))
	GemRB.SetToken ('HOUR', str (hours))
	Label = GemRB.GetControl (Window, 0x10000006)
	#actually it is 16043 <DURATION>, but duration is translated to
	#16041, hopefully this won't cause problem with international version
	GemRB.SetText (Window, Label, 16041)

	#favourite spell
	Label = GemRB.GetControl (Window, 0x10000007)
	GemRB.SetText (Window, Label, stat['FavouriteSpell'])

	#favourite weapon
	Label = GemRB.GetControl (Window, 0x10000008)
	#actually it is 10479 <WEAPONNAME>, but weaponname is translated to
	#the real weapon name (which we should set using SetToken)
	#there are other strings like bow+wname/xbow+wname/sling+wname
	#are they used?
	GemRB.SetText (Window, Label, stat['FavouriteWeapon'])

	#total xp 
	Label = GemRB.GetControl (Window, 0x1000000f)
	if TotalPartyExp != 0:
		PartyExp = int ((stat['KillsTotalXP'] * 100) / TotalPartyExp)
		GemRB.SetText (Window, Label, str (PartyExp) + '%')
	else:
		GemRB.SetText (Window, Label, "0%")

	Label = GemRB.GetControl (Window, 0x10000013)
	if ChapterPartyExp != 0:
		PartyExp = int ((stat['KillsChapterXP'] * 100) / ChapterPartyExp)
		GemRB.SetText (Window, Label, str (PartyExp) + '%')
	else:
		GemRB.SetText (Window, Label, "0%")

	#total xp 
	Label = GemRB.GetControl (Window, 0x10000010)
	if TotalCount != 0:
		PartyExp = int ((stat['KillsTotalCount'] * 100) / TotalCount)
		GemRB.SetText (Window, Label, str (PartyExp) + '%')
	else:
		GemRB.SetText (Window, Label, "0%")

	Label = GemRB.GetControl (Window, 0x10000014)
	if ChapterCount != 0:
		PartyExp = int ((stat['KillsChapterCount'] * 100) / ChapterCount)
		GemRB.SetText (Window, Label, str (PartyExp) + '%')
	else:
		GemRB.SetText (Window, Label, "0%")

	Label = GemRB.GetControl (Window, 0x10000011)
	GemRB.SetText (Window, Label, str (stat['KillsChapterXP']))
	Label = GemRB.GetControl (Window, 0x10000015)
	GemRB.SetText (Window, Label, str (stat['KillsTotalXP']))

	#count of kills in chapter/game
	Label = GemRB.GetControl (Window, 0x10000012)
	GemRB.SetText (Window, Label, str (stat['KillsChapterCount']))
	Label = GemRB.GetControl (Window, 0x10000016)
	GemRB.SetText (Window, Label, str (stat['KillsTotalCount']))

	GemRB.ShowModal (Window, MODAL_SHADOW_GRAY)
	return

def OpenBiographyWindow ():
	global BiographyWindow

	if BiographyWindow != None:
		GemRB.UnloadWindow (BiographyWindow)
		BiographyWindow = None
		GemRB.ShowModal (InformationWindow, MODAL_SHADOW_GRAY)
		return

	BiographyWindow = Window = GemRB.LoadWindow (12)

	TextArea = GemRB.GetControl (Window, 0)
	GemRB.SetText (Window, TextArea, 39424)

	
	# Done
	Button = GemRB.GetControl (Window, 2)
	GemRB.SetText (Window, Button, 1403)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenBiographyWindow")

	GemRB.ShowModal (Window, MODAL_SHADOW_GRAY)
	
###################################################
# End of file GUIREC.py
