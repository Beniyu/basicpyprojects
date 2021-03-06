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
	return int(''.join([i for i in number if i.isdigit()]))
	
def osufriendlyname(name):
	refinedname=""
	for character in name:
		if character==" ":
			refinedname+="_"
		else:
			refinedname+=character
	return refinedname
	
def fixname(name):
	refinedname=""
	for character in name:
		if character=="_":
			refinedname+=" "
		else:
			refinedname+=character
	return refinedname
	
def tournamentsettings():
        while True:
                name=input("Tournament abbreviation: ")
                size=intcreate(input("Tournament team size: "))
                while not (size>=1 and size<=4):
                    print("Team size is not between 1 and 4.")
                    size=intcreate(input("Tournament team size: "))
                subs=intcreate(input("How many maximum subs (per team): "))
                while not (subs>=0 and subs<=4):
                    print("This program cannot handle more than 4 subs.")
                    subs=intcreate(input("How many maximum subs (per team): "))
                score=intcreate(input("What score system would you like to use (1/2): "))
                while not (score==1 or score==2):
                    print("Not valid score system.")
                    score=intcreate(input("What score system would you like to use (1/2): "))
                if size==1:
                    mode="0"
                else:
                    mode="2"
                if input("""Tournament name: {}
Tournament team size: {}
Subs per team: {}
ScoreV{}
(y/n) Confirm? """.format(name,size,subs,score)).lower() == "y":
                        if score==1:
                                score=0
                        if score==2:
                                score=3
                        return {
        'name': name,
        'size': size,
        'subs': subs,
        'mode': mode,
        'score': score,
        'players': False
} 
        
def scriptstart(settings,teams,scriptmain,scriptinstructions):
	playercount=len(teams[0]['main']+teams[0]['subs']+teams[1]['main']+teams[1]['subs'])
	if settings['players']==True:
		players='yes'
	else:
		players='no'
	scriptmain.write((""";{}{}{},{}
#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%\n
>^F2::
	Send,	{{!}}mp size {} {{ENTER}}
	Sleep,  1000
	Send,	{{!}}mp set {} {} {{ENTER}}
Return\n
>^F3::
	Send,	{{!}}mp start 5
Return\n
>^F4::
	Send,	Are you ready for your {} match? {{ENTER}}
Return\n\n""").format(settings['size'],settings['subs'],playercount,players,settings['size']*2,settings['mode'],settings['score'],settings['name']))

def loadscript(name,mode):
	return open("{}.txt".format(name),mode),open("{} instructions.txt".format(name),mode)
	
def endscript():
	scriptmain.close()
	scriptinstructions.close()  	
	
def playerchoice(settings,exemption):
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
		settings['players']=True
		for team in range(2):
			while True:
				buffer=input("Team {} name: ".format(team+1))
				if input('(y/n) Name set to "{}". Confirm? '.format(buffer)).lower()=='y':
					teams[team]['name']=buffer
					break
			while True:
				cls()
				print("""Put * before name if player is a sub. Put : before name if deleting. Type !confirm when finished.
Team {}:
Main players:""".format(team+1))
				for player in teams[team]['main']:
					print(player)
				print("Subs:")
				for player in teams[team]['subs']:
					print("*{}".format(player))
				buffer=input("Enter name: ")
				if buffer=="":
					print("You entered nothing.")
				elif buffer.lower()=="!help":
					print("Put * before name if player is a sub. Put : before name if deleting. Type confirm when finished.")
				elif buffer.lower()=="!confirm":
					if len(teams[team]['main'])==settings['size']:
						break
					else:
						print("Not enough main players.")
				elif buffer[0]==":":
					try:
						teams[team]['main'].remove(buffer[1:])
						print("Main player {} deleted.".format(buffer[1:]))
					except:
						try:
							teams[team]['subs'].remove(buffer[1:])
							print("Sub {} deleted.".format(buffer[1:]))
						except:
							print("No player found with this name.")
				else:
					if listcheck(teams[team]['subs'],buffer[1:])==False or listcheck(teams[team]['main'],buffer)==False:
						print("Player with this name already found.")  
					elif buffer[0]=="*" and len(teams[team]['subs'])<settings['subs']:
						teams[team]['subs'].append(buffer[1:])
					elif len(teams[team]['main'])<settings['size']:
						teams[team]['main'].append(buffer)
					else:
						print("You have reached the maximum amount of players for this category.")
	return settings,teams
	
