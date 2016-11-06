import os
import time
letters="qwertyuiopasdfghjklzxcvbnm"
def intcreate(number):
	numbers=[]
	for i in range(0,len(number)):
		if number[i].isdigit():
				numbers.append(number[i])
	return int(''.join(numbers))
def osufriendlyname(name):
	goodname=[]
	for i in range(0,len(name)):
		if name[i]==" ":
			goodname.append("_")
		else:
			goodname.append(name[i])
	return ''.join(goodname)
def fixname(name):
	goodname=[]
	for i in range(0,len(name)):
		if name[i]=="_":
			goodname.append(" ")
		else:
			goodname.append(name[i])
	return ''.join(goodname)
def playerchoice():
	global tournamentsize
	global tournamentsubs
	global TeamRed
	global TeamBlue
	global TeamRedSubs
	global TeamBlueSubs
	global team1name
	global team2name
	global play
	TeamRed=[]
	TeamBlue=[]
	TeamRedSubs=[]
	TeamBlueSubs=[]
	if input("(y/n) Do you want players to be added to the hotkey: ").lower()=="y":
		team1name=input("Team 1 name: ")
		team2name=input("Team 2 name: ")
		for i in range(0,tournamentsize+tournamentsubs):
			if i<tournamentsize:
				TeamBlue.append(input(("Team ({}) Player {}: ").format(team1name,i+1)))	
			else:
				sub=input(("(leave blank if none) Team ({}) Sub {}: ").format(team1name,i+1-tournamentsize))
				if sub!="":
					TeamBlueSubs.append(sub)
				else:
					break
		for i in range(0,tournamentsize+tournamentsubs):
			if i<tournamentsize:
				TeamRed.append(input(("Team ({}) Player {}: ").format(team2name,i+1)))
			else:
				sub=input(("(leave blank if none) Team ({}) Sub {}: ").format(team2name,i+1-tournamentsize))
				if sub!="":
					TeamRedSubs.append(sub)
				else:
					break
		play="yes"
	else:
		play="no"
