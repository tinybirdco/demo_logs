import string
import faker
import requests
import json
from datetime import datetime, timedelta
import click
import random
from faker import Faker
import uuid

from requests_toolbelt import user_agent

def send_event(ds: str, token: str, messages: list):
  params = {
    'name': ds,
    'token': token,
    'wait': 'false',
  }
  data = '\n'.join(json.dumps(m) for m in messages)
  r = requests.post('https://api.tinybird.co/v0/events', params=params, data=data)
  # uncomment the following two lines in case you don't see your data in the datasource
  # print(r.status_code)
  # print(r.text)

@click.command()
@click.option('--datasource', help ='the destination datasource', default='build_log')
@click.option('--sample', help = 'number of messages simulated in each repetition', type=int, default=100)
@click.option('--events', help = 'number of events per request. Sent as NDJSON in the body', type=int, default=87)
@click.option('--repeat', type=int, default=1)
@click.option('--silent', is_flag=True, default=False)
def send_hfi(datasource,
             sample,
             events,
             repeat,
             silent
             ):
 
  with open ("./.tinyb") as tinyb:
    token = json.load(tinyb)['token']
   
  id_event = random.randint(0, 1000000000)
  build_id = random.randint(0, 1000000000)
  for _ in range(repeat):
    projectId = 'prj_' + ''.join(random.choices(string.ascii_letters + string.digits, k = 30))
    deploymentId = 'dpl_' + ''.join(random.choices(string.ascii_letters + string.digits, k = 30))
    logLevel = random.choices(['Warning','Debug','Error'],k=events)
    entrypoint = random.choices(['package.json','downloading','python','docker'],k=events)
    http_method = random.choices(['GET','POST','PUT','DELETE','HEAD','OPTIONS'],k=events)
    region = random.choices(['US','EU'],k=events)
    userAgent = random.choices(['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
                                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'],k=events)
    request_path = random.choices(['/api/data','/api/event','/api/pipe'],k=events)
    referer = random.choices(['tinybird.','speedwins','log_company'],k=events)
    scheme = random.choices(['http','https'],k=events)
    status_code = random.choices([200,400,403,500],k=events)
  
    nd = []
    
    for i in range(sample):
        id_event += 1
        build_id += 1
        requestId = '-'.join(''.join(random.choices(string.ascii_lowercase + string.digits, k = 6)) for _ in range(6))
        cacheId = ''.join(random.choices(string.ascii_lowercase + string.digits + '-', k = 15))
        clientIp = ".".join((str(random.randint(0, 255)) for _ in range(4)))
        duration = random.randint(5, 3000)
        initDuration = random.randint(5, 500)
        memoryUsed = random.randint(5, 10000)

        message = {
        'timestamp': datetime.utcnow().isoformat(),
        'projectId':  projectId,
        'id': str(id_event),
        'deploymentId': deploymentId,
        'message': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        'ownerId': str(id_event)
        }
        if(datasource == 'build_log'):
            message.update(
            {'buildId': str(build_id),
            'deploymentId': deploymentId,
            'entrypoint': entrypoint[id_event%events],
            'logLevel': logLevel[id_event%events]})
        if(datasource == 'lambda_log' or datasource == 'rewrite_log'):
            message.update(
            { 'requestId': requestId,
            'requestPath': request_path[id_event%events],
            'functionPath': request_path[id_event%events],
            'region': region[id_event%events],
            'cacheId': cacheId,
            'scheme': scheme[id_event%events],
            'httpMethod': http_method[id_event%events],
            'functionStatusCode': status_code[id_event%events],
            'edgeStatusCode': status_code[id_event%events],
            'userAgent': userAgent[id_event%events],
            'duration': duration,
            'initDuration': initDuration,
            'memoryUsed': memoryUsed,
            'clientIp': clientIp,
            'referer': (f"https://{referer[id_event%events]}.vercel.app/")
            })
            if(datasource == 'rewrite_log'):
                message.update({ 'destination': 'destination'})

        nd.append(message) 
        if len(nd) == events:
            send_event(datasource, token, nd)
            projectId = 'prj_' + ''.join(random.choices(string.ascii_letters + string.digits, k = 30))
            nd = []
        if not(silent):
            print(message) 
        if len(nd) % (events /10) == 0:
            deploymentId = 'dpl_' + ''.join((random.choice(string.ascii_letters) for x in range(30)))
    send_event(datasource, token, nd)
    nd = []


if __name__ == '__main__':
    send_hfi()