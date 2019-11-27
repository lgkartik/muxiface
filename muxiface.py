from mutagen.mp3 import MP3
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
import os 
from imutils import paths
from mutagen.id3 import ID3
import pygame
import time
from vlc import *
import cv2 
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter.ttk import Frame
from keras.models import load_model 
from keras.preprocessing.image import img_to_array
import numpy as np 
import mutagen
from tinytag import TinyTag
import time 
import pickle 
import vlc
model = load_model('emotion.h5')
f = open('lyrics_all.pickle','rb')
all_lyrics = pickle.load(f)
index =0

root = tk.Tk()
root.geometry("1212x658")
root.title("MusiXfaCE")
root.configure(background="#aba4d8")
###############song list to be packed #############################
song_list = tk.Listbox(root)

song_list =tk.Listbox(root)
real_name =[]

all_file =[]
images =[]
song_artist =[]

#all song by by category #############
sad_song = list(paths.list_files('/home/kklg/ai_music/all_song/sad'))
romantic_song = list(paths.list_files('/home/kklg/ai_music/all_song/romantic'))
inspirational_song = list(paths.list_files('/home/kklg/ai_music/all_song/Inspirational'))
rap_song = list(paths.list_files('/home/kklg/ai_music/all_song/Rap_remix'))
###section to show all the song
def show_song(file):
    
    #file = list(paths.list_files(dirname))
    index=0
    for f in file:

        #name =f.split(os.path.sep)[-1]
        try:

            #meta_name = ID3(f)
            #name =meta_name['TIT2'].text[0]
            tag = TinyTag.get(f,image=True)
            title=tag.title
            name = title
            image = tag.get_image()
            images.append(bytearray(image))
            artist = tag.artist
            song_artist.append(artist)

                
            real_name.append(name)
            song_list.insert(index,name)
            all_file.insert(index,f)
            index=index+1
        except :
            pass

song_list.place(relx=0.017, rely=0.03, relheight=0.954
                , relwidth=0.261)
song_list.configure(background="#fffbfa")
song_list.configure(disabledforeground="#a22796")
song_list.configure(font='arial')
song_list.configure(highlightbackground="#d834c8")
song_list.configure(highlightcolor="#d9d9d9")
song_list.configure(selectbackground="#c32eb4")
############song list to packed #########################

##############lyrics ###################3
lyrics = tk.Text(root)
lyrics.place(relx=0.653, rely=0.03, relheight=0.953
                , relwidth=0.340)
lyrics.configure(background="#fffbfa")
song_list.configure(font='arial')
lyrics.configure(insertborderwidth="3")
lyrics.configure(selectbackground="#c32eb4")
lyrics.configure(wrap="none")
####################################
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
face_recognized_song = []

