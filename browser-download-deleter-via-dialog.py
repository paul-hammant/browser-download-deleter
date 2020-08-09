#!/usr/local/bin/python3

# See https://github.com/paul-hammant/browser-download-deleter

import tkinter
from tkinter import messagebox
import platform
import os
import subprocess
import sys
import datetime
import sqlite3
from os.path import expanduser

def app_to_front(parent):
    parent.attributes("-topmost", True)
    # Hack because some MacOS tkinter dialogs don't open frontmost :(
    if platform.system() == 'Darwin':
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is {} to true'
        script = tmpl.format(os.getpid())
        output = subprocess.check_call(['/usr/bin/osascript', '-e', script])
    parent.after(0, lambda: parent.attributes("-topmost", False))

def create_table():
    try:
        c.execute("""CREATE TABLE to_delete
                 (name, if_after timestamp)""")
    except:
        pass

def already_noted(name):
    return len(c.execute("SELECT * FROM to_delete WHERE name=?", (name,)).fetchall()) > 0

def insert_row(name, if_after):
    c.execute("INSERT OR REPLACE INTO to_delete (name, if_after) values(?,?)", (name, if_after))

def delete_those_old_enough():
    
    removed = []
    sql = "SELECT name, if_after FROM to_delete"
    recs = c.execute(sql)
    for row in recs:
        if datetime.datetime.now() > row[1]:
            fname = row[0]
            if os.path.exists(fname):
                print("delete in FS ", fname)
                os.remove(fname)
            removed.append(fname)
    for fname in removed:
        print("deleting from 'to_delete' table ", fname)
        c.execute('DELETE FROM to_delete WHERE name=?', (fname,))
        conn.commit()


line = sys.argv[1]

home = expanduser("~")
conn = sqlite3.connect(home + "/.future_deletes.db", detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()
create_table()

if "Downloads" in line and \
        not line.endswith(".crdownload") and \
        not line.endswith(".part") and \
        not line.endswith(".Unconfirmed") and \
        ".com.google.Chrome." not in line and \
        os.path.exists(line):

    fname = line

    if already_noted(fname) is False:
        parent = tkinter.Tk()
        parent.overrideredirect(1)  # Avoid it appearing and then disappearing quickly
        parent.withdraw()  # Hide the window as we do not want to see this one

        app_to_front(parent)
        msgbox_choice = tkinter.messagebox.askquestion('Future File Deletion',
                                                       'Delete ' + fname + ' in 24 hours?',
                                                       icon='warning')
        if msgbox_choice == 'yes':
            insert_row(fname, datetime.datetime.now() + datetime.timedelta(days=1))
            conn.commit()  # commit needed
            print(fname + " marked for delete in 24h")

        parent.destroy()

delete_those_old_enough()
c.close()


