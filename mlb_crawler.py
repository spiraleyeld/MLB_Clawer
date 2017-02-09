# -*- coding:utf-8 -*-
import csv
import requests as r
import json


###### �B�J�@


# team ������T��json��
res = r.get("http://newyork.yankees.mlb.com/lookup/json/named.team_hitting_season_leader_master.bam?season=2016&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27")

mlb_teamInfo = res.json()

team_detail = mlb_teamInfo['team_hitting_season_leader_master']['queryResults']['row']

# team id & ���W
team_idFullname = {}

# team �u�sid
team_id = []


for team in team_detail:

    team_idFullname[team['team_id']]=team['team_full']
    team_id.append(team['team_id'])
    

allTeamDic = {}
allTeamList = []
allMax = []
    


# �ɩu�q2000~2005
# ���B�󴫱��d�ߤ��s��~��
for yy in range(2000,2006):
    for Id in team_id:
        year = yy
        teamId = Id
        
        # �U���U�~�ת��y���W��
        res1 = r.get("http://newyork.yankees.mlb.com/pubajax/wf/flow/stats.splayer?season={}&sort_order=%27desc%27&sort_column=%27avg%27&stat_type=hitting&page_type=SortablePlayer&team_id={}&game_type=%27R%27&player_pool=ALL&season_type=ANY&sport_code=%27mlb%27&results=1000".format(year, teamId))

        player_Info = res1.json()

        player_detail = player_Info['stats_sortable_player']['queryResults']['row']

        # player id & ���W
        player_idFullname = {}

        

        for player in player_detail:

            # player �u�sid
            player_id = []
            player_idFullname[player['player_id']]=player['name_display_first_last']
            player_id.append(yy)
            player_id.append(teamId)
            player_id.append(player['team_name'])
            player_id.append(player['player_id'])
            player_id.append(player['name_display_last_first'])
            
            allMax.append(player_id)
            print(player_id)

allMax.insert(0,['Season','Team_ID','Team_Name','Player_ID','Player_Name'])

# �N�������W��List ���w���@�ܼơA����g�J���ѷ��ܼ�(�]�i����)
data = allMax

# ���B��J���x�s���U�ɩu�U�y�����X�ԦW��
f = open("playerSeason.csv","w")
w = csv.writer(f)
w.writerows(data)
f.close()

# �NallMax(�U�ɩu�U�y�����X�ԦW��)�a�J���}�Ӫ�gamelog
gamelog_list = []

for record in range(1,len(allMax)):
    seasonY = allMax[record][0]
    playeridY = allMax[record][3]
    
    
    
    res2 = r.get("http://m.mlb.com/lookup/json/named.sport_hitting_game_log_composed.bam?game_type=%27R%27&league_list_id=%27mlb%27&player_id={}&season={}&sit_code=%271%27&sit_code=%272%27&sit_code=%273%27&sit_code=%274%27&sit_code=%275%27&sit_code=%276%27&sit_code=%277%27&sit_code=%278%27&sit_code=%279%27&sit_code=%2710%27&sit_code=%2711%27&sit_code=%2712%27".format(playeridY,seasonY))

    mlb_gamelog = res2.json()

    mlb_gamelog
    
    gamelog_detail = mlb_gamelog['sport_hitting_game_log_composed'][ 'sport_hitting_game_log']['queryResults']['row']

    for log in gamelog_detail:
       
        gamelog_list.append(log)
        print(log)

# ������ڦ��\���� & ���Ѫ���( �]����JSON�|�s�@�ժ��Y�A�n�����A�ҥH�N���T���s�iActual_List )       
Actual_List = []
Error_List = []
for Log in gamelog_list:
    if(type(Log)==dict):
        Actual_List.append(Log)
        print(type(Log))
    elif(type(Log)==str):
        Error_List.append(Log)
        print(type(Log))
        

# �]����CSV �ॿ�`�g�J�ɮסA�ݱN��Ƥ@�դ@�ե]�i�h�A���O�]���n"�ֹ���Y!!!!" �ҥH�@�ռƾڷf�t�@�ժ��Y�A�B�n�P�ɦs�J�A���M���Ƿ|�]��        
totalList = Actual_List
list_goodgame = []
kk = []
vv = []
for i in totalList:
    for keys in i:
        
        values = i[keys]
        
        kk.append(keys)
        vv.append(values)
   
    list_goodgame.append(kk)
    list_goodgame.append(vv)
    kk = []
    vv = []
    



# �Ngamelog�g�i�ɮפ� 
data = list_goodgame


f = open("gamelog.csv","w")
w = csv.writer(f)
w.writerows(data)
f.close()
