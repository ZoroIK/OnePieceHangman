# @ Shreesh Shrestha 
#One Piece Hangman Game 

import tkinter as tk
import random
from words import hangman_words
import string 
from tkinter import ttk
from PIL import Image,ImageTk
import subprocess
import os


# Open hint window when hint button is clicked 
global hintOpened 
hintOpened = 0
def hint():
    
    global hintOpened
    
    if hintOpened !=1:
        subprocess.Popen(["python", "hintWindow.py"],shell = True)
        hintOpened = 1
    else:
        return 
    

# Game main canvas 
def button_click():
    print("Button clicked!(1)")
    #destroy canvas
    global canvas,ttk,opFont
    canvas.destroy()
    
    #grid Layout    
    window.rowconfigure((0,1,2,3), weight = 1)
    window.columnconfigure((0,1,2), weight = 1)
    

    #set the hintOpened value back to zerp
    global hintOpened
    hintOpened = 0
    #create a top  canvas to add the image
    global topCanvas
    topCanvas = tk.Canvas(window,width=700, height=50,background='black',bd = 0, highlightthickness=0, relief= 'ridge')
    topCanvas.create_image(0,0, image = topImage_tk, anchor = tk.NW)
    topCanvas.grid(column=0, columnspan=3, row=0, sticky='nsew')
    
    #create a mid  canvas to add the image
    global midCanvas
    midCanvas = tk.Canvas(window,width=700, height=50,background='white',bd = 0, highlightthickness=0, relief= 'ridge')
    midCanvas.create_image(0,0, image = midImage_tk, anchor = tk.NW)
    midCanvas.grid(column=0, columnspan=3, row=1, rowspan=2, sticky='nsew')
    
    #create a bottom canvas 
    global bottomCanvas
    bottomCanvas = tk.Canvas(window,width=700, height=50,background='white',bd = 0, highlightthickness=0, relief= 'ridge')
    bottomCanvas.create_image(0,0, image = bottom_tk, anchor= tk.NW)
    bottomCanvas.grid(column = 1, row =3, sticky='nsew')
    
    
    #create a entry frame 
    
    global entry_widget
    global comment_value
    comment_value = 0
    print("comment value ",comment_value)
    entry_frame = tk.Frame(bottomCanvas, background="black")
    entry_frame.pack(padx=20, pady=20)
    
    entry_label = tk.Label(entry_frame, text="GUESS A LETTER:", font=(opFont,14), foreground="white", background="black")
    entry_label.grid(row=0, column=0, padx=10, pady=5)
    
    entry_widget = tk.Entry(entry_frame)
    entry_widget.grid(row= 0, column=1, padx=10, pady=5)
    entry_widget.bind("<Return>", on_enter_pressed)
    
    bottomCanvas.create_window(140, 20, anchor=tk.CENTER, window=entry_frame)
    
    #create a diplay frame
    global display_text
    
    
    display_label = tk.Label(bottomCanvas, text="GUESSED LETTERS", font=(opFont,14), foreground="white", background="black")
    display_label.place(relx=0.9, rely=0.125, anchor=tk.CENTER, relwidth=0.2, relheight=0.2)
    display_text = tk.Text(bottomCanvas, wrap=tk.WORD, font=(opFont,14), background="black", foreground="white")
    display_text.place(relx=0.9, rely=0.3, anchor=tk.CENTER, relwidth=0.18, relheight=0.2)
    
    #hangman lives 
    global lives
    global c_word
    global letters_word
    global alphabet
    global used_letters
    lives = 5
    c_word = random_words(hangman_words)
    os.environ['THE_WORD'] = c_word
    letters_word = set(c_word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()
    #Display word 
    display_word = [letter if letter in used_letters else '-' for letter in c_word]
    word_label = tk.Label(bottomCanvas, text=display_word, font=(opFont,14), foreground="white", background="black")
    word_label.place(relx=0.5, rely=0.125, anchor=tk.CENTER, relwidth=0.2, relheight=0.2)
    display_lives(5)
    
    #hint button
    hint_button = tk.Button(bottomCanvas, text = '  Hint?', 
                   image = hint_tk, compound='left',  
                   command= hint,
                   bd = 2,
                   font= (opFont,14),
                   fg = "black",
                   highlightthickness=0,
                   bg="grey")
    hint_button.place(relx=0.5, rely=0.45, anchor=tk.CENTER, relwidth=0.125, 
                               relheight=0.189)



#Display lives left 
def display_lives(num):
    #Display Lives
    lives_button = tk.Button(bottomCanvas, text = '   '+str(num), 
                   image = heart_tk, compound='left',  
                   bd = 2,
                   font= (opFont,14),
                   fg = "white",
                   highlightthickness=0,
                   bg="grey")
    lives_button.place(relx=0.1, rely=0.45, anchor=tk.CENTER, relwidth=0.125, 
                               relheight=0.189)

#  Create a canvas when the game ends
def game_ended(value):
    print("They Lost")
    #destroy canvas
    global topCanvas,midCanvas,bottomCanvas,ttk,opFont
    
    if value == False:
        topCanvas.destroy()
        midCanvas.destroy()
        bottomCanvas.destroy()
    
       
        #create a new canvas
        global LostCanvas
        LostCanvas = tk.Canvas(window,width=700, height=50,background='white',bd = 0, highlightthickness=0, relief= 'ridge')
        LostCanvas.create_image(0,0, image = lost_image_tk, anchor= tk.NW)
        LostCanvas.grid(column = 1, row =0, rowspan = 4, sticky='nsew')
        
        word_label = tk.Label(LostCanvas, text="YOUR WORD WAS: " + c_word, font=(opFont,14), foreground="red")
        word_label.place(relx=0.85, rely=0.8, anchor=tk.CENTER, relwidth=0.3, relheight=0.05)
        
        
        playAgain_Button1 = tk.Button(LostCanvas, text = '   Play Again ', 
                   image = logo_tk, compound='left', 
                   command= lostPlay_again, 
                   bd = 2,
                   font= (opFont,14),
                   fg = "white",
                   highlightthickness=0,
                   bg=window.cget("bg"))
        playAgain_Button1.place(relx=0.85, rely=0.9, anchor=tk.CENTER, relwidth=0.2, 
                               relheight=0.1)
        
        
    else:
        topCanvas.destroy()
        midCanvas.destroy()
        bottomCanvas.destroy()
        
        #create a new canvas
        global winCanvas
        winCanvas = tk.Canvas(window,width=700, height=50,background='white',bd = 0, highlightthickness=0, relief= 'ridge')
        winCanvas.create_image(0,0, image = win_image_tk, anchor= tk.NW)
        winCanvas.grid(column = 1, row =0, rowspan = 4, sticky='nsew')
        
        word_label = tk.Label(winCanvas, text="YOUR WORD WAS: " + c_word, font=(opFont,14), foreground="red")
        word_label.place(relx=0.85, rely=0.8, anchor=tk.CENTER, relwidth=0.3, relheight=0.05)
        
        playAgain_Button = tk.Button(winCanvas, text = '   Play Again ', 
                   image = logo_tk, compound='left', 
                   command= winPlay_again, 
                   bd = 2,
                   font= (opFont,14),
                   fg = "white",
                   highlightthickness=0,
                   bg=window.cget("bg"))
        playAgain_Button.place(relx=0.85, rely=0.9, anchor=tk.CENTER, relwidth=0.2, 
                               relheight=0.1)

#play again function in both win and lose cases
def winPlay_again():

    winCanvas.destroy()
    
    button_click()
     
def lostPlay_again():
    LostCanvas.destroy()
    
    button_click()  
       
            
#import random word from words
def random_words(hangman_words):
    word = random.choice(hangman_words)
    while '-' in word or ' ' in word:
        word = random.choice(hangman_words)
    
    return word

# Hangman Game
def hangman(content):
    global lives
    global c_word
    global letters_word
    global alphabet
    global used_letters
    global comment_value
    
    user_input = content
    print(user_input)
   
    if user_input in alphabet - used_letters:
        used_letters.add(user_input)
        print(used_letters)
        display_text.insert(tk.END, user_input + " ")
        if user_input in letters_word:
             letters_word.remove(user_input)
        else:
            lives = lives -1
            change_pic(lives)
            
    elif user_input in used_letters:
            commentLabel("You have already guessed that letter")
            comment_value = 1
    else:
        print('Invalid Input')
    
    #Diplay current word
    display_word = [letter if letter in used_letters else '-' for letter in c_word]
    word_label = tk.Label(bottomCanvas, text=display_word, font=(opFont,14), foreground="white", background="black")
    word_label.place(relx=0.5, rely=0.125, anchor=tk.CENTER, relwidth=0.2, relheight=0.2)
    
    #check if got lives or the word is complete 
    if all(letter in used_letters for letter in c_word):
        game_ended(True)  # Pass True to indicate a successful completion
    elif lives == 0:
        game_ended(False) 

#Change picture in midCanvas with loss of lives  
def change_pic(value):
    if value == 4:
        midCanvas.create_image(0,0, image = midImage_tk2, anchor = tk.NW)
        midCanvas.grid(column=0, columnspan=3, row=1, rowspan=2, sticky='nsew')
        display_lives(value)
        
    if value ==3:
        midCanvas.create_image(0,0, image = midImage_tk3, anchor = tk.NW)
        midCanvas.grid(column=0, columnspan=3, row=1, rowspan=2, sticky='nsew')
        display_lives(value)
        
    if value ==2:
        midCanvas.create_image(0,0, image = midImage_tk4, anchor = tk.NW)
        midCanvas.grid(column=0, columnspan=3, row=1, rowspan=2, sticky='nsew')
        display_lives(value)
        
    if value == 1:
        midCanvas.create_image(0,0, image = midImage_tk5, anchor = tk.NW)
        midCanvas.grid(column=0, columnspan=3, row=1, rowspan=2, sticky='nsew')
        display_lives(value)
        
    
#Even functionto get the letter     
def on_enter_pressed(event):
    content= entry_widget.get()
    global comment_value
    global comment_label
    global display_text
    
    if len(content)==1 and content.isalpha():
        print("Entered:", content+" ")
        #display_text.insert(tk.END, content.upper() + " ")
        
        entry_widget.delete(0, tk.END)
        
        if comment_value==1:
            comment_label.destroy()
        
        comment_value=0
        hangman(content.upper())
    
    else:
        
        entry_widget.delete(0, tk.END)
        
        if comment_value != 1:
            commentLabel("Please Enter Letter Only")
    

        comment_value=1

#Comment label to comment in any user input mistakes
def commentLabel(label):
    global comment_label
    comment_label = tk.Label(bottomCanvas, text=label, font=(opFont,10), foreground="red", background="black")
    comment_label.grid(row=0, column=0, padx=10, pady=5)
    bottomCanvas.create_window(140, 40, anchor=tk.CENTER, window=comment_label)
          
    

# Create the main window
window = tk.Tk()
window.geometry('700x600')
window.title('One Piece Hangman')
window.resizable(False,False)

window.configure(bg = "black"  )

#font we will use through out the game
opFont ="ONE PIECE"

# Create a Canvas widget
canvas = tk.Canvas(window, width=700, height=600,bd = 0, highlightthickness=0, relief= 'ridge')
canvas.pack()

# Load the background image
background_image = Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\mainPicture.jpg").resize((700,600))
image_tk = ImageTk.PhotoImage(background_image)

#import images for hangman game 
top_image = Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\topFrame.jpg").resize((700,200))
topImage_tk = ImageTk.PhotoImage(top_image)

#import images for mid frame 
mid_image =  Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\firstslide (2).jpg").resize((700,300))
midImage_tk = ImageTk.PhotoImage(mid_image)

mid_image2 =  Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\secondslide.jpg").resize((700,300))
midImage_tk2 = ImageTk.PhotoImage(mid_image2)

mid_image3 =  Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\3rd slide.jpg").resize((700,300))
midImage_tk3 = ImageTk.PhotoImage(mid_image3)

mid_image4 =  Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\4thsilde.jpg").resize((700,300))
midImage_tk4 = ImageTk.PhotoImage(mid_image4)

mid_image5 =  Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\finalslide.jpg").resize((700,300))
midImage_tk5 = ImageTk.PhotoImage(mid_image5)

#import image for win frame
win_image = Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\winImage.jpg").resize((700,600))
win_image_tk = ImageTk.PhotoImage(win_image)

#import image for lost frame
lost_image = Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\lostImage.jpg").resize((700,600))
lost_image_tk = ImageTk.PhotoImage(lost_image)

#import images for bottom  frame 
bottom_image =  Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\skull-wallpaper-preview.jpg").resize((700,250))
bottom_tk = ImageTk.PhotoImage(bottom_image)

#import heart logo
heart_image =  Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\love.png").resize((40,30))
heart_tk = ImageTk.PhotoImage(heart_image)

#import hint logo
hint_image =  Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\hintLogo.png").resize((30,25))
hint_tk = ImageTk.PhotoImage(hint_image)

#import hintbg
hint_bg = Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\lostImage.jpg").resize((700,600))
hint_bg_tk = ImageTk.PhotoImage(hint_bg)

# Display the background image on the Canvas
canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)


# Import image for the button 
image_logo= Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\buttonlogo.jpg").resize((40,30))
logo_tk = ImageTk.PhotoImage(image_logo)




# Create a button and place it on top of the background image
button = tk.Button(canvas, text = '   Start Game ', 
                   image = logo_tk, compound='left', 
                   command=button_click, 
                   bd = 2,
                   font= (opFont,14),
                   fg = "white",
                   highlightthickness=0,
                   bg=window.cget("bg"))

canvas.create_window(350, 550, anchor=tk.CENTER, window=button)



# Run the main window's event loop
window.mainloop()
