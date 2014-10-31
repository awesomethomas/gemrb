# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2010 The GemRB Project
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#################### Interchapter text screen functions #################

import GemRB
from GUIDefines import *
import GUICommon
import GameCheck

TextScreen = None
TextArea = None
Row = 1
TableName = None

def FindTextRow (Table):
	global Row

	#this is still not the full implementation, but the original engine never used this stuff
	Row = Table.GetRowIndex("DEFAULT")
	if Table.GetValue (Row, 1)== -1:
		if GemRB.GameGetReputation() >= 100:
			Row = Table.GetRowIndex("GOOD_REPUTATION")
		else:
			Row = Table.GetRowIndex("BAD_REPUTATION")
	return

def StartTextScreen ():
	global TextScreen, TextArea, TableName, Row

	GemRB.GamePause (1, 3)

	ID = -1
	MusicName = "*"
	Message = 17556   # default: Paused for chapter text
	TableName = GemRB.GetGameString (STR_TEXTSCREEN)

	#iwd2/bg2 has no separate music
	if GameCheck.IsIWD1():
		if TableName == "":
			MusicName = "chap0"
		else:
			MusicName = "chap1"
		TableName = "chapters"
	elif GameCheck.IsIWD2():
		TableName = "chapters"

	if TableName == "":
		EndTextScreen ()
		return
	else:
		TextTable = GemRB.LoadTable ("textscrn", 1)
		if TextTable != None:
			TxtRow = TextTable.GetRowIndex (TableName)
			if TxtRow >= 0:
				ID = TextTable.GetValue (TxtRow, 0)
				MusicName = TextTable.GetValue (TxtRow, 1)
				Message = TextTable.GetValue (TxtRow, 2)

	if Message != "*":
		GemRB.DisplayString (Message, 0xff0000)

	if GameCheck.IsIWD2():
		GemRB.LoadWindowPack ("GUICHAP", 800, 600)
	else:
		GemRB.LoadWindowPack ("GUICHAP", 640, 480)

	if GameCheck.IsBG2():
		ID = 62
	elif ID == -1:
		#default: try to determine ID from current chapter
		ID = GemRB.GetGameVar("CHAPTER") & 0x7fffffff
		Chapter = ID + 1

	if MusicName != "*":
		GemRB.LoadMusicPL (MusicName + ".mus")
	else:
		GemRB.HardEndPL ()

	TextScreen = GemRB.LoadWindow (ID)
	TextScreen.SetFrame ()

	TextArea = TextScreen.GetControl (2)
	TextArea.SetFlags (IE_GUI_TEXTAREA_SMOOTHSCROLL)

	Table = GemRB.LoadTable (TableName)
	if GameCheck.IsBG1():
		#these suckers couldn't use a fix row
		FindTextRow (Table)
	elif GameCheck.IsBG2():
		LoadPic = Table.GetValue (-1, -1)
		if LoadPic != "":
			TextScreen.SetPicture (LoadPic)
		FindTextRow (Table)
	else:
		Row = Chapter

	#caption
	Value = Table.GetValue (Row, 0)
	#don't display the fake -1 string (No caption in toscst.2da)
	if Value!="NONE" and Value>0 and TextScreen.HasControl(0x10000000):
		Label=TextScreen.GetControl (0x10000000)
		Label.SetText (Value)

	#done
	Button=TextScreen.GetControl (0)
	Button.SetText (11973)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, EndTextScreen)
	Button.SetFlags (IE_GUI_BUTTON_DEFAULT|IE_GUI_BUTTON_CANCEL,OP_OR)

	#replay
	Button=TextScreen.GetControl (3)
	Button.SetText (16510)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, ReplayTextScreen)

	#if this was opened from somewhere other than game control close that window
	GUICommon.CloseOtherWindow(None)
	GemRB.HideGUI ()
	GUICommon.GameWindow.SetVisible(WINDOW_INVISIBLE) #removing the gamecontrol screen
	TextScreen.SetVisible (WINDOW_VISIBLE)

	ReplayTextScreen()
	return

def EndTextScreen ():
	global TextScreen

	if TextScreen:
		TextScreen.SetVisible (WINDOW_INVISIBLE)
		TextScreen.Unload ()
		GemRB.PlaySound(None, 0, 0, 4)

	GUICommon.GameWindow.SetVisible(WINDOW_VISIBLE) # enable the gamecontrol screen
	GemRB.UnhideGUI ()
	GemRB.GamePause (0, 3)
	return

def ReplayTextScreen ():
	global TextArea, TableName, Row

	TextArea.Rewind ()

	Table = GemRB.LoadTable (TableName)
	Count = Table.GetColumnCount (Row)

	#hack for messy chapters.2da in IWD
	#note: iwd doesn't use TextScreen, only IncrementChapter
	if GameCheck.IsIWD1() or GameCheck.IsIWD2():
		Count = 2

	for i in range(1, Count):
		TextArea.Append ("\n")
		# flag value of 14 = IE_STR_SOUND|IE_STR_SPEECH/GEM_SND_SPEECH|GEM_SND_QUEUE
		TextArea.Append (Table.GetValue (Row, i), -1, 14)

	return
