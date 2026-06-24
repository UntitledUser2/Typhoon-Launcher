import subprocess
from pathlib import Path
import shutil
import time
import customtkinter
from PIL import Image


app_path = Path.home() / ".local/share/applications"
launcher_path = Path(__file__).resolve().parent


def GUI():
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("500x800")

    def setup():

        with open("dat.txt", "w") as dat:
            dat.write("True")
            dat.close()

        #Write to the beginning files the path of the launcher to the desktop file
        with open("typhoon-desktop.txt", "r") as file:
            line = file.readlines()

        line[2] = f"Exec={launcher_path}/typhoon-launcher.sh %u\n"

        with open("typhoon-desktop.txt", "w") as file:
            file.writelines(line)

        root.destroy()

        #Convert .txt into proper .desktop file
        shutil.copy("typhoon-desktop.txt", "typhoon-desktop.desktop")
        time.sleep(1)
        shutil.move("typhoon-desktop.desktop", app_path)

        #Register
        subprocess.run(["/usr/bin/xdg-mime", "default", "typhoon-desktop.desktop", "x-scheme-handler/vortex"])
        subprocess.run(["update-desktop-database", str(app_path), ".local/share/applications/"])

        shutil.copy("typhoon-launcher.txt", "typhoon-launcher.sh")
        subprocess.run(["chmod", "+x", f"{launcher_path}/typhoon-launcher.sh"])


    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, expand=True, fill="both")

    PIL_logo = Image.open("logo.png")
    temp_logo = customtkinter.CTkImage(light_image=PIL_logo,dark_image=PIL_logo,size=(380, 100))
    logo = customtkinter.CTkLabel(text="", image=temp_logo, master=frame)
    logo.place(x=0,y=0)
    

    def setup_button_pressed():
        frame.forget()
        frame2 = customtkinter.CTkFrame(master=root)
        frame2.pack(pady=20, padx=60, expand=True, fill="both")

        PIL_logo = Image.open("logo.png")
        temp_logo = customtkinter.CTkImage(light_image=PIL_logo,dark_image=PIL_logo,size=(380, 100))
        logo = customtkinter.CTkLabel(text="", image=temp_logo, master=frame2)
        logo.place(x=0,y=0)

        label3 = customtkinter.CTkLabel(master=frame2, text="Step 1", font=("Arial",30,"bold"))
        label3.place(x=145,y=200)

        label4 = customtkinter.CTkLabel(master=frame2, text="Typhoon uses bottles to launch \nVortex!", font=("Arial",20))
        label4.place(x=50,y=240)
        
        label5 = customtkinter.CTkLabel(master=frame2, text="Make sure a bottle named Vortex \nis created and Vortex itself is installed \nin program files! (not x86)", font=("Arial",20))
        label5.place(x=20,y=300)

        PIL_ex = Image.open("example1.png")
        temp_ex = customtkinter.CTkImage(light_image=PIL_ex,dark_image=PIL_ex,size=(380, 300))
        ex = customtkinter.CTkLabel(text="", image=temp_ex, master=frame2)
        ex.place(x=0,y=400)

        def last_step():
            frame2.forget()
            frame3 = customtkinter.CTkFrame(master=root)
            frame3.pack(pady=20, padx=60, expand=True, fill="both")

            PIL_logo = Image.open("logo.png")
            temp_logo = customtkinter.CTkImage(light_image=PIL_logo,dark_image=PIL_logo,size=(380, 100))
            logo = customtkinter.CTkLabel(text="", image=temp_logo, master=frame3)
            logo.place(x=0,y=0)

            label6 = customtkinter.CTkLabel(master=frame3, text="We'll take it from here!", font=("Arial",25,"bold"))
            label6.place(x=58,y=200)

            label7 = customtkinter.CTkLabel(master=frame3, text="You've done your part!", font=("Arial",20))
            label7.place(x=90,y=240)

            label7 = customtkinter.CTkLabel(master=frame3, text="Now we'll do ours! \nThanks for using Typhoon!", font=("Arial",20))
            label7.place(x=70,y=300)

            finish = customtkinter.CTkButton(master=frame3, text="Finish", font=("Arial", 20), width=250, command=setup,)
            finish.place(x=70,y=500)
            

        proceed = customtkinter.CTkButton(master=frame2, text="Next Step", font=("Arial", 20), width=250, command=last_step)
        proceed.place(x=70,y=720)

    def Launch_Vortex():
        subprocess.run(["bottles-cli", "run","-b", "Vortex","-e", "C:\\Program Files\\Vortex\\Vortex.exe"])
        
    with open("dat.txt", "r") as dat:
        dat.seek(0)
        if "True" in dat.read():
            button2 = customtkinter.CTkButton(master=frame, text="Launch Vortex", font=("Arial", 20), width=250, command=Launch_Vortex)
            button2.place(x=70,y=300)
        else:
            print(dat.read())
            dat.close()
            welcome = customtkinter.CTkLabel(master=frame, text="Welcome!", font=("Arial",30,"bold"))
            welcome.place(x=120,y=200)
            label = customtkinter.CTkLabel(master=frame, text="It seems like its your first time using \nTyphoon!", font=("Arial",20))
            label.place(x=30,y=240)
            label2 = customtkinter.CTkLabel(master=frame, text="Get it setup below!", font=("Arial",20))
            label2.place(x=110,y=350)
            button = customtkinter.CTkButton(master=frame, text="Setup", font=("Arial", 20), width=250, command=setup_button_pressed)
            button.place(x=70,y=400)


    root.resizable(False, False)
    root.mainloop()

GUI()
