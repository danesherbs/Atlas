import os
import time
import logging
import threading
from tts import say
import speech_recognition as sr


# initialization
r = sr.Recognizer()
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) {%(funcName)s} %(message)s',)
say_t = threading.Thread(name='gTTS', target=say)


# Play programming music
def play_music():
    logging.debug("Starting mpg321")
    os.system("mpg321 %s.mp3 --quiet" % "back_in_black")
    logging.debug("Finished mpg321")


# Stop programming music
def stop_music():
    logging.debug("Killing mpg321")
    os.system("killall mpg321")
    logging.debug("Killed mpg321")


# Speech to text
def listen():
    logging.debug("Listening...")
    with sr.Microphone() as source:  # use the default microphone as the audio source
        audio = r.listen(source)  # listen for the first phrase and extract it into audio data
    logging.debug("Got it! Now recognizing it...")

    try:
        list = r.recognize(audio,True)  # generate a list of possible transcriptions
        logging.debug("Possible transcriptions:")
        for prediction in list:
            logging.debug("    " + prediction["text"] + " (" + str(prediction["confidence"]*100) + "%)")
        logging.debug("You said '%s'" % list[0]["text"])
    except LookupError:  # speech is unintelligible
        logging.debug("Oops! Didn't catch that")
        return None

    return list[0]["text"]


# Listen for particular phrases
def listen_for_phrases():
    secs_inactive = 0
    while(secs_inactive < 10):
        start = time.clock()

        logging.debug("Waiting for phrases:")
        logging.debug("    'Time to program'")
        logging.debug("    'Stop the music'")
        user_said = listen()

        # PHRASE 1
        if user_said == "time to program":
            # say("Let's kick some ass")
            threading.Thread(name='play_music', target=play_music).start()
            logging.debug("'play_music' thread issued")
        
        # PHRASE 2
        if user_said == "stop the music":
            threading.Thread(name='stop_music', target=stop_music).start()
            logging.debug("'stop_music' thread issued")

        end = time.clock()
        secs_inactive = (start-end)/1000


# Await 'Atlas' phrase
def await_commands():
    while(True):
        logging.debug("Waiting for keyword 'Atlas'...")
        if listen() == "Atlas":
            # threading.Thread(name="say", args=["Yes sir?"], target=say).start()
            # time.sleep(2)
            # say("Yes sir?")
            listen_for_phrases()



if __name__ == "__main__":
    await_commands()
    


###############################
logging.debug("END OF PROGRAM")
logging.shutdown()
###############################



