# Junc Documentation

## index
* [Installation](#installation)
* [Quickstart](#quickstart)
* [Things you can do](#things-you-can-do)
  * [Add a server](#add)
  * [Remove a server](#remove)
  * [List servers](#list)
  * [Connect to a server](#connect)
  * [Backup](#backup)
  * [Restore](#restore)
* [Tips](#tips)
  * [Export](#export)

# Installation
Install with pip
```sh
pip install junc
```
Or install from source (not stable)
```
$ git clone https://github.com/llamicron/junc.git
$ cd junc
$ pip install -r requirements.txt
$ make install
```

# Quickstart
```sh
# Add a server
$ junc add
# Follow the prompts...

# See the server table
$ junc list

# Connect to a server
$ junc connect <server_name>
```
To see the version:
```sh
pip list | grep junc
```

# Things you can do

## Connect
```
$ junc connect <name>
Connecting...
```

## Add
Add a server to your server list:
```
$ junc add <server_name> <username> <ip> [<location>]
```
`location` is optional

## List
```
$ junc list
+-------------+-------------------------+-------------+
| Name        | Address                 | Location    |
+-------------+-------------------------+-------------+
| test_rpi    | pi@123.45.67.890        | School      |
| home_rpi    | pi@192.168.0.134        | Home Office |
| securit_cam | pi@192.168.0.169        | Porch       |
| playground  | llamicron@192.168.0.139 | Office      |
+-------------+-------------------------+-------------+
```
![Imgur link](https://i.imgur.com/fDjotEs.png)

image for if the table above doesn't render correctly.

`--json` is an optional flag for `list`. It will output the server list as json.

## Remove
Remove a server:
```
junc remove <name>
```
If there are special characters in the server name that could be interpreted as a unix command ('`[`' for example), you may need to escape it with a backslash `\`.

## Backup
This will copy the server list json file to a backup file.
```sh
junc backup [<file>]
```
You can supply an optional file path to copy to

If you want to backup on gist or export to a service like [hastebin](http://hastebin.com), see the [export tips](#export) section.

## Restore
Copies the backup file to the regular server list json file.
```
junc restore [<file>]
```
The optional file argument is where to copy the file from.


# Tips
## Export
### To Hastebin
If you have the `haste` gem installed (`gem install haste`):
```sh
junc list --json | haste
```
Keep in mind that haste only keeps docs for 30 days since their last view, and they may be removed without notice. This is useful for moving lists between systems or sharing with other developers, but not backups since it will be removed one day.

### To Gist
You'll need the [gist](https://github.com/defunkt/gist) gem or package installed and configured, which requires you to login to your github account. Install the gem with `gem install gist` or on MacOS with `brew install gist`
```sh
junc list --json | gist -f junc_export.json
```
This command will output a url for your gist. Gist are more permanant than hastes, but the url is much longer. Gists are better for backups than sharing.

You can backup your servers (maybe with a periodic cron job?) with the date in the filename:
```sh
junc list --json | gist -f junc_backup_02_04_2018.json
```
