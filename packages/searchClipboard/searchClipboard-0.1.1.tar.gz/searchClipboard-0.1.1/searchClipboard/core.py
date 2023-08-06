# -*- coding: utf-8 -*-
import sys, pyperclip, webbrowser

def search():
    # get search param from command line argument (if given)
    if len(sys.argv) > 1:
        search_param = ' '.join(sys.argv[1:])
    # get search param from clipboard using pyperclip library
    else:
        search_param = pyperclip.paste()
        print(search_param)
    webbrowser.open('https://www.google.com/maps/place/' + search_param)

