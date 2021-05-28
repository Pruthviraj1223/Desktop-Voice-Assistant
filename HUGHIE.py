import pyttsx3     # This module converts text to speech 
import datetime
import speech_recognition as sr
from suntime.suntime import Sun         
import wikipedia
import webbrowser
import os
import json
import cricapi
import pyjokes
from ecapture import ecapture as ec
import smtplib
import cv2
import time
import numpy as np
import requests
from bs4 import BeautifulSoup
import wolframalpha
import pywhatkit as kit


contacts = {'david': '+91 9429123854', 'Pruthviraj Jadeja': '+91 9909527601'}
mail = {'david': 'vatsalj1524@gmail.com', 'Pruthviraj Jadeja': 'pj73270@gmail.com'}

engine = pyttsx3.init('sapi5')            # by using init method we will store engine instance into variable , sapi5 is Microsoft speech api
voices = engine.getProperty('voices')

engine.setProperty('voice',voices[0].id)   # print(voices[0].id) that is male voice 

def send_sms(number, message):
    url = "https://www.fast2sms.com/dev/bulk"

    prams = {
        "authorization" : "w5eozc3FutTfQ4y6I8saLKGdVNnUODq0Z2kCbWpMHBiAmr9jJ77HJ9s61vx02nDtYoQy4wSpRilVUKjA",
        "sender_id" : "TXTIND",
        "route" : "p",
        "language" : "unicode",
        "numbers" : number,
        "message" : message
    }
    response = requests.get(url, params= prams)
    print(json.response)

def get_stock_price(ticker_symbol, api):
    url = f"https://api.twelvedata.com/price?symbol={ticker_symbol}&apikey={api}"
    response = requests.get(url).json()
    price = response['price']
    return price[:-3]

def get_stock_quote(ticker_symbol, api):
    url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey={api}"
    response = requests.get(url).json()
    return response

def speak(audio):
    engine.say(audio)             # say() method speaks the text passed to it as an argument.
    engine.runAndWait()           # It will process the voice commands
    
    rate = engine.getProperty('rate')         # It is for controlling rate of voice 
    engine.setProperty('rate', rate-3)         

    volume = engine.getProperty('volume')       # Here volume is getting controlled
    engine.setProperty('volume', volume+0.25)

def wishme():
    hour =  int(datetime.datetime.now().hour)            # storing current hour into the hour variable for greeting the user

    if hour>=0 and hour<12:
        speak("Good Morning sir")

    elif hour>=12 and hour<=18:
        speak("Good After Noon sir")

    else:
        speak("Good evening sir")

    speak("Hello sir. I am Hughie. Please tell me How may I help you ?")    

def takecommand():

     r = sr.Recognizer()                # It creates Instance of Recognizer class , store it into variable 'r'
     with sr.Microphone() as source:    # It opens our machine's microphone Will take user's command
        
        r.adjust_for_ambient_noise(source,duration=1) 
        print("Listening...")
        r.pause_threshold = 1        # It will take pause after receving command
        audio = r.listen(source)        # our commands will store into audio

     try:
        print("Recognizing.....")
        query = r.recognize_google(audio,language="en-in")          # Instance has seven methods for recognizing speech from an audio source using various APIs
        print(f"You have said: {query}\n")

     except Exception as e:
        print("Say that again.....")
        return "None"

     return query 

def sendEmail(to, content):

    s=smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()

    s.login('email','pass')
    s.sendmail('email', to, content)
    s.close()

