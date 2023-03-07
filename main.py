# Speech to Sign Language Converter

from tkinter import *
import speech_recognition as sr
import nltk.stem as nt
from PIL import ImageTk, Image
from dictionary import dict_of_words

FONT = ("Times New Roman", 20, "normal")
FONT2 = ("Times New Roman", 25, "bold")
r = sr.Recognizer()
count = 0


def get_audio():
    global count
    count = 0
    with open("stopwords.txt") as file:
        string = file.read()
    stop_words = string.split(',')
    try:
        p_stem = nt.PorterStemmer()
        l_stem = nt.LancasterStemmer()

        with sr.Microphone() as source:
            # r.adjust_for_ambient_noise(source, duration=0)
            # print("Say something!")
            audio = r.listen(source)
            my_text = r.recognize_google(audio)
            my_text = my_text.lower()
            text_list = my_text.split(" ")
            stem_list = []

            word_list = [word for word in text_list if word not in stop_words]
            for word in word_list:
                if p_stem.stem(word) == word:
                    stem_list.append(l_stem.stem(word))
                else:
                    stem_list.append(p_stem.stem(word))
            return [my_text, stem_list]

    except sr.RequestError:

        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            print("Did you say '" + r.recognize_sphinx(audio) + "'")

        except sr.UnknownValueError:
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
        word_label.config(text=word_list[count].capitalize())
        canvas.itemconfig(image_of_canvas, image=image_list[count])

    def go_prev():
        global count
        count -= 1
        if count == 0:
            left_button.config(state="disabled")
        right_button.config(state="active")
        word_label.config(text=word_list[count])
        canvas.itemconfig(image_of_canvas, image=image_list[count])

    def closer():
        window.destroy()

    for widgets in mainframe.winfo_children():
        widgets.destroy()
    user_input = get_audio()
    my_text = user_input[0]
    my_text = my_text.capitalize()
    keywords = user_input[1]
    word_list = [keyword for keyword in keywords if keyword in data_dict]
    image_list = [data_dict[keyword] for keyword in keywords if keyword in data_dict]
    canvas = Canvas(mainframe, width=400, height=400, bg="#C1C1FF", borderwidth=0, highlightthickness=0)
    try:
        image_of_canvas = canvas.create_image(200, 200, image=image_list[count])
        word_label = Label(mainframe, text=word_list[count].capitalize(), font=FONT2, bg="#C1C1FF", fg="#22228B")
    except IndexError:
        word_label = Label(mainframe, text="ERROR!!", font=FONT2, bg="#C1C1FF", fg='#22228B')
        image_of_canvas = canvas.create_image(200, 200, image=error)
    canvas.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
    word_label.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    left_button = Button(mainframe, command=go_prev, image=left_arrow, bg="white", borderwidth=0, state="disabled")
    left_button.grid(row=0, column=0, padx=10, pady=10)
    right_button = Button(mainframe, command=go_next, image=right_arrow, bg="white", borderwidth=0)
    right_button.grid(row=0, column=3, padx=10, pady=10)
    try:
        image_list[count+1]
        right_button.config(state="active")
    except IndexError:
        right_button.config(state="disabled")

    textbox = Text(mainframe, font=FONT, padx=20, pady=20, width=3, height=3)
    textbox.insert(END, "Say Something")

    textbox.delete("1.0", END)
    textbox.insert(END, my_text)
    textbox.grid(row=2, column=0, columnspan=4, sticky="EW")
    repeat_button = Button(mainframe, text="Try Again.", command=window_reset)
    repeat_button.config(padx=5, pady=5)
    repeat_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="EW")
    close_button = Button(mainframe, text="Exit", command=closer)
    close_button.config(padx=5, pady=5)
    close_button.grid(row=3, column=2,columnspan=2, padx=20, pady=20, sticky="EW")


new_size = (300, 300)
window = Tk()
window.title("SPEECH TO SIGN LANGUAGE CONVERTER")
window.minsize(width=750, height=750)
window.config(padx=20, pady=20, bg="#C1C1FF")
mainframe = Frame(window, width=700, height=700, bg="#C1C1FF")
mainframe.grid(row=0, column=0, rowspan=4, columnspan=4)
left_arrow = PhotoImage(file="left_arrow_final.png").subsample(2, 2)
right_arrow = PhotoImage(file="right_arrow_final.png").subsample(2, 2)
error = ImageTk.PhotoImage(Image.open("error.jfif"))
mic = ImageTk.PhotoImage(Image.open("new_mic.png"))
data_dict = {keyword: ImageTk.PhotoImage(Image.open(image)) for keyword, image in dict_of_words.items()}

window_reset()
window.mainloop()

# Eat, sleep, travel and do it again
