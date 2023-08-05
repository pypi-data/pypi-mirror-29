runsteps
========

A controlled sequential command runner.

What does that mean? Given a series of commands, perhaps a directory of
shell scripts, and a mechanism for specfying the order of those
commands, runsteps will execute them and monitor them for state and
failure.

More specifically, runsteps collects running times, output and return codes of
each executed step and controls the environment variables of the step. A
mechanism for any step to 'save' key value pairs for use as environment
variables in following steps is also provided. This allows the steps to 'share'
small bits of data between themselves as the entire run progresses.