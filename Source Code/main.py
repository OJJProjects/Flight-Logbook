#Import required libraries
import sys

import customtkinter
from tkinter import ttk
import pyodbc as pyo
import configparser
from configparser import ConfigParser
import os

# Paths
project_path = os.path.dirname(os.path.abspath(sys.argv[0]))
database_path = "DBQ=" + project_path + "/database.accdb"
print(database_path)

# Functions
def on_submit_click():
	cnn_string = (
		r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
		+ database_path
		)
	cnn = pyo.connect(cnn_string)
	cursor = cnn.cursor()
	cursor.execute(
		"INSERT INTO flight_data VALUES	 (?,?,?,?,?,?,?)",
		(flight_number_entry.get(),aircraft_entry.get(),departure_airport_entry.get(),arrival_airport_entry.get(),departure_time_entry.get(),arrival_time_entry.get(),duration_entry.get())

	)
	cursor.commit()

def change_resolution(choice):
    global resolution
    resolution = choice
    if resolution == "3840x2160":
        root.geometry("3840x2160")
    elif resolution == "2560x1440":
        root.geometry("2560x1440")
    elif resolution == "1920x1080":
        root.geometry("1920x1080")
    elif resolution == "800x500":
        root.geometry("800x500")

def dark_mode_switch():
	variable = dark_mode_variable.get()
	if variable == "on":
		customtkinter.set_appearance_mode("dark")
	if variable == "off":
		customtkinter.set_appearance_mode("light")

def save_settings():
        config = ConfigParser()
        config.read("settings.ini")

        # GET DARK MODE THEM SETTING
        dark_mode_setting = dark_mode_variable.get()
        
        config.set('PERSONILISATION','dark_mode_theme',dark_mode_setting)
        config.set('PERSONILISATION','resolution',resolution)
        with open('settings.ini', 'w') as configfile:
                config.write(configfile)

############## GUI SECTION ##############
root = customtkinter.CTk()
config = configparser.ConfigParser()

config.read('settings.ini')
ini_dark_mode = config['PERSONILISATION']['dark_mode_theme']
ini_resolution = config['PERSONILISATION']['resolution']

if ini_dark_mode == "on":
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
if ini_dark_mode == "off":
        customtkinter.set_appearance_mode("light")
        customtkinter.set_appearance_mode("light-blue")

customtkinter.set_window_scaling(1.0)
customtkinter.set_widget_scaling(1.0)

my_tabs = customtkinter.CTkTabview(root)
my_tabs.pack(pady=10)
tab_create_new_flight = my_tabs.add("New Flight")
tab_view_past_flights = my_tabs.add("Past Flight")
tab_settings = my_tabs.add("Settings")
                
root.geometry(ini_resolution)

# Create new flight section
flight_number_entry = customtkinter.CTkEntry(tab_create_new_flight, placeholder_text="Flight Number")
flight_number_entry.pack(pady=5)

aircraft_entry = customtkinter.CTkEntry(tab_create_new_flight, placeholder_text="Aircraft")
aircraft_entry.pack(pady=5)

departure_airport_entry = customtkinter.CTkEntry(tab_create_new_flight, placeholder_text="Departure Airport")
departure_airport_entry.pack(pady=5)

arrival_airport_entry = customtkinter.CTkEntry(tab_create_new_flight, placeholder_text="Arrival Airport")
arrival_airport_entry.pack(pady=5)

departure_time_entry = customtkinter.CTkEntry(tab_create_new_flight, placeholder_text="Departure Time")
departure_time_entry.pack(pady=5)

arrival_time_entry = customtkinter.CTkEntry(tab_create_new_flight, placeholder_text="Arrival Time")
arrival_time_entry.pack(pady=5)

duration_entry = customtkinter.CTkEntry(tab_create_new_flight, placeholder_text="Duration Time")
duration_entry.pack(pady=5)

submit_button = customtkinter.CTkButton(tab_create_new_flight, text="Save", command=on_submit_click)
submit_button.pack(pady=5)

# Past Flights Section
table = ttk.Treeview(tab_view_past_flights, columns = ("treeview_flight_number","treeview_aircraft","treeview_departure_aiport","treeview_arrival_airport","treeview_departure_time","treeview_arrival_time","treeview_duration"), show = "headings")
table.heading("treeview_flight_number", text="Flight Number")
table.heading("treeview_aircraft", text="Aircraft")
table.heading("treeview_departure_aiport", text="Departure Airport")
table.heading("treeview_arrival_airport", text="Arrival Airport")
table.heading("treeview_departure_time", text="Departure Time")
table.heading("treeview_arrival_time", text="Arrival Time")
table.heading("treeview_duration", text="Duration")
table.pack()

cnn_string = (
		r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
		r"DBQ=C:\Users\oscar\Documents\VSCode Projects\flightlogbook\database.accdb"
		)
cnn = pyo.connect(cnn_string)
cursor = cnn.cursor()
cursor.execute("SELECT * FROM flight_data")
for row in cursor:
	table.insert('','end', value=row[0:7])

# Settings Section
dark_mode_variable = customtkinter.StringVar(value="on")
dark_mode_switch = customtkinter.CTkSwitch(tab_settings,text="Dark Mode",variable=dark_mode_variable,onvalue="on",offvalue="off",command=dark_mode_switch)
dark_mode_switch.pack(pady=10)

resolution_options=["3840x2160","2560x1440","1920x1080","800x500"]
resolution_combo_box = customtkinter.CTkComboBox(tab_settings, values=resolution_options, command=change_resolution)
resolution_combo_box.pack(pady=5)

settings_save_button = customtkinter.CTkButton(tab_settings, text="Save",command=save_settings)
settings_save_button.pack(pady=5)


root.mainloop()