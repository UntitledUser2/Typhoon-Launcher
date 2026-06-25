#Import Libaries
import subprocess
from pathlib import Path
import shutil
import time
import customtkinter
from PIL import Image
import os

#Define Variables
app_path = Path.home() / ".local/share/applications"
launcher_path = Path(__file__).resolve().parent

#Main GUI loop
def GUI():
    #Set some theme stuff for the window
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("dark-blue")

    #Instanciate the window
    root = customtkinter.CTk()
    root.geometry("500x800")
    root.resizable(False, False)

    #Checkbox logic
    state = customtkinter.BooleanVar(value=False)
    with open(f"{launcher_path}/dat/dat.txt", "r") as dat:
        dat.seek(0)
        temp = dat.read()
        if "logging:false" in temp:
            pass
        elif "logging:true" in temp:
            state = customtkinter.BooleanVar(value=True)
            print("state")
    dat.close()

    #Creates the actual .sh and .desktop files for the browser to use to pass the token to the app
    def setup():

        #Save to dat file that the user has already gone through the setup
        with open(f"{launcher_path}/dat/dat.txt") as dat:
            lines = dat.readlines()
            lines[0] = "setup:true" + "\n"
            with open(f"{launcher_path}/dat/dat.txt", "w") as dat:
                for line in lines:
                    dat.write(line)
        dat.close()

        #Write to the beginning files the path of the launcher to the desktop file
        with open(f"{launcher_path}/resources/typhoon-desktop.txt", "r") as file:
            line = file.readlines()

        line[2] = f"Exec={launcher_path}/typhoon-launcher.sh %u\n"

        with open(f"{launcher_path}/resources/typhoon-desktop.txt", "w") as file:
            file.writelines(line)

        root.destroy()

        #Convert .txt into proper .desktop file
        shutil.copy(f"{launcher_path}/resources/typhoon-desktop.txt", "typhoon-desktop.desktop")
        time.sleep(1)
        shutil.move("typhoon-desktop.desktop", app_path)

        #Register
        subprocess.run(["/usr/bin/xdg-mime", "default", "typhoon-desktop.desktop", "x-scheme-handler/vortex"])
        subprocess.run(["update-desktop-database", str(app_path), ".local/share/applications/"])

        shutil.copy(f"{launcher_path}/resources/typhoon-launcher.txt", "typhoon-launcher.sh")
        subprocess.run(["chmod", "+x", f"{launcher_path}/typhoon-launcher.sh"])

    #Creates the main frame
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, expand=True, fill="both")

    #Loads the logo image
    load_logo = Image.open(f"{launcher_path}/assets/logo.png")
    logo = customtkinter.CTkImage(light_image=load_logo, dark_image=load_logo, size=(400,140))
    logo_label = customtkinter.CTkLabel(frame, image=logo, text="")
    logo_label.place(x=-10,y=0)
    
    

    def refresh(page):

        for child in frame.winfo_children():
                if child != logo_label:
                    child.destroy()

        if page == 2:
            title = customtkinter.CTkLabel(master=frame, text="Step 1", font=("Arial",30,"bold"))
            title.place(x=142,y=200)
            label = customtkinter.CTkLabel(master=frame, text='First create a bottle named "Vortex"', font=("Arial",20))
            label.place(x=35,y=240)
            label2 = customtkinter.CTkLabel(master=frame, text="Than download Vortex itself into the\n Program Files (not x86) folder in your\n bottle!", font=("Arial",20))
            label2.place(x=15,y=280)

            load_example = Image.open(f"{launcher_path}/assets/example1.png")
            example = customtkinter.CTkImage(light_image=load_example, dark_image=load_example, size=(350,240))
            example_label = customtkinter.CTkLabel(frame, image=example, text="")
            example_label.place(x=15,y=400)

            button = customtkinter.CTkButton(master=frame, text="Continue", font=("Arial", 20), width=250, command=lambda:refresh(3))
            button.place(x=64,y=700)
        
        if page == 3:
            title = customtkinter.CTkLabel(master=frame, text="Step 2", font=("Arial",30,"bold"))
            title.place(x=142,y=200)
            label = customtkinter.CTkLabel(master=frame, text="Simply just let Typhoon work its magic!", font=("Arial",20))
            label.place(x=18,y=240)
            label2 = customtkinter.CTkLabel(master=frame, text="Thanks for using Typhoon!", font=("Arial",15))
            label2.place(x=100,y=270)

            button = customtkinter.CTkButton(master=frame, text="Finish Setup!", font=("Arial", 20), width=250, command=setup)
            button.place(x=64,y=700)
    
    #Checks wether the User has already gone through the setup
    with open(f"{launcher_path}/dat/dat.txt", "r") as dat:

        #Launches the game from the bottle
        def Launch_Vortex():
            with open(f"{launcher_path}/dat/dat.txt", "r") as dat:
                dat.seek(0)
                temp = dat.read()
                if "logging:false" in temp:
                    subprocess.run(["bottles-cli", "run","-b", "Vortex","-e", "C:\\Program Files\\Vortex\\Vortex.exe"])
                elif "logging:true" in temp:
                    print("test")
                    subprocess.run(f"{launcher_path}/typhoon-launcher.sh vortex://test", shell=True)
                
        #Handles all the logic to see if the user has enabled logging
        def logging():
            #Launcher & dat update logic
            with open(f"{launcher_path}/dat/dat.txt") as dat:
                lines = dat.readlines()
                dat.seek(0)

                if state.get() == True:
                    lines[1] = "logging:true"
                    with open(f"{launcher_path}/resources/typhoon-launcher.txt") as laun:
                        lines2 = laun.readlines()
                        lines2[1] = lines2[1].rstrip("\n") + " >> ~/typhoon-debug.log" + "\n"
                        lines2[2] = lines2[2].rstrip("\n") + "  >> ~/typhoon-debug.log 2>&1" + "\n"
                        with open(f"{launcher_path}/resources/typhoon-launcher.txt", "w") as laun:
                            for line2 in lines2:
                                laun.write(line2)
                    laun.close()

                elif state.get() == False:
                    lines[1] = "logging:false"
                    with open(f"{launcher_path}/resources/typhoon-launcher.txt") as laun:
                        lines2 = laun.readlines()
                        lines2[1] = 'echo "URL received: $1"' + "\n"
                        lines2[2] = 'WINEPREFIX=~/.local/share/bottles/bottles/Vortex ~/.local/share/bottles/runners/soda-9.0-1/bin/wine "C:/Program Files/Vortex/Vortex.exe" "$1"'
                        with open(f"{launcher_path}/resources/typhoon-launcher.txt", "w") as laun:
                            for line2 in lines2:
                                laun.write(line2)
                    laun.close()

                with open(f"{launcher_path}/dat/dat.txt", "w") as dat:
                    for line in lines:
                        dat.write(line)
            dat.close()

            try:
                os.remove("typhoon-launcher.sh")
            except:
                pass
            shutil.copy(f"{launcher_path}/resources/typhoon-launcher.txt", "typhoon-launcher.sh")
            subprocess.run(["chmod", "+x", f"{launcher_path}/typhoon-launcher.sh"])



        dat.seek(0)
        temp = dat.read()
        if "setup:true" in temp:
            button2 = customtkinter.CTkButton(master=frame, text="Launch Vortex", font=("Arial", 20), width=250, command=Launch_Vortex)
            button2.place(x=70,y=300)

            tick = customtkinter.CTkCheckBox(master=frame, text="Enable Logging", variable=state, onvalue=True, offvalue=False, command=logging)
            tick.place(x=132,y=340)
        elif "setup:false" in temp:
            dat.close()
            title = customtkinter.CTkLabel(master=frame, text="Welcome!", font=("Arial",30,"bold"))
            title.place(x=122,y=200)
            label = customtkinter.CTkLabel(master=frame, text="It seems like its your first time using \nTyphoon!", font=("Arial",20))
            label.place(x=30,y=240)
            label2 = customtkinter.CTkLabel(master=frame, text="Get it setup below!", font=("Arial",20))
            label2.place(x=108,y=350)
            button = customtkinter.CTkButton(master=frame, text="Setup", font=("Arial", 20), width=250, command=lambda:refresh(2))
            button.place(x=64,y=400)

    #Creates the window
    root.mainloop()



    dat.close



GUI()
