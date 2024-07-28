import subprocess                       #to get system process detail used in varios command 
import wolframalpha                       #to compute expert leve answers
import pyttsx3  
from threading import Thread 
from tkinter import *                        #for text to speech conversion
import json
import speech_recognition as sr            #convert audio into text
import datetime                              #for time and date
import wikipedia                    #to fetch information from wikipedia website
import webbrowser                    #allows web based document
import os
import winshell
import random
import pyautogui
import pyjokes                #collection of python jokes over the internet
import smtplib
import ctypes
import time
import requests  
import shutil
from tkinter import *               
from twilio.rest import Client            #used to make calls and messages
import progress
import win32com.client as wincl
from urllib.request import urlopen
import requests
from googletrans import Translator



# Set up API key
weather_api_key = os.getenv('WEATHER_API_KEY')
wolfram_api_key = os.getenv('WOLFRAM_API_KEY')
news_api_key = os.getenv('NEWS_API_KEY')




# Initialize pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


# Create an instance of the Translator class for language translation
translator = Translator()

# Create the main Tkinter window
window = Tk()
window.title("MAYA Voice Assistant")

# Create a Text widget for displaying conversation text with specified dimensions and word wrapping
conversation_text = Text(window, height=40, width=70, wrap=WORD)
conversation_text.pack()

# Function to append text to the conversation Text widget and scroll to the end
def append_text(text):
	conversation_text.insert(END, text + '\n')
	conversation_text.see(END)  # Scroll to the end of the text


# Function to speak given text
def speak(audio):
	engine.say(audio)
	engine.runAndWait()
	append_text("MAYA: " + audio)


# Function to prompt the user for their username
def username():
	speak("What should i call you ?")
	uname = takeCommand()
	speak("Welcome ")
	speak(uname)
	columns = shutil.get_terminal_size().columns
	
	print("#####################".center(columns))
	print("Welcome ", uname.center(columns))
	print("#####################".center(columns))
	
	speak("How can i Help you?")

# Function to recognize user's voice command.
def takeCommand():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		append_text("Listening...")
		r.pause_threshold = 1
		audio = r.listen(source)

	try:
		append_text("Recognizing...")
		query = r.recognize_google(audio, language ='en-in')
		append_text(f"User said: {query}\n")

	except Exception as e:
		print(e)
		append_text("Unable to Recognize your voice.")
		return "None"
	
	return query


# Function to wish the user based on the time of day."
def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		speak("Good Morning  !")

	elif hour>= 12 and hour<18:
		speak("Good Afternoon !")

	else:
		speak("Good Evening !")

	assname =("MAYA")
	speak("I am your Assistant")
	speak(assname)

# Function to search for a query on Wikipedia.
def search_wikipedia(query):
    speak('Searching Wikipedia...')
    print('Searching Wikipedia...')
    summary = wikipedia.summary(query, sentences=3)
    speak("According to Wikipedia")
    print(summary)
    speak(summary)

# Function to interact with Maya (voice assistant) for queries
def ask_maya():
    speak("Sure, what would you like to know about?")
    user_input = takeCommand()
    if user_input:
        response = wolfram_alpha_query(user_input)
        speak(response)
        print(response)

# Function to query Wolfram Alpha for expert-level answers
def wolfram_alpha_query(query):
    client = wolframalpha.Client(wolfram_api_key)
    res = client.query(query)
    return next(res.results).text	


# Function to send an email
def sendEmail(to, content):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()	
	# Enable low security in gmail
	server.login('your email id', 'your email password')
	server.sendmail('your email id', to, content)
	server.close()
	speak("Email has been sent!")


# Function to get weather information for a city.
def get_weather_info(city):
	
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp_kelvin = data['main']['temp']
        temp_celsius = temp_kelvin - 273.15  # Convert temperature to Celsius
        return f"The weather in {city} is {weather_desc}. Temperature: {temp_celsius:.2f}°C"
    else:
        return "Sorry, I couldn't fetch the weather information."
	

