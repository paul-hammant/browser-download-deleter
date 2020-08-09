# Description

Each time Chrome, Firefox, Safari (etc) drop a file in your downloads folder, a dialog pops up asking you 
if you want to delete the file in 24 hours. Note this also works or ANYTHING that finds its way into your 
~/Downloads folder.

## Screenshots

Down a pic (or video, or anything) to save somehow:

![image](https://user-images.githubusercontent.com/82182/89728791-d75d0a00-da27-11ea-8c34-574b6c567810.png)

![image](https://user-images.githubusercontent.com/82182/89728843-24d97700-da28-11ea-8cd2-115ab5b8f0e1.png)

After the item arrives in ~/Downloads/ this dialog appears:

![image](https://user-images.githubusercontent.com/82182/89728867-44709f80-da28-11ea-9448-3aaa740e6889.png)

# Technology Choices

A shell script that depends on "fswatch" is running when you log in. That should be minimal RAM and CPU use. 
Each time a file drops your downloads folder a Python3 program starts to examine what it is. There's lots of 
noise in your download folder, but when that's not the case a dialog pops up to ask that question. The Python 
launch is more RAM and CPU use, but it is infrequent, so you shouldn't worry about it so much.

It should all be rewritten in Rust for minimal footprint.

Note this technology cheats a little - the actual deletions happen when the script/dialog is next triggered. So if 
you don't save anything to the downloads folder it does not get cleared out. Most people won't feel this is an 
inconvenience.

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