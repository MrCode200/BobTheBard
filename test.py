import threading
import time
from threading import *
from tkinter import *
import customtkinter as ctk
import ttkbootstrap as ttk
from PIL import Image
from ttkbootstrap.toast import ToastNotification

import json

from gtts import gTTS
import speech_recognition as sr
import pydub
from pydub.playback import play
from pydub.effects import speedup
import winsound

import pywhatkit as pwk
import clipboard
import AppOpener
import webbrowser as web
import wikipedia

from bardapi import Bard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

token = "fwgAR8peqO1Zm0j2OBmL-jx0dOOc8nxJJXzH5T6X0OOdcWU4uZBCfIv5WJRrzjWH3uLSuw."
toastActive = 1
popupActive = 1
askBardHotword = ""
youtubeHotword = ""
popupHotword = ""
searchHotword = ""
findInformationHotword = ""
copyPromptHotword = ""
openAppHotword = ""
closeAppHotword = ""
killBobHotword = ""

winMsgDur = 1

recorder = sr.Recognizer()

bobActive = False
bobActiveAssistant = False
duration = 0

"""class AnimatedGif(ctk.CTkButton):
    def __init__(self, master):
        # open the GIF and create a cycle iterator
        file_path = Path(__file__).parent / "animations/hudUiGif.gif"
        with Image.open(file_path) as im:
            # create a sequence
            sequence = ImageSequence.Iterator(im)
            images = [ImageTk.PhotoImage(s) for s in sequence]
            for i in images:
                self.image_cycle = cycle(images)

            # length of each frame
                self.framerate = im.info["duration"]

                self.img_container = object.configure(image=next(self.image_cycle))
                self.after(self.framerate, self.next_frame)

    def next_frame(self):
        self.img_container.configure(image=next(self.image_cycle))
        self.after(self.framerate, self.next_frame)"""


# Loads all values from the settings.json to their corresponding values
def setup():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    settings = settings["custom"]

    global token, toastActive, popupActive, popupWordCount, activateBobHotword, askBardHotword, youtubeHotword, popupHotword, searchHotword, findInformationHotword, copyPromptHotword, openAppHotword, closeAppHotword, killBobHotword

    token = settings["states"]["token"]
    toastActive = settings["states"]["toastActive"]
    popupActive = settings["states"]["popupActive"]
    popupWordCount = settings["states"]["popupWordCount"]

    activateBobHotword = settings["hotwords"]["activateBobHotword"]
    askBardHotword = settings["hotwords"]["askBardHotword"]
    youtubeHotword = settings["hotwords"]["youtubeHotword"]
    popupHotword = settings["hotwords"]["popupHotword"]
    searchHotword = settings["hotwords"]["searchHotword"]
    findInformationHotword = settings["hotwords"]["findInformationHotword"]
    copyPromptHotword = settings["hotwords"]["copyPromptHotword"]
    openAppHotword = settings["hotwords"]["openAppHotword"]
    closeAppHotword = settings["hotwords"]["closeAppHotword"]
    killBobHotword = settings["hotwords"]["killBobHotword"]


