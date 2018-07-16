import boto3
import io
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    s3 = boto3.resource('s3')

    topic = sns.Topic('arn:aws:sns:us-east-1:078411551710:DeploySiteTopic')

    try:
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

        print('Site deployment completed.')
        topic.publish(Subject="Site Deployed", Message="New ServerlessAnalytics.io site build and deployment successful.")
    except:
        print('Site deployment failed.')
        topic.publish(Subject="Site Failed Deploy", Message="New deployment of ServerlessAnalytics.io not deployed successful.")
        raise

    return 'Lambda function was called to deploy site.'
