import gzip
from logging import getLogger

import boto3
from botocore.exceptions import ClientError

from requests_cache import SerializerPipeline, Stage, pickle_serializer
from requests_cache.backends import BaseCache, BaseStorage

logger = getLogger(__name__)

class S3Cache(BaseCache):
  def __init__(
    self,
    bucket_name,
    access_key_id,
    secret_access_key,
    endpoint_url,
    prefix='lego-store-availability/cache',
    **kwargs
  ):
    super().__init__(**kwargs)

    session = boto3.Session(
      aws_access_key_id=access_key_id,
      aws_secret_access_key=secret_access_key
    )

    self.client = session.client(
      's3',
      endpoint_url=endpoint_url
    )

    s3_resource = session.resource(
      's3',
      endpoint_url=endpoint_url
    )
    self.bucket = s3_resource.Bucket(bucket_name)

    self.redirects = S3Storage(
      "redirects",
      self.client,
      self.bucket,
      f"{prefix}/redirects",
      **kwargs
    )
    self.responses = S3Storage(
      "responses",
      self.client,
      self.bucket,
      f"{prefix}/responses",
      **kwargs
    )

class S3Storage(BaseStorage):
  def __init__(self, name, client, bucket, prefix, **kwargs):
    serializer = SerializerPipeline([
      pickle_serializer, # Serialize to a Pickle string
      Stage(dumps=gzip.compress, loads=gzip.decompress), # Compress
    ])
    super().__init__(serializer=serializer, **kwargs)

    self.name = name

    self.client = client
    self.bucket = bucket
    self.prefix = prefix

  def __getitem__(self, key):
    try:
      res = self.client.get_object(
        Bucket=self.bucket.name,
        Key=f"{self.prefix}/{key}"
      )
    except ClientError as error:
      if error.response['Error']['Code'] == 'NoSuchKey':
        raise KeyError from error

      raise error

    logger.debug("%s | Get %s", self.name, key)

    return self.serializer.loads(res['Body'].read())

  def __setitem__(self, key, value):
    logger.debug("%s | Set %s", self.name, key)

    self.client.put_object(
      Bucket=self.bucket.name,
      Key=f"{self.prefix}/{key}",
      Body=self.serializer.dumps(value)
    )

  def __delitem__(self, key):
    logger.debug("%s | Delete %s", self.name, key)

    self.client.delete_object(
      Bucket=self.bucket.name,
      Key=f"{self.prefix}/{key}"
    )

  def __iter__(self):
    res = self.client.list_objects(
      Bucket=self.bucket.name,
      Prefix=self.prefix
    )
    for obj in res['Contents']:
      yield obj['Key']

  def __len__(self):
    res = self.client.list_objects(
      Bucket=self.bucket.name,
      Prefix=self.prefix
    )

    return len(res['Contents'])

  def clear(self):
    self.bucket.objects.filter(Prefix=self.prefix).delete()
