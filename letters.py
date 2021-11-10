from random import  choice

class letters():
    def __init__(self):
        self.letters = {}
        
    def make_letter(self):
        text = choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        