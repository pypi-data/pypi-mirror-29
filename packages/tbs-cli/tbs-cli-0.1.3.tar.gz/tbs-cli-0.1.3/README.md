# 3Blades Command-line Interface Tools


## Setup
Currently, this package requires python3.6 for proper functionality.

- `pip3.6 install tbs-cli`

To use these tools with our development environment (or any other environment), set your corresponding ENV variable appropriately:
- `export TBS_API_URL="https://dev-api.3blades.ai"` (or another appropriate URL.)

The 3Blades production environment will default if no environment is set.

## Usage
To invoke a command, the syntax is as follows:
`$ tbs <command_group> <subcommand> <parameters>`

All command parameters should have both a standard flag denoted with two dashes and the flag name, as well as a short flag denoted by a single dash and a letter.
A flag and its corresponding short flag should be interchangeable for the purpose of convenience and speed.
The command flag `--deployment` should be the same as the command short flag `-d`, for example.
A list of all flags is available in the `docs/` folder.

Any command can be appended with the flag `--help` or the short flag `-h` to view that command's help doc.
`tbs login --help` or `tbs projects create -h` would both bring up a help doc.
A command's help doc also includes a list of any available subcommands.



## Command Groups
#### Login
`tbs login <parameters>`
You will be prompted for your username and password. This will create a `threeblades.token` file in your `$HOME` directory that will be used for subsequent logins. Delete this file if you would like to login as a different user, or to a different environment.

#### Projects
`tbs projects <subcommand> <parameters>`
Currently implemented subcommands: `list`, `detail`, `create`,  and `delete`. You will be prompted for any required arguments. Flags (`--name`, etc.) will come at a later date.

#### Deployments
`tbs deployments <subcommand> <parameters>`
Currently implemented subcommands: `list`, `detail`, `create`, `update`, `delete`

Currently available runtimes:
- `python2.7`

Currently available frameworks:
- `tensorflow`, `tensorflow1.4`

In order to deploy the model you've created at the command line, just send a `POST` request to `https://dev-api.3blades.ai/v1/<namespace>/projects/<project>/deployments/<deployment>/`. The ability to do this from the command line will be added very soon (in the next day or so).


**Note:** This document is very much a work in progress, and it will be updated rapidly for the forseeable future.
