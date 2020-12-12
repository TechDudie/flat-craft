import hashlib
import tkinter
import pygame
import threading
import numpy
import time
import os
import math
import gc
gc.disable()
root = tkinter.Tk()
root.title("PyCraft 2D")
game_on = False
action_db = []
action_id = 0
def create_world():
    global nw
    nw = tkinter.Tk()
    nw.title("New World")
    seed_frame = tkinter.Frame(nw)
    seed_frame.pack()
    w = tkinter.Label(seed_frame, text="")
    w.pack(padx=100, pady=20, side=tkinter.LEFT)
    w = tkinter.Label(seed_frame, text="Seed:")
    w.pack(padx=5, pady=20, side=tkinter.LEFT)
    global d
    d = tkinter.Text(seed_frame, height=0, width=32)
    d.pack(padx=5, pady=20, side=tkinter.LEFT)
    w = tkinter.Label(seed_frame, text="")
    w.pack(padx=100, pady=20, side=tkinter.TOP)
    w = tkinter.Button(nw, text="Done", bg="gray", fg="white", command=read_seed)
    w.pack(fill=tkinter.X, pady=10, padx=250, ipadx=80)
    nw.mainloop()
def read_seed():
    seed = d.get("1.0","end-1c")
    print(seed)
    global seed_hash
    seed_hash = eval("hashlib.md5(b\"" + seed + "\").hexdigest()")
    print(seed_hash)
    nw.destroy()
def render_world(seed_hash_input):
    hex_list = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "a": 10,
        "b": 11,
        "c": 12,
        "d": 13,
        "e": 14,
        "f": 15
    }
    global g
    g = tkinter.Tk()
    g.title("Game")
    global c
    c = tkinter.Canvas(width=512, height=544,bg='skyblue')
    c.bind("<Key>", item_switch)
    c.bind("<Button-1>", break_block)
    c.bind("<Button-3>", place_block)
    c.pack()
    tree_loc_str = seed_hash_input[1:2]
    tree_loc = hex_list[tree_loc_str]
    landscape.tree(tree_loc,1)
    landscape.ground()
    frame = tkinter.PhotoImage(file=r"textures/default/frame.png")
    grass_item = tkinter.PhotoImage(file=r"textures/default/grass_item.png")
    dirt_item = tkinter.PhotoImage(file=r"textures/default/dirt_item.png")
    log_item = tkinter.PhotoImage(file=r"textures/default/log_item.png")
    leaf_item = tkinter.PhotoImage(file=r"textures/default/leaf_item.png")
    root.frame = frame
    root.grass_item = grass_item
    root.dirt_item = dirt_item
    root.log_item = log_item
    root.leaf_item = leaf_item
    c.create_image(192, 512, image=frame, anchor=tkinter.NW)
    c.create_image(224, 512, image=frame, anchor=tkinter.NW)
    c.create_image(256, 512, image=frame, anchor=tkinter.NW)
    c.create_image(288, 512, image=frame, anchor=tkinter.NW)
    c.create_image(192, 512, image=grass_item, anchor=tkinter.NW)
    c.create_image(224, 512, image=dirt_item, anchor=tkinter.NW)
    c.create_image(256, 512, image=log_item, anchor=tkinter.NW)
    c.create_image(288, 512, image=leaf_item, anchor=tkinter.NW)
def render_block(posx,posy,img,action_id_p):
    action_db.append(tkinter.PhotoImage(file="textures/default/" + img + ".png"))
    c.create_image(posx, posy, image=action_db[action_id_p], anchor=tkinter.NW)
def delete_world():
    choice = input("Are you sure? [Y/N] ")
    lower_choice = choice.lower()
    if lower_choice == "y" or lower_choice == "yes":
        print("Deleting...")
        time.sleep(1)
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("Done", end="")
        try:
            os.rmdir("world")
        except:
            print(" with an error: world does not exist", end="")
        print(".")
def connect():
    global game_on
    game_on = True
    root.destroy()
