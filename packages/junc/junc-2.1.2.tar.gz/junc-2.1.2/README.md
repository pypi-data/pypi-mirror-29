# Junc
[![Build Status](https://travis-ci.org/llamicron/junc.svg?branch=master)](https://travis-ci.org/llamicron/junc)
[![Build Status](https://ci.appveyor.com/api/projects/status/llamicron/junc)](https://ci.appveyor.com/project/llamicron/junc)
## SSH to servers easily
Now you don't have to remember usernames and IPs, and no more aliases for each of your machines.

## Quickstart
```sh
# Install
$ pip install junc


# Add a server
$ junc add
# Follow the prompts...

# See the server table
$ junc list

# Connect to a server
$ junc connect <server_name>
```

## [Documentation](docs/index.md)
[See the full docs here](docs/index.md)

## Contributing
This may appear to be a small project, but I'm using all the building and test tools under the sun. It may seem like overkill, but this is mainly for me to learn how to use all these tools like Travis CI, AppVeyor, Tox, etc..

Fork this repo and add a new feature, write some unit tests and a bit of documentation and it'll probably get merged.
