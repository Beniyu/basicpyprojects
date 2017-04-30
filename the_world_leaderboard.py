import time
from urllib.request import urlopen
import json

key='' #Enter API Key Here

class ScoreLeaderboard(object):
    def __init__(self,key,user_list):
        self.key=key
        self.user_list=user_list
        score_leaderboard=[]
        for user in user_list:
            print('Getting scores from {}.'.format(user))
            user_scores=self.player_score_retrieve(user)
            for score in user_scores:
                for best_score in score_leaderboard:
                    if score['beatmap']==best_score['beatmap']:
                        if score['pp']>best_score['pp']:
                            score_leaderboard.remove(best_score)
                            score_leaderboard.append(score)
                        else:
                            break
                else:
                    score_leaderboard.append(score)
            time.sleep(5)
        self.score_leaderboard=score_leaderboard
    def player_score_retrieve(self,user):
        player=json.loads(urlopen('https://osu.ppy.sh/api/get_user_best?k={}&u={}&limit=100'.format(self.key,user)).read().decode('utf-8'))
        scores=[]
        for score in player:
            scores.append({'beatmap':score['beatmap_id'],'pp':score['pp']})
        return scores
    def calculate_pp(self):
        clean_scores_pp=list(map(lambda x: x['pp'], self.score_leaderboard))
        clean_scores_pp.sort()
        clean_scores_pp=clean_scores_pp[::-1]
        total_pp=list(map(lambda x: float(x[1])*0.95**x[0], enumerate(clean_scores_pp)))
        total_pp=sum(total_pp)
        self.pp=total_pp
        print('The total PP within this user list is {}.'.format(total_pp))

user_list=['Vaxei','Angelsim','Rafis','hvick225','filsdelama','Spare','_index','Dustice','Azerite','Gayzmcgee','DanyL','HappyStick','Rohulk','-Konpaku-','free_mutual','Emilia','Musty','talala','Adamqs','Toy','Sanze','Wilchq','CXu','Mizuru','-Zirba-','Axarious','Green_NPC','Recia','Mathi','kablaze','Piggey','rustbell','Tarulas','WubWoofWolf','Azer','Yaong','MouseEasy','Salieri','Xilver','Reimu-Desu','Vettel','Mlaw22','kuu01','fieryrage','Akcel','Dunois','i_suck','Dumii','Neliel','FunOrange','MiruHong','DoKito','ThePooN','Beafowl','Plz_Enjoy_Game','My_Angel_Serena','-_Nikliu_-','Monko2k','[_Zane_]','Bubbleman','-Hebel-','_RyuK','Arnold24x24','waaiiru','MyAngelNamirin','aleho8','MoeYandere','1E308','hallowatcher','Rucker','Afrodafro','uyghti','Loli_Silica','Kyoko','Fenrir','Elysion','Karthy','Fedora_Goose','Leaf','La_Valse','Spook','My_Aim_Trash','Mayoler','[_ZhengS_]','Aireu','Meltina','Flask','Korilak','AtHeoN','EmertxE','Avenging_Goose','hshs','Kynan','Rizer','Red_Pixel','DenierNezzar','Apraxia','zeluaR','cmnk']

the_world=ScoreLeaderboard(key,user_list)
the_world.calculate_pp()