def select_frame():
    selected_frame_id = 0
    prev = 0
    selected_frame = tkinter.PhotoImage(file=r"textures/default/selected_frame.png")
    root.selected_frame = selected_frame
    selection_db = []
    selection_db.append(c.create_image(selected_frame_id * 32 + 192, 512, image=selected_frame, anchor=tkinter.NW))
    selection_id = 1
    while True:
        selected_frame_id_file = open("other_data/selected.txt","r")
        try:
            selected_frame_id = int(selected_frame_id_file.read()) - 1
        except:
            pass
        if selected_frame_id != prev:
            prev = selected_frame_id
            selection_db.append(c.create_image(selected_frame_id * 32 + 192, 512, image=selected_frame, anchor=tkinter.NW))
            c.delete(selection_db[selection_id - 1])
            selection_id = selection_id + 1
def item_switch(event):
    file = open("other_data/selected.txt","w")
    char_str = repr(event.char)
    file.write(char_str[1:2])
    file.close()
def break_block(event):
    c.focus_set()
    global action_id
    block_x = math.floor(event.x / 32) * 32
    block_y = math.floor(event.y / 32) * 32
    render_block(block_x,block_y,"air",action_id)
    action_id = action_id + 1
def place_block(event):
    global action_id
    img_names = {
        1: "grass",
        2: "dirt",
        3: "log",
        4: "leaf"
    }
    selected_frame_id = 1
    block_x = math.floor(event.x / 32) * 32
    block_y = math.floor(event.y / 32) * 32
    selected_frame_id_file = open("other_data/selected.txt","r")
    try:
        selected_frame_id = int(selected_frame_id_file.read())
    except:
        pass
    img_name = img_names[selected_frame_id]
    render_block(block_x,block_y,img_name,action_id)
    action_id = action_id + 1
def music():
    music_array = ["a.mp3","b.mp3","c.mp3","d.mp3","e.mp3","f.mp3","g.mp3","h.mp3"]
    numpy.random.shuffle(music_array)
    pygame.mixer.init()
    while True:
        pygame.mixer.music.load("soundtrack/default/" + music_array[0])
        pygame.mixer.music.play()
        while True:
            if pygame.mixer.music.get_busy() == 0:
                break
        time.sleep(1)
        pygame.mixer.music.load("soundtrack/default/" + music_array[1])
        pygame.mixer.music.play()
        while True:
            if pygame.mixer.music.get_busy() == 0:
                break
        time.sleep(1)
        pygame.mixer.music.load("soundtrack/default/" + music_array[2])
        pygame.mixer.music.play()
        while True:
            if pygame.mixer.music.get_busy() == 0:
                break
        time.sleep(1)
        pygame.mixer.music.load("soundtrack/default/" + music_array[3])
        pygame.mixer.music.play()
        while True:
            if pygame.mixer.music.get_busy() == 0:
                break
        time.sleep(1)
        pygame.mixer.music.load("soundtrack/default/" + music_array[4])
        pygame.mixer.music.play()
        while True:
            if pygame.mixer.music.get_busy() == 0:
                break
        time.sleep(1)
        pygame.mixer.music.load("soundtrack/default/" + music_array[5])
        pygame.mixer.music.play()
        while True:
            if pygame.mixer.music.get_busy() == 0:
                break
        time.sleep(1)
        pygame.mixer.music.load("soundtrack/default/" + music_array[6])
        pygame.mixer.music.play()
        while True:
            if pygame.mixer.music.get_busy() == 0:
                break
        time.sleep(1)
        pygame.mixer.music.load("soundtrack/default/" + music_array[7])
        pygame.mixer.music.play()
        while True:
            if pygame.mixer.music.get_busy() == 0:
                break
        time.sleep(1)
        numpy.random.shuffle(music_array)
def splash_screen_change():
    splash_screen = ["Hello World!","20 GOTO 10!","Call your mother!","Guess what?","Oops.","Oh man!","What happened?","OMG!","Never Mind.","Gibberish!","Did you finish your homework?","Fun!","274 lines of code!"]
    while True:
        try:
            numpy.random.shuffle(splash_screen)
            time.sleep(0.1)
            sv.set(splash_screen[0])
            time.sleep(9.9)
        except:
            pass