def playerwrite(settings,teams,scriptmain,scriptinstructions):
	playertype={0:{'type':'main','hotkey':'^'},
	1:{'type':'subs','hotkey':'+'}
}
	if settings['players']==True:
		hotkey=[["F5","F6","F7","F8"],["F9","F10","F11","F12"]]
		scriptmain.write((""">^F1::
	Send,	{{!}}mp make {}: ({}) vs ({})
Return\n\n""").format(settings['name'],teams[0]['name'],teams[1]['name']))
		for team in range(2):
			scriptinstructions.write(("-----------------\nTeam {} players ({}):\n".format(teams[team]['color'],teams[team]['name'])))
			for playertypenum in range(2):
				playercounter=0
				for player in teams[team][playertype[playertypenum]['type']]:
					playerbuffer=player
					if playertypenum==1:
						playerbuffer="*{}".format(playerbuffer)
					scriptmain.write((""">{0}{1}::
	loop {{		
		if GetKeyState("1","P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {2} 1 {{ENTER}}
			break
			}}
		if GetKeyState("2", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {2} 2 {{ENTER}}
			break
			}}
		if GetKeyState("3", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {2} 3 {{ENTER}}
			break
			}}
		if GetKeyState("4", "P")=1
			{{
			Send,	{{BACKSPACE}}{{!}}mp move {2} 4 {{ENTER}}
			break
			}}
		if GetKeyState("ESC", "P")=1
			{{
			Return
			}}
	}}
	Sleep,  1000
	Send,	{{!}}mp team {2} {3} {{ENTER}}
Return\n\n""").format(playertype[playertypenum]['hotkey'],hotkey[team][playercounter],osufriendlyname(player),teams[team]['color']))
					scriptinstructions.write(playerbuffer+"\n")
					playercounter+=1
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

def mappoolcreation():
	mappool=[]
	print("Put !confirm when finished. Put : before map name to delete a map. ( syntax: -(id) example: -8 )")
	while True:
		mapcounter=0
		for mapp in mappool:
			print("ID {}: \"{}\" - mode {} - map-id {}".format(mapcounter,mapp['name'],mapp['mod'],mapp['id']))
			mapcounter+=1
		buffer=input("Map name: ")
		if buffer=="!help":
			print("Put confirm when finished. Put - before map name to delete a map. ( syntax: -(id) example: -8 )")
		elif buffer=="!confirm":
			if mapcounter>0:
				break
			else:
				print("Not enough maps.")
		elif buffer[0]==":":
			try:
				del mappool[intcreate(buffer[1:])]
			except:
				print("No map with this ID found.")
		elif mapcounter==26:
			print("This program only supports 26 maps. Please delete some if you want to add more.")
		else:
			idd=input("Map ID: ")
			while True:
				if idd.isdigit()==False:
					idd=input("Invalid map ID (not an integer). Please retype: ")
				elif int(idd)<0:
					idd=input("Invalid map ID (negative). Please retype: ")
				else:
					break
			mod=input("(1:nomod, 2:hidden, 3:hardrock, 4:doubletime, 5:freemod, 6:tiebreaker)\nMap mod: ")
			while True:
				if mod.isdigit()==False:
					mod=input("Map mods are invalid (not an integer). Please retype: ")			
				elif int(mod)>6 or int(mod)<1:
					mod=input("Map mods are invalid (not between 1 and 6). Please retype: ")
				else:
					break
			mappool.append({'name': buffer,
	'id': int(idd),
	'mod': int(mod)
})
	return mappool
	
def logmap(mappool,scriptmain,scriptinstructions):
	mapnumber=0
	modtype={1:{'name':'Nomod maps','mod':'nomod'},
	2:{'name':'Hidden maps','mod':'hd'},
	3:{'name':'Hard rock maps','mod':'hr'},
	4:{'name':'Double time maps','mod':'dt'},
	5:{'name':'Freemod maps','mod':'freemod'},
	6:{'name':'Tie breaker','mod':'freemod'}
}
	for mod in range(1,7):
		scriptinstructions.write("-----------------\n{}:\n".format(modtype[mod]['name']))		
		for mapp in range(len(mappool)):
			if mappool[mapp]['mod']==mod:
				mapnumber=mapnumber+1
				scriptinstructions.write(("Map {}: {} (Shortcut: {})\n").format(mapnumber,mappool[mapp]['name'],letters[mapp]))	
	mapcounter=0
	for mapp in mappool:
		scriptmain.write((""">^{}::
	Send,   {{!}}mp map {} {{ENTER}}
	Sleep,	1000
	Send,	{{!}}mp mods {} {{ENTER}}
Return\n\n""").format(letters[mapcounter],mapp['id'],modtype[mapp['mod']]['mod']))		
		mapcounter+=1

def mappoolsavefile(mappool):
	if input("(y/n) Save maps to mapfile? ").lower()=="y":
		savefilename=input("(txt files with this name will be overwritten) Save to what file name? ")
		scriptmappoolsave=open("{}.txt".format(savefilename),"w")
		for mapp in mappool:
			scriptmappoolsave.write("{},{},{}\n".format(mapp['name'],mapp['id'],mapp['mod']))
		scriptmappoolsave.close()
		
