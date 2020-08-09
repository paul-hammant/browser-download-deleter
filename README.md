# Description

Each time Chrome, Firefox, Safari (etc) drop a file in your downloads folder, a dialog pops up asking you 
if you want to delete the file in 24 hours

# Technology Choices

A shell script that depends on "fswatch" is running when you log in. That should be minimal RAM and CPU use. 
Each time a file drops your downloads folder a Python3 program starts to examine what it is. There's lots of 
noise in your download folder, but when that's not the case a dialog pops up to ask that question. The Python 
launch is more RAM and CPU use, but it is infrequent, so you shouldn't worry about it so much.

It should all be rewritten in Rust for minimal footprint.

# Installation

## Mac

```
brew install fswatch python3
sudo cp launch_agent.xml  ~/Library/LaunchAgents/browser-download-deleter-launcher.plist
cp browser-download-deleter-via-dialog.py /usr/local/bin/
cp browser-download-deleter-launcher.sh /usr/local/bin/

defaults write "$HOME/Library/LaunchAgents/browser-download-deleter-launcher.plist" StandardOutPath "$HOME/.browser-download-deleter.stdout.log"

defaults write "$HOME/Library/LaunchAgents/browser-download-deleter-launcher.plist" StandardErrorPath "$HOME/.browser-download-deleter.stderr.log"

```

Mac "Launch Agents" can be for all users, (/Library/LaunchAgents/) or for specfic user (~/Library/LaunchAgents/). We need the latter here.