import pyathena
import pymysql
import yaml

def get_db_info(config_file_path, db_name):

    with open(config_file_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    print('DB STATUS : {}'.format(config['phase']))

    db_info = config[db_name]

    host = db_info['host']
    port = db_info['port']
    user = db_info['user']
    passwd = db_info['passwd']

    return host, port, user, passwd

def get_db_connection(host, port, user, passwd):

    db = pymysql.connect(
        host=host,
        port=port,
        user=user,
        passwd=passwd
    )

    return db

def get_athena_db_info(config_file_path, db_name):

    with open(config_file_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    db_info = config[db_name]

    access_key = db_info['aws_access_key_id']
    secret_key = db_info['aws_secret_access_key']
    s3_path = db_info['s3_staging_dir']
    region = db_info['region_name']
    work_group = db_info['work_group']

    return access_key, secret_key, s3_path, region, work_group

def get_athena_db_connection(access_key, secret_key, s3_path, region, work_group):

    db = pyathena.connect(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        s3_staging_dir=s3_path,
        region_name=region,
        work_group=work_group
    )

    return db

