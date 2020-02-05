Things that PrimusBot does:

Removes messages containing "Whalecum" or "whalecum"

Combats "dig good" or "dupe bad"

Protects RR from ping

Commands:

/getmcdata: Admin only command, gets stats from server

/s arg <all>: Shows scoreboard for the argument.  Valid type arguments are: "use", "pickup", "drop", "mine", "craft", "kill", "break".
  Example of valid argument: "use.diamond_pickaxe".  "all" argument shows the full scoreboard instead of only part.

/poll "title" arg1 arg2 <arg3>... <arg26>: Creates a poll in the channel that the message is sent in.  First argument sets the title, next arguments set the options, until 26 arguments.

/resolvepoll "title": Uses the title of a poll to resolve a poll in the channel in which it was sent.  Outputs a summary to the poll output channel.

/clear integer: Replacing "integer" with a real number, clears the number of messages specified, starting from the bottom.

/setmodchannel: Sets channel for mod messages (in the case we would ever need one) to be the channel in which the command was sent.

/setpolloutputchannel: Sets channel for polls resolved by /resolvepoll to be outputted to be the channel in which the command was sent.

/listcommands: WIP, sends a list of commands in the channel.

/stop: Owner only, stops bot from running.

/togglewhaledefense: toggles the "whalecum" defense function