def playerwrite():
	if play=="yes":
		global TeamRed
		global TeamBlue
		global TeamRedSubs
		global TeamBlueSubs
		global team1name
		global team2name
		global scriptmain
		global scriptinstructions
		global tournamentsize
		global tournamentname
		team1hotkeys=["F5","F6","F7","F8"]
		team2hotkeys=["F9","F10","F11","F12"]
		scriptmain.write((""">^F1::
	Send,	{{!}}mp make {}: ({}) vs ({})
Return\n\n""").format(tournamentname,team1name,team2name))
		for i in range(0,tournamentsize+len(TeamBlueSubs)):
			if i<tournamentsize:
				scriptmain.write((""">^{0}::
	loop {{		
		if GetKeyState("1","P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 1 {{ENTER}}
			break
			}}
		if GetKeyState("2", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 2 {{ENTER}}
			break
			}}
		if GetKeyState("3", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 3 {{ENTER}}
			break
			}}
		if GetKeyState("4", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 4 {{ENTER}}
			break
			}}
		if GetKeyState("ESC", "P")=1
			{{
			Return
			}}
	}}
	Sleep,  1000
	Send,	{{!}}mp team {1} blue {{ENTER}}
Return\n\n""").format(team1hotkeys[i],osufriendlyname(TeamBlue[i])))
			else:
				scriptmain.write((""">+{0}::
	loop {{		
		if GetKeyState("1","P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 1 {{ENTER}}
			break
			}}
		if GetKeyState("2", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 2 {{ENTER}}
			break
			}}
		if GetKeyState("3", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 3 {{ENTER}}
			break
			}}
		if GetKeyState("4", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 4 {{ENTER}}
			break
			}}
		if GetKeyState("ESC", "P")=1
			{{
			Return
			}}
	}}
	Sleep,  1000
	Send,	{{!}}mp team {1} blue {{ENTER}}
Return\n\n""").format(team1hotkeys[i-tournamentsize],osufriendlyname(TeamBlueSubs[i-tournamentsize])))
		for i in range(0,tournamentsize+len(TeamRedSubs)):
			if i<tournamentsize:
				scriptmain.write((""">^{0}::
	loop {{		
		if GetKeyState("1","P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 1 {{ENTER}}
			break
			}}
		if GetKeyState("2", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 2 {{ENTER}}
			break
			}}
		if GetKeyState("3", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 3 {{ENTER}}
			break
			}}
		if GetKeyState("4", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 4 {{ENTER}}
			break
			}}
		if GetKeyState("ESC", "P")=1
			{{
			Return
			}}
	}}
	Sleep,  1000
	Send,	{{!}}mp team {1} red {{ENTER}}
Return\n\n""").format(team2hotkeys[i],osufriendlyname(TeamRed[i])))
			else:
				scriptmain.write((""">+{0}::
	loop {{		
		if GetKeyState("1","P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 1 {{ENTER}}
			break
			}}
		if GetKeyState("2", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 2 {{ENTER}}
			break
			}}
		if GetKeyState("3", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 3 {{ENTER}}
			break
			}}
		if GetKeyState("4", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {1} 4 {{ENTER}}
			break
			}}
		if GetKeyState("ESC", "P")=1
			{{
			Return
			}}
	}}
	Sleep,  1000
	Send,	{{!}}mp team {1} red {{ENTER}}
Return\n\n""").format(team2hotkeys[i-tournamentsize],osufriendlyname(TeamRedSubs[i-tournamentsize])))
		scriptinstructions.write(("-----------------\nTeam Blue players ({}):\n").format(team1name))
		for i in range(0,tournamentsize+len(TeamBlueSubs)):
			if i<tournamentsize:
					scriptinstructions.write(TeamBlue[i]+"\n")
			else:
				scriptinstructions.write(("*{}\n").format(TeamBlueSubs[i-tournamentsize]))
		scriptinstructions.write(("-----------------\nTeam Red players ({}):\n").format(team2name))
		for i in range(0,tournamentsize+len(TeamRedSubs)):
			if i<tournamentsize:
				scriptinstructions.write(TeamRed[i]+"\n")
			else:
				scriptinstructions.write(("*{}\n").format(TeamRedSubs[i-tournamentsize]))
	scriptinstructions.write("""-----------------
Instructions:
Use right control and designated key (etc: q) for changing maps.
Use right control and F5-F12 keys to move players (F5-F8 for Team Blue and F9-F12 for Team Red)
Use right shift and F5-F12 keys to move subs (shown on the list with a *)
Use 1-4 after using either of the 2 moving hotkeys to choose slot
Extra right control commands:
F1 to create match with Bancho
F2 to add settings
F3 to start match
F4 for generic message on asking if player is ready""")
	scriptmain.close()
	scriptinstructions.close()
def tournamentsettings():
	global tournamentname
	global tournamentsize
	global tournamentsubs
	global tournamentmode
	tournamentname=input("Tournament abbreviation: ")
	while True:
		tournamentsize=intcreate(input("Tournament team size: "))
		if tournamentsize>=1 and tournamentsize<=4:
			while True:
				tournamentsubs=intcreate(input("How many maximum subs (per team): "))
				if tournamentsubs>=1 and tournamentsubs<=4:
					break
				else:
					print("This program cannot handle more than 4 subs.")
			break
	if tournamentsize==1:
		tournamentmode="0"
	else:
		tournamentmode="2"
def mappoolcreation():
	global mappool
	mappool=[]
	while True:
		maps=intcreate(input("How many maps in the map pool: "))
		if maps>26:
			print("This program doesn't support more than 26 maps.")
		if maps<1:
			print("You can't have no maps.")
		else:
			break
	for i in range(0,maps):
		mapid=input(("Map ID {}: ").format(i+1))
		while True:
			if mapid.isdigit()==False:
				mapid=input("Invalid map ID. Please retype: ")
			elif int(mapid)<0:
				mapid=input("Invalid map ID. Please retype: ")
			else:
				break
		mapname=input("Map name: ")
		mapmods=input("(1-nomod, 2-hidden, 3-hardrock, 4-doubletime, 5-freemod, 6-tiebreaker/nomod) Map mod: ")
		while True:
			if mapmods.isdigit()==False:
				mapmods=input("Map mods are invalid. Please retype: ")			
			if int(mapmods)>6 or int(mapmods)<1:
				mapmods=input("Map mods are invalid. Please retype: ")
			else:
				break
		mappool.append([int(mapid),mapname,int(mapmods)])
