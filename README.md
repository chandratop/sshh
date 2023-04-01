# sshh

An ssh helper when you have too many ssh hosts

## Installation

1. Get inside the `sshh` directory

```bash
$ cd sshh
```

2. Get the absolute path to this `sshh` directory and copy that path

```bash
$ pwd

> /path/to/sshh
```

3. Open your `.bashrc`, `.zshrc` or whatever configuration file your terminal uses and add the following line to it

```bash
alias sshh='/path/to/sshh/sshh.py'
```

4. Run the source command to apply the changes (example below)

```bash
$ source ~/.zshrc
```

5. You can now execute `sshh` from anywhere

```bash
$ sshh
```

## Usage

- You can use the tool from anywhere using the `sshh` command.
- To get help on the arguments you can run `sshh -h`.
- The first time you run the command you will have to navigate the folder where you are storing all your pem files.
- To add a new instance ssh you can run `sshh -a <friendly_name>`. This will prompt you to enter the instance IP. Then it will ask you to choose the pem file from the directory where you store all pem files.
- To ssh into an instance using a friendly name you can run `sshh -n <friendly_name>`.
- To ssh into an instance using the instance IP you can run `sshh -i <instance_ip>`.
- You can also just run `sshh` command to choose which instance to ssh into.