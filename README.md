# eLO!2017 - Unofficial API
API for eLO! 2017 application for freshmen in average school
More information about app you can find on [Google Play]( https://play.google.com/store/apps/details?id=pl.edu.vulcan.elo2017)

## A little something about application
Application is only WebView for mobile website and available only for Android.
Result is small communication with new classmates. Why we created this shit app? Idk.. 
Only one reason can be notifications, but with new fuctions a browsers they can displayed in him.

In next years please - write better website ;)
>but idea on this is nice

Ekhem... [kek](https://elo.edu.pl/)

##Example with API

###Simple echo-bot:
'''python
from eLO import eLO

bot_name = 'example'
bot = eLO('email@example.com', '')
bot.login()

while(1):
	last_message = bot.last_messeages(1)
	if last_message[1]['member'] != your_name:
		bot.send_message(last_message[1]['text'])
	else:
		pass
'''


