# Junc Documentation

## Index
* [Quickstart and Usage Overview](#table-of-contents)
* [Code Overview](code.md)
* [Roadmap](https://github.com/llamicron/junc/projects)
* [Contributing](contributing.md)
* [License](license.md)

## Table Of Contents
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
  * [Debugging](#debugging)
* [Footnotes](#footnotes)

# Installation [↑](#table-of-contents)
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

# Quickstart [↑](#table-of-contents)
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

# Things you can do [↑](#table-of-contents)

## Connect [↑](#table-of-contents)
```
$ junc connect <name>
Connecting...
```

## Add [↑](#table-of-contents)
Add a server to your server list:
```
$ junc add <server_name> <username> <ip> [<location>]
```
`location` is optional

## List [↑](#table-of-contents)
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

## Remove [↑](#table-of-contents)
Remove a server:
```
junc remove <name>
```
If there are special characters in the server name that could be interpreted as a unix command ('`[`' for example), you may need to escape it with a backslash `\`.

## Backup [↑](#table-of-contents)
This will copy the server list json file to a backup file.
```sh
junc backup [<file>]
```
You can supply an optional file path to copy to

If you want to backup on gist or export to a service like [hastebin](http://hastebin.com), see the [export tips](#export) section.

## Restore [↑](#table-of-contents)
Copies the backup file to the regular server list json file.
```
junc restore [<file>]
```
The optional file argument is where to copy the file from.


# Tips [↑](#table-of-contents)
## Export
### To Hastebin [↑](#table-of-contents)
If you have the `haste` gem installed (`gem install haste`):
```sh
junc list --json | haste
```
Keep in mind that haste only keeps docs for 30 days since their last view, and they may be removed without notice. This is useful for moving lists between systems or sharing with other developers, but not backups since it will be removed one day.

### To Gist [↑](#table-of-contents)
You'll need the [gist](https://github.com/defunkt/gist) gem or package installed and configured, which requires you to login to your github account. Install the gem with `gem install gist` or on MacOS with `brew install gist`
```sh
junc list --json | gist -f junc_export.json
```
This command will output a url for your gist. Gist are more permanant than hastes, but the url is much longer. Gists are better for backups than sharing.

You can backup your servers (maybe with a periodic cron job?) with the date in the filename:
```sh
junc list --json | gist -f junc_backup_02_04_2018.json
```
## Debugging [↑](#table-of-contents)
If things aren't working properly, hit me up. Otherwise, if you want to try and fix it on your own, try adding the `--debug` flag. This will do a number of things:

1. Actually throw an exception in python when one occurs
2. Use a test file (`~/.junc.json.test`) instead of your actual file.

Currently, when the `--debug` flag is missing, if a python exception occurs [[1]](#1), junc will catch the error and only print the attached message instead of the full error message. This is just to make things a little more user friendly. It also completely prevents users from getting an ugly error message. Adding the `--debug` flag reverses this behavior.

# Footnotes [↑](#table-of-contents)
### 1 [↑](#table-of-contents)
This is expected during normal usage. For example, if you try to add a server with a name that's already taken, junc with raise a `ValidationError`.
