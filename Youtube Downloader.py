import tkinter 
from tkinter import ttk
import pytube
import os
import pyperclip
import datetime

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1) # remove blur


username = os.getlogin()
save_dir = f'C:/users/{username}/Downloads/Youtube_downloader'

root =tkinter.Tk()
# root.tkinter.call('tk', 'scaling', 2.0)
# root.configure(bg='#000000')
root.title('Youtube Audio/Video Downloader')
root.geometry('555x300')


root.option_add('*Font', 'aerial 10')
# root.option_add('*Entry.font','aerial 8 italic')
# root.option_add('*Entry.foreground','blue')
# root.option_add('*Button.background','#990000')
# root.option_add('*Button.foreground','#ffffff')

#_____________________________________________ PYTUBE FUNCTIONS _____________________________________________

'''Progressive video has both audio and video on same .mp4 file
but are availablle only upto 720p

Higher resolution video are on non-progressive_combobox or adaptive form( as per pytube module docs)
so audio and video files have to be downloaded separately and then merged.
which takes quite a bit of time using moviepy module

'''
# def set_download_path():
#     username = os.getlogin()
#     pytube.helpers.target_directory(f"C:/users/{username}/Downloads/Youtube_downloader")

def download_audio():
    message.config(text='Audio is Downloading :)')
    audio = available_streams.get_audio_only()
    video.streams.get_by_itag(audio.itag).download(filename = f'{save_dir}/{video.title}_{audio.abr}.mp3')
    message.config(text='Audio Download completed :)')

   

def get_available_progressive_video_resolution():
    available_progressive_video_list = [720,480,360,240,144]
    q720p = available_streams.get_by_resolution('720p')
    if q720p is None:
        available_progressive_video_list.remove(720)
    q480p = available_streams.get_by_resolution('480p')
    if q480p is None:
        available_progressive_video_list.remove(480)
    q360p = available_streams.get_by_resolution('360p')
    if q360p is None:
        available_progressive_video_list.remove(360)
    q240p = available_streams.get_by_resolution('240p')
    if q240p is None:
        available_progressive_video_list.remove(240)
    q144p = available_streams.get_by_resolution('144p')
    if q144p is None:
        available_progressive_video_list.remove(144)

    return available_progressive_video_list


def download_progressive_video(resolution:str):
    message.config(text='Video is Downloading :)')
    video.streams.get_by_resolution(resolution).download(filename = f'{save_dir}/{video.title}_{resolution}.mp4')
    message.config(text=f'{resolution} Video Download completed :)')
    view_download_location_button.grid(row = 2, column = 3)

def get_available_adaptive_video_resolution():
    
    available_adaptive_video_list = []
    x = video.streams.filter(adaptive = True,resolution = '1080p')
    if len(x) != 0:
        available_adaptive_video_list.append((1080,x[0].itag))

    a = video.streams.filter(adaptive = True,resolution = '1440p')
    if len(a) != 0:
        available_adaptive_video_list.append((1440,a[0].itag))

    b = video.streams.filter(adaptive = True,resolution = '2160p')
    if len(b) != 0:
        available_adaptive_video_list.append((2160,b[0].itag))

    c = video.streams.filter(adaptive = True,resolution = '4320p')
    if len(c) != 0:
        available_adaptive_video_list.append((4320,c[0].itag))

    return available_adaptive_video_list



def merge(audio_path,video_path,saveas):
    import moviepy.editor as mpe
    clip = mpe.VideoFileClip(video_path)
    clip.write_videofile(saveas,audio =audio_path)
    clip.close()


def download_adaptive_video(resolution):
    tag = video.streams.filter(resolution=f'{resolution}p', adaptive= True)[0].itag

    message.config(text='1. Video is downloading :)')
    # video.streams.get_by_itag(itag).download(filename = f'{video.title}_{resolution}p.mp4')

    video.streams.get_by_itag(tag).download(filename = 'merge_video.mp4')
    message.config(text='2. Audio is downloading :)')
    audio = available_streams.get_audio_only()
    video.streams.get_by_itag(audio.itag).download(filename = 'merge_audio.mp3')
    message.config(text='3. Audio and Video are Merging together, Patience is key to success :)')
    merge('merge_audio.mp3','merge_video.mp4',saveas = f'{save_dir}/{video.title}_{resolution}p.mp4')
    
    import os
    os.remove('merge_video.mp4')
    os.remove('merge_audio.mp3')

    message.config(text=f'{resolution}p Video Download completed :)')
    view_download_location_button.grid(row = 2, column = 3)




