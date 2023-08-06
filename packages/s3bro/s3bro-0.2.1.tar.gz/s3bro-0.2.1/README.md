# s3bro
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://raw.githubusercontent.com/rsavordelli/s3bro/master/README.md)

# s3bro! A handy s3 cli tool
s3bro?
---
It's your s3 friend (bro). Often you'll need to run complex CLI/AWS commands in order to execute tasks against S3.  Let's say you need to restore all your keys from S3 Glacier storage class, we know (probably) that AWS CLI does not provide an easy way to run this in "batch". So you would need mix aws cli and pipe it to additional commands. Additionally, it would restore key by key, very slowly.
The s3bro do it for you nicely, and using multiprocessing/threading. That means that you could get it done way faster than using the normal method. Oh, also in an elegant way.

This is a python cli that will abstract a big portion of this work for you.
> Why would you run the two following commands to wipe your bucket:
```
aws s3api list-object-versions --bucket rsavordelli --output json --query
    'Versions\[\].\[Key, VersionId\]' | jq -r '.\[\] | "--key '\\''" + .\[0\] + "'\\''
         --version-id " + .\[1\]' |  xargs -L1 aws s3api delete-object --bucket rsavordelli
aws s3api list-object-versions --bucket rsavordelli --output json --query
     'DeleteMarkers\[\].\[Key, VersionId\]' | jq -r '.\[\] | "--key '\\''" + .\[0\] + "'\\''
         --version-id " + .\[1\]' |  xargs -L1 aws s3api delete-object --bucket rsavordelli
```
> when you could run:
```
s3bro purge --bucket rsavordelli
```
> what if you need to restore all your keys from glacier storage class? Or just some of them?
```
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
```
----
# Overview
#### Available commands
 - [restore](#restore)
 - [purge](#purge)
 - [scanperms](#scanperms)

# Installation
```
 virtualenv .
 source bin/activate
 pip install git+git://github.com/rsavordelli/s3bro/ -U
```
# Examples
```
# s3bro restore --help
# s3bro restore --bucket bucketName --prefix myglacierPrefix --days 20 --type Bulk
# s3bro restore --bucket bucketName --prefix myglacierPrefix --days 20 --type Bulk --include .css --versions
# s3bro restore --bucket bucketName --prefix myglacierPrefix --days 20 --type Bulk --exclude .exe --update-restore-date
# s3bro purge --bucket bucketName
```
# Commands
##  restore
 Restore S3 keys in Glacier Storage class
#### Options
```
--bucket <bucket name>  [required]
--days  <days to restore>  [required]
--type <Standard|Expedited|Bulk> [required]
--prefix <your Prefix>
--include <string to match | and include> (accept multiple)
--exclude <strign to match | and exclude> (accept multiple)
--workers <how many workers to spawn> [default 10]
--versions  [default false]
--update-restore-date [default false]
--log-level <INFO|DEBUG|ERROR|WARNING> [default ERROR]
```
### Details:
 - --bucket -  (String) - should be your bucket name
 - --days - (integer) - how many days you want to keep the s3 keys restored
 - --type - The type of glacier restore (check aws docs as it has cost implications)
 - --prefix (string) - filter the content that will be restored (similar to aws cli)
 - --include (string) - only restore keys that match with the string passed. Note: You can pass --include multiple times to specify
   different patterns
 - --exclude (string) - skip keys that match with the pattern passed through it. You can also give multiple inputs by repeating --exclude
 - --workers (integer) - how many workers to spawn to help with the restoring process
 - --versions (None) - if passed, it will include all versions (current and non-current versions)
 - --update-restore-date (None) - if passed, it will check for already restored keys and update the restore expiration. It will "extend" the
   restore. Note: It does not send the restore again, it just replace
   the date.
 - --log-level <INFO|DEBUG|ERROR|WARNING> - Default is ERROR

## purge

 Delete all keys within a bucket - as simple as that (versions, delete markers, everything)

### Options
```
  --bucket TEXT  Bucket name  [required]
  --prefix TEXT  prefix name  [optional]
  --yes          first confirmation
  --yes-really   second confirmation
  --help         Show this message and exit.
  --log-level <INFO|DEBUG|ERROR|WARNING> [default ERROR]
```
### Details
> You can bypass the confirmations passing the --yes --yes-really (yes, it confirms twice). I don't want to hear no anyone crying about this.

> It does not delete your bucket, only the data inside it
## scanperms

Look for objects with Public permissions in your bucket
### Options
```
 --bucket TEXT Bucket Name
 --prefix TEXT  prefix name  [optional]
 --workers (integer) - how many workers to spawn to help with the restoring process
 --log-level <INFO|DEBUG|ERROR|WARNING> [default ERROR]
```
> Note: Not support for versions. Only current versions

# TODO
- refine setuptools and pip to host this tool in pip repository
- implement tests
- new feature are being added frequently