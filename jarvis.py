import sys
import pyttsx3 # python text to speech module (pip install)
import datetime  
import time #built in
import speech_recognition as sr #(pip install)
import wikipedia # (pip install)
import webbrowser #(built in)
import os #opens windows directories (built in)
import random #(built in)
import smtplib #(built in)


mail_list = {"papa":"dasgupta.27@gmail.com", "mamma":"mousumi10.c@gmail.com"}


engine = pyttsx3.init("sapi5") #sapi5 is like an API... windows ki voice hai
voices = engine.getProperty("voices") #List of pyttsx.voice.Voice descriptor objects
#print(voices[0].id) #david select kara
engine.setProperty('voice',voices[0].id) #0 is purush and 1 is mahila



def speak(audio):
    engine.say(audio) 
    engine.runAndWait() 

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Sir!")
    elif hour>=12 and hour<16:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir!")
    
    speak("Jarvis at your service. How may I help you?")

def TakeCommand():    
    #it takes input from mic and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        r.energy_threshold=1000
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language= "en-in")
        print (f"User said: {query}\n")
    except Exception as e:
        # print(e)  # Comment out if you don't want to see the error
         print("Say that again, please")
         return "None"

    
    return query

def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com",587) #modern port for secure SMTP
    server.ehlo()
    server.starttls()
    server.login("jyotikadasgupta@gmail.com","tacmp@123")
    server.sendmail("jyotikadasgupta@gmail.com",to,content)
    server.close()

    

 
if __name__=="__main__": #ye wala part run sirf isi module me hoga
    wishMe()
    while True:
        query = TakeCommand().lower()
        #logic for executing tasks
        if "wikipedia" in query:
            speak("Searching wikipedia, sir")
            query = query.replace("wikipedia","")
            #print(query)
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            print(results)
            speak(results)
        
        elif "open youtube" in query:
            speak("Opening youtube, sir.")
            webbrowser.open("https://www.youtube.com",new=2)
        
        elif "open google" in query:
            speak("Opening google, sir.")
            webbrowser.open_new_tab("https://www.google.co.in")
        
        elif "open amazon" in query:
            speak("Sure! Happy Shopping!")
            webbrowser.open_new_tab("https://www.amazon.in")

        elif "photos" in query:
            pic_dir = "D:\Wallpapers"
            pictures = os.listdir(pic_dir)
            speak("Showing photos, sir.")
            os.startfile(os.path.join(pic_dir,pictures[random.randint(30,400)]))
        
        elif "the time" in query:
            t = datetime.datetime.now().strftime("%H:%M:%S")
            print(t)
            speak (f"Sir, the time right now is {t}.")
        
        elif "visual studio" in query:
            codepath="C:\Program Files\Microsoft VS Code"
            speak("Good luck with coding sir!")
            os.startfile(codepath)

        elif "music" in query or "can you open spotify for me " in query:
            speak("enjoy sir!")
            webbrowser.open_new_tab("https://in.pinterest.com/")
        
        elif "open pinterest" in query or "can you open pinterest for me " in query:
            speak("enjoy sir!")
            webbrowser.open_new_tab("https://open.spotify.com")
        
        

        elif "remind me" in query:      
            query=query.replace("remind me to","")
            print("writing sir")
            speak("writing sir")
            
            with open("C:\\Desktop\\Reminder.txt","w") as f:
                f.write(query)
                f.write("\n")
            
        elif "send email" in query:
            if "mamma" in query or "mama" in query:
                try:
                    speak("What should I write?")
                    content = TakeCommand()
                    to = mail_list.get("mamma")
                    sendEmail(to,content)
                    speak("Mail sent, sir.")
                except Exception as e:
                    print(e)
                    speak("Sorry sir! Unable to send the mail due to some error.")

            elif "papa" in query:
                try:
                    speak("What should I write?")
                    content = TakeCommand()
                    to = mail_list.get("papa")
                    sendEmail(to,content)
                    speak("Mail sent, sir.")
                except Exception as e:
                    print(e)
                    speak("Sorry sir! Unable to send the mail due to some error.")
            
            else:
                try:
                    speak("What should I write?")
                    content = TakeCommand()
                    to = "jyotikadasgupta@gmail.com"
                    sendEmail(to,content)
                    speak("Mail sent, sir.")
                except Exception as e:
                    print(e)
                    speak("Sorry sir! Unable to send the mail due to some error.")

        
        elif any(keyword in query for keyword in ["quit", "exit", "stop", "shut up", "goodbye", "good bye"]):
            speak("Goodbye sir! See you soon.")
            sys.exit()
        
        else:
            speak("Sorry. I don't know that command. Please tell the developer to add this command.")


            