class landscape:
    def tree(loc,height):
        leaf = tkinter.PhotoImage(file=r"textures/default/leaf.png")
        root.leaf = leaf
        log = tkinter.PhotoImage(file=r"textures/default/log.png")
        root.log = log
        c.create_image(loc * 32 - 32, 320 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32 - 32, 320 - height * 32))
        c.create_image(loc * 32, 320 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32, 320 - height * 32))
        c.create_image(loc * 32 + 32, 320 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32 + 32, 320 - height * 32))
        c.create_image(loc * 32 - 64, 352 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32 - 64, 352 - height * 32))
        c.create_image(loc * 32 - 32, 352 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32 - 32, 352 - height * 32))
        c.create_image(loc * 32, 352 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32, 352 - height * 32))
        c.create_image(loc * 32 + 32, 352 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32 + 32, 352 - height * 32))
        c.create_image(loc * 32 + 64, 352 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32 + 64, 352 - height * 32))
        c.create_image(loc * 32 - 64, 384 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32 - 64, 384 - height * 32))
        c.create_image(loc * 32 - 32, 384 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32 - 32, 384 - height * 32))
        c.create_image(loc * 32, 384 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32, 384 - height * 32))
        c.create_image(loc * 32 + 32, 384 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32 + 32, 384 - height * 32))
        c.create_image(loc * 32 + 64, 384 - height * 32, image=leaf, anchor=tkinter.NW, tags=(loc * 32 + 64, 384 - height * 32))
        c.create_image(loc * 32, 416 - height * 32, image=log, anchor=tkinter.NW, tags=(loc * 32, 416 - height * 32))
        c.create_image(loc * 32, 448 - height * 32, image=log, anchor=tkinter.NW, tags=(loc * 32, 448 - height * 32))
        c.create_image(loc * 32, 480 - height * 32, image=log, anchor=tkinter.NW, tags=(loc * 32, 480 - height * 32))
    def ground():
        grass = tkinter.PhotoImage(file=r"textures/default/grass.png")
        root.grass = grass
        for i in range(0,16):
            c.create_image(i * 32, 480, image=grass, anchor=tkinter.NW, tags=(i * 32, 480))
background_image1=tkinter.PhotoImage(file="other_data/label_background1.png")
background_image2=tkinter.PhotoImage(file="other_data/label_background2.png")
### music_thread = threading.Thread(target=music)
### music_thread.start()
background_image=tkinter.PhotoImage(file="other_data/background.png")
background_label = tkinter.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
w = tkinter.Label(root, text="", bg="skyblue")
w.pack(fill=tkinter.X, pady=50)
w = tkinter.Label(root, text="PyCraft 2D", font=("Helvetica", 48), bg="skyblue")
w.pack(fill=tkinter.X)
sv = tkinter.StringVar()
w = tkinter.Label(root, text="Hello World", textvariable=sv, image=background_image1, compound="center", bd=0)
w.pack(fill=tkinter.X, pady=20)
w = tkinter.Label(root, image=background_image2, bd=0)
w.pack(fill=tkinter.X)
splash_thread = threading.Thread(target=splash_screen_change)
splash_thread.start()
w = tkinter.Label(root, image=background_image2, bd=0)
w.pack(fill=tkinter.X, pady=20)
w = tkinter.Button(root, text="Create", bg="gray", fg="white", command=create_world, bd=0, relief="raised")
w.pack(fill=tkinter.X, pady=10, padx=250, ipadx=80)
w = tkinter.Button(root, text="Delete", bg="gray", fg="white", command=delete_world, bd=0, relief="raised")
w.pack(fill=tkinter.X, pady=10, padx=250, ipadx=80)
w = tkinter.Button(root, text="Play", bg="gray", fg="white", command=connect, bd=0, relief="raised")
w.pack(fill=tkinter.X, pady=10, padx=250, ipadx=80)
w = tkinter.Label(root, text="", bg="#693b00")
w.pack(fill=tkinter.X, pady=5, padx=10)
root.mainloop()
if game_on == True:
    try:
        render_world(seed_hash)
        select_thread = threading.Thread(target=select_frame)
        select_thread.start()
        g.mainloop()
    except:
        pass