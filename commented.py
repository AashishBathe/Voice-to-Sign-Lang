# Speech to Text

from tkinter import *  # Graphical package
import speech_recognition as sr
import nltk.stem as nt  # Natural Language Toolkit for Stemming.

r = sr.Recognizer()


def get_audio():
    with open("stopwords.txt") as file:  # Opening stopwords file to get string
        string = file.read()
    stop_words = string.split(',')  # Getting stopwords list from string (NLTK stopwords)
    try:
        p_stem = nt.PorterStemmer()
        l_stem = nt.LancasterStemmer()  # Porter and Lancaster Stemmer objects

        with sr.Microphone() as source:  # Using microphone of device
            r.adjust_for_ambient_noise(source, duration=0)
            print("Say something!")
            audio = r.listen(source)
            my_text = r.recognize_google(audio)  # Google speech to text API
            my_text = my_text.lower()
            text_list = my_text.split(" ") # Split our text into list
            stem_list = [] # Empty list to append stemmed keywords.

            word_list = [word for word in text_list if word not in stop_words]  # Removing useless words
            for word in word_list: # Applying Stemming Algorithms
                if p_stem.stem(word) == word:
                    stem_list.append(l_stem.stem(word))
                else:
                    stem_list.append(p_stem.stem(word))

            print(stem_list)
            print("Did you say '" + my_text + "'")

    except sr.RequestError:  # If no internet, then request error. So use CMU Sphinx.
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


window = Tk() # Tkinter main class Tk()
window.title("SPEECH TO SIGN LANGUAGE CONVERTER")  # Heading of window
window.minsize(width=700, height=700)
mic = PhotoImage(file="new_mic.png")  # Image to be used in button has to be photoimage
small_mic = mic.subsample(1, 1)
button_1 = Button(image=small_mic, bg="white", borderwidth=0.5, command=get_audio)
button_1.place(x=220, y=200) # Placing button on window
# button_2 = Button(text="X", bg="white", borderwidth=0.5, command=cancel, width=15, height=7)
# button_2.place(x=300, y=300)

window.mainloop()
