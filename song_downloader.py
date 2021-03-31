import os
import shutil

from pytube import YouTube
from pytube import Playlist
from pytube.exceptions import VideoUnavailable
from datetime import datetime

try:
  #Create list of anime to download
  op_list = open("op_list.txt", "r")
  op_list_lines = op_list.readlines()
except:
  print("Erreur lors de la gestion du fichier d'OP/ED")

#Download every anime in the list
for line in op_list_lines:
  #Split the data received from the file into name, address and the number of OP/ED
  line_splitted = line.split("><")
  name = line_splitted[0].strip()
  address = line_splitted[1].strip()
  op_ed = line_splitted[3].strip()
  filename = name + " - " + op_ed

  #Tries to download the song
  try:   
    yt = YouTube(address)
    print("Téléchargement de " + filename)  
    yt.streams.filter(only_audio=True).first().download(filename=filename, output_path="./songs")
  #If the video is unavailable, note the unavailable song in a file
  except VideoUnavailable:
    unavailable_op_ed_file = open("./unavailable_op_ed.txt","a+")
    formatted_date = str(datetime.now().day) + "/" + str(datetime.now().month) + "/" + str(datetime.now().year)
    formatted_date += " " + str(datetime.now().hour) + ":" + str(datetime.now().minute)
    unavailable_op_ed_file.write(filename + " " + formatted_date + "\n")   
    #Skip videos that can't be loaded 
    pass    