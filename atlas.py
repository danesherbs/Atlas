import os
import sys
import time
import logging
import threading
from tts import say
import speech_recognition as sr

# Print ATLAS
ATLAS = open('ATLAS.txt','r')
for line in ATLAS:
    print line,
ATLAS.close()

# Initialization
r = sr.Recognizer()
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) {%(funcName)s} %(message)s',)
say_t = threading.Thread(name='gTTS', target=say)
phrases = ["time to program", "stop the music", "power off"]

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
    MAX_WAIT = 5  # seconds
    logging.debug("Listening...")
    with sr.Microphone() as source:  # use the default microphone as the audio source
        try:
            audio = r.listen(source, MAX_WAIT)  # listen for the first phrase and extract it into audio data
        except:  # TODO: catch TimeoutError, a type of OSError
            logging.debug("Timeout exception")
            return None
        
    try:
        logging.debug("Got it! Now recognizing it...")
        list = r.recognize(audio,True)  # generate a list of possible transcriptions
        logging.debug("Possible transcriptions:")
        for prediction in list:
            logging.debug("    " + prediction["text"] + " (" + str(prediction["confidence"]*100) + "%)")
        logging.debug("You said '%s'" % list[0]["text"])
    except LookupError:  # speech is unintelligible
        logging.debug("Oops! Didn't catch that")
        return False

    return list[0]["text"]


# Listen for particular phrases
def listen_for_phrases(timeouts=0):
    while(timeouts < 5):

        logging.debug("Waiting for phrases:")
        for phrase in phrases:
            logging.debug("    '%s'" % phrase)

        # Listen for phrase
        user_said = listen()
        if user_said is None:
            timeouts += 1  # record timeout

        # PHRASE
        if user_said == "time to program":
            threading.Thread(name='play_music', target=play_music).start()
            logging.debug("'play_music' thread issued")
        
        # PHRASE
        elif user_said == "stop the music":
            threading.Thread(name='stop_music', target=stop_music).start()
            logging.debug("'stop_music' thread issued")

        # PHRASE
        elif user_said == "power off":
            # Print ATLAS
            bye = open('Goodbye.txt','r')
            for line in bye:
                print line,
            bye.close()
            sys.exit(-1)

        else:
            continue

        timeouts = 0  # reset timeouts if received response


# Await 'Atlas' phrase
def await_commands():
    while(True):
        logging.debug("Waiting for keyword 'Atlas'...")
        if listen() == "Atlas":
            # threading.Thread(name="say", args=["Yes?"], target=say).start()
            # time.sleep(2)
            # say("Yes?")
            listen_for_phrases()


##########################
#          MAIN          #
##########################
if __name__ == "__main__":
    
    await_commands()
    
    ###############################
    logging.debug("END OF PROGRAM")
    logging.shutdown()
    ###############################