# Function to fetch a random joke.
def get_joke():
    return pyjokes.get_joke()

# Function to calculate the result of a mathematical expression
def calculate_expression(expression):
    try:
        client = wolframalpha.Client(wolfram_api_key)
        res = client.query(expression)
        answer = next(res.results).text
        return answer
    except Exception as e:
        print("Error calculating expression:", e)
        return "Error calculating expression"

	
	
# Function to change the wallpaper using the specified image path
def change_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

# Function to translate text to a specified target language (default is English)
def translate_text(text, target_lang='en'):
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return "Translation error"
	
# Function to handle translation operations	
def handle_translate():
    speak("What text would you like to translate?")
    text_to_translate = takeCommand()

    if text_to_translate:
        if 'to' in text_to_translate:
            target_lang = text_to_translate.split('to')[-1].strip()
            text_to_translate = text_to_translate.split('to')[0].strip()
            translated_text = translate_text(text_to_translate, target_lang=target_lang)
        else:
            translated_text = translate_text(text_to_translate)
        speak(f"The translated text is: {translated_text}")


    # the user specifies the target language in their command, like "Translate this to French"
    if 'to' in text_to_translate:
        target_lang = text_to_translate.split('to')[-1].strip()
        text_to_translate = text_to_translate.split('to')[0].strip()
        translated_text = translate_text(text_to_translate, target_lang=target_lang)
    else:
        # If target language is not specified, default to English
        translated_text = translate_text(text_to_translate)

    speak(f"The translated text is: {translated_text}")



# Function to generate and get the user's choice in a game or decision-making scenario
def get_user_choice():
    speak("Choose rock, paper, or scissors.")
    while True:
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            user_choice = recognizer.recognize_google(audio).lower()
            if user_choice in ['rock', 'paper', 'scissors']:
                return user_choice
            else:
                speak("Invalid choice. Please choose rock, paper, or scissors.")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError:
            speak("Sorry, I'm having trouble processing your request.")
