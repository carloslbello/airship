#!/usr/bin/python
print("This won't do anything yet, because we don't have any applicable games. That'll change soon, though!")
'''
import os, subprocess
games = [{
	# None yet!
}]
void = open(os.devnull, "w")
for game in games:
	if os.path.isdir(os.path.expanduser("~/Library/Mobile Documents/" + game["icloudfolder"])):
		subprocess.call(["python", "propeller.py", game["appid"], game["icloudfolder"], game["steamfolder"], game["regex"]], stdout = void, stderr = void)
'''
