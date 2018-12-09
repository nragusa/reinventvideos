import boto3
import json
import os
import re
from botocore.exceptions import ClientError

PODCAST_TABLE = os.environ['PODCAST_TABLE']
ddb = boto3.resource('dynamodb')
PODCAST_TABLE_CLIENT = ddb.Table(PODCAST_TABLE)
YEAR_REGEX = re.compile(r'20[1-9]{1}[0-9]{1}')

def main(event, context):
    for record in event['Records']:
        key = record['s3']['object']['key']
        print('New object added {}'.format(key))
        paths = key.split('/')
        # podcasts/2018/ARC201.m4a
        if len(paths) == 3:
            year_match = re.search(YEAR_REGEX, paths[1])
            if year_match:
                year = year_match.group()
                podcast_file = paths[2]
                if podcast_file.endswith('.mp3') or podcast_file.endswith('m4a'):
                    # and a file that ends in mp3 or m4a - success
                    try:
                        url = '/' + key
                        response = PODCAST_TABLE_CLIENT.put_item(
                            Item={
                                'session': podcast_file.split('.')[0],
                                'year': year,
                                'url': url
                            }
                        )
                    except ClientError as error:
                        print('Problem updating table {}'.format(error))
                else:
                    print('Found incompatible podcast extension')
            else:
                print('Found incompatible year')
        else:
            print('Invalid path sent to function')
