from django import forms

REGION_CHOICES = (
    ("","Region..."),
    ("br1", "Brazil"),
    ("eun1", "Europe Nordic & East"),
    ("euw1", "Europe West"),
    ("kr", "Koreea"),
    ("la1", "Latin America North"),
    ("la2", "Latin America South"),
    ("na1", "North America"),
    ("oc1", "Oceania"),
    ("ru", "Russia"),
    ("tr1", "Turkey")
)



class SummonerData(forms.Form):
    summoner_name = forms.CharField(required=True,
                                    widget=forms.TextInput(attrs={'placeholder': 'Summoner name'}))
    region = forms.ChoiceField(
        choices=REGION_CHOICES, required=True, widget=forms.Select())
