# this will contain Functions to control music playback using pygame
import pygame.mixer  #mixer module is just like a cd player it lets you play mp3 songs
# import pygame library's mixer module for audio
pygame.mixer.init()
# initialize mixer system -- required before using any audio

playlist=[]#global playlist
current_index=0#current song tracker

#set the playlist this will be called from main
def setPlaylist(songs):
 global playlist
 playlist=songs

# funtion to play music 
def playMusic(filepath):
# loads and plays an mp3 
 pygame.mixer.music.load(filepath)#load the file into memory
 pygame.mixer.music.play()#play music

#function to stop currently playing music
def pause():
 #pauses the audio .. can be resumed with unpause()
 pygame.mixer.music.pause() #freezes the audio

#function to unpause i.e to resume the paused song
def unpause():
 pygame.mixer.music.unpause()#resumes from where it was paused

#function to stop playback completely
def stop():
 pygame.mixer.music.stop()#ends the playback and clears the loaded song

# play next song
def play_next():
 global current_index
 if current_index<len(playlist)-1:
  current_index+=1
  playMusic(playlist[current_index])
 else:
  print("at the end of the playlist 🎵")

#play previous
def play_previous():
 global current_index
 if current_index>0:
  current_index-=1
  playMusic(playlist[current_index])
 else:
  print("already at first song 🎵")
  