# the gui of Bob
# if you want to edit the gui ask me for good websites where you can see what is available
def bobs_skin():
    root = ttk.Window(themename="darkly")
    root.title("Bob the Bard")
    root.geometry("900x450")

    def notification(title, text):
        if toastActive:
            toast = ToastNotification(
                title=title,
                message=text,
                duration=2000,
                bootstyle="dark"
            )
            toast.show_toast()

    # the setting GUI
    def popup_change_settings():
        settingsWindow = ttk.Window()
        settingsWindow.title("Settings")
        settingsWindow.geometry("600x930+650+0")
        settingsWindow.resizable(False, False)

        def sliderpopupWordCount_change(event=None, init=False):
            if init:
                sliderpopupWordCount.set(popupWordCount)
            labelpopupWordCountValue.configure(text=str(sliderpopupWordCount.get()))

        def sliderSettingsPopup_change(event=None, init=False):
            if init:
                sliderSettingsPopup.set(popupActive)
            if sliderSettingsPopup.get() == 0:
                labelPopupInfo.configure(text="Popup disabled", text_color="red")
            elif sliderSettingsPopup.get() == 1:
                labelPopupInfo.configure(text="Popup active when over " + str(popupWordCount) + " Words in prompt",
                                         text_color="yellow")
            else:
                labelPopupInfo.configure(text="Popup always active", text_color="green")

        def switchToast_change(init=False):
            if not init:
                if switchToast.get() == 1:
                    switchToast.configure(text="On", text_color="green")
                else:
                    switchToast.configure(text="Off", text_color="red")
            else:
                if toastActive == 1:
                    switchToast.configure(text="On", text_color="green")
                    switchToast.select()
                else:
                    switchToast.configure(text="Off", text_color="red")
                    switchToast.deselect()

        def loadSetting():
            entryToken.insert(index=0, string=token)
            switchToast_change(True)
            sliderSettingsPopup_change(init=True)
            sliderpopupWordCount_change(init=True)

            entryActivateBobHotword.insert(index=0, string=activateBobHotword)
            entryAskBardHotword.insert(index=0, string=askBardHotword)
            entryYoutubeHotword.insert(index=0, string=youtubeHotword)
            entryPopupHotword.insert(index=0, string=popupHotword)
            entrySearchHotword.insert(index=0, string=searchHotword)
            entryFindInformationHotword.insert(index=0, string=findInformationHotword)
            entryCopyPromptHotword.insert(index=0, string=copyPromptHotword)
            entryOpenAppHotword.insert(index=0, string=openAppHotword)
            entryCloseAppHotword.insert(index=0, string=closeAppHotword)
            entryKillBobHotword.insert(index=0, string=killBobHotword)

        def reset():
            with open('settings.json', "r+") as f:
                data = json.load(f)

            data["custom"] = data["default"]

            with open("settings.json", "w") as jsonFile:
                json.dump(data, jsonFile, indent=4)

            setup()

            entryToken.delete(0, END)

            entryActivateBobHotword.delete(0, END)
            entryAskBardHotword.delete(0, END)
            entryYoutubeHotword.delete(0, END)
            entryPopupHotword.delete(0, END)
            entrySearchHotword.delete(0, END)
            entryFindInformationHotword.delete(0, END)
            entryCopyPromptHotword.delete(0, END)
            entryOpenAppHotword.delete(0, END)
            entryCloseAppHotword.delete(0, END)
            entryKillBobHotword.delete(0, END)

            loadSetting()

        def save():
            with open('settings.json', "r+") as f:
                data = json.load(f)

            data["custom"]["states"]["token"] = entryToken.get().lower()
            data["custom"]["states"]["toastActive"] = switchToast.get()
            data["custom"]["states"]["popupActive"] = sliderSettingsPopup.get()
            data["custom"]["states"]["popupWordCount"] = sliderpopupWordCount.get()

            data["custom"]["hotwords"]["activateBobHotword"] = entryActivateBobHotword.get().lower()
            data["custom"]["hotwords"]["askBardHotword"] = entryAskBardHotword.get().lower()
            data["custom"]["hotwords"]["youtubeHotword"] = entryYoutubeHotword.get().lower()
            data["custom"]["hotwords"]["popupHotword"] = entryPopupHotword.get().lower()
            data["custom"]["hotwords"]["searchHotword"] = entrySearchHotword.get().lower()
            data["custom"]["hotwords"]["findInformationHotword"] = entryFindInformationHotword.get().lower()
            data["custom"]["hotwords"]["copyPromptHotword"] = entryCopyPromptHotword.get().lower()
            data["custom"]["hotwords"]["openAppHotword"] = entryOpenAppHotword.get().lower()
            data["custom"]["hotwords"]["closeAppHotword"] = entryCloseAppHotword.get().lower()
            data["custom"]["hotwords"]["killBobHotword"] = entryKillBobHotword.get().lower()

            with open("settings.json", "w") as jsonFile:
                json.dump(data, jsonFile, indent=4)

            setup()

        frameSettingsTitleState = ctk.CTkFrame(master=settingsWindow)
        frameSettingsTitleState.pack(pady=6, padx=6, fill="both")
        labelTitleState = ctk.CTkLabel(master=frameSettingsTitleState, text="States", font=("Terminal", 24))
        labelTitleState.pack(pady=6, padx=6)

        frameSettingsToken = ctk.CTkFrame(master=frameSettingsTitleState)
        frameSettingsToken.pack(pady=6, padx=6, fill="both")
        labelToken = ctk.CTkLabel(master=frameSettingsToken, text="Token: ", font=("Terminal", 19))
        labelToken.pack(pady=6, padx=6, side="left")
        entryToken = ctk.CTkEntry(master=frameSettingsToken, placeholder_text="Not Loaded", width=300,
                                  font=("Terminal", 19))
        entryToken.pack(pady=6, padx=6, side="right")

        frameSettingsToast = ctk.CTkFrame(master=frameSettingsTitleState, height=400, width=450)
        frameSettingsToast.pack(pady=6, padx=6, fill="both")
        labelToast = ctk.CTkLabel(master=frameSettingsToast, text="Windows Notification: ",
                                  font=("Terminal", 19))
        labelToast.pack(pady=6, padx=6, side="left")
        switchToast = ctk.CTkSwitch(master=frameSettingsToast, font=("Terminal", 19), text="Not Loaded",
                                    text_color="red", fg_color="red", progress_color="green",
                                    command=switchToast_change)
        switchToast.pack(pady=6, padx=6)

        frameSettingsPopup = ctk.CTkFrame(master=frameSettingsTitleState, height=400, width=450)
        frameSettingsPopup.pack(pady=6, padx=6, fill="both")
        frameSettingsPopupMain = ctk.CTkFrame(master=frameSettingsPopup, height=400, width=450, fg_color="transparent")
        frameSettingsPopupMain.pack(pady=6, padx=6, fill="both")
        labelPopup = ctk.CTkLabel(master=frameSettingsPopupMain, text="Popup Text: ", font=("Terminal", 19))
        labelPopup.pack(pady=6, padx=6, side="left")
        sliderSettingsPopup = ctk.CTkSlider(master=frameSettingsPopupMain, from_=0, to=2, number_of_steps=2,
                                            command=sliderSettingsPopup_change)
        sliderSettingsPopup.pack(pady=6, padx=6, side="right")
        frameSettingsPopupInfo = ctk.CTkFrame(master=frameSettingsPopup, height=400, width=450, fg_color="transparent")
        frameSettingsPopupInfo.pack(pady=6, padx=6, fill="both")
        labelPopupInfo = ctk.CTkLabel(master=frameSettingsPopupInfo, text="Error: couldn't run function",
                                      font=("Terminal", 19))
        labelPopupInfo.pack(pady=6, padx=6, side="left")

        frameSettingspopupWordCount = ctk.CTkFrame(master=frameSettingsTitleState)
        frameSettingspopupWordCount.pack(pady=6, padx=6, fill="both")
        labelpopupWordCount = ctk.CTkLabel(master=frameSettingspopupWordCount, text="Popup Word Count: ",
                                           font=("Terminal", 19))
        labelpopupWordCount.pack(pady=6, padx=6, side="left")
        sliderpopupWordCount = ctk.CTkSlider(frameSettingspopupWordCount, from_=0, to=500, number_of_steps=50,
                                             command=sliderpopupWordCount_change)
        sliderpopupWordCount.pack(pady=6, padx=6, side="right")
        labelpopupWordCountValue = ctk.CTkLabel(master=frameSettingspopupWordCount,
                                                text="Not Loaded", font=("Terminal", 19))
        labelpopupWordCountValue.pack(pady=6, padx=6, side="left")

        frameSettingsTitleHotword = ctk.CTkFrame(master=settingsWindow)
        frameSettingsTitleHotword.pack(pady=[0, 6], padx=6, fill="both")
        labelTitleHotwords = ctk.CTkLabel(master=frameSettingsTitleHotword, text="Hotwords",
                                          font=("Arial Rounded MT", 24))
        labelTitleHotwords.pack(pady=6, padx=6)

        frameSettingsActivateBobHotword = ctk.CTkFrame(master=frameSettingsTitleHotword)
        frameSettingsActivateBobHotword.pack(pady=6, padx=6, fill="both")
        labelActivateBobHotword = ctk.CTkLabel(master=frameSettingsActivateBobHotword, text="Activat Bob: ",
                                               font=("Terminal", 19))
        labelActivateBobHotword.pack(pady=6, padx=6, side="left")
        entryActivateBobHotword = ctk.CTkEntry(master=frameSettingsActivateBobHotword,
                                               placeholder_text="Not Loaded", width=300, font=("Terminal", 19))
        entryActivateBobHotword.pack(pady=6, padx=6, side="right")

        frameSettingsAskBardHotword = ctk.CTkFrame(master=frameSettingsTitleHotword)
        frameSettingsAskBardHotword.pack(pady=6, padx=6, fill="both")
        labelAskBardHotword = ctk.CTkLabel(master=frameSettingsAskBardHotword, text="Ask Bard: ",
                                           font=("Terminal", 19))
        labelAskBardHotword.pack(pady=6, padx=6, side="left")
        entryAskBardHotword = ctk.CTkEntry(master=frameSettingsAskBardHotword, placeholder_text="Not Loaded", width=300,
                                           font=("Terminal", 19))
        entryAskBardHotword.pack(pady=6, padx=6, side="right")

        frameSettingsYoutubeHotword = ctk.CTkFrame(master=frameSettingsTitleHotword)
        frameSettingsYoutubeHotword.pack(pady=6, padx=6, fill="both")
        labelYoutubeHotword = ctk.CTkLabel(master=frameSettingsYoutubeHotword, text="Find in Youtube: ",
                                           font=("Terminal", 19))
        labelYoutubeHotword.pack(pady=6, padx=6, side="left")
        entryYoutubeHotword = ctk.CTkEntry(master=frameSettingsYoutubeHotword, placeholder_text="Not Loaded",
                                           width=300, font=("Terminal", 19))
        entryYoutubeHotword.pack(pady=6, padx=6, side="right")

        frameSettingsPopupHotword = ctk.CTkFrame(master=frameSettingsTitleHotword)
        frameSettingsPopupHotword.pack(pady=6, padx=6, fill="both")
        labelPopupHotword = ctk.CTkLabel(master=frameSettingsPopupHotword, text="Change popup State: ",
                                         font=("Terminal", 19))
        labelPopupHotword.pack(pady=6, padx=6, side="left")
        entryPopupHotword = ctk.CTkEntry(master=frameSettingsPopupHotword, placeholder_text="Not Loaded", width=300,
                                         font=("Terminal", 19))
        entryPopupHotword.pack(pady=6, padx=6, side="right")

        frameSettingsSearchHotword = ctk.CTkFrame(master=frameSettingsTitleHotword)
        frameSettingsSearchHotword.pack(pady=6, padx=6, fill="both")
        labelSearchHotword = ctk.CTkLabel(master=frameSettingsSearchHotword, text="Search in web: ",
                                          font=("Terminal", 19))
        labelSearchHotword.pack(pady=6, padx=6, side="left")
        entrySearchHotword = ctk.CTkEntry(master=frameSettingsSearchHotword, placeholder_text="Not Loaded", width=300,
                                          font=("Terminal", 19))
        entrySearchHotword.pack(pady=6, padx=6, side="right")

        frameSettingsFindInformationHotword = ctk.CTkFrame(master=frameSettingsTitleHotword)
        frameSettingsFindInformationHotword.pack(pady=6, padx=6, fill="both")
        labelFindInformationHotword = ctk.CTkLabel(master=frameSettingsFindInformationHotword,
                                                   text="Find Information: ", font=("Terminal", 19))
        labelFindInformationHotword.pack(pady=6, padx=6, side="left")
        entryFindInformationHotword = ctk.CTkEntry(master=frameSettingsFindInformationHotword,
                                                   placeholder_text="Not Loaded", width=300, font=("Terminal", 19))
        entryFindInformationHotword.pack(pady=6, padx=6, side="right")

        frameSettingsCopyPromptHotword = ctk.CTkFrame(master=frameSettingsTitleHotword)
        frameSettingsCopyPromptHotword.pack(pady=6, padx=6, fill="both")
        labelCopyPromptHotword = ctk.CTkLabel(master=frameSettingsCopyPromptHotword, text="Copy Prompt: ",
                                              font=("Terminal", 19))
        labelCopyPromptHotword.pack(pady=6, padx=6, side="left")
        entryCopyPromptHotword = ctk.CTkEntry(master=frameSettingsCopyPromptHotword, placeholder_text="Not Loaded",
                                              width=300, font=("Terminal", 19))
        entryCopyPromptHotword.pack(pady=6, padx=6, side="right")

        frameSettingsOpenAppHotword = ctk.CTkFrame(master=frameSettingsTitleHotword)
        frameSettingsOpenAppHotword.pack(pady=6, padx=6, fill="both")
        labelOpenAppHotword = ctk.CTkLabel(master=frameSettingsOpenAppHotword, text="Open App: ",
                                           font=("Terminal", 19))
        labelOpenAppHotword.pack(pady=6, padx=6, side="left")
        entryOpenAppHotword = ctk.CTkEntry(master=frameSettingsOpenAppHotword, placeholder_text="Not Loaded",
                                           width=300, font=("Terminal", 19))
        entryOpenAppHotword.pack(pady=6, padx=6, side="right")

        frameSettingsCloseAppHotword = ctk.CTkFrame(master=frameSettingsTitleHotword)
        frameSettingsCloseAppHotword.pack(pady=6, padx=6, fill="both")
        labelCloseAppHotword = ctk.CTkLabel(master=frameSettingsCloseAppHotword, text="Close App: ",
                                            font=("Terminal", 19))
        labelCloseAppHotword.pack(pady=6, padx=6, side="left")
        entryCloseAppHotword = ctk.CTkEntry(master=frameSettingsCloseAppHotword, placeholder_text="Not Loaded",
                                            width=300, font=("Terminal", 19))
        entryCloseAppHotword.pack(pady=6, padx=6, side="right")

        frameSettingsKillBobHotword = ctk.CTkFrame(master=frameSettingsTitleHotword)
        frameSettingsKillBobHotword.pack(pady=6, padx=6, fill="both")
        labelKillBobHotword = ctk.CTkLabel(master=frameSettingsKillBobHotword, text="Terminate App: ",
                                           font=("Terminal", 19))
        labelKillBobHotword.pack(pady=6, padx=6, side="left")
        entryKillBobHotword = ctk.CTkEntry(master=frameSettingsKillBobHotword, placeholder_text="Not Loaded",
                                           width=300, font=("Terminal", 19))
        entryKillBobHotword.pack(pady=6, padx=6, side="right")

        btnSave = ctk.CTkButton(master=frameSettingsTitleHotword, text="Save", command=save)
        btnSave.pack(pady=6, padx=6, side="left", fill="x", expand=True)
        btnReset = ctk.CTkButton(master=frameSettingsTitleHotword, text="Reset", command=reset)
        btnReset.pack(pady=6, padx=6, side="left", fill="x", expand=True)
        btnClose = ctk.CTkButton(master=frameSettingsTitleHotword, text="Close", command=settingsWindow.destroy)
        btnClose.pack(pady=6, padx=6, side="right", fill="x", expand=True)

        switchToast_change(True)
        sliderSettingsPopup_change(init=True)
        sliderpopupWordCount_change()
        loadSetting()
        settingsWindow.mainloop()

    # just for fun
    def popup_cookies():
        infoWindow = ttk.Window()
        infoWindow.title("Cookies")
        # infoWindow.geometry("600x200")
        infoWindow.resizable(False, False)

        labelData = ctk.CTkLabel(master=infoWindow, text="To continue using Bob you have to ACCEPT our Cookies")
        labelData.pack(side="top", padx=10, pady=[10, 0], expand=True)

        linkBtn = ctk.CTkButton(master=infoWindow, text="Data protection", fg_color="transparent",
                                bg_color="transparent", text_color="#add8e6", width=40)
        linkBtn.bind("<Button-1>", lambda event: open_link())
        linkBtn.pack(anchor="w", padx=5)

        btnClose = ctk.CTkButton(master=infoWindow, text="ACCEPT ALL", height=20)
        # btnClose.bind("<Button-1>", lambda event: progress_bar())
        btnClose.bind("<Button-1>", lambda event: infoWindow.destroy())
        btnClose.pack(side="right", padx=10, pady=10, expand=True)

        btnClose = ctk.CTkButton(master=infoWindow, text="close", height=20)
        btnClose.bind("<Button-1>", lambda event: root.destroy())
        btnClose.bind("<Button-1>", lambda event: infoWindow.destroy())
        btnClose.pack(side="left", padx=10, pady=10, expand=True)

        # wanted to create fake progress bar for fun after accepting the cookies
        """ def progress_bar():
                text = ["Stealing your Password", "Searching for hidden files", "Collecting Data"]
                for i in text:
                    progressWindow = ttk.Window(themename="darkly")
                    progressbar = ttk.Progressbar(master=progressWindow, bootsyle="danger", length=160).pack()
                while True:
                     progressbar.step(50)"""

        # click to see what we do with your data;)
        def open_link():
            web.open("https://www.youtube.com/watch?v=xvFZjo5PgG0")

        infoWindow.mainloop()

    # Window for visualizing the output
    def popup_window(text=""):
        window = ctk.CTk()
        window.title("Bob the Bard")
        window.geometry("500x500")
        window.resizable(False, True)

        frameTitle = ctk.CTkFrame(master=window)
        frameTitle.pack(pady=20, padx=20, fill="both", expand=True)
        labelTitel = ctk.CTkLabel(master=frameTitle, text="Bob The Bard", font=("Roboto", 24))
        labelTitel.pack(pady=12, padx=10, side="top", anchor="nw")

        frameMsg = ctk.CTkFrame(master=frameTitle)
        frameMsg.pack(pady=12, padx=12, fill="both", expand=True)
        labelMsg = ctk.CTkLabel(master=frameMsg, text=text, wraplength=420)
        labelMsg.pack(pady=12, padx=10, side="top", anchor="nw")

        btnFrame = ctk.CTkFrame(master=window)
        btnFrame.pack(pady=[0, 12], padx=20, anchor="center")

        # Place buttons on the same column with padding
        btnCopy = ctk.CTkButton(master=btnFrame, text="copy")
        btnCopy.bind("<Button-1>", lambda event: copy_text(text))
        btnCopy.pack(fill="both", expand=True, side="left", padx=10, pady=10)

        btnClose = ctk.CTkButton(master=btnFrame, text="close")
        btnClose.bind("<Button-1>", lambda event: window.destroy())
        btnClose.pack(fill="both", expand=True, side="right", padx=10, pady=10)

        window.mainloop()

    # the always on STAND BY for checking if you said activateBobHotword to activate the wake main bob
    def bobs_banana_assistant():
        global bobActiveAssistant
        global bobActive
        labelState.configure(text="Waiting", text_color="white")
        create_log("bobs banana assistant activated", "white")

        def play_start_sound():
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

            # check that bob is not active 'or you should turn off
            # (for closing thread and stoppping the possablily of running multiple bobs when saying multiple times the
            # activateBobHotword)
        while not bobActive and bobActiveAssistant:
            # with microphone adjust to ambient sound for no noise
            with sr.Microphone() as source:
                recorder.adjust_for_ambient_noise(source)
                print("lis")
                # if takes to long to start phrase time limit = 4; records 4 seconds long
                audio = recorder.listen(source)

            try:
                prompt = recorder.recognize_google(audio)
                print(prompt)
                if activateBobHotword in prompt.lower():
                    # start thread and set bobActive to true so not multiple bobs threads get created
                    Thread(target=play_start_sound).start()
                    bobActive = True
                    threading.Thread(bobs_heart()).start()

            except sr.exceptions.UnknownValueError:
                create_log("Couldn't understand your ugly voice! >:(", "red")

            except Exception as ex:
                print(ex)
                create_log("Error from google speech recognition" + ex, "red")
                return

        create_log("bobs banana assistant deactivated", "red")
        return

    # main bob listening to your command
    def bobs_ear():
        with sr.Microphone() as source:
            recorder.adjust_for_ambient_noise(source)

            labelState.configure(text="Recording", text_color="green")
            labelMeter.configure(bootstyle="success")
            meterInfo.configure(bootstyle="success")
            Thread(target=meter_amount).start()

            notification("Recording...", "Recording your beatiful voice []~(￣▽￣)~*")

            try:
                # listen for 20 seconds or stop after 10 seconds saying nth.
                audio = recorder.listen(source, timeout=20, phrase_time_limit=10)

            except sr.WaitTimeoutError:
                create_log("Error: WaitTimeoutError", "red")
                print("u took too long, AGAIN!!!")

        labelState.configure(text="Transcripting", text_color="yellow")
        labelMeter.configure(bootstyle="warning")
        meterInfo.configure(bootstyle="warning")
        notification("Transcripting", "Deciphering these ancient texts ¯\(°_o)/¯   (´･ω･`)?")

        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            prompt = recorder.recognize_google(audio)
        except sr.UnknownValueError:
            prompt = ""
            bobs_voice_thread(
                "Error101: Google Speech Recognition could not understand audio, probably cuz you are dumb as hell")
            create_log(
                "Error101: Google Speech Recognition could not understand audio, probably cuz you are dumb as hell",
                "red")
        except sr.RequestError as e:
            prompt = ""
            bobs_voice_thread(
                "Error102: Could not request results from Google Speech Recognition service; {0}".format(e))
            create_log("Error102: Could not request results from Google Speech Recognition service; {0}".format(e),
                       "red")

        return prompt

    #checks for commands
    def gods_voice_commands(prompt):
        prompt = prompt.lower()

        labelState.configure(text="Checking for Commands")
        notification("Searching for holy scripts", "God pls I have waited so long. (っ °Д °;)っ")

        if youtubeHotword in prompt:
            prompt = prompt.replace("search in youtube ", "")
            create_log("searching in youtube", "white")
            create_log("found video " + prompt, "white")
            pwk.playonyt(prompt, open_video=True)
            prompt = "found video " + prompt

        elif popupHotword in prompt:
            global popupActive
            with open("settings.json", "r+") as f:
                settings = json.load(f)
            if popupActive == 2:
                settings["custom"]["states"]["popupActive"] = 0
                popupActive = 0
                create_log("deactivated popup windows", "red")
                prompt = "deactivated popup windows"
            elif popupActive == 1:
                settings["custom"]["states"]["popupActive"] = 2
                popupActive = 2
                prompt = "activated popup windows"
                create_log("deactivated popup windows", "white")
            else:
                settings["custom"]["states"]["popupActive"] = 1
                popupActive = 1
                prompt = "opens popup window on condition: " + str(popupWordCount) + " words"
                create_log("deactivated popup windows", "yellow")

            with open("settings.json", "w") as jsonFile:
                json.dump(settings, jsonFile, indent=4)

        elif searchHotword in prompt:
            prompt = prompt.replace(searchHotword + " ", "")
            create_log("searching: " + prompt, "white")
            if "telegram" in prompt:
                web.open("https://web.telegram.org/k/#@kian2000_5")
            else:
                pwk.search(prompt)
            prompt = "found: " + prompt

        elif findInformationHotword in prompt:
            prompt = prompt.replace(findInformationHotword + " ", "")
            create_log("searching information: " + prompt, "white")
            try:
                prompt = pwk.info(prompt, return_value=True)
                create_log("found information: ", "white")
            except wikipedia.exceptions.PageError:
                create_log("not found information", "red")
                prompt = ("No, i could find the information, but I don't want to!")

        elif openAppHotword in prompt:
            prompt = prompt.replace(openAppHotword + " ", "")
            create_log("opened " + prompt, "white")
            AppOpener.open(prompt, match_closest=True)
            prompt = "sucessfuly opened " + prompt

        elif closeAppHotword in prompt:
            prompt = prompt.replace(closeAppHotword + " ", "")
            create_log("closed " + prompt, "white")
            AppOpener.close(prompt, match_closest=True)
            prompt = "sucessfuly closed " + prompt

            notification("Holy scripts found", "Finally blessed (˘ ˘ ˘)")

        else:
            create_log("No commands found!", "white")
            create_log("Output: " + prompt)

        return prompt

    # create a voice for the answer
    def bobs_voice(prompt):
        if prompt != "":
            # translate and save as mp3
            tts = gTTS(text=prompt, lang="en")
            tts.save("bard_response.mp3")

            labelState.configure(text="Speaking", text_color="green")
            labelMeter.configure(bootstyle="success")
            meterInfo.configure(bootstyle="success")

            # turn it into a pydub soundSegment and speed up the voice
            sound = pydub.AudioSegment.from_mp3("bard_response.mp3")
            new_sound = speedup(sound, 1.2, 150, 25)
            new_sound.export("bard_responsemp3.mp3", format="mp3")
            global duration
            # calculate duration for exact calculations in meter durations
            duration = pydub.AudioSegment.from_mp3("bard_responsemp3.mp3").duration_seconds
            play(new_sound)

    # when asking bard (doesn't work now with gemini)
    def bobs_brain(prompt):
        try:
            labelState.configure(text="Asking Bob")
            labelMeter.configure(bootstyle="info")
            meterInfo.configure(bootstyle="info")

            # set token and get answer
            bob = Bard(token=token)
            bobsAnswer = bob.get_answer(prompt)
            return bobsAnswer["content"]

        except Exception:
            create_log("Wrong Token", "red")
            return "It seems, you were too incompetend insert the right token, disspointing"

    # copy text if it is called
    def copy_text(text):
        create_log("copied prompt", "white")
        clipboard.copy(text)
        bobs_voice_thread("copied prompt")

    def create_log(text, color="green"):
        # text = textwrap.fill(text, )
        labelLog = ctk.CTkLabel(master=frameLog, text=text, text_color=color, font=("Terminal", 17), wraplength=350)
        labelLog.pack(padx=4, pady=4, anchor="w")

    # so the gui doesn't wate for the mp3 to get played
    def bobs_voice_thread(text=""):
        thread_voice = Thread(target=bobs_voice, args=(text,)).start()
        thread_voice.join()

    # here run check thread to see if the key ` or the button was clicked to start the bobAssitant
    def run_check_thread(event):
        global bobActiveAssistant
        global bobActive
        if not bobActiveAssistant and (event.keycode == 192 or event.num == 1):
            bobActiveAssistant = True
            btnRecord.configure(image=recActiveImage)
            Thread(target=bobs_banana_assistant).start()
        elif bobActiveAssistant and (event.keycode == 192 or event.num == 1):
            bobActiveAssistant = False
            bobActive = False
            btnRecord.configure(image=recInactiveImage)
            labelState.configure(text="Off", text_color="red")
            # closing all threads not working
            """for thread in threading.enumerate():
                thread.join()
                return"""

    # meter
    def meter_amount():
        meterInfo.configure(amountused=0)
        labelMeter.configure(text="00.0%")
        meterRunning = True
        while meterRunning:
            # check if meter is max then wait and decrease fast
            if meterInfo["amountused"] >= 1000:
                time.sleep(0.01)
                while meterRunning:
                    meterInfo.configure(amountused=meterInfo["amountused"] - 19)
                    labelMeter.configure(text=str(meterInfo["amountused"] / 10) + "%")
                    if meterInfo["amountused"] <= 19:
                        meterRunning = False
            # check for each state and if threshhold(here: 400) is reached add amount to the meter depending on state
            elif labelState.cget("text") == "Recording" and meterInfo["amountused"] < 400:
                time.sleep(0.0105)
                meterInfo.configure(amountused=meterInfo["amountused"] + 1)
            elif meterInfo["amountused"] < 400 and labelState.cget("text") == "Transcripting":
                meterInfo.configure(amountused=meterInfo["amountused"] + 9)

            elif labelState.cget("text") == "Transcripting" and meterInfo["amountused"] < 550:
                meterInfo.configure(amountused=meterInfo["amountused"] + 1)
            elif meterInfo["amountused"] < 550 and labelState.cget("text") == "Checking for Commands":
                meterInfo.configure(amountused=meterInfo["amountused"] + 9)

            elif labelState.cget("text") == "Checking for Commands" and meterInfo["amountused"] < 650:
                meterInfo.configure(amountused=meterInfo["amountused"] + 3)
            elif meterInfo["amountused"] < 650 and labelState.cget("text") == "Asking Bob":
                meterInfo.configure(amountused=meterInfo["amountused"] + 9)

            elif labelState.cget("text") == "Asking Bob" and meterInfo["amountused"] < 800:
                time.sleep(0.005)
                meterInfo.configure(amountused=meterInfo["amountused"] + 1)
            elif meterInfo["amountused"] < 800 and labelState.cget("text") == "Speaking":
                meterInfo.configure(amountused=meterInfo["amountused"] + 9)

            elif labelState.cget("text") == "Speaking" and meterInfo["amountused"] < 999:
                global duration
                time.sleep(duration / 650)
                meterInfo.configure(amountused=meterInfo["amountused"] + 1)
            elif meterInfo["amountused"] <= 1000 and labelState.cget("text") == "Waiting":
                meterInfo.configure(amountused=meterInfo["amountused"] + 9)

            if meterRunning:
                labelMeter.configure(text=str(meterInfo["amountused"] / 10) + "%")
            else:
                meterInfo.configure(amountused=0, bootstyle="light")
                labelMeter.configure(text="00.0%")

    # the main of bob
    def bobs_heart():
        global bobActive
        copyBool = False

        # audio to text
        text = bobs_ear()

        create_log("You said: " + text)

        # check if copy prompt
        if copyPromptHotword in text:
            copyBool = True
            text = text.replace(copyPromptHotword + "", "")

        # check if to ask bard(now: gemini)
        if askBardHotword in text:
            text = text.replace(askBardHotword + " ", "")
            text = bobs_brain(text)
            create_log("Output: " + text)
        else:
            text = gods_voice_commands(text)

        # labelLog.configure(text=labelLog["text"]+"\n ")
        if popupActive == 2 or popupActive == 1 and len(text) > 120:
            popup_window(text)

        # turn text to speech
        bobs_voice(text)

        # terminate if you want to kill bob
        if killBobHotword in text:
            # doesn't terminate all threads
            for thread in threading.enumerate():
                thread.join()

            btnRecord.configure(image=recInactiveImage)
            labelState.configure(text="Killed", text_color="red")
            meterInfo.configure(bootstyle="danger")
            create_log("killed", "red")

            notification("Killing Bob", "You MONSTER, how could you!!! ╰(艹皿艹 )")
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

            close()

            return
        else:
            labelState.configure(text="Waiting", text_color="white")

        if copyBool:
            copy_text(text)

        bobActive = False
        print(text)

    frameTop = ctk.CTkFrame(master=root, height=30)
    frameTop.pack(fill="both")

    labelTitle = ctk.CTkLabel(master=frameTop, text="Bob The Bard", font=("Terminal", 24))
    labelTitle.pack(side="left", padx=5)

    settingsImage = ctk.CTkImage(Image.open("images/setting.png"), size=(30, 30))
    recInactiveImage = ctk.CTkImage(Image.open("images/recorderInactive.png"), size=(30, 30))
    recActiveImage = ctk.CTkImage(Image.open("images/recorderActive.png"), size=(30, 30))

    btnSettings = ctk.CTkButton(master=frameTop, text="", image=settingsImage, fg_color="transparent", height=30,
                                width=30,
                                command=popup_change_settings)
    btnSettings.pack(side="right")

    btnRecord = ctk.CTkButton(master=frameTop, text="", fg_color="transparent", image=recInactiveImage, height=30,
                              width=50)
    btnRecord.bind("<Button-1>", lambda event: run_check_thread(event))
    btnRecord.pack(side="right")

    frameState = ctk.CTkFrame(master=root, width=300, height=50)
    frameState.pack(padx=15, pady=15, side="right", anchor="ne")
    # frameState.pack_propagate(True)

    labelState = ctk.CTkLabel(master=frameState, text="Off", text_color="red", font=("Terminal", 24))
    labelState.pack(padx=14, pady=4, expand=True, fill="both")

    meterInfo = ttk.Meter(master=root, metersize=200, bootstyle='light', amounttotal=1000, showtext=False)
    meterInfo.place(rely=1.0, relx=1.0, x=-80, y=-60, anchor="se")

    labelMeter = ttk.Label(master=meterInfo, text="00.0%", bootstyle="light", font=("Terminal", 21))
    labelMeter.place(rely=1.0, relx=1.0, x=-57, y=-87, anchor="se")

    frameLog = ctk.CTkScrollableFrame(master=root, width=350, height=250, label_font=("Terminal", 17),
                                      label_text_color="white", label_text="Log")
    frameLog.pack(padx=15, pady=15, side="left", anchor="sw")

    # make sure that all threads die(works most of the time when closing like intended)
    def close():
        global bobActiveAssistant, bobActive
        bobActiveAssistant = False
        bobActive = False
        root.quit()

    root.bind("<KeyRelease>", func=run_check_thread)
    # root.after(1000, func=popup_cookies)
    root.protocol("WM_DELETE_WINDOW", func=close)
    root.mainloop()

#load all values and run the GUI
setup()
bobs_skin()
