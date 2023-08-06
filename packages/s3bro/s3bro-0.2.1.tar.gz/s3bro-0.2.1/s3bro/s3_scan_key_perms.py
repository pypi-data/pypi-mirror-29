import boto3
import click
from pool_map import multi_process
import logging
from termcolor import colored

public_perms = "http://acs.amazonaws.com/groups/global/AllUsers"


def get_bucket_permission(bucket):
    s3 = boto3.resource( 's3' )
    bkt = s3.Bucket( bucket )
    bucket_acl = bkt.Acl().grants
    owner = bkt.Acl().owner['ID']
    perms = {'Public': [], 'Canonical': [], 'Owner': []}
    print("Owner ID: %s" %owner)
    for p in bucket_acl:
        if p['Grantee']['Type'] == "Group":
            if p['Grantee']['URI'] == public_perms:
                perms['Public'].append(p['Permission'])
        if p['Grantee']['Type'] == "CanonicalUser":
            o = p['Grantee']['ID']
            if owner != o:
                perms['Canonical'].append(p['Permission'])
            if owner == o:
                perms['Owner'].append( p['Permission'] )
    if perms['Public']:
        print(colored('Public Access: %s', 'red')) % perms['Public']
    if perms['Canonical']:
        print(colored('Canonical Access: %s', 'yellow')) % perms['Canonical']
    print(colored('You: %s', 'green')) % perms['Owner']


def get_permission(x):
    s3 = boto3.resource( 's3' )
    bucket, key = x[0], x[1]
    bkt = s3.Bucket( bucket )
    owner = bkt.Acl().owner['ID']
    obj = s3.Object(bucket, key)
    obj_acl = obj.Acl().grants
    perms = {'Public': [], 'Canonical': [], 'Owner': []}
    for p in obj_acl:
        if p['Grantee']['Type'] == "Group":
            if p['Grantee']['URI'] == public_perms:
                perms['Public'].append( p['Permission'] )
        if p['Grantee']['Type'] == "CanonicalUser":
            o = p['Grantee']['ID']
            if owner != o:
                perms['Canonical'].append(p['Permission'])
            if owner == o:
                perms['Owner'].append( p['Permission'] )

    if perms['Public'] or perms['Canonical']:
        print('KEY: %s ; Permissions: %s' % (key, perms))
    else:
        logging.warning('Key is Safe: %s' % key)


def scan_key_perms(scanperms, bucket, prefix, workers):
    s3 = boto3.resource( 's3' )
    bkt = s3.Bucket( bucket )
    click.echo('Scanning bucket permissions')
    # get bucket permissions first
    get_bucket_permission(bucket)
    click.echo(30*'=')
    click.echo('Scanning object permissions')
    objects = []
    iterator = bkt.objects.filter( Prefix=prefix )
    processed = False
    keys_processed = 0
    for k in iterator:
        keys_processed += 1
        processed = False
        if len(objects) < 1000:
            objects.append( [bucket, k.key] )
        else:
            multi_process(get_permission, objects, workers)
            del objects[:]
            processed = True
    if not processed:
        multi_process(get_permission, objects, workers)

    click.echo('{} keys processed'.format(keys_processed))