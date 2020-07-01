import requests, string
API_KEY = 'RGAPI-8d9c07ba-ddc6-4b30-8c06-bb58f4f01506'

def get_summoner_data(region, summoner_name):
    URL = 'https://' + str(region) + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+ str(summoner_name)+'?api_key=' + API_KEY 
    response = requests.get(URL)
    return response.json()

def get_ranked_data(region, id):
    URL = 'https://' + str(region) + '.api.riotgames.com/lol/league/v4/entries/by-summoner/'+ str(id) + '?api_key=' + API_KEY
    response = requests.get(URL)
    return response.json()


def get_tier_icon(tier):
    return 'Emblem_' + str(tier).lower().capitalize() + '.png'


def get_main(summoner_name):
    pass
def MKDA(minions, kills, deaths, assits, minutes, role):
    if role == 'support':
        return (kills+assits)/max(1,deaths) + 1
    elif role == 'jungle':
        return (kills+assits)/max(1, deaths) + minions/(minutes*7)
    else:
        return (kills+assits)/max(1, deaths) + minions/(minutes*9)


def tier_avarage(server,tier,rank):
    player_total = 0
    tier_total = 0
    #URL = 'https://' + str(server)+ '.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/' + str(tier) + '/' +str(rank) + '?page=1&api_key=' + str(API_KEY)
    LINK = 'https://eun1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=1&api_key=RGAPI-4b7e3fde-1960-4aa9-956e-9fb018296142'
    response = requests.get(LINK).json()
    for player in response:
        print(player)
        summoner = requests.get(
            'https://'+str(server)+'.api.riotgames.com/lol/summoner/v4/summoners/'+str(player['summonerId'])+'?api_key='+str(API_KEY)).json()
        print(summoner)
        account_id = summoner['accountId']
        matchlist = requests.get(
            'https://' + str(server) + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + str(account_id) + '?season=13&api_key=' + str(API_KEY)).json()
        for match in matchlist['matches']:
            if match['queue'] == '420':
                print(match)
                minutes = match['timestamp'][:5]/60
                champion = match['champion']
                role = match['lane']
                game = requests.get(
                    'https://'+str(server)+'.api.riotgames.com/lol/match/v4/matches/'+str(match['gameId']) + '?api_key=' +str(API_KEY)).json
                if game['participants']['championId'] == champion:
                    participant_id = game['participants']['participantId']
                    stats = game['participants']['stats'][participant_id]
                    player_total += MKDA(stats['totalMinionsKilled'], stats['kills'],  stats['deaths'],
                    stats['assists'], minutes, role)
        player_mkda = player_total/len(matchlist)
        tier_total += player_mkda
    tier_mkda = tier_total/len(response)
    print(tier_mkda)
    return tier_mkda
