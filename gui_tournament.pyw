import tkinter as tk
import tkinter.filedialog
import json
from urllib.request import urlopen
import os

def normal_to_osu(name):
    refinedname=""
    for character in name:
        if character==" ":
            refinedname+="_"
        else:
            refinedname+=character
    return refinedname

def key_list(dictionary):
    key_list=[]
    for key in dictionary:
        key_list.append(key)
    key_list.sort()
    return key_list

def specified_key_list(dictionaries,key):
    key_list=[]
    for dictionary in dictionaries:
        key_list.append(dictionaries[dictionary][key])
    return key_list

def dictionary_result_list(dictionary):
    key_list=[]
    for key in dictionary:
        key_list.append(dictionary[key])
    return key_list

class SettingsFile(object):
    terms={'key':''}
    allowed_terms=key_list(terms)
    directory = os.path.dirname(__file__)
    def __init__(self,map_manager):
        self.maps=map_manager
        if os.path.isfile('{}/tpy_settings.txt'.format(self.directory)):
            file=open('{}/tpy_settings.txt'.format(self.directory),'r')
            for line in file:
                self.import_setting(line)
            file.close()
        map_manager.key=self.terms['key']
        if self.terms['key']=='':
            window=tk.Toplevel()
            tk.Label(window,text='Please be aware that you must add your API key to add maps to the map pool').pack()
        self.recreate_file()
    def edit_setting_window(self,setting):
        window=tk.Toplevel()
        var=tk.StringVar()
        var.set(self.maps.key)
        tk.Label(window,text='Editing {}:'.format(setting)).grid(row=0,column=0,columnspan=2)
        tk.Entry(window,textvariable=var,width=40).grid(row=1,column=0)
        tk.Button(window,text='Continue',command=lambda:self.redo_setting(setting,var.get(),window)).grid(row=1,column=1)
    def redo_setting(self,setting,var,window):
        if setting=='key':
            self.maps.key=var
        self.import_setting('{}:{}'.format(setting,var))
        self.recreate_file()
        window.destroy()
    def add_setting_to_file(self,setting,file):
        file.write('{}:'.format(setting))
    def import_setting(self,entry):
        entries=entry.split(':')
        if len(entries)==2:
            term,definition=entries
            if term in self.allowed_terms:
                self.terms[term]=definition
    def recreate_file(self):
        directory = os.path.dirname(__file__)
        file=open('{}/tpy_settings.txt'.format(directory),'w')
        for term in self.terms:
            file.write('{}:{}'.format(term,self.terms[term]))
        for term in self.allowed_terms:
            if term not in key_list(self.terms):
                self.add_setting_to_file(term,file)
        file.close()

class TournamentImport(object):
    def __init__(self,abbreviation,main_size,sub_size,score_system,gui,maps):
        self.validity=True
        file=tk.filedialog.askopenfilename(filetypes=[('Tourney file',('.ahk','.sav','.tmaps'))])
        if file!='':
            self.file_type=file.split('.')[-1:][0]
            self.file=open(file,'r')
        else:
            self.validity=False
        self.tourney_info=[]
        self.abb=abbreviation
        self.m=main_size
        self.s=sub_size
        self.v=score_system
        self.g=gui
        self.p=maps
    def import_data(self):
        if self.file_type in ['ahk','sav']:
            for line in range(2):
                self.tourney_info.append(self.file.readline().replace('\n','')[1:])
        self.map_info=self.file.readline().replace('\n','')[1:]
    def split_data(self):
        if self.map_info!='':
            maps=self.map_info.split('<>')
        else:
            maps=[]
        self.map_list=[]
        self.settings={}
        self.teams={}
        for map_entry in maps:
            map_info=map_entry.split('`')
            map_dictionary={}
            for detail in enumerate(['name','id','mod','diff']):
                map_dictionary[detail[1]]=map_info[detail[0]]
            self.map_list.append(map_dictionary)
        if self.file_type in ['ahk','sav']:
            for detail in enumerate(['abbreviation','team_size','sub_size','score_system']):
                self.settings[detail[1]]=self.tourney_info[0].split('|')[detail[0]]
            for team in enumerate(self.tourney_info[1].split('~')):
                team_entry={}
                team_details=team[1].split('ø')
                print(team[1])
                print(team_details)
                for detail in enumerate(['Name','Main','Substitute']):
                    returned_detail=team_details[detail[0]]
                    if detail[1] in ['Main','Substitute']:
                        returned_detail=returned_detail.split('`')
                    if returned_detail==['']:
                        returned_detail=[]
                    team_entry[detail[1]]=returned_detail
                self.teams[team[0]]=team_entry
    def add_data(self):
        self.p.map_list=self.map_list
        self.p.recreate_listbox()
        if self.file_type in ['ahk','sav']:
            self.abb.set(self.settings['abbreviation'])
            self.m.override_variable(self.settings['team_size'])
            self.s.override_variable(self.settings['sub_size'])
            self.v.set_option(self.settings['score_system'])
            self.g.team_button_controller(0)
            self.g.te.set(self.teams[0]['Name'])
            self.g.teams.team_list=self.teams
            self.g.recreate_listbox()
            