def savefile(name):
	if input("(y/n) Create save file? ").lower()=="y":
		scriptmain,scriptinstructions=loadscript(name,"r")
		scriptsavefile=open("savefile-{}.txt".format(name),"w")
		linecounter=0
		list1=[]
		for line in scriptmain:
			list1.append(line)
			linecounter=linecounter+1
		for line in scriptinstructions:
			list1.append(line)
		scriptsavefile.write(str(linecounter)+"\n")
		for i in range(0,len(list1)):
			scriptsavefile.write(list1[i])
		endscript()
		scriptsavefile.close()
		os.rename("savefile-{}.txt".format(name),"savefile-{}.xddd".format(name))

while True:
	cls()
	option=input("""Python file created by Beniyu.
Please install AutoHotkeys if you do not have it yet.
0 - New tournament file (destroys files with same tournament name)
1 - Update existing file
2 - Import map file
3 - Create map file through python
4 - Recreate tournament file using savefile\n""")

	if option=="0":
		settings=tournamentsettings()
		scriptmain,scriptinstructions=loadscript(settings['name'],"w")
		settings,teams=playerchoice(settings,"n")
		scriptstart(settings,teams,scriptmain,scriptinstructions)
		mappool=mappoolcreation()	
		mappoolsavefile(mappool)
		logmap(mappool,scriptmain,scriptinstructions)
		playerwrite(settings,teams,scriptmain,scriptinstructions)
		endscript()
		savefile(settings['name'])
		os.rename("{}.txt".format(settings['name']),"{}.ahk".format(settings['name']))
		
	if option=="1":
		while True:
			try:
				name=input("Tournament abbreviation: ")
				os.rename("{}.ahk".format(name),"{}.txt".format(name))
				break
			except:
				print("You have no existing file for this tournament.")
		scriptmain,scriptinstructions=loadscript(name,"r")
		filemain=[]
		fileinstructions=[]
		marker=scriptmain.readline()
		settings={}
		for line in scriptmain:
			filemain.append(line)
		for line in scriptinstructions:
			fileinstructions.append(line)
		if marker[-4:]=="yes\n":
			players=int(marker[3:-5])
			for i in range(0,int(marker[3:-5])*31+4):
				filemain.pop()
			for i in range(0,int(marker[3])+15):
				fileinstructions.pop()
		else:
			filemain.append("\n")
		settings['size']=int(marker[1])
		settings['subs']=int(marker[2])
		settings['name']=name
		settings['players']=True
		settings,teams=playerchoice(settings,"y")
		endscript()
		scriptmain,scriptinstructions=loadscript(name,"w")
		scriptmain.write(";{}{}{},yes\n".format(settings['size'],settings['subs'],len(teams[0]['main']+teams[0]['subs']+teams[1]['main']+teams[1]['subs'])))
		for line in filemain:
			scriptmain.write(line)
		for line in fileinstructions:
			scriptinstructions.write(line)
		playerwrite(settings,teams,scriptmain,scriptinstructions)
		endscript()
		savefile(name)
		os.rename("{}.txt".format(name),"{}.ahk".format(name))
		
	if option=="2":
		mappool=[]
		while True:
			importfile=input("Name of imported file: ")
			try:
				mapimport=open("{}.txt".format(importfile),'r')
				break
			except:
				print("No map import file with the name {}.txt".format(importfile))
		try:		
			for line in mapimport:
				name,idd,mod=line.split(",")
				if int(mod)<1 or int(mod)>6:
					print("Bad file (invalid mod values)")
					time.sleep(3)
					quit()
				if int(idd)<0:
					print("Bad file (negative map ids)")
					time.sleep(3)
					quit()
				mappool.append({'name':name,
		'id':int(idd),
		'mod':int(mod)
	})
		except:
			print("Bad file (error, possible non-integers found)")
			time.sleep(3)
			quit()
		settings=tournamentsettings()
		settings,teams=playerchoice(settings,"n")
		scriptmain,scriptinstructions=loadscript(settings['name'],"w")
		scriptstart(settings,teams,scriptmain,scriptinstructions)
		logmap(mappool,scriptmain,scriptinstructions)
		playerwrite(settings,teams,scriptmain,scriptinstructions)
		endscript()
		savefile(settings['name'])
		os.rename("{}.txt".format(settings['name']),"{}.ahk".format(settings['name']))
		
	if option=="3":
		mappool=mappoolcreation()
		savefilename=input("(txt files with this name will be overwritten) Save to what file name? ")
		scriptmappoolsave=open("{}.txt".format(savefilename),"w")
		for mapp in mappool:
			scriptmappoolsave.write("{},{},{}\n".format(mapp['name'],mapp['id'],mapp['mod']))
		scriptmappoolsave.close()

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
			
