from aquests.lib.athreads import trigger
from aquests import lifetime
import sys, asyncore, time
import gc
import select
import os
import bisect
import socket
import time

if os.name == "nt":
	from errno import WSAENOTSOCK
	
_shutdown_phase = 0
_shutdown_timeout = 30 # seconds per phase
_exit_code = 0
_last_maintern = 0
_maintern_interval = 3.0
_killed_zombies = 0
_select_errors = 0

def status ():
	fds = []
	for fdno, channel in list(asyncore.socket_map.items ()):
		d = {}	
		d ["name"] = "%s.%s" % (channel.__module__, channel.__class__.__name__)
		d ["fdno"] = fdno
		
		status = "NOTCON"
		if channel.accepting and channel.addr: status = "LISTEN"
		elif channel.connected: status = "CONNECTED"
		d ["status"] = status		
		addr = ""
		if channel.addr is not None:
			try: addr = "%s:%d" % channel.addr
			except TypeError: addr = "%s" % repr (channel.addr)
		if addr:
			d ["address"] = addr

		if hasattr (channel, "channel_number"):
			d ["channel_number"] = channel.channel_number
		if hasattr (channel, "request_counter"):	
			d ["request_counter"] = channel.request_counter
		if hasattr (channel, "event_time"):
			d ["last_event_time"] = time.asctime (time.localtime (channel.event_time))
		if hasattr (channel, "zombie_timeout"):
			d ["zombie_timeout"] = channel.zombie_timeout
		if hasattr (channel, "get_history"):
			d ["history"] = channel.get_history ()
						
		fds.append (d)
		
	return {
		"killed_zombies": _killed_zombies,
		"select_errors": _select_errors,
		"selecting_sockets": len (asyncore.socket_map),	
		"in_the_map": fds
	}

def maintern_zombie_channel (now):
	global _killed_zombies
		
	for channel in list(asyncore.socket_map.values()):
		if hasattr (channel, "handle_timeout"):
			try:
				iszombie = (now - channel.event_time) > channel.zombie_timeout + 3
			except AttributeError:
				continue
			if iszombie:				
				_killed_zombies += 1
				try:
					channel.handle_timeout ()
				except:
					channel.handle_error ()

maintern = None
def init (kill_zombie_interval = 10.0, logger = None):
	global maintern
	
	lifetime.EXHAUST_DNS = False
	lifetime._logger = logger
	maintern = lifetime.Maintern ()
	maintern.sched (kill_zombie_interval, lifetime.maintern_zombie_channel)
	maintern.sched (300.0, lifetime.maintern_gc)

def shutdown (exit_code, shutdown_timeout = 30.0):
	global _shutdown_phase
	global _shutdown_timeout
	global _exit_code
	
	if _shutdown_phase:
		# aready entered
		return
		
	if _shutdown_phase == 0:
		_exit_code = exit_code
		_shutdown_phase = 1
		
	_shutdown_timeout = shutdown_timeout
	
	trigger.wakeselect ()
	
def loop (timeout = 30.0):
	global _shutdown_phase
	global _shutdown_timeout
	global _exit_code
	global maintern
	
	if maintern is None:
		init ()
		
	_shutdown_phase = 0
	_shutdown_timeout = 30
	_exit_code = 0	

	try: 
		lifetime_loop(timeout)
	except KeyboardInterrupt:
		_shutdown_timeout = 1
		graceful_shutdown_loop()
	else:
		graceful_shutdown_loop()	

def lifetime_loop (timeout = 30.0):
	global _last_maintern
	global _maintern_interval
				
	map = asyncore.socket_map
	while map and _shutdown_phase == 0:
		lifetime.poll_fun_wrap (timeout, map)
		now = time.time()
		if (now - _last_maintern) > _maintern_interval:
			maintern (now)
			_last_maintern = time.time ()
				
def graceful_shutdown_loop ():
	global _shutdown_phase
	timestamp = time.time()
	timeout = 1.0
	map = asyncore.socket_map	
	while map and _shutdown_phase < 4:
		time_in_this_phase = time.time() - timestamp
		veto = 0
		for fd,obj in list(map.items()):
			try:
				fn = getattr (obj,'clean_shutdown_control')
			except AttributeError:
				pass
			else:
				try:
					veto = veto or fn (_shutdown_phase, time_in_this_phase)
				except:					
					obj.handle_error()
					
		if veto and time_in_this_phase < _shutdown_timeout:
			lifetime.poll_fun_wrap (timeout, map)					
		else:
			_shutdown_phase += 1
			timestamp = time.time()
