import jinja2
import boto3

loader = jinja2.FileSystemLoader('templates')
env = jinja2.Environment(autoescape=True, loader=loader)

def secretsmanager(input):
    input_dict = parse_reference(input)
    client = boto3.client('secretsmanager')
    params = { "SecretId": input_dict['secret-id']}
    if 'version-id' in input_dict: params['VersionId'] = input_dict['version-id']
    if 'version-stage' in input_dict: params['VersionStage'] = input_dict['version-stage']
    response = client.get_secret_value(**params)
    return response['SecretString']

def parse_reference(string):
    # sample reference string - https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references-secretsmanager.html
    # {{resolve:secretsmanager:secret-id:secret-string:json-key:version-stage:version-id}}
    values = string.split(':')
    keys = ["resolve", "secretsmanager", "secret-id", "secret-string", "json-key", "version-stage", "version-id"]
    return dict(map(lambda i,j : (i,j) , keys, values))


env.filters['secretsmanager'] = secretsmanager
print (env.get_template('template.j2').render())