# Function to generate and get the computer's choice in a game or decision-making scenario
def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])
# Function to handle playing a game 
def handle_play_game():
    def determine_winner(user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        elif user_choice == 'rock':
            return "You win!" if computer_choice == 'scissors' else "Computer wins!"
        elif user_choice == 'paper':
            return "You win!" if computer_choice == 'rock' else "Computer wins!"
        elif user_choice == 'scissors':
            return "You win!" if computer_choice == 'paper' else "Computer wins!"

    user_choice = get_user_choice()
    computer_choice = get_computer_choice()
    speak(f"You chose {user_choice}.")
    speak(f"Computer chose {computer_choice}.")
    speak(determine_winner(user_choice, computer_choice))


# Function to fetch cricket updates (scores, news, etc.)	
def cricket_updates():
    url = "https://cricapi.com/api/matches"
    params = {
        "apikey": "c3767224-6cdf-4a83-8ec2-f21a0b286959"  # Get your API key from https://www.cricapi.com/
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "matches" in data:
            return data["matches"]
        else:
            return []
    else:
        return None  # Return None for failed request
	
# Function to open a folder at the specified folder path	
def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
        speak(f"Folder '{folder_name}' created successfully")
    except FileExistsError:
        speak(f"Folder '{folder_name}' already exists")
    except Exception as e:
        speak(f"Error creating folder: {e}")

# Function to search for a folder with the given name within the system
def open_folder(folder_path):
    try:
        subprocess.Popen(f'explorer "{folder_path}"')
        speak(f"Opening folder '{folder_path}'")
    except Exception as e:
        speak(f"Error opening folder: {e}")

# Function to search a file at the specified file path
def search_folder(folder_name):
    try:
        search_results = []
        for root, dirs, files in os.walk('C:\\Users\\avani yadav\\Documents\\VA folder'):
            if folder_name in dirs:
                search_results.append(os.path.join(root, folder_name))
        if search_results:
            speak(f"Found {len(search_results)} instances of folder '{folder_name}'")
            for result in search_results:
                speak(result)
        else:
            speak(f"Folder '{folder_name}' not found")
    except Exception as e:
        speak(f"Error searching folder: {e}")

# Function to open a file at the specified file path
def open_file(file_path):
    try:
        os.startfile(file_path)
        speak(f"Opening file '{file_path}'")
    except Exception as e:
        speak(f"Error opening file: {e}")

# Function to change the desktop background to a random image from the specified folder path
def change_random_background(folder_path):
    # Get a list of all image files in the specified folder
    image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        speak("No image files found in the specified folder.")
        return
    
    # Select a random image file from the list
    random_image = random.choice(image_files)
    
    # Change the background using the selected image
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(folder_path, random_image), 0)
    
    speak("Background changed successfully")		


def check_for_updates():
    # Call assistant logic function 
    assistant_logic()
    # Schedule this function to run again after a delay (e.g., 100 milliseconds)
    window.after(100, check_for_updates)

def assistant_logic():
	append_text("Initializing Assistant...")
	time.sleep(2)
	wishMe()
	username()
	while True:
		
		query = takeCommand().lower()
		
		# All the commands said by user will be
		# stored here in 'query' and will be
		# converted to lower case for easily
		# recognition of command
		if 'query' in query or 'Ask Maya' in query:
			speak("Sure, what would you like to know  about?")
			user_input = takeCommand()
			response = wolfram_alpha_query(user_input)
			if user_input:
				response = wolfram_alpha_query(user_input)
				speak(response)
				print(response)

			# Ask if the user wants to continue
			speak("Would you like to ask something else?")
			user_response = takeCommand().lower()

			if 'no' in user_response:
				speak("Alright, have a great day!")
				

		elif 'search wikipedia' in query:
			search_query = query.replace('search wikipedia for', '').strip()
			search_wikipedia(search_query)

		elif'calculate' in query:
			expression = query.split('calculate')[-1].strip()
			result = calculate_expression(expression)
			speak(f"The answer is {result}")

		elif'youtube search' in query:
			query = query.replace("youtube search", "")
			webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
			speak("Here are the  results on YouTube for your search.")

		elif"google search" in query:
			query = query.replace("google search", "")
			webbrowser.open(f"https://www.google.com/search?q={query}")
			speak("Here are the  results on google for your search.")

		

		elif 'open youtube' in query:
			speak("Here you go to Youtube\n")
			webbrowser.open("youtube.com")

		elif 'open browser' in query or 'Open web browser' in query:
			speak("Opening web browser")		
			path = "C:\\ProgramData\\Microsoft\Windows\\Start Menu\\Programs\\Firefox.lnk"
			os.startfile(path)

		elif 'open google' in query:
			speak("Here you go to Google\n")
			webbrowser.open("google.com")

		elif 'open stackoverflow' in query:
			speak("Here you go to Stack Over flow.Happy coding\n")
			webbrowser.open("stackoverflow.com")

		elif 'play music' in query or "play song" in query:
			speak("Here you go with music")
			# music_dir
			music_dir = "C:\\Users\\avani yadav\\Documents\\Music"
			songs = os.listdir(music_dir)
			print(songs)
			random = os.startfile(os.path.join(music_dir, songs[5]))

		elif 'the time' in query or 'time' in query:
			strtime = datetime.datetime.now().strftime("%H:%M:%S")
			speak(f"The time is %s" % strtime)

		elif 'send a mail' in query:
			try:
				speak("What should I say?")
				content = takeCommand()
				speak("whome should i send")
				to = input()
				sendEmail(to, content)
				speak("Email has been sent !")
			except Exception as e:
				print(e)
				speak("I am not able to send this email")

		elif 'how are you' in query:
			speak("I am fine, Thank you")
			speak("How are you?")

		elif 'fine' in query or "good" in query:
			speak("It's good to know that your fine")

		elif "change my name to" in query:
			query = query.replace("change my name to", "")
			assname = query

		elif "change name" in query:
			speak("What would you like to call me ? ")
			assname = takeCommand()
			speak("Thanks for naming me")

		elif "what's your name" in query or "What is your name" in query:
			speak("My friends call me")
			speak(assname)
			print("My friends call me", assname)

		elif 'exit' in query:
			speak("Thanks for giving me your time")
			exit()
			
		elif 'joke' in query:
			speak(pyjokes.get_joke())
			
		elif "calculate" in query:
			
			app_id = "Wolframalpha api id"
			client = wolframalpha.Client(app_id)
			indx = query.lower().split().index('calculate')
			query = query.split()[indx + 1:]
			res = client.query(' '.join(query))
			answer = next(res.results).text
			print("The answer is " + answer)
			speak("The answer is " + answer)

		elif 'search' in query or 'play' in query:
			
			query = query.replace("search", "")
			query = query.replace("play", "")		
			webbrowser.open(query)

		elif "who i am" in query:
			speak("If you talk then definitely your human.")

		elif "why you came to world" in query:
			speak(" It's a secret")

		elif 'open PPT presentation' in query:
			speak("opening Power Point presentation")
			power = r"C:\\Users\\avani yadav\\Documents\\PPT Presentation"
			os.startfile(power)


		elif 'change background' in query:
			folder_path = r"C:\Users\avani yadav\Pictures\Wallpapers4K\HD"  # Specify the folder path where your images are stored
			change_random_background(folder_path)


		 

		elif 'news' in query:
			
			try:
				jsonObj = urlopen(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}")
				data = json.load(jsonObj)
				i = 1
				
				speak('here are some top news from india')
				print('''=============== TOP HEADLINES FROM INDIA ============'''+ '\n')
				
				for item in data['articles']:
					
					print(str(i) + '. ' + item['title'] + '\n')
					print(item['description'] + '\n')
					speak(str(i) + '. ' + item['title'] + '\n')
					i += 1
			except Exception as e:
				
				print(str(e))

		
		elif 'lock window' in query:
				speak("locking the device")
				ctypes.windll.user32.LockWorkStation()

		elif 'shutdown system' in query:
				speak("Hold On a Sec ! Your system is on its way to shut down")
				subprocess.call('shutdown / p /f')
				
		elif 'empty recycle bin' in query:
			winshell.recycle_bin().empty(confirm = False, show_progress = False,  sound = True)
			speak("Recycle Bin Recycled")

		elif "don't listen" in query or "stop listening" in query:
			speak("for how much time you want to stop maya from listening commands")
			a = int(takeCommand())
			time.sleep(a)
			print(a)

		elif "where is" in query:
			query = query.replace("where is", "")
			location = query
			speak("User asked to Locate")
			speak(location)
			webbrowser.open("https://www.google.com/maps/place/" + location + "")

		

		elif "restart" in query:
			subprocess.call(["shutdown", "/r"])
			
		elif "hibernate" in query or "sleep" in query:
			speak("Hibernating")
			subprocess.call("shutdown / h")

		elif "log off" in query or "sign out" in query:
			speak("Make sure all the application are closed before sign-out")
			time.sleep(5)
			subprocess.call(["shutdown", "/l"])

		elif "Open notepad" in query or "Notepad" in query:
			os.start("notepad.exe")
			speak("Opening Notepad")
			print("Opening Notepad")

		elif "Open Calculator" in query or "Calculator" in query:
			os.start("calc.exe")
			speak("Opening Calculator")
			print("Opening Calculator")

		elif "write a note" in query:
			speak("What should i write ")
			note = takeCommand()
			file = open('maya.txt', 'w')
			speak("Should i include date and time")
			snfm = takeCommand()
			if 'yes' in snfm or 'sure' in snfm:
				strTime = datetime.datetime.now().strftime("% H:% M:% S")
				file.write(strTime)
				file.write(" :- ")
				file.write(note)
			else:
				file.write(note)
		
		elif "show note" in query:
			speak("Showing Notes")
			file = open("maya.txt", "r")
			print(file.read())
			speak(file.read(6))

		elif "update assistant" in query:
			speak("After downloading file please replace this file with the downloaded one")
			url = '# url after uploading file'
			r = requests.get(url, stream = True)
			
			with open("Voice.py", "wb") as Pypdf:
				
				total_length = int(r.headers.get('content-length'))
				
				for ch in progress.bar(r.iter_content(chunk_size = 2391975),
									expected_size =(total_length / 1024) + 1):
					if ch:Pypdf.write(ch)

			
		elif "send message " in query:
				# You need to create an account on Twilio to use this service
				account = 'Account  key'
				auth_token = 'Auth token'
				client = Client(account, auth_token)

				message = client.messages \
								.create(
									body = takeCommand(),
									from_='Sender No',
									to ='Receiver No'
								)

				print(message.sid)

		elif "wikipedia" in query:
			webbrowser.open("wikipedia.com")

		elif "Good Morning" in query:
			speak("A warm" +query)
			speak("How are you ")
			speak(assname)

		# most asked question from google Assistant
		elif "how are you" in query:
			speak("I'm fine, glad you ask me that")

		elif "thank you" in query:
			speak("You're welcome!")

		elif "what is" in query or "who is" in query:
			
			client = wolframalpha.Client("app_id")
			res = client.query(query)
			
			try:
				print (next(res.results).text)
				speak (next(res.results).text)
			except StopIteration:
				print ("No results")


		elif (" open Microsoft Excel"in query) or ("open ms excel" in query):
			path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
			os.startfile(path)
			speak("OPENING Microsoft EXCEL")


		elif ("Microsoft World" in query) or ("open ms word" in query):
			path="C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
			os.startfile(path)
			speak("Opening ms word")


		elif "open powerpoint" in query or "open ppt" in query:
			path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
			os.startfile(path)
			speak("opening ppt")

		elif "open instagram" in query:
			speak("opening instagram")
			webbrowser.open("instagram.com")


		elif "open Amazon" in query:
			speak("opening amazon")
			webbrowser.open("amazon.in")


		elif "open flipkart" in query:
			speak("opening flipkart")
			webbrowser.open("flipkart.com")
			

		elif "refresh" in query:
			try:
				if "refresh" in query:
					pyautogui.moveTo(1551, 551, 2)
					pyautogui.click(x=1551, y=551, clicks=1, interval=0, button='right')
					pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='left')
					pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='left')
					print("page refreshed successfully!")
				
			except "Exception" as e:
				print("An error occurred while refreshing the page:", e)
		
		elif"SCROLL DOWN" in query:
			pyautogui.scroll(1000)
			speak("Sure, scrolling down now.")

		elif 'open new window' in query:
			pyautogui.hotkey('ctrl', 'n')
			speak("Opening a new window.")        
			
		elif 'open new tab' in query:
			pyautogui.hotkey('ctrl', 't') 
			speak("Opening a new tab.")       
		
		elif 'open incognito window' in query:
			pyautogui.hotkey('ctrl', 'shift', 'n') 
			speak("Opening an incognito window.")       
			
		elif 'minimize this window' in query:
			pyautogui.hotkey('alt', 'space')
			time.sleep(1)
			pyautogui.press('n')
			
			
		elif 'open history' in query:
			pyautogui.hotkey('ctrl', 'h')
			speak("Opening browsing history.")
			
			
		elif 'open downloads' in query:
			pyautogui.hotkey('ctrl', 'j')
			speak("Opening downloads.")
			
			
		elif 'previous tab' in query:
			pyautogui.hotkey('ctrl', 'shift', 'tab')
			speak("Switching to the previous tab.")
			
		elif 'next tab' in query:
			pyautogui.hotkey('ctrl', 'tab')
			speak("Switching to the previous tab.")
		
		elif 'close tab' in query:
			pyautogui.hotkey('ctrl', 'w')
			speak("Closing the current tab.")
		
		elif 'close window' in query:
			pyautogui.hotkey('ctrl', 'shift', 'w')
			speak("Closing this window.")
			
		elif 'clear browsing histroy' in query:
			pyautogui.hotkey('ctrl', 'shift', 'delete')
			speak("Clearing browsing history.")
		
		elif 'close browser' in query:
			os.system("taskkill/f/im Firefox.exe")
			speak("Closing the browser.")

		
		elif'weather' in query:
			speak("Sure, which city would you like to check the weather for?")
			print("Sure, which city would you like to check the weather for?")
			city_name = takeCommand()
			weather_info = get_weather_info(city_name)
			speak(weather_info)
			print(weather_info)


		elif "change system volume" in query:
			speak("What should I set the volume to?")
			volume = takeCommand()
			volume = takeCommand()
			volume = int(volume)
			if volume < 0 or volume > 100:
				speak("Volume should be between 0 and 100")
			else:
				pyautogui.hotkey("win", "ctrl", "v")
				pyautogui.write(str(volume))
				pyautogui.press("enter")
				speak("volume changed")

		elif "play game" in query:
			handle_play_game()

		elif 'create folder' in query:
			speak("Please provide the folder name")
			folder_name = takeCommand()
			create_folder(folder_name)
		
		elif 'open folder' in query:
			speak("Please provide the folder path")
			folder_path = takeCommand()
			open_folder(folder_path)
		
		elif 'search folder' in query:
			speak("Please provide the folder name to search")
			folder_name = takeCommand()
			search_folder(folder_name)
			
		elif 'open file' in query:
			speak("Please provide the file path to open")
			file_path = takeCommand()
			open_file(file_path)
			

