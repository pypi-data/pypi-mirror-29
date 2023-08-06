# vectordash-cli
A command line tool for interacting with [Vectordash](http://vectordash.com) GPU instances.


#### Usage Examples

1) `vectordash secret <secret_token>` - update's the user's secret token which is used for authentication

2) `vectordash list` - lists the machines the user can connect to; these are machines user is currently renting

3) `vectordash ssh <machine_id>` - connect the user to a machine via SSH

4) `vectordash push <machine_id> <from_path> <to_path>`

  This uses scp to push files to the machine. If `<to_path>` is not included,
  then `scp` pushes it to the machine's home directory.

5) `vectordash pull <machine_id> <from_path> <to_path>`

  Same command as above, except we're copying files from the machine to the local machine. 
  If `<to_path>` is not provided, then copies the files to the current directory.
