#!/usr/bin/python

#http://adamv.com/dev/python/curses/

import curses
import time

try:
	stdscr=curses.initscr()
	
	curses.noecho()
	curses.cbreak()
	
	stdscr.addstr(5,33,"Hello",curses.A_NORMAL)
	stdscr.refresh()
	
	time.sleep(5)
	
finally:
	stdscr.keypad(0)
	curses.echo()
	curses.nocbreak()
	curses.endwin()