# Function to handle various commands based on user input			
def handle_command(command):
    if command == 'open youtube':
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
		
    elif command == 'play game':
        handle_play_game()

    elif command == 'Ask Maya':
        ask_maya()

    elif command == 'calculate':
        speak("What expression would you like to calculate?")
        append_text("What expression would you like to calculate?")
        expression = takeCommand()
        result = calculate_expression(expression)
        speak(f"The answer is {result}")

    elif command == 'Translate':
        handle_translate()

    elif command == 'Cricket Update':
        live_matches = cricket_updates()
        if not live_matches:
            speak("No live matches currently.")
            append_text("No live matches currently.")
        else:
            speak("Here are the live matches:")
            append_text("Here are the live matches:")
            for match in live_matches:
                team1 = match.get("team-1", "Team 1")
                team2 = match.get("team-2", "Team 2")
                score = match.get("score", "Score not available")
                speak(f"{team1} vs {team2}, {score}")

    elif command == 'exit':
        speak("Thanks for giving me your time")
        window.destroy()  # Close the Tkinter window


# Function to start the assistant in a separate thread to check for updates          
def start_assistant():
    Thread(target=check_for_updates).start()

# Function to create GUI buttons for different commands
def create_buttons():
    btn_frame = Frame(window)
    btn_frame.pack(pady=10)

# Dictionary mapping button text to corresponding command functions
    commands = {
    'Open YouTube': lambda: handle_command('open youtube'),
    'Play Game': lambda: handle_command('play game'),
    'Ask Maya': lambda: handle_command('Ask Maya'),
    'Calculate': lambda: handle_command('calculate'),
    'Translate': lambda: handle_command('Translate'),
    'Cricket Update': lambda: handle_command('Cricket Update'),
    'Exit': lambda: handle_command('exit')
}

# Create buttons based on the commands dictionary
    for text, command in commands.items():
        btn = Button(btn_frame, text=text, command=command)
        btn.pack(side=LEFT, padx=10)

# Create a button to start the assistant and create buttons
start_button = Button(window, text="Start Assistant", command=lambda: [create_buttons(), start_assistant()])
start_button.pack(pady=20)

# Create buttons initially
create_buttons()

# Start the GUI event loop
window.mainloop()		