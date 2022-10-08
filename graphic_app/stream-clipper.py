import os
import time
from tkinter import *
#from tkinter import filedialog
from threading import Thread
import sys
import cv2
from PIL import Image
from PIL import ImageTk
import subprocess

#rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4

catchup_frames = 60
file_dir = './test-images'
starting_frame = 0
fd_gate = True
export_dir = './exports'
rtsp_subp = None

#GUI_STUFF----------------
root = Tk()
root.title("Stream Clipper Tool")
img_frame = Frame(root, highlightbackground='black', highlightthickness=2)
img_frame.pack()
img_label = Label(img_frame)
img_label.pack(side = LEFT)
b_frame = Frame(root, highlightbackground='black', highlightthickness=2)
b_frame.pack()

saveclip_button = Button(b_frame, text = 'Save Clip', fg = 'black')
saveclip_button.pack(side = LEFT)

def save_clip_images(event):#need to update
    global fd_gate, catchup_frames,starting_frame

    #Stop the file deletion
    fd_gate = False

    #Copy all the files with all the catchup frames to the exports dir

    image_arr = []

    for i in range(0, catchup_frames):
        curr_num = starting_frame + i
        curr_img = cv2.imread("./test-images/frame{a}.jpeg".format(a = curr_num))
        height, width, layers = curr_img.shape
        size = (width, height)
        image_arr.append(curr_img)

    num_of_exports = len(os.listdir("./exports"))

    out = cv2.VideoWriter('{p}/exports/clip{a}.mp4'.format(p = os.getcwd(), a = num_of_exports + 1),cv2.VideoWriter_fourcc(*'MP4V'), 30, size)

    for img in image_arr:
        out.write(img)

    out.release()

    #Restart the deletion thread
    fd_gate = True

saveclip_button.bind("<Button-1>", save_clip_images)

quit_button = Button(b_frame, text = 'Quit', fg = 'black')
quit_button.pack(side = LEFT)

def quit_system(event):#working
    global rtsp_subp

    #rtsp_subp.terminate()
    root.destroy()
    sys.exit()

quit_button.bind("<Button-1>", quit_system)

def delete_all_files():#working 

    global catchup_frames
    num_files_in_dir = len(os.listdir(file_dir))

    if num_files_in_dir <- catchup_frames:
        return

    num_files_todel = num_files_in_dir - catchup_frames

    for i in range(0, num_files_todel):
        delete_file_at_frame()

def delete_file_at_frame():#working
    global starting_frame
    os.remove("{a}/frame{b}.jpeg".format(a = file_dir, b = starting_frame))
    starting_frame = starting_frame + 1


def file_deleter():#Need to test

    global fd_gate

    while True:
        if fd_gate == False:
            continue

        delete_all_files()
        time.sleep(1/60)

def cv_to_tk(image):#working

    tk_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tk_image = Image.fromarray(tk_image)
    tk_image = ImageTk.PhotoImage(tk_image)
    
    return tk_image

def image_updater():

    global starting_frame

    while len(os.listdir('./test-images')) == 0:
        time.sleep(.1)

    prev_image_num = 0

    time.sleep(3)

    while True: 
        start = time.time()

        image_num = len(os.listdir('./test-images')) + starting_frame - 3 
        if image_num == prev_image_num:
            time.sleep(1/60)
            continue
        latest_img = cv2.imread('./test-images/frame{a}.jpeg'.format(a = image_num))
        tk_latest = cv_to_tk(latest_img)
        #We need to convert the opencv image to tk image
        img_label.configure(image = tk_latest)
        time.sleep(max(0, 1/60 - (time.time() - start)))
        prev_image_num = image_num

#This is the thread section
deletion_thread = Thread(target = file_deleter)
deletion_thread.setDaemon(True)
image_update_thread = Thread(target = image_updater)
image_update_thread.setDaemon(True)

def main():
    #Start the deletion thread
    global rtsp_subp

    #Now the deletion thread and the image update thread just have to start

    global deletion_thread, image_update_thread

    deletion_thread.start()
    image_update_thread.start()

    root.mainloop()

    print("Threads + GUI are now running")



if __name__ == '__main__':
    print('Starting Stream Clipper GUI tool. . .')
    main()