def logmap(mappool):
	global scriptinstructions
	global scriptmain
	mapnumber=0
	for i in range(1,7):
		if i==1:
			scriptinstructions.write("-----------------\nNomod maps:\n")
		if i==2:
			scriptinstructions.write("-----------------\nHidden maps:\n")
		if i==3:
			scriptinstructions.write("-----------------\nHard rock maps:\n")
		if i==4:
			scriptinstructions.write("-----------------\nDouble time maps:\n")
		if i==5:
			scriptinstructions.write("-----------------\nFreemod maps:\n")
		if i==6:
			scriptinstructions.write("-----------------\nTie breaker:\n")		
		for j in range(0,len(mappool)):
			if mappool[j][2]==i:
				mapnumber=mapnumber+1
				scriptinstructions.write(("Map {}: {} (Shortcut: {})\n").format(mapnumber,mappool[j][1],letters[j]))	
	for i in range(0,len(mappool)):
		if mappool[i][2]==1:
			mappool[i][2]="nomod"
		if mappool[i][2]==2:
			mappool[i][2]="hd"
		if mappool[i][2]==3:
			mappool[i][2]="hr"
		if mappool[i][2]==4:
			mappool[i][2]="dt"
		if mappool[i][2]==5:
			mappool[i][2]="freemod"
		if mappool[i][2]==6:
			mappool[i][2]="freemod"
		scriptmain.write((""">^{}::
	Send,   {{!}}mp map {} {{ENTER}}
	Sleep,	1000
	Send,	{{!}}mp mods {} {{ENTER}}
Return\n\n""").format(letters[i],mappool[i][0],mappool[i][2]))				
def mappoolsavefile():
	global mappool
	if input("(y/n) Save maps to mapfile? ").lower()=="y":
		savefilename=input("(txt files with this name will be overwritten) Save to what file name? ")
		scriptmappoolsave=open("{}.txt".format(savefilename),"w")
		for i in range(0,len(mappool)):
			scriptmappoolsave.write("{},{},{}\n".format(mappool[i][0],mappool[i][1],mappool[i][2]))
		scriptmappoolsave.close()
def savefile(tournamentname):
	if input("(y/n) Create save file? ").lower()=="y":
		scriptmain=open("{}.txt".format(tournamentname),"r")
		scriptinstructions=open("{} instructions.txt".format(tournamentname),"r")
		scriptsavefile=open("savefile-{}.txt".format(tournamentname),"w")
		linecounter=0
		list=[]
		for line in scriptmain:
			list.append(line)
			linecounter=linecounter+1
		for line in scriptinstructions:
			list.append(line)
		scriptsavefile.write(str(linecounter)+"\n")
		for i in range(0,len(list)):
			scriptsavefile.write(list[i])
		scriptmain.close()
		scriptinstructions.close()
		scriptsavefile.close()
		os.rename("savefile-{}.txt".format(tournamentname),"savefile-{}.xddd".format(tournamentname))
def scriptstart(realcount,playerstrue):
	global scriptmain
	global scriptinstructions
	global tournamentname
	global tournamentsize
	global tournamentsubs
	scriptmain=open("{}.txt".format(tournamentname),"w")
	scriptinstructions=open("{} instructions.txt".format(tournamentname),"w")
	scriptmain.write((""";{}{}{},{}
#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%\n
>^F2::
	Send,	{{!}}mp size {} {{ENTER}}
	Sleep,  1000
	Send,	{{!}}mp set {} {{ENTER}}
Return\n
>^F3::
	Send,	{{!}}mp start 5
Return\n
>^F4::
	Send,	Are you ready for your {} match? {{ENTER}}
Return\n\n""").format(tournamentsize,tournamentsubs,realcount,playerstrue,tournamentsize*2,tournamentmode,tournamentname))
option=input("""0 - New Tournament File (destroys files with same tournament name)
1 - Update existing file
2 - Import map file\n""")
if option=="0":
	tournamentsettings()
	playerchoice()
	scriptstart(tournamentsize*2+len(TeamRedSubs)+len(TeamBlueSubs),play)
	mappoolcreation()	
	mappoolsavefile()
	logmap(mappool)
	playerwrite()
	savefile(tournamentname)
	os.rename("{}.txt".format(tournamentname),"{}.ahk".format(tournamentname))
