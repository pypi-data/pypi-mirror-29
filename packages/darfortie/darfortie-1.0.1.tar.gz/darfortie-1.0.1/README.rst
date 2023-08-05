darfortie
=========

Darfortie is a front-end for the dar (Disk ARchive) utility
(http://dar.linux.free.fr/). It adds functionality to the dar utility
and makes it simpler to use for creating incremental backups. It is
meant to facilitate a more convienent backup strategy, typically one run
periodically by a cron task.

The utility can be run repeatedly with the same parameters, and each run
will generate a new incremental archive based on the last one created.
It will search the directory where the current archive is being created
for past reference archives, or a directory can be specified to search
in (-I).

The first backup is created without the incremental option (-i).

Further incremental backups are created using the -i option and the
**same** (base) name. Darfortie adds the date/time to the final name to
make it unique. It relies on this naming convention to find the most
recent reference backup it should use.

--------------

It is suggested that for the base name you adopt a convention such as::

    machine_daily

where “`machine`” is the machine name being backed up, and “`daily`”
is for daily incremental backups. The end result would result in names
like::

  machine_daily_20160228T0352UTC.1.dar
  machine_daily_20160228T0403UTC_based_on_20160228T0352UTC.1.dar

--------------

A configuration file can be passed through to dar by using the -c
switch. If not specified, dar will search for and use any dar
configuration file it normally would (ie. /etc/darrc, ~/.darrc). See the
dar man page for details on its structure (“CONDITIONAL SYNTAX”).

It also allows you to pass thru dar prune paths.

--------------

Install darfortie by running:

1.  Installing Python (either v2 or v3) if not already installed.

2.  Download a configuration file to use with the -c option at https://github.com/kagalle/darfortie/blob/master/darfortie.conf.

3.  Run ``pip install -i https://pypi.python.org/pypi darfortie``

If this is done as a normal user, then the install puts the package in

    /home/ken/.local/lib/python2.7/site-packages/darfortie

and creates an execuatable such that the application can be run by:

    $ ./local/bin/darfortie

If installed as `root`, then the install is done into

    /usr/local/lib/python2.7/dist-packages/darfortie

and the executable is created as:

    /usr/local/bin/darfortie

which is normally on the system PATH.

--------------

For a complete list of options, run::

    python darfortie --help

--------------

This is BETA software. Use at your own risk. Please:

#. Test for suitability before using for “real” data.
#. During testing, use “dar -d …” to compare the created backup against
   the filesystem.
#. For testing, do a complete restore to a separate filesystem and
   compare results.

--------------

There is an older bash-based version in the “bash\_version” directory,
kept ONLY for historical reasons.

--------------

There is currently no restore option - use the dar utility directly to
do restores.
