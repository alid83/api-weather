from datetime import datetime
from tkinter import *
from tkinter import ttk
import requests
import tkintermapview
from khayyam import JalaliDatetime
latitude = None
longitude = None

def tk():
    output1.delete("1.0", "end")
    output2.delete("1.0", "end")
    selected_value = selected_var.get()
    x = selected_value
    if latitude is None or longitude is None:
        output1.insert(END, "Please select a location on the map.\n")
        return

    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&forecast_days={x}'
    response = requests.get(url)
    data = response.json()

    for i in range(len(data['hourly']['time'])):
        date = datetime.strptime(data['hourly']['time'][i], "%Y-%m-%dT%H:%M")
        output1.insert(END,
                       f'{str(JalaliDatetime(datetime(date.year, date.month, date.day, date.hour, date.minute)))} = temp:{data["hourly"]["temperature_2m"][i]}, wind speed:{data["hourly"]["wind_speed_10m"][i]}\n')
    output2.insert(END,
                   f'maximum temp: {data["daily"]["temperature_2m_max"]}\nminimum temp: {data["daily"]["temperature_2m_min"]}\nsunrise: {data["daily"]["sunrise"]}\nsunset: {data["daily"]["sunset"]}\ncurrent temperature: {data["current"]["temperature_2m"]}\ncurrent wind speed: {data["current"]["wind_speed_10m"]}')


def on_map_click(coordinate):
    global latitude, longitude
    latitude, longitude = coordinate
    selected_location.set(f"Latitude: {latitude}, Longitude: {longitude}")


root = Tk()
root.configure(background='skyblue')
root.title('Weather')
label1 = Label(root, text='Temperature:', font='Helvetica 12 bold', background='skyblue')
label1.place(x=10, y=270)
btn1 = Button(root, text='Start', height=2, width=15, background='Green', command=tk)
btn1.place(x=238, y=625)
root.geometry('1200x700')

output1 = Text(root, height=20, width=72)
output1.place(x=15, y=300)

output2 = Text(root, height=20, width=72)
output2.place(x=605, y=300)

btn2 = Button(root, text='Exit', height=2, width=15, background='Red', command=root.destroy)
btn2.place(x=838, y=625)

selected_var = StringVar()

options = ["days", "1", "3", "7", "14", "16"]
selected_var.set(options[0])

option_menu = ttk.OptionMenu(root, selected_var, *options)
option_menu.place(x=500, y=270)

map_widget = tkintermapview.TkinterMapView(root, width=700, height=250, corner_radius=0)
map_widget.place(x=15, y=5)
map_widget.set_position(32.4279, 53.6880)
map_widget.set_zoom(5)
map_widget.add_left_click_map_command(on_map_click)

selected_location = StringVar()

location_label = Label(root, textvariable=selected_location)
location_label.place(x=15, y=260)

root.mainloop()
