#!/usr/bin/env python3
import sys, os, json, re
assert sys.version_info >= (3,9), "This script requires at least Python 3.9"

print("Earlier this morning while taking a stroll, you found a tiny little alien creature huddling in the forest! To your human eyes, it looked like something of a mixture between a cat and a bird, only the fur (feathers?) were neon green! Feeling pity on the small creature, you scooped it up and took it home. What do you want to name the creature? ")
name = input()
name = name.capitalize()
def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p 
    return{}

# Removes Harlowe formatting from Twison description
def format_passage(description):
    description = re.sub(r'//([^/]*)//',r'\1',description)
    description = re.sub(r"''([^']*)''",r'\1',description)
    description = re.sub(r'~~([^~]*)~~',r'\1',description)
    description = re.sub(r'\*\*([^\*]*)\*\*',r'\1',description)
    description = re.sub(r'\*([^\*]*)\*',r'\1',description)
    description = re.sub(r'\^\^([^\^]*)\^\^',r'\1',description)
    description = re.sub(r'(\[\[[^\|]*?)\|([^\]]*?\]\])',r'\1->\2',description)
    description = re.sub(r'\[\[([^(->\])]*?)->[^\]]*?\]\]',r'[ \1 ]',description)
    description = re.sub(r'\[\[(.+?)\]\]',r'[ \1 ]',description)
    return description

def update(current, choice, game_desc):
    if choice == "":
        return current
    for l in current["links"]:
        if l["name"].lower() == choice:
            current = find_passage(game_desc, l["pid"])
            return current
    print ("That is not a choice. Please try again.")
    return current
def render(current):
    print("\n\n")
    print(current["name"])
    print("\n")
    print(format_passage(current["text"]))
    print("\n")

def get_input():
    choice = input("Choose one. (Type quit to exit.) ")
    choice = choice.lower().strip()
    return choice



def main():
    game_desc = load("game.json")
    for item in game_desc["passages"]:
        item["text"] = item["text"].replace("xyz", name)
    current = find_passage(game_desc, game_desc["startnode"])
    choice = ""
    while choice != "quit" and current != {}:
        current = update(current, choice, game_desc)
        render(current)
        choice = get_input()
    print("Thanks for playing!")

if __name__ == "__main__":
  main()