# Live-Translator-En-Kr-
Side project (Python)

Anyone who has difficulties with speaking foreign language can use this Live translator

For now, the source langauge is only in English and destination language is Korean and French.

However, soon user will have a choice to choose which source and destination langauge he/she wants to set up

So basically start the app and speak

The app will automatically translate your message and show it to terminal

and when you want to stop say "quit" or "exit" then the app will terminate and

it will save your conversation in 3 different langauges MP3 files (English, Korean, French)


Mechnism of the app

First when user say anything, 

Google speech to text API (Streaming option) will get text through mic

then the text will be translated to destination languages (French and Korean) through google translate API

and finally when user say "quit" or "exit"

it will use Google text to speech API and will create MP3 files with the conversation history data

So total 3 APIs are used for this project
