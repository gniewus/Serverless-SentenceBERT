
try:
  import unzip_requirements
except ImportError:
  pass

import json, re
from sentence_transformers import SentenceTransformer, util, models

import pandas as pd
import pymysql
from sqlalchemy import create_engine



import boto3,tarfile, io, base64, json,re
from os import environ

S3_BUCKET = environ['S3_BUCKET'] if 'S3_BUCKET' in environ else 'fallback-test-value'
MODEL_PATH = environ['MODEL_PATH'] if 'MODEL_PATH' in environ else 'fallback-test-value'
HUD_HOST = environ['HUD_HOST_URL'] if 'MODEL_PATH' in environ else 'fallback-test-value'
HUD_DATABASE_NAME = environ['HUD_DATABASE_NAME'] if "HUD_DATABASE_NAME" in environ else 'fallback-test-value'
HUD_LOGIN = environ.get('HUD_LOGIN') if 'HUD_LOGIN' in environ else 'fallback-test-value'
HUD_PASSWORD = environ.get('HUD_PASSW') if 'HUD_PASSW' in environ else 'fallback-test-value'
TABLE_NAME = environ.get('ARTICLES_TABLE')

db_connection = create_engine('mysql+pymysql://{}/hud'.format(HUD_HOST),echo=True)
s3 = boto3.client('s3')

def load_model_from_s3():
    try:
    # get object from s3
    #   obj = s3.get_object(Bucket=S3_BUCKET, Key=MODEL_PATH)
    # unzip it
    #   tar = tarfile.open(fileobj=bytestream, mode="r:gz")
        word_embedding_model = models.Transformer('T-Systems-onsite/bert-german-dbmdz-uncased-sentence-stsb',max_seq_length=512)

        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                                       pooling_mode_mean_tokens=True,
                                       pooling_mode_cls_token=False,
                                       pooling_mode_max_tokens=False)

        # join BERT model and pooling to get the sentence transformer
        model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
        return model
    except Exception as e:
        raise(e)

model = load_model_from_s3()


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
