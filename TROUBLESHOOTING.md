# Troubleshooting

## Exit codes

It may be a bit of an over engineering feat for this project.

In the event that parts of the shell scripts fail, it can be helpful to have some user-defined exit codes to track down the exact failure occurred:

* 80 - pushd failed
* 81 - popd failed
* 82 - ...

More exit codes for bash can be found in The Linux Documentation Project's Advanced Bash-Scripting Guide: https://tldp.org/LDP/abs/html/exitcodes.html
