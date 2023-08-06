import click
from s3_restore import *
from s3_empty_bucket import *
from s3_scan_key_perms import *
from __init__ import *

@click.group()
def cli():
    """This is your s3 friend(bro), that will help you with bucket iterations.
    Try:\n
    # s3bro restore --help\n
    # s3bro purge --help\n
    # s3tk --help\n
    """
    pass


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@cli.command()
@click.argument('restore', nargs=-1)
@click.option('--bucket', type=str, help='bucket name', required=True)
@click.option('--prefix', type=str, help=' prefix', default='')
@click.option('--days', type=int, help='Days to keep the restore', required=True)
@click.option('--type', type=click.Choice(['Standard', 'Expedited', 'Bulk']), help='restore type', required=True)
@click.option('--versions/--no-versions', default=False, help='[--no-versions is DEFAULT] - this option will make the restore to include all versions excluding delete markers')
@click.option('--update-restore-date/--do-not-update-restore-date', default=False, help='If passed, it will change the restore date for already restored key')
@click.option('--include', type=str, multiple=True, help='Only restore keys that ends with a given pattern, you can add '
                                                         'multiples patterns by inputing --include multiple times')
@click.option('--exclude', type=str, multiple=True, help='Do not restore if ends with a given pattern, you can add '
                                                         'multiple patterns by inputing --exclude multiple times')
@click.option('--workers', type=int, help='How many helpers to include in task, default is 10', default=10)
@click.option('--log-level', type=click.Choice(['INFO', 'ERROR', 'DEBUG', 'WARNING']), help='logging type', default='ERROR')
def restore(restore, bucket, prefix, days, type, versions, update_restore_date, workers, include, exclude, log_level):
    loglevel(log_level)
    collect_keys(restore, bucket, prefix, days, type, versions, update_restore_date, workers, include, exclude)


@cli.command()
@click.argument('purge', nargs=-1)
@click.option('--bucket', type=str, help='Bucket name', required=True)
@click.option('--prefix', type=str, default='', help='prefix name - optional')
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to wipe the bucket?', help="first confirmation")
@click.option('--yes-really', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt="I'm going to delete everything in your bucket, are you really sure?", help="second confirmation")
@click.option('--log-level', type=click.Choice(['INFO', 'ERROR', 'DEBUG', 'WARNING']), help='logging type', default='ERROR')
def purge(purge, bucket, prefix, log_level):
    loglevel(log_level)
    clean_bucket(bucket, prefix)


@cli.command()
@click.argument('scanperms', nargs=-1)
@click.option('--bucket', type=str, help='Bucket name', required=True)
@click.option('--prefix', type=str, default='', help='prefix name - optional')
@click.option('--workers', type=int, help='How many helpers to include in task, default is 10', default=10)
@click.option('--log-level', type=click.Choice(['INFO', 'ERROR', 'DEBUG', 'WARNING']), help='logging type', default='ERROR')
def scanperms(scanperms, bucket, prefix, workers, log_level):
    loglevel(log_level)
    scan_key_perms(scanperms, bucket, prefix, workers)

