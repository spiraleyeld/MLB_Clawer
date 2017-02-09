# -*- coding:utf-8 -*-
import csv
import requests as r
import json





# team 相關資訊的json檔
res = r.get("http://newyork.yankees.mlb.com/lookup/json/named.team_hitting_season_leader_master.bam?season=2016&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27")

mlb_teamInfo = res.json()

team_detail = mlb_teamInfo['team_hitting_season_leader_master']['queryResults']['row']

# team id & 全名
team_idFullname = {}

# team 只存id
team_id = []


for team in team_detail:

    team_idFullname[team['team_id']]=team['team_full']
    team_id.append(team['team_id'])
    

allTeamDic = {}
allTeamList = []
allMax = []
    


# 賽季從2000~2005
# 此處更換欲查詢之連續年度
for yy in range(2000,2006):
    for Id in team_id:
        year = yy
        teamId = Id
        
        # 各隊各年度的球員名單
        res1 = r.get("http://newyork.yankees.mlb.com/pubajax/wf/flow/stats.splayer?season={}&sort_order=%27desc%27&sort_column=%27avg%27&stat_type=hitting&page_type=SortablePlayer&team_id={}&game_type=%27R%27&player_pool=ALL&season_type=ANY&sport_code=%27mlb%27&results=1000".format(year, teamId))

        player_Info = res1.json()

        player_detail = player_Info['stats_sortable_player']['queryResults']['row']

        # player id & 全名
        player_idFullname = {}

        

        for player in player_detail:

            # player 只存id
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

# 將完成的名單List 指定給一變數，為後寫入之參照變數(也可不做)
data = allMax

# 此處填入欲儲存之各賽季各球隊之出戰名單
f = open("playerSeason.csv","w")
w = csv.writer(f)
w.writerows(data)
f.close()

# 將allMax(各賽季各球隊之出戰名單)帶入網址來爬gamelog
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

# 紀錄實際成功的值 & 失敗的值( 因為該JSON會存一組表頭，要拿掉，所以將正確的存進Actual_List )       
Actual_List = []
Error_List = []
for Log in gamelog_list:
    if(type(Log)==dict):
        Actual_List.append(Log)
        print(type(Log))
    elif(type(Log)==str):
        Error_List.append(Log)
        print(type(Log))
        

# 因為讓CSV 能正常寫入檔案，需將資料一組一組包進去，但是因為要"核對表頭!!!!" 所以一組數據搭配一組表頭，且要同時存入，不然順序會跑掉        
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
    



# 將gamelog寫進檔案中 
data = list_goodgame


f = open("gamelog.csv","w")
w = csv.writer(f)
w.writerows(data)
f.close()
