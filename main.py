# Speech to Text

from tkinter import *
import speech_recognition as sr
# import pyttsx3
import nltk.stem as nt
from PIL import ImageTk, Image
from dictionary import dict_of_words

FONT = ("Times New Roman", 20, "normal")
r = sr.Recognizer()
count = 0
# def speaktext(command):
#     # Initialize the engine
#     engine = pyttsx3.init()
#     engine.say(command)
#     engine.runAndWait()


def get_audio():

    # string = "i, me, my, myself, we, our, ours, ourselves, you, your, yours, yourself, yourselves, he,him,his,
    # " \ "himself,she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom,
    # " \ "this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,a,an,the,
    # " \ "and,but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during,
    # " \ "before,after,above,below,to,from,up,down,in,out,on,off,over,under,again,further,then,once,here,there" \ ",
    # when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than," \ "too,
    # very,s,t,can,will,just,don,should,now"

    with open("stopwords.txt") as file:
        string = file.read()
    stop_words = string.split(',')
    try:
        p_stem = nt.PorterStemmer()
        l_stem = nt.LancasterStemmer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0)
            print("Say something!")
            # label2 = Label(text="Say Something!")
            # label2.grid(row=1, column=0)
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
            return [my_text, stem_list]

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
        return ["Audio Not Recognized. Please try again.", []]


def window_reset():
    for widgets in mainframe.winfo_children():
        widgets.destroy()
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    button_1 = Button(mainframe, image=mic, bg="white", borderwidth=0.5, command=output_window)
    button_1.grid(row=0, column=0)
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(1, weight=1)


def output_window():
    global count

    def go_next():
        global count
        count += 1
        try:
            image_list[count+1]
            right_button.config(state="active")
        except IndexError:
            right_button.config(state="disabled")
        left_button.config(state="active")
        canvas.itemconfig(image_of_canvas, image=image_list[count])

    def go_prev():
        global count
        count -= 1
        if count == 0:
            left_button.config(state="disabled")
        right_button.config(state="active")
        canvas.itemconfig(image_of_canvas, image=image_list[count])

    for widgets in mainframe.winfo_children():
        widgets.destroy()
    user_input = get_audio()
    my_text = user_input[0]
    my_text = my_text.capitalize()
    keywords = user_input[1]
    image_list = [data_dict[keyword] for keyword in keywords if keyword in data_dict]

    canvas = Canvas(mainframe, width=400, height=400)
    try:
        image_of_canvas = canvas.create_image(200, 200, image=image_list[count])
    except IndexError:
        image_of_canvas = canvas.create_image(200, 200, image=error)
    canvas.grid(row=0, column=1, padx=10, pady=10)
    left_button = Button(mainframe, command=go_prev, image=left_arrow, bg="white", borderwidth=0, state="disabled")
    left_button.grid(row=0, column=0, padx=10, pady=10)
    right_button = Button(mainframe, command=go_next, image=right_arrow, bg="white", borderwidth=0)
    right_button.grid(row=0, column=2, padx=10, pady=10)
    try:
        image_list[count+1]
        right_button.config(state="active")
    except IndexError:
        right_button.config(state="disabled")
    textbox = Text(mainframe, font=FONT, padx=20, pady=20, width=3, height=3)
    textbox.insert(END, "Say Something")

    # for word in keywords if word in dict_to_image:
    #     image_list.append(dict_to_image[word])

    textbox.delete("1.0", END)
    textbox.insert(END, my_text)
    textbox.grid(row=1, column=0, columnspan=3, sticky="EW")
    repeat_button = Button(mainframe, text="Try Again.", command=window_reset)
    repeat_button.config(padx=5, pady=5)
    repeat_button.grid(row=2, column=1, padx=20, pady=20, sticky="EW")


new_size = (300, 300)
window = Tk()
window.title("SPEECH TO SIGN LANGUAGE CONVERTER")
window.minsize(width=750, height=750)
window.config(padx=20, pady=20)
mainframe = Frame(window, width=700, height=700)
mainframe.grid(row=0, column=0, rowspan=4, columnspan=4)
mic = ImageTk.PhotoImage(Image.open("new_mic.png"))
cat = ImageTk.PhotoImage(Image.open("cat.jpg"))
nice_cat = ImageTk.PhotoImage(Image.open("small_nice_cat.png"))
# nice_cat = ImageTk.PhotoImage(file=Image.open("nice_cat.jpg").resize(new_size))
# small_mic = mic.subsample(1, 1)
left_arrow = PhotoImage(file="left_arrow_final.png").subsample(2, 2)
right_arrow = PhotoImage(file="right_arrow_final.png").subsample(2, 2)
error = ImageTk.PhotoImage(Image.open("error.jfif"))

data_dict = {keyword: ImageTk.PhotoImage(Image.open(image)) for keyword, image in dict_of_words.items()}

window_reset()
window.mainloop()
