from .extras import get_ranked_data, get_summoner_data, get_tier_icon, tier_avarage
from .forms import SummonerData
from django.shortcuts import render, redirect


# Create your views here.
def main_view(request):
	if request.method == 'POST':
		form = SummonerData(request.POST)
		if form.is_valid():
			summoner_name = form.cleaned_data['summoner_name']
			region = form.cleaned_data['region']
			return redirect('player-info', region, summoner_name)
	else:
		form = SummonerData()
		context = {'form': form}
	return render(request, 'home.html')

def game_wiki(request):
	return render(request, 'lol-wiki.html')

def player_info(request, region, summoner_name):
	response_json = get_summoner_data(region, summoner_name)
	main_bg = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Sylas_0.jpg'
	#mkda = tier_avarage('eun1', 'DIAMOND', 1)
	item1 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/item/1001.png'
	item2 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/item/1001.png'
	item3 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/item/1001.png'
	item4 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/item/1001.png'
	item5 ='http://ddragon.leagueoflegends.com/cdn/10.12.1/img/item/1001.png'
	item6 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/item/1001.png'
	summoner_spell1 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/spell/SummonerFlash.png'
	summoner_spell2 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/spell/SummonerHeal.png'
	champion = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/champion/Sylas.png'
	player2 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/champion/Annie.png'
	player3 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/champion/Anivia.png'
	player4 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/champion/Urgot.png'
	player5 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/champion/Darius.png'
	player6 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/champion/Aatrox.png'
	player7 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/champion/Jax.png' 
	player8='http://ddragon.leagueoflegends.com/cdn/10.12.1/img/champion/Jayce.png' 
	player9 ='http://ddragon.leagueoflegends.com/cdn/10.12.1/img/champion/Zyra.png' 
	player10 = 'http://ddragon.leagueoflegends.com/cdn/10.12.1/img/champion/Varus.png' 
	icon = response_json['profileIconId']
	summoner_icon = 'http://ddragon.leagueoflegends.com/cdn/10.11.1/img/profileicon/' + str(icon) + '.png'
	if 'status' in response_json:
		context = {}
	else:
		ID = response_json['id']
		response_json2 = get_ranked_data(region, ID)
		summoner_name = response_json2[0]['summonerName']
		solo_tier = response_json2[0]['tier']
		solo_rank = response_json2[0]['rank']
		solo_tier_icon = get_tier_icon(solo_tier)
		solo_leaguePoints = response_json2[0]['leaguePoints']

		flex_tier = response_json2[1]['tier']
		flex_rank = response_json2[1]['rank']
		flex_tier_icon = get_tier_icon(flex_tier)
		flex_leaguePoints = response_json2[1]['leaguePoints']
		context = {
			'summoner_icon': summoner_icon,
			'summoner_name': summoner_name,
			'solo_tier_icon': solo_tier_icon,
			'solo_tier': solo_tier,
			'solo_rank': solo_rank,
			'solo_lp': solo_leaguePoints,
			'flex_tier_icon': flex_tier_icon,
			'flex_tier': flex_tier,
			'flex_rank': flex_rank,
			'flex_lp': flex_leaguePoints,
		#	'mkda':mkda
			'main_bg':main_bg,
			 'item1':item1,
			 'item2':item2,
			 'item3': item3,
			 'item4':item4,
			 'item5': item5,
			 'item6': item6,
			 'summoner_spell1':summoner_spell1,
			 'summoner_spell2': summoner_spell2,
			 'champion':champion,
			 'player2':player2,
			 'player3':player3,
			 'player4':player4,
			 'player5':player5,
			 'player6':player6,
			 'player7':player7,
			 'player8':player8,
			 'player9': player9,
			 'player10': player10,
			
		}
	return render(request, 'player_info.html', context)
