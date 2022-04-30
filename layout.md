# File layout

```
base/
 | .MCVCS/
    | branches/ # contains branch info
       | master/ # default branch
          | commits/ # contains comit files
    | keys/ # contains keys for users
       | example.key # example key
    | data_storage.json

 | servers/
    | exampleSrv/ # example server
       | master/ # srv version from the master branch
          | plugins/
             | ...
          | logs/
             | ...

          | eula.txt
          | server.properties
          | server.jar

          | mcvcs_plugin_store.json # plugin versions, file paths, etc. Alot of this is from unpacking the plugin jar.

       | info.json # contains info. ex: port ranges and backup intervals
  | backups/ # contains backups
     | exampleSrv/ # example  server
       | master/ # backups from master
         | YYYY-MM-DD--hh-mm-ss.tar.gz 
           || plugins/...
           || mcvcs_plugin_store.json
           || server.jar
           || server.properties
           || world/... # have more than just this world ofc
```

# commit file

Alot of this is to make it pretty and readable. Its not perfect, but I like the way it looks. There are ways to make the format much, much denser. I don't really see a need due to the small amount of data this will store in the first place.

```
################
<message>
<author>
<date>
################
|<server>::<tracked files> <last commit|hex commit id> <since>
|<server>::<trackked files> <hex commit id> <since>

))<change type> <server>::<file>
((<line-no, 0->inf>-[<<|>>]<data>

]]<server>::<filename> <size in bytes> // data that can't be logged (ex: jar file)
<data with the exact same size as specified above>
```

## change types

|identifier|meaning|
|-|-|
|C| File Creation|
|M| File Modified|
|D| File Delete|

## example

```
################
Updating EssentialsX and changing chat formatting
spidertyler2005
2022-04-24--10:21:16
################
|lobby::plugins/essentials/config.yml F8 0
|lobby::plugins/essentialsX.jar 2 0
|lobby::plugins/vault.jar F7 0
|lobby::plugins/vault/config.yml 1 0
|lobby::plugins/luckperms.jar F7 0
|lobby::server.jar F6 0
|lobby::mcvcs_plugin_store.json F8 0

))M lobby::plugins/essentials/config.yml
((710>>  format: '<{DISPLAYNAME}>  {MESSAGE}'
((710<<  format: '{DISPLAYNAME}  {MESSAGE}'
((943>>spawn-on-join: false
((943<<spawn-on-join: true
))M lobby::mcvcs_plugin_store.json
((1>>   "essentials":{"version":"2.20.0-dev+5-d891260","path":"plugins/essentialsX.jar"},
((1<<   "essentials":{"version":"2.20.0-dev+5-d891268","path":"plugins/essentialsX.jar"},


]]lobby::plugins/essentialsX.jar 2,925,643
<data I can't be bother to put here>
```