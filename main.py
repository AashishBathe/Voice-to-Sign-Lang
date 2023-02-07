# Speech to Text

from tkinter import *
import speech_recognition as sr
# import pyttsx3
import nltk.stem as nt

r = sr.Recognizer()

# def speaktext(command):
#     # Initialize the engine
#     engine = pyttsx3.init()
#     engine.say(command)
#     engine.runAndWait()


def get_audio():

    # string = "i, me, my, myself, we, our, ours, ourselves, you, your, yours, yourself, yourselves, he,him,his," \
    #          "himself,she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom," \
    #          "this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,a,an,the," \
    #          "and,but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during," \
    #          "before,after,above,below,to,from,up,down,in,out,on,off,over,under,again,further,then,once,here,there" \
    #          ",when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than," \
    #          "too,very,s,t,can,will,just,don,should,now"

    with open("stopwords.txt") as file:
        string = file.read()
    stop_words = string.split(',')
    try:
        p_stem = nt.PorterStemmer()
        l_stem = nt.LancasterStemmer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0)
            print("Say something!")
            audio = r.listen(source)
            my_text = r.recognize_google(audio)
            my_text = my_text.lower()
            text_list = my_text.split(" ")
            stem_list = []

            # lemma = wordnet.WordNetLemmatizer()
            # word_list = [lemma.lemmatize(word) for word in text_list if word not in stop_words]
            word_list = [word for word in text_list if word not in stop_words]
            for word in word_list:
                if p_stem.stem(word) == word:
                    stem_list.append(l_stem.stem(word))
                else:
                    stem_list.append(p_stem.stem(word))

            print(stem_list)
            print("Did you say '" + my_text + "'")

    except sr.RequestError:
        # for phrase in LiveSpeech():
        #     # here the result is stored in phrase which
        #     # ultimately displays all the words recognized
        #     print(phrase)
        # else:
        #     print("Sorry! could not recognize what you said")

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0)
            print("Say something!")
            audio = r.listen(source)

        try:
            print("Did you say '" + r.recognize_sphinx(audio) + "'")

        except sr.UnknownValueError:
            # If the voice is unclear
            print("Could not understand")

        except sr.RequestError as e:
            print("Error; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")


def window_reset():
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    button_1 = Button(image=small_mic, bg="white", borderwidth=0.5, command=get_audio)
    button_1.grid(row=0, column=0)
    button_1.grid_rowconfigure(1, weight=1)
    button_1.grid_columnconfigure(1, weight=1)


def window2():
    canvas = Canvas(width=400, height=400)
    

    window_reset()


window = Tk()
window.title("SPEECH TO SIGN LANGUAGE CONVERTER")
window.minsize(width=700, height=700)
window.config(padx=20, pady=20)
mic = PhotoImage(file="new_mic.png")
small_mic = mic.subsample(1, 1)
window_reset()

window.mainloop()