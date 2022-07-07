from threading import Thread
import speech_recognition as sr


class Speech(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.r = sr.Recognizer()
        self.output = ""
        self.found = False
        self.kill = True

    
    def run(self):

        while self.kill:
            # Listen for audioF
            try:
                    
                # use the microphone as source for input.
                with sr.Microphone() as source2:
                        
                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level
                    self.r.adjust_for_ambient_noise(source2, duration=0.2)
                        
                    #listens for the user's input
                    audio2 = self.r.listen(source2)
                        
                    # Using google to recognize audio
                    MyText = self.r.recognize_google(audio2)

                    self.found = True

                    MyText = MyText.lower()

                    self.output = MyText

                    self.found = False
                    print(MyText)
                        
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
                    
            except sr.UnknownValueError:
                print("unknown error occured")

            except OSError as e:
                if once:
                    print("OS ERROR: {0}".format(e))
                    once = False
    
    def Kill_Thread(self):
        self.kill = False