#!/usr/bin/python
from Tkinter import *
#import cv2
import os
import subprocess
from time import sleep

def close():
	proc = subprocess.Popen(["xdotool search --onlyvisible --sync --name Python\ 2.7"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	for i in out.split():
		os.system("xdotool windowactivate --sync "+i)
		os.system("xdotool getactivewindow windowkill")

def compass():
	os.system("idle-python2.7 -r compass.py &")

	proc = subprocess.Popen(["xdotool search --onlyvisible --name MRM"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	cmd="xdotool windowmove "+out.strip()+" 0 0 &"
	os.system(cmd)
	sleep(1)
	proc = subprocess.Popen(["xdotool search --onlyvisible --name cam10"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	cmd="xdotool windowmove "+out.strip()+" 100 0 &"
	os.system(cmd)
	sleep(1)
	proc = subprocess.Popen(["xdotool search --onlyvisible --sync --name Python\ 2.7"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	
	#os.system("xdotool search --onlyvisible --sync --name \"Python\ 2.7+\ Shell\" set_window --name \"Motorcode\"")
	for i in out.split():
		os.system("xdotool windowminimize "+i.strip())
def compass_gui():
	os.system("idle-python2.7 -r compass_gui.py &")

	proc = subprocess.Popen(["xdotool search --onlyvisible --name MRM"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	cmd="xdotool windowmove "+out.strip()+" 0 0 &"
	os.system(cmd)
	sleep(1)
	proc = subprocess.Popen(["xdotool search --onlyvisible --name cam10"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	cmd="xdotool windowmove "+out.strip()+" 100 0 &"
	os.system(cmd)
	sleep(1)
	proc = subprocess.Popen(["xdotool search --onlyvisible --sync --name Python\ 2.7"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	
	#os.system("xdotool search --onlyvisible --sync --name \"Python\ 2.7+\ Shell\" set_window --name \"Motorcode\"")
	for i in out.split():
		os.system("xdotool windowminimize "+i.strip())
def laksh_map():
	os.system("idle-python2.7 -r laksh_map.py &")

	proc = subprocess.Popen(["xdotool search --onlyvisible --name MRM"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	cmd="xdotool windowmove "+out.strip()+" 0 0 &"
	os.system(cmd)
	sleep(1)
	proc = subprocess.Popen(["xdotool search --onlyvisible --name cam10"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	cmd="xdotool windowmove "+out.strip()+" 100 0 &"
	os.system(cmd)
	sleep(1)
	proc = subprocess.Popen(["xdotool search --onlyvisible --sync --name Python\ 2.7"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	
	#os.system("xdotool search --onlyvisible --sync --name \"Python\ 2.7+\ Shell\" set_window --name \"Motorcode\"")
	for i in out.split():
		os.system("xdotool windowminimize "+i.strip())

def motorcode():

	proc = subprocess.Popen(["xdotool search --onlyvisible --name MRM"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	cmd="xdotool windowmove "+out.strip()+" 0 0 &"
	os.system(cmd)
	os.system("idle-python2.7 -r tcp_send.py &")
	sleep(1)
	proc = subprocess.Popen(["xdotool search --onlyvisible --name gear"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	cmd="xdotool windowmove "+out.strip()+" 1060 150 &"
	os.system(cmd)

	proc = subprocess.Popen(["xdotool search --onlyvisible --sync --name Python\ 2.7"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	#print out
	for i in out.split():
		cmd="xdotool windowsize "+i.strip()+" 350 100 && xdotool windowmove "+i.strip()+" 0 97 &"
		print cmd
		os.system(cmd)
	

a = Tk()
a.title("MRM")

Button(a, text="Close All", command = close, bg="white", fg="black",font=("comic_sans",15,"bold")).grid(row = 0,column=3)
Button(a, text="Laksh_map", command = laksh_map, bg="white", fg="black",font=("comic_sans",15,"bold")).grid(row = 0,column=0)
Button(a, text="Compass_gui", command = compass_gui, bg="white", fg="black",font=("comic_sans",15,"bold")).grid(row = 0,column=1)
Button(a, text="Compass", command = compass, bg="white", fg="black",font=("comic_sans",15,"bold")).grid(row = 0,column=2)


a.mainloop()
