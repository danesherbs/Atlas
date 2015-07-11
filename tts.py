from gtts import gTTS
import os

def to_file_name(sentence):
    return filter(lambda x: x.isalpha() or x == '_', '_'.join(sentence.split(' ')))

# Says sentence
def say(sentence):
    tts = gTTS(text=sentence, lang='en')
    file_name = to_file_name(sentence)
    tts.save("%s.mp3" % file_name)
    os.system("mpg321 %s.mp3 -quiet" % file_name)
    # print "error"

if __name__ == "__main__":
	say("Hello!")