#----------------------------- END OF PYTUBE MODULES-----------------------------
#----------------------------- Start of tkinter functions-----------------------------


def read_link():
    download_video_button_progressive.grid_remove()
    download_video_button_adaptive.grid_remove()
    fast.grid_remove()
    slow.grid_remove()
    progressive_combobox.grid_remove()
    adaptive_combobox.grid_remove()
    message.config(text='Scanning Link')
    global link
    link = pyperclip.paste()
    link_entry.delete(0,'end')
    link_entry.insert(0,link)
    global video
    global available_streams

    try:
        message.config(text ="Invalid link :(")
        video = pytube.YouTube(link)
    except Exception:
        message.config(text ="Invalid link :(")
        return
    available_streams = video.streams
    message.config(text='Link is valid :)')
    video_details.config(text= f'[{str(datetime.timedelta(seconds = video.length))}] {video.title[0:40]}')
    # set_download_path()
    # audio_download_button.config(state='active')
    # choose_video_resolution_button.config(state='active')
    audio_download_button.grid(row = 5, column= 1, padx = 10,pady = 30)
    choose_video_resolution_button.grid(row = 5, column= 2, padx = 10,pady = 30)

def download_audio_command():
    download_audio()
    message.config(text='Audio Download completed')
    view_download_location_button.grid(row = 2, column = 3)
    
    
def show_available_videos():
    global a
    a = get_available_adaptive_video_resolution()
    p = get_available_progressive_video_resolution()
    adaptive_list = []
    for items in a:
        adaptive_list.append(items[0])
    progressive_combobox.config(values = p)
    adaptive_combobox.config(values=adaptive_list)
    progressive_combobox.grid(row =6, column=2, )
    fast.grid(row = 6,column =1)
    adaptive_combobox.grid(row = 7, column=2, )
    slow.grid(row = 7,column =1,pady=10)

    

def download_video():
    show_available_videos()



def change_download_button_progressive(wtf):
    resolution = progressive_combobox.get()
    download_video_button_progressive.config(text=f'Download {resolution}p (fast)',state='active')
    download_video_button_progressive.grid(row = 6, column = 1, )

def change_download_button_adaptive(wtf):
    resolution = adaptive_combobox.get()
    download_video_button_adaptive.config(text=f'Download {resolution}p (slow)',state='active')

    download_video_button_adaptive.grid(row = 7, column = 1, )

def open_save_dir():
    os.startfile(save_dir)

#----------------------------- END of tkinter functions-----------------------------
#----------------------------- Start of tkinter widgets-----------------------------
message = ttk.Label(root,text=':)')
video_details = ttk.Label(root)
link_entry = ttk.Entry(root,width = 45)
link_entry.insert(0,'Please paste your link and wait for 10s...')

Paste_buttom = ttk.Button(root, text= 'Paste & Submit',command=read_link)

audio_download_button = ttk.Button(root, text='Download Audio',command= download_audio_command)

view_download_location_button = ttk.Button(root, text='View save location', command= open_save_dir)

fast = ttk.Label(root,text='Fast Download',anchor='s')
slow = ttk.Label(root,text='Slow Download')

choose_video_resolution_button = ttk.Button(root, text='Choose video quality',command= download_video)

download_video_button_progressive = ttk.Button(root, text= 'Download',state = 'disabled',command =lambda: download_progressive_video(f'{progressive_combobox.get()}p'))
download_video_button_adaptive = ttk.Button(root, text= 'Download',state = 'disabled',command=lambda: download_adaptive_video(adaptive_combobox.get()))

progressive_combobox = ttk.Combobox(root,width=7,state='readonly')
adaptive_combobox = ttk.Combobox(root,width=7,state='readonly')
progressive_combobox.bind('<<ComboboxSelected>>',change_download_button_progressive)
adaptive_combobox.bind('<<ComboboxSelected>>',change_download_button_adaptive)


message.grid(row = 2, column = 1,columnspan=2 , pady=5)
link_entry.grid(row = 0, column = 1, columnspan=2,padx=5)
Paste_buttom.grid(row = 0 , column = 3,pady = 10)
video_details.grid(row =1,column = 1,columnspan=2)

root.mainloop()