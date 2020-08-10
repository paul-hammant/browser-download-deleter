# Description

Each time Chrome, Firefox, Safari (etc) drop a file in your downloads folder, a dialog pops up asking you 
if you want to delete the file in 24 hours. Note this also works or ANYTHING that finds its way into your 
~/Downloads folder.

Not for everyone, but fo some download is a "workflow" moment. You intention may be to send a pic from your 
phone to your desktop, (work on it a little bit in a picture package, then out it out on social media etc. 
That last marks the last time you need it on your desktop, so it would be nice if it could be silently
deleted sometime after your likely finishing with it. 24 hours later seems like a reasonable amount of time, but 
others might like 7 days (not coded yet).

## Screenshots

Down a pic (or video, or anything) to save somehow:

![image](https://user-images.githubusercontent.com/82182/89728791-d75d0a00-da27-11ea-8c34-574b6c567810.png)

![image](https://user-images.githubusercontent.com/82182/89728843-24d97700-da28-11ea-8cd2-115ab5b8f0e1.png)

After the item arrives in ~/Downloads/ this dialog appears:

![image](https://user-images.githubusercontent.com/82182/89728867-44709f80-da28-11ea-9448-3aaa740e6889.png)

# Technology Choices

A shell script that depends on [fswatch](https://github.com/emcrisostomo/fswatch) is running when you log in. That should be minimal RAM and CPU use. 
Each time a file drops your downloads folder a Python3 program starts to examine what it is. There's lots of 
noise in your download folder, but when that's not the case a dialog pops up to ask that question. The Python 
launch is more RAM and CPU use, but it is infrequent, so you shouldn't worry about it so much.

It should all be rewritten in Rust for minimal footprint.

Note this technology cheats a little - the actual deletions happen when the script/dialog is next triggered. So if 
you don't save anything to the downloads folder it does not get cleared out. Most people won't feel this is an 
inconvenience.

# Installation

## Mac via Homebrew

```
brew install fswatch python3
sudo cp launch_agent.xml  ~/Library/LaunchAgents/browser-download-deleter-launcher.plist
# hack as launch daemon plists don't recognize '~' or '$HOME' for home:
defaults write "$HOME/Library/LaunchAgents/browser-download-deleter-launcher.plist" StandardOutPath "$HOME/.browser-download-deleter.stdout.log"
defaults write "$HOME/Library/LaunchAgents/browser-download-deleter-launcher.plist" StandardErrorPath "$HOME/.browser-download-deleter.stderr.log"

cp browser-download-deleter-via-dialog.py /usr/local/bin/
cp browser-download-deleter-launcher.sh /usr/local/bin/

```

Mac "Launch Agents" can be for all users, (/Library/LaunchAgents/) or for specific user (~/Library/LaunchAgents/). We need the latter here.

# Footnote

I'd really like such features build into file download (and upload) dialogs for the browsers themselves.

![image](https://user-images.githubusercontent.com/82182/89753062-bbf90a00-dace-11ea-9f72-0f00a84f47b9.png)

The key is that this has to be one-click with no further "are you sure" confirmation dialog. Though your new problem is that 
there probably needs to be a way to visualize in another list (Finder or WindowsExplorer?) and change your mind about future 
deletion