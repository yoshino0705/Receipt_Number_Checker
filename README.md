# Receipt_Number_Checker

A LINE bot dedicated to comparing the Taiwanese receipts' numbers (kinda like lottery) to the numbers that grants cash.

QR Code to invite the bot (Up to 50 users can befriend the bot, due to the limits of free plan)

![alt tag](https://i.imgur.com/OtZ5uOd.png)

# Features:
- Examines the input numbers and reply with messages such as:
  'no hit', 'congrats you have won ...', and 'invalid inputs' (in Chinese that is)
  
- Can handle multiple sets of numbers, where each set of numbers is separated by either a newline or a white space

- Filters out any non-numerical characters in the inputs, so users do not need to go back and delete any mis-typed characters, just hit send, and the bot will handle it all

# Uses 
- [Heroku](https://heroku.com)
- [LINE API](https://github.com/line/line-bot-sdk-python)

# Dependencies:
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [requests](https://github.com/requests/requests)
- [Flask](http://flask.pocoo.org/docs/0.12/)
- [gunicorn](https://github.com/benoitc/gunicorn)

# Disclaimer:
```
This bot is not responsible for any losses of fortune due to problems in the code that causes the users to receive incorrect results.
```
