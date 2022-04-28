# Minecraft Version Control System (MCVCS)

MCVCS is used to manage your Minecraft servers, or server networks, with the power of version control

This software is completely built from the ground-up using python but could be implemented in any language you like!
The goal is to provide an extensive VCS that is completely open for everyone.

## Why use MCVCS?

MCVCS is completely open-source and is driven by community feedback! We are dedicated to trying to make everyone's lives easier when it comes to doing the boring parts of running your server! No one likes sifting thru backups to revert some plugin config.

This VCS is also completely hand-made to work specifically with minecraft servers. This isn't a patch onto some existing VCS sollution.

## Later Expansion

Later, I intend on using this system for a graphic server managing client I am working on!

# All commands

|name|description|usage|
|----|-----------|-----|
|init| initializes vcs in current directory|`$ mcvcs init`|
|set-remote| set the remote and connect| `$ mcvcs activate ip:port usr pswd`|
|commit|commits staged changes| `$ mcvcs commit "your message here"`|
|stage| stage a change for commit| `$ mcvsc stage [<server>:]<file>`|
|unstage| unstage a change| `$ mcvsc unstage [<server>:]<file>`|