ml = MediaList()
mlp = MediaListPlayer()
mp = MediaPlayer()
mlp.set_media_player(mp)
def show_face():
    face_recognized_song = []
    
    video = cv2.VideoCapture(0)
    i = 0
    j=0
    k=0 
    global all_file
    global ml
    
    while True:
        
        ret,frame = video.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w-5,y+h-5),(255,0,0),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48))
            roi_gray = roi_gray.astype('float')/255.0
            roi_gray = img_to_array(roi_gray)
            roi_gray= np.expand_dims(roi_gray,axis=0)
            name = model.predict_classes(roi_gray)
            if name==0:
                if i <len(romantic_song):
                    face_recognized_song.append(romantic_song[i])
                    i+=1
                text = 'Happy'
            elif name==1:
                if j<len(rap_song):
                    face_recognized_song.append(rap_song[j])
                    j+=1
                text ='Neutral'
            else:
                if k<len(sad_song):
                    face_recognized_song.append(sad_song[k])
                    k+=1
                text ='Sad'
            cv2.putText(frame,text,(x+w,y+h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
        if ret==True:
            cv2.imshow('Image',frame)
            
            if cv2.waitKey(25) &0xFF==ord('q'):
                
                show_song(face_recognized_song)
                
                
                
                for file in all_file:
                    ml.add_media(file)
                
                mlp.set_media_list(ml)
                break
    
    video.release()
    cv2.destroyAllWindows()

def reset_library():
    song_list.delete(0,tk.END)
    real_name =[]

    all_file =[]
    images =[]
    song_artist =[]
    for i in range(len(ml)):
        ml.remove_index(i)

def set_volume(val):
    val = int(val)
    mp.audio_set_volume(val)

################################recognize face#################3333
face_recognition = tk.Button(root,command = show_face)
face_recognition.place(relx=0.38, rely=0.061, height=31, width=199)
face_recognition.configure(activebackground="#8224ed")
face_recognition.configure(activeforeground="white")
face_recognition.configure(background="#fff838")
face_recognition.configure(disabledforeground="#a22796")
face_recognition.configure(text='''Recognize emotion''')

#############################close ###############3
close = tk.Button(root,command = reset_library)
close.place(relx=0.38, rely=0.137, height=31, width=199)
close.configure(background="#fff838")
close.configure(activebackground="#8224ed")
close.configure(activeforeground="white")
close.configure(text='''reset''')

#############volume ##########################3333
volume = tk.Scale(root, from_=0.0, to=100.0,command=set_volume)
volume.place(relx=0.347, rely=0.213, relwidth=0.233, relheight=0.0
                , height=42, bordermode='ignore')
volume.configure(activebackground="#1fed33")
volume.configure(background="#fff838")
volume.configure(length="278")
volume.configure(orient="horizontal")
volume.configure(troughcolor="#d9d9d9")

#################play and pause button ####################33
def cb(event):
    global index
    index = index+1
    song_name['text'] = real_name[index]
    f = open('img.jpeg','wb')
    f.write(images[index])
    f.close()
    load = Image.open('/home/kklg/ai_music/img.jpeg')
    load.save('/home/kklg/ai_music/img.png')
    img = PhotoImage(file ='img.png')
    song_image.configure(image=img)
    song_image.image = img
    
    if all_lyrics[real_name[index]]:
        lyrics.delete('1.0',END)
        lyrics.insert(tk.END,all_lyrics[real_name[index]])
        
    else:
        lyrics.delete('1.0',END)
        lyrics.insert(tk.END,'No Lyrics available in my memory')

mp_em = mp.event_manager()
mp_em.event_attach(vlc.EventType.MediaPlayerEndReached, cb)
mp.audio_set_volume(50)






#############all auxullary function #################

def play_music():
    
    mlp.play()
    global index 
    
    song_name['text'] = real_name[index]
    f = open('img.jpeg','wb')
    f.write(images[index])
    f.close()
    load = Image.open('/home/kklg/ai_music/img.jpeg')
    load.save('/home/kklg/ai_music/img.png')
    img = PhotoImage(file ='img.png')
    song_image.configure(image=img)
    song_image.image = img
    
    
def pause_music():
    mlp.pause()
def stop_music():
    mlp.stop()
    global index 
    index =0
def next_song():
    mlp.next()
    global index  
    index = index+1
    song_name['text'] = real_name[index]
    f = open('img.jpeg','wb')
    f.write(images[index])
    f.close()
    load = Image.open('/home/kklg/ai_music/img.jpeg')
    load.save('/home/kklg/ai_music/img.png')
    img = PhotoImage(file ='img.png')
    song_image.configure(image=img)
    song_image.image = img
    
    if all_lyrics[real_name[index]]:
        lyrics.delete('1.0',END)
        lyrics.insert(tk.END,all_lyrics[real_name[index]])
        
    else:
        lyrics.delete('1.0',END)
        lyrics.insert(tk.END,'No Lyrics available in my memory')
def prev_song():
    mlp.previous()
    global index  
    index = index -1
    song_name['text'] = real_name[index]
    f = open('img.jpeg','wb')
    f.write(images[index])
    f.close()
    load = Image.open('/home/kklg/ai_music/img.jpeg')
    load.save('/home/kklg/ai_music/img.png')
    img = PhotoImage(file ='img.png')
    song_image.configure(image=img)
    song_image.image = img
    
    if all_lyrics[real_name[index]]:
        lyrics.delete('1.0',END)
        lyrics.insert(tk.END,all_lyrics[real_name[index]])
        
    else:
        lyrics.delete('1.0',END)
        lyrics.insert(tk.END,'No Lyrics available in my memory')
def choose_song():
    global index 
    index_str =song_list.curselection()
    index =int(index_str[0])
    mlp.play_item_at_index(index)
    song_name['text'] = real_name[index]
    f = open('img.jpeg','wb')
    f.write(images[index])
    f.close()
    load = Image.open('/home/kklg/ai_music/img.jpeg')
    load.save('/home/kklg/ai_music/img.png')
    img = PhotoImage(file ='img.png')
    song_image.configure(image=img)
    song_image.image = img
    
    if all_lyrics[real_name[index]]:
        lyrics.delete('1.0',END)
        lyrics.insert(tk.END,all_lyrics[real_name[index]])
        
    else:
        lyrics.delete('1.0',END)
        lyrics.insert(tk.END,'No Lyrics available in my memory')
        
############################
select_and_play = tk.Button(root,command=choose_song)
select_and_play.place(relx=0.38, rely=0.304, height=31, width=199)
select_and_play.configure(background="#fff838")
select_and_play.configure(activebackground="#8224ed")
select_and_play.configure(disabledforeground="#a22796")
select_and_play.configure(text='''select and play''')

##
Label2_1 = tk.Button(root,command=next_song)
Label2_1.place(relx=0.536, rely=0.38, height=31, width=89)
Label2_1.configure(activebackground="#8224ed")
Label2_1.configure(background="#fff838")

Label2_1.configure(highlightbackground="#d834c8")
Label2_1.configure(text='''next''')

Label2_2 = tk.Button(root,command=pause_music)
Label2_2.place(relx=0.429, rely=0.38, height=31, width=99)
Label2_2.configure(activebackground="#8224ed")
Label2_2.configure(background="#fff838")

Label2_2.configure(highlightbackground="#d834c8")
Label2_2.configure(text='''pause''')

Label2_3 = tk.Button(root,command=prev_song)
Label2_3.place(relx=0.33, rely=0.38, height=31, width=89)
Label2_3.configure(activebackground="#8224ed")
Label2_3.configure(background="#fff838")

Label2_3.configure(highlightbackground="#d834c8")
Label2_3.configure(text='''prev''')



#image for song 
image_of_song = PhotoImage(file='img.png')
song_image = tk.Label(root,image=image_of_song)
song_image.place(relx=0.289, rely=0.471, height=331, width=479)
song_image.configure(disabledforeground="#a22796")

song_name = tk.Label(root)
song_name.place(relx=0.289, rely=0.935, height=41, width=476)
song_name.configure(activebackground="#f877e6")
song_name.configure(background="#fffbfa")
song_name.configure(disabledforeground="#a22796")
song_name.configure(highlightbackground="#d834c8")
song_name.configure(text='''no song is in play mode''')



root.mainloop()