def call_import(abbreviation,main_size,sub_size,score_system,gui,maps):
    importer=TournamentImport(abbreviation,main_size,sub_size,score_system,gui,maps)
    if importer.validity==True:
        importer.import_data()
        importer.split_data()
        importer.add_data()

class TournamentExport(object):
    basic_hotkey={'Main':'^','Substitute':'+'}
    team_hotkey=[["F5","F6","F7","F8"],["F9","F10","F11","F12"]]
    team_color=['Blue','Red']
    user_symbol={'Main':'','Substitute':'*'}
    modtype={'NM':{'name':'Nomod maps','mod':'none'},
    'HD':{'name':'Hidden maps','mod':'hd'},
    'HR':{'name':'Hard rock maps','mod':'hr'},
    'DT':{'name':'Double time maps','mod':'dt'},
    'FM':{'name':'Freemod maps','mod':'freemod'},
    'TB':{'name':'Tie breaker','mod':'freemod'}}
    modlist=['NM','HD','HR','DT','FM','TB']
    def __init__(self,abbreviation,main_players,sub_players,score_system,teams,map_pool):
        teams.team_button_controller(teams.team_state)
        teams=teams.teams.team_list
        self.active_script=''
        self.abb=abbreviation
        self.m=main_players
        self.s=sub_players
        self.v=score_system
        self.p=map_pool
        self.t=[]
        for team in teams:
            self.t.append(teams[team])
        if main_players==1:
            self.mode='0'
        else:
            self.mode='2'
        if score_system=='V1':
            self.v_2='0'
        else:
            self.v_2='3'
    def condense_team(self):
        team_string=''
        for team in self.t:
            main=''
            substitute=''
            for player in team['Main']:
                main+='{}`'.format(player)
            for player in team['Substitute']:
                substitute+='{}`'.format(player)
            team_string+='{}ø{}ø{}~'.format(team['Name'],main[:-1],substitute[:-1])
        return team_string[:-1]
    def condense_map(self):
        map_string=''
        for map_info in self.p:
            map_string+='{}`{}`{}`{}<>'.format(map_info['name'],map_info['id'],map_info['mod'],map_info['diff'])
        return map_string[:-2]
    def log_save_info(self,**kwargs):
        active_script=self.active_script
        if 'script' in kwargs:
                active_script=kwargs['script']
        active_script.write(""";{0}|{1}|{2}|{3}
;{4}
;{5}\n""".format(self.abb,self.m,self.s,self.v,self.condense_team(),self.condense_map()))
    def start_export(self):
        self.active_script.write("""#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%\n
>^F2::
        Send,   {{!}}mp set {} {} {} {{ENTER}}
Return\n
>^F3::
        Send,   {{!}}mp start 5
Return\n
>^F4::
        Send,   Are you ready for your {} match? {{ENTER}}
Return\n\n""".format(self.mode,self.v_2,self.m*2,self.abb))
    def add_players(self):
        teams=self.t
        self.active_script.write(""">^F1::
        Send,   {{!}}mp make {}: ({}) vs ({})
Return\n\n""".format(self.abb,teams[0]['Name'],teams[1]['Name']).replace('#',"{{#}}"))
        for team in enumerate(teams):
            self.passive_script.write("-----------------\n{} players ({}):\n".format(team[1]['Name'],self.team_color[team[0]]))
            for group in ['Main','Substitute']:
                for player in enumerate(team[1][group]):
                    self.active_script.write(""">{0}{1}::
        loop {{         
                if GetKeyState("1","P")=1
                        {{
                        Send,   {{BACKSPACE}}{{!}}mp move {2} 1 {{ENTER}}
                        break
                        }}
                if GetKeyState("2", "P")=1
                        {{
                        Send,   {{BACKSPACE}}{{!}}mp move {2} 2 {{ENTER}}
                        break
                        }}
                if GetKeyState("3", "P")=1
                        {{
                        Send,   {{BACKSPACE}}{{!}}mp move {2} 3 {{ENTER}}
                        break
                        }}
                if GetKeyState("4", "P")=1
                        {{
                        Send,   {{BACKSPACE}}{{!}}mp move {2} 4 {{ENTER}}
                        break
                        }}
                if GetKeyState("ESC", "P")=1
                        {{
                        Return
                        }}
        }}
        Sleep,  1000
        Send,   {{!}}mp team {2} {3} {{ENTER}}
Return\n\n""".format(self.basic_hotkey[group],self.team_hotkey[team[0]][player[0]],normal_to_osu(player[1]),self.team_color[team[0]]))
                    self.passive_script.write('{}{}\n'.format(self.user_symbol[group],player[1]))
    def add_instructions(self):
        self.passive_script.write("""-----------------
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
    def add_map(self):
        map_pool=self.p
        key_database={}
        letters="qwertyuiopasdfghjklzxcvbnm,."
        for map_entry in enumerate(map_pool):
            self.active_script.write(""">^{}::
        Send,   {{!}}mp map {} {{ENTER}}
        Sleep,  1000
        Send,   {{!}}mp mods {} {{ENTER}}
Return\n\n""".format(letters[map_entry[0]],map_entry[1]['id'],self.modtype[map_entry[1]['mod']]['mod'].replace('TB','FM')))
            key_database[map_entry[1]['id']]=letters[map_entry[0]]              
        for mod in self.modlist:
            self.passive_script.write("-----------------\n{}:\n".format(self.modtype[mod]['name']))
            for map_entry in map_pool:
                if map_entry['mod']==mod:  
                    self.passive_script.write("{} [{}] ({}) (Shortcut: {})\n".format(map_entry['name'],map_entry['diff'],map_entry['id'],key_database[map_entry['id']]))
    def create_file(self,file):
        self.active_script=open('{}/5bGyVVuwUFw683A.txt'.format(file[1]),'w')
        self.passive_script=open('{} instructions (for AHK file).txt'.format(file[0]),'w')
        self.log_save_info()
        self.start_export()
        self.add_players()
        self.add_map()
        self.add_instructions()
        self.active_script.close()
        self.passive_script.close()
        override_file('{}.ahk'.format(file[0]))
        os.rename('{}/5bGyVVuwUFw683A.txt'.format(file[1]),'{}.ahk'.format(file[0]))
    def create_save(self,file):
        script=open('5bGyVVuwUFw683A.txt'.format(file[1]),'w')
        self.log_save_info(script=script)
        script.close()
        override_file('{}.sav'.format(file[0]))
        os.rename('{}/5bGyVVuwUFw683A.txt'.format(file[1]),'{}.sav'.format(file[0]))
    def create_maps(self,file):
        maps=self.condense_map()
        script=open('{}/5bGyVVuwUFw683A.txt'.format(file[1]),'w')
        script.write(';{}'.format(maps))
        script.close()
        override_file('{}.tmaps'.format(file[0]))
        os.rename('{}/5bGyVVuwUFw683A.txt'.format(file[1]),'{}.tmaps'.format(file[0]))
        
class TeamController(object):
    def __init__(self,team_count,**groups):
        self.team_list={}
        self.player_limits={}
        for team in range(team_count):
            temp_team_dict={'Name':'Team {}'.format(team+1)}
            for group in groups:
                temp_team_dict[group]=[]
            self.team_list[team]=temp_team_dict
        group_list=[]
        for group in groups:
            group_list.append(group)
            self.player_limits[group]=groups[group]
        self.groups=group_list
    def add_member(self,team,group,member,entry):
        if self.group_size(team,group)<self.player_limits[group].get() and member not in self.team_list[team][group]:
            self.team_list[team][group].append(member)
            entry.set('')
    def del_member(self,team,group,member):
        if member in self.team_list[team][group]:
            self.team_list[team][group].remove(member)
    def group_size(self,team,group):
        return len(self.team_list[team][group])
    def check_player(self,player):
        for team in self.team_list:
            for group in self.groups:
                if player in self.team_list[team][group]:
                    return False
                    break
        return True

class IndefiniteTeamController(TeamController):
    def __init__(self,**groups):
        self.player_limits={}
        group_list=[]
        for group in groups:
            group_list.append(group)
            self.player_limits[group]=groups[group]
        self.groups=group_list
        self.empty_var=tk.StringVar()
        self.last_used=1
        self.team_state=1
        self.team_list={}
        self.team_list[1]=self.generate_team_dict()
        self.team_list[1]['Name']='New team 1'
    def generate_team_dict(self):
        temp_dict={'Name':''}
        for group in self.groups:
            temp_dict[group]=[]
        return temp_dict
    def name_to_id(self,name):
        for team in self.team_list:
            if self.team_list[team]['Name']==name:
                return team
    def add_team(self,team_name):
        if team_name not in key_list(self.team_list):
            temp_dict=self.generate_team_dict()
            temp_dict['Name']=team_name
            self.team_list[self.last_used+1]=temp_dict
            self.last_used+=1
    def del_team(self,team_name):
        if self.check_team_exists(team_name):
            team=self.name_to_id(team_name)
            del self.team_list[team]
    def receive_team_information(self,team_name,*args):
        if self.check_team_exists(team_name):
            team=self.name_to_id(team_name)
            group_info=self.team_list[team]
            del group_info['Name']
            return group_info
    def check_team_exists(self,team_name):
        if team_name in specified_key_list(self.team_list,'Name'):
            return True
        else:
            return False
    def add_member_2(self,team,group,member,entry):
        self.add_member(self.name_to_id(team),group,member,self.empty_var)
    def del_member_2(self,member):
        for team in dictionary_result_list(self.team_list):
            for group in self.groups:
                for possible_member in team[group]:
                    if member==possible_member:
                        del team[group][member]
    def check_team_amount(self):
        return len(self.team_list)

class MapController(object):
    key=''
    def __init__(self,listbox,map_entry,map_type):
        self.map_list=[]
        self.map_mods=['NM','HD','HR','DT','FM','TB']
        self.me=map_entry
        self.mt=map_type
        self.lb=listbox
    def extract_map(self,map_id):
        try:
            map_info=json.loads(urlopen('https://osu.ppy.sh/api/get_beatmaps?k={}&b={}'.format(self.key,map_id)).read().decode('utf-8'))
        except:
            window=tk.Toplevel()
            tk.Label(window,text='Your API key is invalid, please add a valid API key to add maps to the map pool.').pack()
            map_info=[]
        if map_info==[]:
            return 'break'
        else:
            return map_info[0]
    def add_map(self):
        selected_map=self.me.get()
        for map_possibility in self.map_list:
            if map_possibility['id']==selected_map:
                break
        else:
            map_info=self.extract_map(selected_map)
            if map_info!='break':
                self.map_list.append({'name':map_info['title'],'id':selected_map,'mod':self.mt.get(),'diff':map_info['version']})
                self.lb.insert(tk.END,'{} - {} ({}) [{}]'.format(selected_map,map_info['title'],map_info['version'],self.mt.get()))
                self.recreate_listbox()
                self.me.set('')
    def del_map(self):
        selection=self.lb.curselection()
        if selection!=():
            unfiltered_name=self.lb.get(selection)
            map_id=unfiltered_name.split(' ')[0]
            for map_entry in enumerate(self.map_list):
                if map_entry[1]['id']==map_id:
                    del self.map_list[0]
            self.lb.delete(selection)
    def recreate_listbox(self):
        maps=self.lb.get(0,tk.END)
        self.lb.delete(0,tk.END)
        for mod_type in self.map_mods:
            for map_entry in self.map_list:
                if map_entry['mod']==mod_type:
                    self.lb.insert(tk.END,'{} - {} ({}) [{}]'.format(map_entry['id'],map_entry['name'],map_entry['diff'],map_entry['mod']))

class GUIController(object):
    def __init__(self,teams,team1_button,team2_button,team_entry,listbox,player_entry,player_type):
        self.team_state=0
        self.teams=teams
        team1_button.config(relief='sunken')
        self.tb=[team1_button,team2_button]
        self.te=team_entry
        self.lb=listbox
        self.pe=player_entry
        self.pt=player_type
    def group_size(self,team,group):
        return len(self.teams.team_list[team][group])
    def team_button_controller(self,new_team):
        self.tb[new_team].config(relief='sunken')
        self.tb[1-new_team].config(relief='raised')
        self.teams.team_list[self.team_state]['Name']=self.te.get()
        self.te.set(self.teams.team_list[new_team]['Name'])
        self.team_state=new_team
        self.recreate_listbox()
    def player_addition(self):
        if self.teams.check_player(self.pe.get()):
            self.teams.add_member(self.team_state,self.pt.get(),self.pe.get(),self.pe)
        self.recreate_listbox()
    def player_removal(self,**kwargs):
        player=self.lb.curselection()
        if player!=():
            player=self.lb.get(player)
        else:
            player=self.lb.get(tk.END)
        player=player
        if 'player' in kwargs:
            player=kwargs['player']
        for team in enumerate(self.teams.team_list):
            for group in ['Main','Substitute']:
                if player in self.teams.team_list[team[1]][group]:
                    self.teams.team_list[team[1]][group].remove(player)
        self.recreate_listbox()
    def recreate_listbox(self):
        team=self.teams.team_list[self.team_state]
        self.lb.delete(0,tk.END)
        for group in ['Main','Substitute']:
            for player in team[group]:
                self.lb.insert(tk.END,player)
                if group=='Substitute':
                    self.lb.itemconfig(tk.END,{'fg':'grey'})
                    
class ButtonOptions(object): 
    def __init__(self,frame,variable,*options):
        self.button_list={}
        self.var=variable
        for option in options:
            self.button_list[option]=tk.Button(frame,text=option,padx=5,command=lambda option=option: self.set_option(option))
            self.button_list[option].pack(side='left',fill='x',expand='yes')
    def set_option(self,option):
        self.var.set(option)
        for button in self.button_list:
            if self.button_list[button].cget('text')!=option:
                self.button_list[button].config(relief='raised')
            else:
                self.button_list[button].config(relief='sunken')

class TournamentButtonOptions(ButtonOptions):
    def define_window_list(self,window_list):
        self.window_list=window_list
    def set_option_with_update(self,option):
        self.set_option(option)
        for window in self.window_list:
            if window != option:
                self.window_list[window].grid_remove()
            else:
                self.window_list[window].grid()

class VariableNumber(object):
    def __init__(self,frame,variable,minimum_value,maximum_value):
        self.counter=tk.Label(frame,text=minimum_value,padx=10)
        tk.Button(frame,text='+',command=self.plus_var).pack(side='left')
        self.counter.pack(side='left')
        tk.Button(frame,text='-',command=self.minus_var).pack(side='left')
        self.min=minimum_value
        self.max=maximum_value
        self.var=variable
        variable.set(minimum_value)
        self.update_counter()
    def plus_var(self):
        value=self.var.get()
        if value<self.max:
            self.var.set(value+1)
        self.update_counter()
    def minus_var(self):
        value=self.var.get()
        if value>self.min:
            self.var.set(value-1)
        self.update_counter()
    def update_counter(self):
        self.counter.config(text=self.var.get())
    def override_variable(self,value):
        self.var.set(value)
        self.update_counter()

class TeamVariableNumber(VariableNumber):
    def __init__(self,frame,variable,minimum_value,maximum_value,group):
        super(TeamVariableNumber,self).__init__(frame,variable,minimum_value,maximum_value)
        self.group=group
    def minus_var(self):
        value=self.var.get()
        if value>self.min:
            self.var.set(value-1)
        self.update_counter()
        for team in self.gui.teams.team_list:
            group_size=self.gui.group_size(team,self.group)
            if group_size>self.var.get():
                removed_player=self.gui.teams.team_list[team][self.group][group_size-1]
                self.gui.player_removal(player=removed_player)

class TournamentController(GUIController):
    def __init__(self):
        window=tk.Toplevel()
        window.title('Tournament settings')
        tmenu=tk.Menu(window)
        window.config(menu=tmenu)
        dropdownMenu=tk.Menu(tmenu,tearoff=0)
        tmenu.add_cascade(label='File Control',menu=dropdownMenu)
        dropdownMenu.add_command(label='Import')
        dropdownMenu.add_command(label='Export')
        dropdownMenu.add_command(label='Load')
        button_frame=tk.Frame(window)
        button_frame.grid(row=0,column=0)
        settings=tk.Frame(window)
        self.settings_list(settings)
        settings.grid(row=1,column=0)
        players=tk.Frame(window)
        self.team_list(players)
        maps=tk.Frame(window)
        self.map_list(maps)
        self.frames={'Settings':settings,'Players':players,'Maps':maps}
        button_list={}
        for option in ['Settings','Players','Maps']:
            button_list[option]=tk.Button(button_frame,text=option,padx=5,command=lambda option=option: self.set_option(option))
            button_list[option].pack(side='left',fill='x',expand='yes')
    def load_settings(self):
        self.validity=True
        file=tk.filedialog.askopenfilename(filetypes=[('Tourney file',('.ahk','.sav','.tmaps'))])
        if file!='':
            self.file_type=file.split('.')[-1:][0]
            self.file=open(file,'r')
        else:
            self.validity=False
    def set_option(self,option):
        for frame in self.frames:
            self.frames[frame].grid_remove()
        self.frames[option].grid(row=1,column=0)
    def get_selected_team(self,*args):
        selection=self.team_selection_listbox.curselection()
        if selection!=() or 'last_team' in args:
            if selection==():
                selection=self.team_selection_listbox.get(tk.END)
            else:
                selection=self.team_selection_listbox.get(selection)
            for team in self.teams.team_list:
                if self.teams.team_list[team]['Name']==selection:
                    return team
    def force_update_name(self):
        self.teams.team_list[self.team_state]['Name']=self.te.get()
        self.recreate_teams_listbox()
    def change_team_list(self):
        selection=self.get_selected_team()
        if selection!=False:
            self.teams.team_list[self.team_state]['Name']=self.te.get()
            self.te.set(self.teams.team_list[selection]['Name'])
            self.team_state=selection
            self.recreate_teams_listbox()
            self.recreate_listbox()
    def switch_to_last(self):
        self.team_state=key_list(self.teams.team_list)[-1:][0]
        self.te.set(self.teams.team_list[self.team_state]['Name'])
        self.recreate_listbox()
    def recreate_teams_listbox(self):
        self.team_selection_listbox.delete(0,tk.END)
        teams=specified_key_list(self.teams.team_list,'Name')
        for team in teams:
            self.team_selection_listbox.insert(tk.END,team)
    def add_team(self):
        self.teams.add_team('New team {}'.format(self.teams.last_used+1))
        self.recreate_teams_listbox()
        self.switch_to_last()
    def del_team(self):
        if self.teams.check_team_amount()!=1:
            selection=self.get_selected_team('last_team')
            self.teams.del_team(self.teams.team_list[selection]['Name'])
            self.switch_to_last()
            self.recreate_teams_listbox()
    def load_team_details(self,team_entry,listbox,player_entry,player_type):
        self.team_state=0
        self.te=team_entry
        self.lb=listbox
        self.pe=player_entry
        self.pt=player_type
    def settings_list(self,variable_frame):
        variable_frame.config(padx=10,pady=10,relief='sunken',bd=5)
        self.abbreviation=tk.StringVar()
        self.main_size=tk.IntVar()
        self.sub_size=tk.IntVar()
        self.score_type=tk.StringVar()
        tk.Label(variable_frame,text='Abbreviation:',pady=2).grid(row=0,column=0)
        tk.Entry(variable_frame,textvariable=self.abbreviation,justify='center').grid(row=0,column=1)
        tk.Label(variable_frame,text='Team size:').grid(row=1,column=0)
        tmain_size_frame=tk.Frame(variable_frame)
        tmain_size_counter=TeamVariableNumber(tmain_size_frame,self.main_size,1,4,'Main')
        tmain_size_counter.gui=self
        tmain_size_frame.grid(row=1,column=1)
        tk.Label(variable_frame,text='Sub size:').grid(row=2,column=0)
        tsub_size_frame=tk.Frame(variable_frame)
        tsub_size_counter=TeamVariableNumber(tsub_size_frame,self.sub_size,0,4,'Substitute')
        tsub_size_counter.gui=self
        tsub_size_frame.grid(row=2,column=1)
        tk.Label(variable_frame,text='Score system').grid(row=3,column=0)
        tscore_system_frame=tk.Frame(variable_frame)
        tscore_system=ButtonOptions(tscore_system_frame,self.score_type,'V1','V2')
        tscore_system.set_option('V1')
        tscore_system_frame.grid(row=3,column=1)
        self.teams=IndefiniteTeamController(Main=self.main_size,Substitute=self.sub_size)        
    def team_list(self,variable_frame):
        tteam_selection_frame=tk.LabelFrame(variable_frame,text='Teams')
        tteam_selection_frame.config(padx=10,pady=10,relief='sunken',bd=5)
        tteam_selection_listbox_frame=tk.Frame(tteam_selection_frame)
        self.team_selection_listbox=tk.Listbox(tteam_selection_listbox_frame,selectmode='browse')
        tteam_selection_listbox_scrollbar=tk.Scrollbar(tteam_selection_listbox_frame,command=self.team_selection_listbox.yview)
        self.team_selection_listbox.config(yscrollcommand=tteam_selection_listbox_scrollbar.set)
        self.team_selection_listbox.pack(side='left')
        tteam_selection_listbox_scrollbar.pack(side='right',expand='yes',fill='y')
        tteam_selection_listbox_frame.grid(row=0,column=0,columnspan=2)
        tteam_selection_frame.pack(side='left')
        tk.Button(tteam_selection_frame,text='+',command=self.add_team).grid(row=1,column=0,ipadx=25)
        tk.Button(tteam_selection_frame,text='-',command=self.del_team).grid(row=1,column=1,ipadx=25)
        self.team_selection_listbox.bind('<<ListboxSelect>>',lambda x: self.change_team_list())
        self.recreate_teams_listbox()
        tteam_frame=tk.LabelFrame(variable_frame,text='Players')
        tteam_frame.config(padx=10,pady=10,relief='sunken',bd=5)
        tteam_entry=tk.StringVar()
        tteam_entry.set('New team 1')
        tteam_entry_box=tk.Entry(tteam_frame,textvariable=tteam_entry)
        tteam_entry_box.bind('<Return>',lambda x: self.force_update_name())
        tteam_entry_box.grid(row=0,column=0,columnspan=4)
        tentry=tk.StringVar()
        tteam_listbox=tk.Listbox(tteam_frame,selectmode='browse')
        tentrybox=tk.Entry(tteam_frame,textvariable=tentry,justify='center')
        tteam_listbox.grid(row=1,column=0,columnspan=4,sticky='we')
        tgroup_choice_frame=tk.Frame(tteam_frame)
        tplayer_type=tk.StringVar()
        tplayer_type_option=ButtonOptions(tgroup_choice_frame,tplayer_type,'Main','Substitute')
        tplayer_type_option.set_option('Main')
        tentrybox.grid(row=2,column=1,columnspan=2,sticky='ns')
        tgroup_choice_frame.grid(row=3,columnspan=4,sticky='ew')
        tk.Button(tteam_frame,text='+',command=self.player_addition).grid(row=2,column=0)
        tentrybox.bind('<Return>',lambda x: self.player_addition)
        tk.Button(tteam_frame,text='-',command=self.player_removal).grid(row=2,column=3)
        tteam_frame.pack(side='right')
        self.load_team_details(tteam_entry,tteam_listbox,tentry,tplayer_type)
    def map_list(self,variable_frame):
        tmap_frame=tk.LabelFrame(variable_frame,text='Maps')
        tmap_mod_convert={'NM':1,'HD':2,'HR':3,'DT':4,'FM':5,'TB':6}
        tmap_frame.config(padx=10,pady=10,relief='sunken',bd=5) 
        tmap_entry=tk.StringVar()
        tmap_listbox_frame=tk.Frame(tmap_frame)
        tmap_scrollbar=tk.Scrollbar(tmap_listbox_frame)
        tmap_listbox=tk.Listbox(tmap_listbox_frame,selectmode='browse',yscrollcommand=tmap_scrollbar.set)
        tmap_scrollbar.config(command=tmap_listbox.yview)
        tmap_entrybox_frame=tk.LabelFrame(tmap_frame,text='Map ID')
        tmap_entrybox=tk.Entry(tmap_entrybox_frame,textvariable=tmap_entry,justify='center')
        tmap_entrybox.pack()
        tmap_listbox.pack(side='left',expand='yes',fill='x')
        tmap_scrollbar.pack(side='right',expand='no',fill='y')
        tmap_listbox_frame.grid(row=0,column=0,columnspan=4,sticky='we',ipadx=150)
        tmod_type_frame=tk.Frame(tmap_frame) 
        tmap_type=tk.StringVar()
        tmap_type_option=ButtonOptions(tmod_type_frame,tmap_type,'NM','HD','HR','DT','FM','TB')
        tmap_type_option.set_option('NM')
        tmplusb=tk.Button(tmap_frame,text='+')
        tmplusb.grid(row=1,column=0,sticky='ew')
        tmminusb=tk.Button(tmap_frame,text='-')
        tmminusb.grid(row=1,column=3,sticky='ew')
        tmap_entrybox_frame.grid(row=1,column=1,columnspan=2,sticky='ns')
        tmod_type_frame.grid(row=2,columnspan=4,sticky='ew') 
        tMapManager=MapController(tmap_listbox,tmap_entry,tmap_type)
        tmplusb.config(command=tMapManager.add_map)
        tmap_entrybox.bind('<Return>',lambda x: tMapManager.add_map())
        tmminusb.config(command=tMapManager.del_map)
        tmap_frame.pack()
        settings=SettingsFile(tMapManager)

def export_validity_check(export_class):
    if len(export_class.t[0]['Main'])==export_class.m and len(export_class.t[1]['Main'])==export_class.m:
        export_window(export_class)
    else:
        window=tk.Toplevel()
        tk.Label(window,text='You have not added enough players to each team.').pack()

def export_window(export_class):
    file=tk.filedialog.asksaveasfilename(defaultextension='.ahk',filetypes=[('Hotkey file','.ahk'),('Save file','.sav'),('Map pool file','.tmaps')])
    if file!='':
        file_type=file.split('.')[-1:][0]
        if file_type=='ahk':
            export_class.create_file(path_to_name(file))
        if file_type=='sav':
            export_class.create_save(path_to_name(file))
        if file_type=='tmaps':
            export_class.create_maps(path_to_name(file))

def path_to_name(path):
    name=''.join(path.split('.')[:-1])
    directory=''.join(path.split('/')[:-1])
    return [name,directory]

def override_file(path):
    if os.path.exists(path):
        os.remove(path)

def create_tournament():
    tourney=TournamentController()

root=tk.Tk()

#frame1
menu_frame=tk.Frame(root)
menu_controller=tk.Menu(menu_frame)
root.config(menu=menu_controller)
menu_control=tk.Menu(menu_controller,tearoff=0)
menu_controller.add_cascade(label='File Control',menu=menu_control)
menu_control.add_command(label='Import',command=lambda:call_import(abbreviation,main_size,sub_size,score_system,GUIManager,MapManager))
menu_control.add_command(label='Export',command=lambda:export_window(TournamentExport(abbreviation.get(),team_size.get(),sub_size_int.get(),score_type.get(),GUIManager,MapManager.map_list)))
menu_tournament=tk.Menu(menu_controller,tearoff=0)
menu_controller.add_cascade(label='Tournaments',menu=menu_tournament)
menu_tournament.add_command(label='Edit tournament',command=create_tournament)
menu_tournament.add_command(label='Load tournament')
menu_settings=tk.Menu(menu_controller,tearoff=0)
menu_controller.add_cascade(label='Settings',menu=menu_settings)
menu_settings.add_command(label='Key',command=lambda:settings.edit_setting_window('key'))

#frame2
variable_frame=tk.LabelFrame(root,text='Settings')
variable_frame.config(padx=10,pady=10,relief='sunken',bd=5)
team_size=tk.IntVar()
team_size.set(1)
sub_size_int=tk.IntVar() 
abbreviation=tk.StringVar()
score_type=tk.StringVar()
tk.Label(variable_frame,text='Abbreviation:',pady=2).grid(row=0,column=0)
tk.Entry(variable_frame,textvariable=abbreviation,justify='center').grid(row=0,column=1)
tk.Label(variable_frame,text='Team size:').grid(row=1,column=0)
main_size_frame=tk.Frame(variable_frame)
main_size=TeamVariableNumber(main_size_frame,team_size,1,4,'Main')
main_size_frame.grid(row=1,column=1)
tk.Label(variable_frame,text='Sub size:').grid(row=2,column=0)
sub_size_frame=tk.Frame(variable_frame)
sub_size=TeamVariableNumber(sub_size_frame,sub_size_int,0,4,'Substitute')
sub_size_frame.grid(row=2,column=1)
tk.Label(variable_frame,text='Score system').grid(row=3,column=0)
score_system_frame=tk.Frame(variable_frame)
score_system=ButtonOptions(score_system_frame,score_type,'V1','V2')
score_system.set_option('V1')
score_system_frame.grid(row=3,column=1)

#frame3
team_frame=tk.LabelFrame(root,text='Players')
team_frame.config(padx=10,pady=10,relief='sunken',bd=5)
team_selection_frame=tk.Frame(team_frame)
t1b=tk.Button(team_selection_frame,text='1')
t2b=tk.Button(team_selection_frame,text='2')
t1b.pack(side='left')
team_name=tk.StringVar()
team_name.set('Team 1')
tk.Entry(team_selection_frame,textvariable=team_name,justify='center').pack(expand='yes',fill='x',side='left')
t2b.pack(side='left')
team_selection_frame.grid(row=0,column=0,columnspan=4)
entry=tk.StringVar()
team_listbox=tk.Listbox(team_frame,selectmode='browse')
entrybox=tk.Entry(team_frame,textvariable=entry,justify='center')
team_listbox.grid(row=1,column=0,columnspan=4,sticky='we')
group_choice_frame=tk.Frame(team_frame)
player_type=tk.StringVar()
player_type_option=ButtonOptions(group_choice_frame,player_type,'Main','Substitute')
player_type_option.set_option('Main')
entrybox.grid(row=2,column=1,columnspan=2,sticky='ns')
group_choice_frame.grid(row=3,columnspan=4,sticky='ew')
TeamManager=TeamController(2,Main=team_size,Substitute=sub_size_int)
GUIManager=GUIController(TeamManager,t1b,t2b,team_name,team_listbox,entry,player_type)
t1b.config(command=lambda: GUIManager.team_button_controller(0))
t2b.config(command=lambda: GUIManager.team_button_controller(1))
tk.Button(team_frame,text='+',command=GUIManager.player_addition).grid(row=2,column=0)
entrybox.bind('<Return>',lambda x: GUIManager.player_addition())
tk.Button(team_frame,text='-',command=GUIManager.player_removal).grid(row=2,column=3)
main_size.gui=GUIManager
sub_size.gui=GUIManager

#frame4
map_frame=tk.LabelFrame(root,text='Maps')
map_mod_convert={'NM':1,'HD':2,'HR':3,'DT':4,'FM':5,'TB':6}
map_frame.config(padx=10,pady=10,relief='sunken',bd=5) 
map_entry=tk.StringVar()
map_listbox_frame=tk.Frame(map_frame)
map_scrollbar=tk.Scrollbar(map_listbox_frame)
map_listbox=tk.Listbox(map_listbox_frame,selectmode='browse',yscrollcommand=map_scrollbar.set)
map_scrollbar.config(command=map_listbox.yview)
map_entrybox_frame=tk.LabelFrame(map_frame,text='Map ID')
map_entrybox=tk.Entry(map_entrybox_frame,textvariable=map_entry,justify='center')
map_entrybox.pack()
map_listbox.pack(side='left',expand='yes',fill='x')
map_scrollbar.pack(side='right',expand='no',fill='y')
map_listbox_frame.grid(row=0,column=0,columnspan=4,sticky='we',ipadx=150)
mod_type_frame=tk.Frame(map_frame) 
map_type=tk.StringVar()
map_type_option=ButtonOptions(mod_type_frame,map_type,'NM','HD','HR','DT','FM','TB')
map_type_option.set_option('NM')
mplusb=tk.Button(map_frame,text='+')
mplusb.grid(row=1,column=0,sticky='ew')
mminusb=tk.Button(map_frame,text='-')
mminusb.grid(row=1,column=3,sticky='ew')
map_entrybox_frame.grid(row=1,column=1,columnspan=2,sticky='ns')
mod_type_frame.grid(row=2,columnspan=4,sticky='ew') 
MapManager=MapController(map_listbox,map_entry,map_type)
mplusb.config(command=MapManager.add_map)
map_entrybox.bind('<Return>',lambda x: MapManager.add_map())
mminusb.config(command=MapManager.del_map)

#finished frame
root.title('Match creation')
variable_frame.grid(row=0,column=0,sticky='s')
team_frame.grid(row=0,column=1,rowspan=2,sticky='ew')
map_frame.grid(row=0,column=2,rowspan=2,sticky='ew')
emptymenu=tk.Menu(root)


settings=SettingsFile(MapManager)
root.mainloop()