if option=="1":
	while True:
		try:
			tournamentname=input("Tournament abbreviation: ")
			os.rename("{}.ahk".format(tournamentname),"{}.txt".format(tournamentname))
			break
		except:
			print("You have no existing file for this tournament.")
	scriptmain=open("{}.txt".format(tournamentname),"r")
	scriptinstructions=open("{} instructions.txt".format(tournamentname),"r")
	file=[]
	file2=[]
	marker=scriptmain.readline()
	tournamentsize=int(marker[1])
	tournamentsubs=int(marker[2])
	for line in scriptmain:
		file.append(line)
	for line in scriptinstructions:
		file2.append(line)
	if marker[-4:]=="yes\n":
		players=int(marker[3:-5])
		for i in range(0,int(marker[3:-5])*31+5):
			file.pop()
		for i in range(0,int(marker[3])+5):
			file2.pop()
	else:
		file.append("\n")
	playerchoice()
	scriptmain=open("{}.txt".format(tournamentname),"w")
	scriptinstructions=open("{} instructions.txt".format(tournamentname),"w")	
	scriptmain.write(";{}{}{},yes\n".format(tournamentsize,tournamentsubs,(tournamentsize*2+len(TeamRedSubs)+len(TeamBlueSubs))))
	for i in range(0,len(file)):
		scriptmain.write(file[i])
	for i in range(0,len(file2)):
		scriptinstructions.write(file2[i])
	playerwrite()
	savefile(tournamentname)
	os.rename("{}.txt".format(tournamentname),"{}.ahk".format(tournamentname))
if option=="2":
	mappool=[]
	while True:
		importfile=input("Name of imported file: ")
		try:
			mapimport=open("{}.txt".format(importfile),'r')
			break
		except:
			print("No import file with the name {}.txt".format(importfile))
	try:		
		for line in mapimport:
			mapid,mapname,mapmods=line.split(",")
			mappool.append([int(mapid),mapname,int(mapmods)])
			if int(mapmods)<1 or int(mapmods)>6:
				print("Bad file (1)")
				time.sleep(3)
				quit()
	except:
		print("Bad file")
		time.sleep(3)
		quit()
	tournamentsettings()
	playerchoice()
	scriptstart(tournamentsize*2+len(TeamRedSubs)+len(TeamBlueSubs),play)
	logmap(mappool)
	playerwrite()
	savefile(tournamentname)
	os.rename("{}.txt".format(tournamentname),"{}.ahk".format(tournamentname))
if option=="3":
	inputmethod=input("""0 - Start from scratch
1 - Import map file
2 - Import from savefile""")
	if option=="0":
		tournamentsettings()
		banamount=input("How many bans per team? ")
		while True:
			banformat=intcreate(input("""How are bans selected?
0 - Alternating bans
1 - Teams pick all their bans together
"""))
			if banformat<=0 or banformat>=1:
				break
		playerchoice()
		mappoolcreation()
		mappoollist=[]
		for i in range(0,len(mappool)):
			mappoollist.append(mappool[i][1],letters[i])
			print("Please ask captains to roll.")
			if input("(1/2) Higher team: ") == "1":
				team1=[team1name,"blue"]
			else:
				team2=[team2name,"red"]
			warmup=[]
			bans=[]
			team1bans=[]
			team2bans=[]
			for i in range(0,2):
				warmup.append(input("Warmup: "))
			for i in range(0,len(mappool)):
				print("{} - {}".format(mappool[i][1],letters[i]))
			for i in range(0,banamount*2):
				if i=="0":
					   print("(use map letters, not name)")
				if (i/2).is_integer:
					team1bans.append(input("Banned map ({}): "))
				else:
					team2bans.append(input("Banned map ({}): "))		
		mappoolsavefile()		
if option=="4":
	while True:
		try:
			tournamentname=input("Tournament name: ")
			os.rename("savefile-{}.xddd".format(tournamentname),"temporarysavefile.txt")
			break
		except:
			print("Invalid save file name.")
	script=open("temporarysavefile.txt","r")
	marker=script.readline()
	list1=[]
	list2=[]
	linenumber=0
	for line in script:
		linenumber=linenumber+1
		if linenumber<=int(marker):
			list1.append(line)
		else:
			list2.append(line)
	script.close()
	os.rename("temporarysavefile.txt","savefile-{}.xddd".format(tournamentname))
	script2=open("{}.txt".format(tournamentname),"w")
	script3=open("{} instructions.txt".format(tournamentname),"w")
	for i in range(0,len(list1)):
		script2.write(list1[i])
	for i in range(0,len(list2)):
		script3.write(list2[i])
	script2.close()
	script3.close()
	os.rename("{}.txt".format(tournamentname),"{}.ahk".format(tournamentname))
		
