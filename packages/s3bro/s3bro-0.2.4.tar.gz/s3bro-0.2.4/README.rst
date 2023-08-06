.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://raw.githubusercontent.com/rsavordelli/s3bro/master/LICENSE

=============================
# s3bro! A handy s3 cli tool
=============================
============
Overview
============
It's your s3 friend (bro). Often you'll need to run complex CLI/AWS commands in order to execute tasks against S3.  Let's say you need to restore all your keys from S3 Glacier storage class, we know (probably) that AWS CLI does not provide an easy way to execute this in "batch". So you would need to mix aws cli commands and pipe it to additional commands. Additionally, it would restore key by key, very slowly.
The s3bro do it for you nicely using multiprocessing/threading. That means that you can get it done way faster than using the normal method. Oh, also in an elegant way. This is a python cli that will abstract a big portion of this work for you.

>>> 'Why would you run the two following commands to wipe your bucket:'
aws s3api list-object-versions --bucket rsavordelli --output json --query
    'Versions\[\].\[Key, VersionId\]' | jq -r '.\[\] | "--key '\\''" + .\[0\] + "'\\''
         --version-id " + .\[1\]' |  xargs -L1 aws s3api delete-object --bucket rsavordelli
aws s3api list-object-versions --bucket rsavordelli --output json --query
     'DeleteMarkers\[\].\[Key, VersionId\]' | jq -r '.\[\] | "--key '\\''" + .\[0\] + "'\\''
         --version-id " + .\[1\]' |  xargs -L1 aws s3api delete-object --bucket rsavordelli

>>> 'if you can run this?'
s3bro purge --bucket rsavordelli


>>> 'what if you need to restore all your keys from glacier storage class? Or just some of them?'
➜  ~ s3bro restore --bucket jusbroo-glacier --prefix glacier --days 10 --type Expedited --exclude .html --workers 10
Initiating Expedited restore for jusbroo-glacier/glacier...
Restoring keys for 10 days
==============================
All versions: False
==============================
Restoration completed: glacier/River Flows In You - A Love Note (CM Remix).mp3 until "Sat, 03 Mar 2018 00:00:00 GMT"
Submitting restoration request: glacier/asd.js
Restoration completed: glacier/Yiruma - River Flows In You (English Version).mp3 until "Sat, 03 Mar 2018 00:00:00 GMT"
Restoration completed: glacier/River Flows In You- Lindsey Stirling.mp3 until "Sat, 03 Mar 2018 00:00:00 GMT"
Restoration completed: glacier/River Flows In You - A Love Note (Ryan Wong Remix).mp3 until "Sat, 03 Mar 2018 00:00:00 GMT"
Restoration completed: glacier/ until "Sat, 03 Mar 2018 00:00:00 GMT"
Restoration completed: glacier/Endless Love {Piano Version} | Beautiful Piano.mp3 until "Sat, 03 Mar 2018 00:00:00 GMT"
Total keys proccessed: 7 in 5.44s


******************
Available Commands
******************
- restore_
- purge_
- scanperms_

============
Installation
============
   ``pip install s3bro -U``

***********
From source
***********
    ``git clone https://github.com/rsavordelli/s3bro ; cd s3bro``

    ``pip install .``

============
Examples
============

.. code:: sh

    # s3bro restore --help
    # s3bro restore --bucket bucketName --prefix myglacierPrefix --days 20 --type Bulk
    # s3bro restore --bucket bucketName --prefix myglacierPrefix --days 20 --type Bulk --include .css --versions
    # s3bro restore --bucket bucketName --prefix myglacierPrefix --days 20 --type Bulk --exclude .exe --update-restore-date
    # s3bro purge --bucket bucketName

============
Commands
============
***************
restore
***************
 Restore S3 keys in Glacier Storage class

Options
------------------
>>> 'options'
Usage: s3bro restore [OPTIONS] [RESTORE]...
Options:
  --bucket TEXT                   bucket name  [required]
  --prefix TEXT                   prefix
  --days INTEGER                  Days to keep the restore  [required]
  --type [Standard|Expedited|Bulk]
                                  restore type (Tier) [required]
  --versions / --no-versions      [--no-versions is DEFAULT] - this option
                                  will make the restore to include all
                                  versions excluding delete markers
  --update-restore-date / --do-not-update-restore-date
                                  If passed, it will change the restore date
                                  for already restored key
  --include TEXT                  Only restore keys that matches with a given
                                  string, you can add multiples times by
                                  passing --include multiple times
  --exclude TEXT                  Do not restore if key name matches with a given pattern,
                                  you can add multiple patterns by inputting
                                  --exclude multiple times
  --workers INTEGER               How many helpers to include in task, default
                                  is 10
  --log-level [INFO|ERROR|DEBUG|WARNING]
                                  logging type
  --help                          Show this message and exit.

Details
^^^^^^^^^^^^^^^^^^

>>> 'the option --log-level is can be useful to debug errors/behaviors.'
DEBUG - similar to boto3 debug leve with additional information
WARNING - will print some threading information and Keys excluded during the iteration (exclude, include, storage-class, delete-marker, etc)

>>> 'the option --workers allows you to specify how many workers will consume the list. Calculate max 5 workers per core'

>>> 'the option --update-restore-date can be used to "extend" a key that is already restored. It will send a new "expiry" date to the object'

***************
purge
***************
Delete all keys in the bucket - as simple as that. It will delete versions, delete markers. Everything

Options
------------------

>>> 'options'
Usage: s3bro purge [OPTIONS] [PURGE]...
Options:
  --bucket TEXT                   Bucket name  [required]
  --prefix TEXT                   prefix name - optional
  --yes                           first confirmation
  --yes-really                    second confirmation
  --log-level [INFO|ERROR|DEBUG|WARNING]
                                  logging type
  --help                          Show this message and exit.


Details
^^^^^^^^^^^^^^^^^^

>>> 'it does not delete the bucket. It only delete the keys'

***************
scanperms
***************
Look for objects with Public permissions in your bucket

Options
------------------
>>> 'options'
Usage: s3bro scanperms [OPTIONS] [SCANPERMS]...
Options:
  --bucket TEXT                   Bucket name  [required]
  --prefix TEXT                   prefix name - optional
  --workers INTEGER               How many helpers to include in task, default
                                  is 10
  --log-level [INFO|ERROR|DEBUG|WARNING]
                                  logging type
  --help                          Show this message and exit.

Details
^^^^^^^^^^^^^^^^^^
>>> 'Not support for versions. Only current versions'

