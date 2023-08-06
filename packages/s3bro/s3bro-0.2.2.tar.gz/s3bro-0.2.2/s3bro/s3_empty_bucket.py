import boto3
import click
import logging
import time, sys


def clean_bucket(bucket, prefix):
    s3 = boto3.resource( 's3' )
    click.echo('I will start the cleaning %s in 10 seconds, you still have the chance to stop' %bucket)
    for remaining in range( 10, 0, -1 ):
        sys.stdout.write( "\r" )
        sys.stdout.write( "{:2d} seconds remaining.".format( remaining ) )
        sys.stdout.flush()
        time.sleep( 1 )
    click.echo('\nStart cleaning...')
    bkt = s3.Bucket(bucket)
    iterator = bkt.object_versions.filter( Prefix=prefix )
    objects = []
    for obj in iterator:
        objects.append( {'Key': obj.key, 'VersionId': obj.id} )
        logging.warning('Sending to deletion: %s %s' % (obj.key, obj.id))
        if len(objects) == 1000:
            response = bkt.delete_objects(Delete={'Objects': objects})
            objects = []
    if len(objects) > 0:
        click.echo('You have only %s keys, deleting'%len(objects))
        response = bkt.delete_objects( Delete={'Objects': objects} )
    else:
        print('it seem that you got no keys')

