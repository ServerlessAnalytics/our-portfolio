import boto3
import io
import zipfile
import mimetypes

def lambda_handler(event, context):
    s3 = boto3.resource('s3')

    site_bucket = s3.Bucket('serverlessanalytics.io')
    build_bucket = s3.Bucket('build.serverlessanalytics.io')

    build_zip = io.BytesIO()
    build_bucket.download_fileobj('ServerlessAnalyticsBuild', build_zip)

    with zipfile.ZipFile(build_zip) as myzip:
        for name in myzip.namelist():
            obj = myzip.open(name)
            site_bucket.upload_fileobj(obj, name,
            ExtraArgs={'ContentType': mimetypes.guess_type(name)[0]})
            site_bucket.Object(name).Acl().put(ACL='public-read')

    return 'Lambda function called to deploy site.'
