from flask import Flask, session
import string
import random

def getState():
	if 'state' in session:
		return session["state"]
	else:
		session["state"] = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(16))
		print "Set session['state']: " + session["state"]
		return session["state"]