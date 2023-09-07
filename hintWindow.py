#@ Shreesh Shrestha 
# Hint Window for Hangman 

import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import csv
import sys
from util import Node, QueueFrontier
import os

# Create a new window for hint 
window2 = tk.Tk()
window2.geometry('700x600')
window2.title('HINT')
window2.resizable(False, False)

#One piece font
global opFont
opFont ="ONE PIECE"

#import hintbg
hint_bg = Image.open(r"C:\Users\shree\OneDrive\Documents\NYIT\Programming\One Piece Game\Pictures\luffy-one-piece.gif").resize((700,600))
hint_bg_tk = ImageTk.PhotoImage(hint_bg)
    
    
#canvas for hint window
canvas2 = tk.Canvas(window2, width=700, height=600,bd = 0, highlightthickness=0, relief= 'ridge')
canvas2.pack()
canvas2.create_image(0, 0, anchor=tk.NW, image=hint_bg_tk)

# retrive the hangman word
global hangman_word
hangman_word = os.environ.get('THE_WORD')

# Maps names to a set of corresponding character_ids
names = {}

# Maps character_ids to a dictionary of: name, code, arcs (a set of arc_ids)
opcharacters = {}

# Maps arc_ids to a dictionary of: title, year, connections (a set of character_ids)
arcs = {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load opcharacters
    with open(f"{directory}/opcharacters.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            opcharacters[row["id"]] = {
                "name": row["name"],
                "code": row["code"],
                "arcs": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load arcs
    with open(f"{directory}/arcs.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            arcs[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "connections": set()
            }

    # Load connections
    with open(f"{directory}/connections.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                opcharacters[row["character_id"]]["arcs"].add(row["arc_id"])
                arcs[row["arc_id"]]["connections"].add(row["character_id"])
            except KeyError:
                pass


def main():
    global display_text
    display_text = tk.Text(canvas2, wrap=tk.WORD, font=(opFont,14), background="black", foreground="white")
    display_text.place(relx=0.23, rely=0.15, anchor=tk.CENTER, relwidth=0.4, relheight=0.2)
    
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")

    directory = "small"
    
    # Load data from files into memory
    load_data(directory)
    
    source = character_id_for_name("Luffy")
    
    target = character_id_for_name(hangman_word)
    if target is None:
        display_text.insert(tk.END, "Person not found." + " ")
        sys.exit("Person not found.")
        

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
        display_text.insert(tk.END, "Not connected." + " ")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        display_text.insert(tk.END, f"{degrees} degrees of separation." + " ")
        
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = opcharacters[path[i][1]]["name"]
            person2 = opcharacters[path[i + 1][1]]["name"]
            movie = arcs[path[i + 1][0]]["title"]
            
            
            
            if str(person1).lower() == hangman_word.lower():
                person1 = "(________)"
            elif str(person2).lower() == hangman_word.lower():
                person2 = "(________)"
            else:
                print(f"IDK")
                
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
            display_text.insert(tk.END, f"\n{i + 1}: {person1} and {person2} starred in {movie}" + " ")
            person1 = opcharacters[path[i][1]]["name"]
            person2 = opcharacters[path[i + 1][1]]["name"]
        global hint
        hint =1


def shortest_path(source, target):
    """
    Returns the shortest list of (arc_id, character_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    
    """
    # Frontier for BFS
    frontier = QueueFrontier()
    
    #starting node
    start = Node(state = source, parent = None, action = None)
    
    #Keeping track of expored state
    explored = set()
    
    #adding the starting node to the frontier
    frontier.add(start) 
    
    #searching until the frontier is Empty 
    
    while not frontier.empty():
        #get the next node
        node  = frontier.remove()
        
        #mark the node as explored
        explored.add(node.state)
        
        #check if the target character_id is found
        if node.state == target:
            #build a path form target to the source
            path = []
            
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()# reverse the path to start from the source
            
            return path

        #Expand the node by getting neighours
        neighbors = neighbors_for_person(node.state)
        for arc_id, character_id in neighbors:
            if character_id not in explored and not frontier.contains_state(character_id):
                child = Node(state = character_id, parent = node, action= arc_id)
                frontier.add(child)

    #Return none if no path is found 
    return None





def character_id_for_name(name):
    """
    Incomplete at the moment.
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    character_ids = list(names.get(name.lower(), set()))
    if len(character_ids) == 0:
        return None
    elif len(character_ids) > 1:
        print(f"Which '{name}'?")
        for character_id in character_ids:
            person = opcharacters[character_id]
            name = person["name"]
            code = person["code"]
            print(f"ID: {character_id}, Name: {name}, code: {code}")
        try:
            character_id = input("Intended Person ID: ")
            if character_id in character_ids:
                return character_id
        except ValueError:
            pass
        return None
    else:
        return character_ids[0]


def neighbors_for_person(character_id):
    """
    Returns (arc_id, character_id) pairs for opcharacters
    who starred with a given person.
    """
    arc_ids = opcharacters[character_id]["arcs"]
    neighbors = set()
    for arc_id in arc_ids:
        for character_id in arcs[arc_id]["connections"]:
            neighbors.add((arc_id, character_id))
    return neighbors

main()
window2.mainloop()



    

