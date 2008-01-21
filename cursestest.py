#!/usr/bin/python

import curses
import time

try:
	stdscr=curses.initscr()
	
	curses.noecho()
	curses.cbreak()
	
	screen=stdscr.subwin(23,79,0,0)
	screen.box()
	screen.addstr(5,33,"Hello",curses.A_NORMAL)
	screen.refresh()
	
	time.sleep(5)
	
finally:
	stdscr.keypad(0)
	curses.echo()
	curses.nocbreak()
	curses.endwin()