if __name__ == "__main__":
    #  wishme()
     
     while True:
          query = takecommand().lower()

          if 'wikipedia' in query:
                try:
                  speak("Searching on wikipedia.........")
                  query = query.replace("wikipedia","")
                  list=wikipedia.search(query,results=3)
                  speak("please, choose one of these 3 options")
                  print(list)
                  query = takecommand()
                  results = wikipedia.summary(query, sentences=3)
                  speak("According to wikipedia")
                  print(results)
                  speak(results)

                except Exception as e:
                  print(e)
                  speak("I am not able to search")          

          elif 'open youtube' in query:
              webbrowser.open('youtube.com')
        
          elif 'open google' in query:
              webbrowser.open('google.com')
          
          elif 'the time' in query:
                time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"sir, the time is {time}")

          elif 'open prolog' in query:
              
                codepath= "C:\\Program Files (x86)\\swipl\\bin\\swipl-win.exe"
                os.startfile(codepath)

          elif 'open stackoverflow' in query:
            speak("Here you go to Stack Over flow.Happy coding")
            webbrowser.open_new_tab("stackoverflow.com")   

          elif 'play music' in query:
                  speak("Here you go with music")
                  music_dir = "C:\\Users\\Vandana\\Desktop\\New folder (2)"
                  songs=os.listdir(music_dir)
                  print(songs)
                  random = os.startfile(os.path.join(music_dir,songs[1]))

          elif "who made you" in query or "who created you" in query: 
            speak("I have been created by Pruthviraj Jadeja and Vatsal Jain.")

          elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir?")
 
          elif 'fine' in query or "good" in query:
            speak("It's good to know that your fine")

          elif 'joke' in query:
              speak("choose a category for joke")
              print('1. Neutral','2. chuck','3. all')
              category = takecommand().lower()
              joke= pyjokes.get_joke(language='en',category=category)
              speak(joke)
              # time.sleep(4)
              print(joke)
          
          elif 'send a mail' in query:
                try:
                  speak("What should I send?")
                  content = takecommand()
                  speak("whom should I send?")
                  to=takecommand().lower() 
                  sendEmail(mail[to], content)
                  speak("Email has been sent !")
                except Exception as e:
                  print(e)
                  speak("I am not able to send this email")

          elif 'search' in query or 'play' in query:
             
              query = query.replace("search", "") 
              query = query.replace("play", "")          
              webbrowser.open(query) 
              #  ans2 = ans['queryresult']['pods'][4]['subpods'][0]['plaintext']

          elif "camera" in query or "take a photo" in query:
                                
                  cap = cv2.VideoCapture(0)

                  # Check if the webcam is opened correctly
                  if not cap.isOpened():
                      raise IOError("Cannot open webcam")

                  while True:
                      ret, frame = cap.read()
                      frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
                      cv2.imshow('Input', frame)

                      c = cv2.waitKey(1)
                      if c == 27:
                          break

                  cap.release()
                  cv2.destroyAllWindows()

          elif "write a note" in query:
                  speak("what should I write sir?")
                  note=takecommand()
                  file=open('jarvis.txt','w')
                  speak("should I include  date and time?")
                  ans=takecommand()
                  if 'yes' in ans:
                    strTime = datetime.datetime.now().strftime(" %H %M %S")
                    file.write(strTime)
                    file.write("-")
                    file.write(note)
                  else:
                    file.write(note)  

          elif "show notes" in query:
                   speak("Showing Notes")
                   file = open("jarvis.txt", "r") 
                   print(file.read())
                   speak(file.read(6))

          elif "weather" in query:
                  api_address='http://api.openweathermap.org/data/2.5/weather?appid=60e65d065f206e5773b0c2e72ffe4e24&q='
                  speak("ENTER A CITY NAME")
                  city = takecommand()
                  url = api_address + city
                  json_data = requests.get(url).json()
                  temp= json_data['main']['temp']
                  temp=int(temp-273.15)
                  feel= json_data['main']['feels_like']
                  feel=feel-273.15
                  feel=int(feel)
                  humidity= json_data['main']['humidity']
                  desc= json_data['weather'][0]['description']
                  wind= json_data['wind']['speed']
                  latitude = json_data["coord"]['lat']
                  longitude = json_data["coord"]['lon']

                  sun = Sun(latitude,longitude)
                  time_zone = datetime.date(2021, 3,18) 
                  sun_rise = sun.get_local_sunrise_time(time_zone) 
                  sun_dusk = sun.get_local_sunset_time(time_zone) 
                  sun_rise = sun_rise.strftime('%H:%M')
                  sun_dusk = sun_dusk.strftime('%H:%M')
                  
                  speak(f"weather is {desc}")
                  print(f"weather is {desc}")
                  speak(f"temperature in {city} is {temp} celsius but it feels like {feel} celsius")
                  print(f"temperature in {city} is {temp} celsius but it feels like {feel} celsius")
                  speak(f"Humidity is {city} is {humidity} Percentage")
                  print(f"Humidity is {city} is {humidity}% ")      
                  speak("Do you want more information ?")
                  ans = takecommand().lower()
                  if "yes" in ans:
                      speak(f"Wind in {city} is {wind} ")
                      print(f"Wind in {city} is {wind} ")
                      speak(f"Sun rise at : {sun_rise}") 
                      print(f"Sun rise at :  {sun_rise}") 
                      speak(f"Sun dusk at : {sun_dusk}") 
                      print(f"Sun dusk at :  {sun_dusk}") 
                  else:
                      pass

          elif "alpha" in query:
                            
                speak("Wolfram Aplha is enabled")
                speak("Enter your query")

                ques = takecommand()
                api = 'TUU4U2-L8QGGGYY7Q'
                client = wolframalpha.Client(api)
                res = client.query(ques)
                ans = next(res.results).text
                print(ans)
               
          elif 'leave' in query:
                speak("Thanks for giving me your time")
                exit()

          elif 'news' in query:
                q = input("enter topic")
                # c = input("enter category")
                # we can ask for sources and country codes

                link = f'https://newsapi.org/v2/everything?q={q}&apiKey=91e0ac4ab5aa4284aba04acb54e2a1cf'

                data = requests.get(link).json()
                # for i in range(len(data)):
                #     print(f" Title : {data['articles'][i]['title']}")
                #     print(f" Description : {data['articles'][i]['description']}")

                print(f" Title : {data['articles'][0]['title']}")
                print(f" Description : {data['articles'][0]['description']}")
                speak(f" Title : {data['articles'][0]['title']}")
                speak(f" Description : {data['articles'][0]['description']}")
                print(f" Title : {data['articles'][1]['title']}")
                print(f" Title : {data['articles'][2]['title']}")
                print(f" Title : {data['articles'][3]['title']}")
       
          elif 'information' in query:
                                  
                  speak('Enter Player Name')
                  bats = takecommand()  
                  apikey = "Ts4OzOuPZrfwWCh9vICKYnzIEE93"
                  criapi = cricapi.Cricapi(apikey)

                  params = {'name':bats}
                  id = criapi.playerFinder(params)['data'][0]['pid']


                  params2 = {'pid':id}

                  # get layer stats from pid(PlayerId)

                  profile = criapi.playerStats(params2)['profile']
                  role =  criapi.playerStats(params2)['playingRole']
                  bat_t20_Runs = criapi.playerStats(params2)['data']['batting']['T20Is']['Runs']
                  bat_t20_Ave = criapi.playerStats(params2)['data']['batting']['T20Is']['Ave']
                  bat_ODI_Runs = criapi.playerStats(params2)['data']['batting']['ODIs']['Runs']
                  bat_ODI_Ave = criapi.playerStats(params2)['data']['batting']['ODIs']['Ave']
                  bat_TEST_Runs = criapi.playerStats(params2)['data']['batting']['tests']['Runs']
                  bat_TEST_Ave = criapi.playerStats(params2)['data']['batting']['tests']['Ave']

                  print(f'Profile is {profile}')
                  speak(f'Profile is {profile}')
                  print(f'Role is {role}')
                  speak(f'Role is {role}')
                  print(f'Batting (T20) : RUN = {bat_t20_Runs} , Avg = {bat_t20_Ave}')
                  speak(f'Run and Average in T20 is {bat_t20_Runs} and {bat_t20_Ave}')
                  print(f'Batting (ODI) : RUN = {bat_ODI_Runs} , Avg = {bat_ODI_Ave}')
                  speak(f'Run and Average in ODI is {bat_ODI_Runs} and {bat_ODI_Ave}')
                  print(f'Batting (TEST) : RUN = {bat_TEST_Runs} , Avg = {bat_TEST_Ave}')
                  speak(f'Run and Average in Test is {bat_TEST_Runs} and {bat_TEST_Ave}')

          elif 'cricket match' in query:
                  apikey = "Ts4OzOuPZrfwWCh9vICKYnzIEE93"
                  criapi = cricapi.Cricapi(apikey)
                  data = criapi.matches()
                  for i in range(len(data)):
                    data2 = data['matches'][i]['unique_id']

                  try:
                    params =  {'unique_id': data2 }   
                    sc = criapi.cricketScore(params)['score']   
                    print(sc)
                    speak(sc)
                  
                  except Exception as e:
                        continue

          elif 'upcoming matches' in query:
                apikey = "Ts4OzOuPZrfwWCh9vICKYnzIEE93"
                criapi = cricapi.Cricapi(apikey)
                data = criapi.cricket()
                match1 = data['data'][0]['description']
                print(match1)
                speak(match1)
                match2 = data['data'][1]['description']
                print(match2)
                speak(match2)

          elif 'whatsapp' in query:
            try:
                speak("Who's the recipient?")
                name = takecommand().lower()
                number = contacts[name.lower()]

                speak("What's the message?")
                message = takecommand()
                
                hour =  int(datetime.datetime.now().hour)
                minute =  int(datetime.datetime.now().minute)

                kit.sendwhatmsg(number, message, hour, minute + 1)

            except Exception as e:
                      speak('try again')
                      print('try again')

          elif 'share price' in query:

            speak("Tell me the stock symbol")
            ticker = takecommand()
                  
            api_key = "76ca0ee83ff94e1f9f4284a7dc8d5d61"

            stockdata = get_stock_quote(ticker, api_key)
            stock_price = get_stock_price(ticker, api_key)

            name = stockdata['name']

            print(f"Price of {name} is {stock_price}")
            speak(f"Price of {name} is {stock_price}")

            speak("Need more details?")
            choice = takecommand()

            if "yes" in choice:
                exchange = stockdata['exchange']
                currency = stockdata['currency']
                open_price = stockdata['open'][:-3]
                high_price = stockdata['high'][:-3]
                low_price = stockdata['low'][:-3]
                close_price = stockdata['close'][:-3]
                volume = stockdata['volume']
                
                print(f"exchange is {exchange}, currency is {currency}, open price is {open_price}, high price is {high_price}, low price is {low_price}, close price is {close_price}, volume is {volume}")
                speak(f"exchange is {exchange}, currency is {currency}, open price is {open_price}, high price is {high_price}, low price is {low_price}, close price is {close_price}, volume is {volume}")

          elif 'online' in query:

              speak('enter song name')
              song = takecommand().lower()
              kit.playonyt(song)
