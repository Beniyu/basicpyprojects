import os
import time
letters="qwertyuiopasdfghjklzxcvbnm"
def listcheck(a,b):
        for entity in a:
                if entity==b:
                        return False
                else:
                        return True
def cls():
        os.system('cls' if os.name=='nt' else 'clear')
def intcreate(number):
	return int(''.join([i for i in number if i.isdigit()))
def osufriendlyname(name):
	goodname=[]
	for i in name:
		if i==" ":
			goodname.append("_")
		else:
			goodname.append(i)
	return ''.join(goodname)
def fixname(name):
	goodname=[]
	for i in name:
		if i=="_":
			goodname.append(" ")
		else:
			goodname.append(i)
	return ''.join(goodname)
def playerchoice(exemption):
        global settings
        teams=[{
        'color':'Blue',
        'main':[],
        'subs':[],
},{
        'color':'Red',
        'main':[],
        'subs':[],
}]
	if exemption=="y" or input("(y/n) Do you want players to be added to the hotkey: ").lower()=="y":
                settings['players']==True
		for i in range(2):
			while True:
				buffer=input("Team {} name: ".format(i+1))
				if input('(y/n) Confirm? ').lower()=='y':
					Teams['name'][i]=buffer
					break
		for i in range(2):
			while True:
                                cls()
                                print("""Put * before name if player is a sub. Put - before name if deleting. Type confirm when finished.")
Team {}:
Main players:""".format(i+1))
                   		for player in teams['main'][i]:
                                        print(player)
                                print("Subs:")
                                for player in teams['subs'][i]:
                                        print("*{}".format(player))
                                buffer=input("Enter name: ")
                                if buffer.lower()=="confirm":
                                        if len(teams['main'][i])==settings['size']:
                                                break
                                        else:
                                                print("Not enough main players.")
                                if buffer[0]=="-":
                                        try:
                                                teams['main'][i].delete(buffer[1:])
                                                print("Main player {} deleted.".format(buffer[1:]))
                                        except:
                                                try:
                                                        teams['subs'][i].delete(buffer[1:])
                                                        print("Sub {} deleted.".format(buffer[1:]))
                                                except:
                                                        print("No player found with this name.")
                                if listcheck(teams['subs'][i],buffer[1:])==False or listcheck(teams['main'][i],buffer[1:])==False:
                                        print("Player with this name already found.")  
                                elif buffer[0]=="*" and teams['subs'][i]<settings['subs']:
                                        teams['subs'][i].append(buffer[1:])
                                elif teams['main'][i]<settings['main'] :
                                        teams['main'][i].append(buffer[1:])
                                else:
                                        print("You have reached the maximum amount of players for this category.")
                return teams
def playerwrite(settings,scriptmain,scriptinstructions):
	if settings['players']==True:
                hotkey=[["F5","F6","F7","F8"],["F9","F10","F11","F12"]]
		scriptmain.write((""">^F1::
	Send,	{{!}}mp make {}: ({}) vs ({})
Return\n\n""").format(tournamentname,team1name,team2name))
                for i in range(2):
                        for j in range(2):
                                if j==0:
                                        playertype='main'
                                        scriptinstructions.write(("-----------------\nTeam {} players ({}):\n".format(teams['color'][i])))
                                else:
                                        playertype='subs'
                                for player in range(len(teams[playertype][i])):
                                        playerbuffer=osufriendlyname(teams[player][playertype][i]
                                        if j==1:
                                                playerbuffer="*{}".format(playerbuffer)
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
	Send,	{{!}}mp team {1} {2} {{ENTER}}
Return\n\n""").format(hotkey[player][i],playerbuffer,hotkey[player][i]),teams['color'][i]))
                                        scriptinstructions.write(playerbuffer,end="\n\n")
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
        while True:
                name=input("Tournament abbreviation: ")
                while True:
                        size=intcreate(input("Tournament team size: "))
                        if size>=1 and size<=4:
                        	while True:
                        		subs=intcreate(input("How many maximum subs (per team): "))
                        		if subs>=0 and subs<=4:
                        			break
                        		else:
                        			print("This program cannot handle more than 4 subs.")
                        	break
                if size==1:
                	tmode="0"
                else:
                        mode="2"
                if input("""Tournament name: {}
Tournament team size: {}
Subs per team: {}
(y/n) Confirm? """).lower() == "y":
                        return {
    'name': name,
    'size': size,
    'subs': subs,
    'mode': mode,
    'players': False
} 
#remember to recode mappool creation
def mappoolcreation():
	mappool=[]
	while True:
		maps=intcreate(input("How many maps in the map pool: "))
		if maps>26:
			print("This program doesn't support more than 26 maps.")
		if maps<1:
			print("You can't have no maps.")
		else:
			break
	for i in range(maps):
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
		for j in range(len(mappool)):
			if mappool[j][2]==i:
				mapnumber=mapnumber+1
				scriptinstructions.write(("Map {}: {} (Shortcut: {})\n").format(mapnumber,mappool[j][1],letters[j]))	
	for i in range(len(mappool)):
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
def mappoolsavefile(mappool):
	if input("(y/n) Save maps to mapfile? ").lower()=="y":
		savefilename=input("(txt files with this name will be overwritten) Save to what file name? ")
		scriptmappoolsave=open("{}.txt".format(savefilename),"w")
		for i in mappool:
			scriptmappoolsave.write("{},{},{}\n".format(i[0],i[1],i[2]))
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
	global tournamentname
	global tournamentsize
	global tournamentsubs
        
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
def loadscript():
        return open("{}.txt".format(tournamentname),"w"),open("{} instructions.txt".format(tournamentname),"w")
option=input("""0 - New Tournament File (destroys files with same tournament name)
1 - Update existing file
2 - Import map file\n""")
if option=="0":
	settings=tournamentsettings()
	scriptmain,scriptinstructions=loadscript()
	teams=playerchoice("n")
	scriptstart(len(teams['main'][0]+teams['subs'][0]+teams['main'][1]+teams['subs'][1]),settings['players'])
	mappoolcreation()	
	mappoolsavefile(mappool)
	logmap(mappool)
	playerwrite(settings,scriptmain,scriptinstructions)
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
		for i in range(0,int(marker[3:-5])*31+4):
			file.pop()
		for i in range(0,int(marker[3])+15):
			file2.pop()
	else:
		file.append("\n")
	playerchoice("y")
	scriptmain=open("{}.txt".format(tournamentname),"w")
	scriptinstructions=open("{} instructions.txt".format(tournamentname),"w")	
	scriptmain.write(";{}{}{},yes\n".format(tournamentsize,tournamentsubs,(tournamentsize*2+len(TeamRedSubs)+len(TeamBlueSubs))))
	for i in range(0,len(file)):
		scriptmain.write(file[i])
	for i in range(0,len(file2)):
		scriptinstructions.write(file2[i])
	playerwrite(settings,scriptmain,scriptinstructions)
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
	except:
		print("Bad file")
		time.sleep(3)
		quit()
	tournamentsettings()
	playerchoice("n")
	scriptstart(tournamentsize*2+len(TeamRedSubs)+len(TeamBlueSubs),play)
	logmap(mappool)
	playerwrite(settings,scriptmain,scriptinstructions)
	savefile(tournamentname)
	os.rename("{}.txt".format(tournamentname),"{}.ahk".format(tournamentname))
##if option=="3":
##	inputmethod=input("""0 - Start from scratch
##1 - Import map file
##2 - Import from savefile\n""")
##	if inputmethod=="0":
##		tournamentsettings()
##		playerchoice("y")
##		mappoolcreation()
##		mappoollist=[]
##		#map prep macros here
##		bannumber=intcreate(input("Bans per team: "))
##		bo=intcreate(input("Best of: "))
##		for i in range(0,len(mappool)):
##			mappoollist.append([mappool[i][1],letters[i]])
##		print("Please ask captains to roll.")
##		roll=input("(1/2) Higher team: ")
##		if roll=="1":
##			team1=[team1name,"blue"]
##			team2=[team2name,"red"]
##		else:
##			team1=[team2name,"red"]
##			team2=[team1name,"blue"]
##		warmup=[]
##		team1bans=[]
##		team2bans=[]
##		for i in range(0,2):
##			warmup.append(input("Warmup: "))
##		for i in range(0,len(mappool)):
##			print("{} - {}".format(mappool[i][1],letters[i]))
##		print("(use map letters, not name)")
##		for i in range(0,bannumber*2):
##			print(i/2)
##			if (i/2).is_integer():
##				team1bans.append(input("Team ({}) Ban {}: ".format(team1[0],int((i+2)/2))))
##			else:
##				team2bans.append(input("Team ({}) Ban {}: ".format(team2[0],int((i+1)/2))))
##		tempscript=open("tempscript.txt","w")
##		tempscript.write("""SendMode Input
##^F2::\n""")
##		better1bans=[]
##		better2bans=[]
##		for i in range(0,bannumber):
##			for j in range(0,len(mappool))):
##				if team1bans[i]==letters[j]:
##					better1bans.append(mappool[j][1])
##		for i in range(0,bannumber):
##			for j in range(0,len(mappool))):
##				if team2bans[i]==letters[j]:
##					better2bans.append(mappool[j][1])
##		if roll=="1":
##			tempscript.write("""	Send 	{} bans: {{SHIFT}}{{ENTER}}
##	Send 	{} {{SHIFT}}{{ENTER}}
##	Send	{} bans: {{SHIFT}}{{ENTER}}
##	Send 	{} {{ENTER}}
##ExitApp""".format(team1name," & ".join(better1bans),team2name," & ".join(team2bans)))
##		else:
##			tempscript.write("""	Send 	{} bans: {{SHIFT}}{{ENTER}}
##	Send 	{} {{SHIFT}}{{ENTER}}
##	Send	{} bans: {{SHIFT}}{{ENTER}}
##	Send 	{} {{ENTER}}
##ExitApp""".format(team1name," & ".join(better2bans),team2name," & ".join(team1bans)))
##		tempscript.close()
##		os.rename("tempscript.txt","tempscript.ahk")
##		os.startfile("tempscript.ahk")
##		mappoolsavefile(mappool) 
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
		
