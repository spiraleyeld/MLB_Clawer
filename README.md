本例主要是爬取ＭＬＢ官方的gamelog之Json檔案，屬於爬蟲的基本入門．

主要流程為：


1.取得球隊ID 跟 相關資訊(名稱等)
http://newyork.yankees.mlb.com/lookup/json/named.team_hitting_season_leader_master.bam?season=2016&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27


2.透過步驟1的ID跟年度(SeasonYear)，取得每年每隊出賽名單
http://newyork.yankees.mlb.com/pubajax/wf/flow/stats.splayer?season={}&sort_order=%27desc%27&sort_column=%27avg%27&stat_type=hitting&page_type=SortablePlayer&team_id={}&game_type=%27R%27&player_pool=ALL&season_type=ANY&sport_code=%27mlb%27&results=1000".format(year, teamId)


3.透過步驟2產生的名單依據球員ID跟年度(SeasonYear)撈取單一球員的該年度gamelog
http://m.mlb.com/lookup/json/named.sport_hitting_game_log_composed.bam?game_type=%27R%27&league_list_id=%27mlb%27&player_id={}&season={}&sit_code=%271%27&sit_code=%272%27&sit_code=%273%27&sit_code=%274%27&sit_code=%275%27&sit_code=%276%27&sit_code=%277%27&sit_code=%278%27&sit_code=%279%27&sit_code=%2710%27&sit_code=%2711%27&sit_code=%2712%27".format(playeridY,seasonY)


hitting(打擊) & pitching(投手) 拆成兩個檔案(網址若干差異)
