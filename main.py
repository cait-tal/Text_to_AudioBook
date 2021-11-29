import requests
from tkinter import *
from tkinter import filedialog
from playsound import playsound
import docx2txt
import os

#-----------------------------UI Settings----------------------------------------#
LIGHT_BROWN = "#E1BC91"
CHESTNUT_BROWN = "#C19277"
TEAL = "#62959C"
FONT_BUTTON = ("Arial", 16, "bold")
FONT_LABEL = ("Arial", 14, "normal")

#------------------------------API PARAMETERS--------------------------------#
API_KEY = os.environ.get("API_KEY")
RSS_URL = "https://api.voicerss.org/"

PARAMETERS = {
    "key": API_KEY,
    "src": "",
    "hl": "en-us",
    "v": "Mary",
    "c": "WAV",
}


class UI:

    def __init__(self):

        self.screen = Tk()
        self.screen.geometry("800x750")
        self.screen.configure(bg=LIGHT_BROWN)
        self.screen.title("Text to Audiobook Converter")

        self.book_image = PhotoImage(file="images/audio_book.png")
        self.music_image = PhotoImage(file="images/music_note.png")
        self.canvas = Canvas(width=500, height=400, bg=CHESTNUT_BROWN)
        self.canvas.grid(row=0, column=0, padx=150, pady=(100, 20))

        self.bg_img = self.canvas.create_image(250, 200)

        self.button = Button(width=20, height=5, bg=TEAL, font=FONT_BUTTON)
        self.button.grid(row=1, column=0)
        self.label = Label(width=50, height=2, bg=LIGHT_BROWN,
                      font=FONT_LABEL,
                      fg=LIGHT_BROWN,)
        self.label.grid(row=3, column=0)

        self.initial_setup()

        self.screen.resizable(False, False)
        self.screen.mainloop()
    def initial_setup(self):
        self.canvas.itemconfig(self.bg_img, image=self.book_image)
        self.button.config(text="Upload File", command=self.choose_file)
        self.label.config(text="That file type is not supported.\nOnly .txt and .docx can be converted into an audiofile.", fg=LIGHT_BROWN)

    def choose_file(self):
        filename = filedialog.askopenfile(initialdir="/", title="Select File", filetypes=(("Text Files", "*.txt"), ("Word Documents", "*.docx"), ("All Files", "*.*")))
        self.label.configure(fg=LIGHT_BROWN)
        if filename.name[-4:] == "docx":
            text = docx2txt.process(filename.name)
            self.convert_to_audio(text)
        elif filename.name[-3:] == "txt":
            text = filename.readlines()
            self.convert_to_audio(text)
        else:
            self.label.configure(fg="black")

    def convert_to_audio(self, text):
        PARAMETERS["src"] = text
        response = requests.get(url=RSS_URL, params=PARAMETERS)
        if response.status_code == 200:
            self.path = filedialog.asksaveasfilename(title="Save as")
            with open(f"{self.path}.wav", mode="bx") as file:
                file.write(response.content)
            self.canvas.itemconfig(self.bg_img, image=self.music_image)
            self.button.configure(text="Play Audio", command=self.playback_audio)
        else:
            pass

    def playback_audio(self):
        try:
            playsound(f"{self.path}.wav")
        except:
            self.label.config(text="File could not be played at this time.", fg="black")
        finally:
            self.button.configure(text="Convert Another FIle", command=self.initial_setup)




if __name__ == "__main__":
    ui = UI()



