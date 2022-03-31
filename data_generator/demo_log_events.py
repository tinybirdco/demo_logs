from re import I
import string
import requests
import json
from datetime import datetime, timedelta
import click
import random

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
@click.option('--datasource', help ='the destination datasource. Default = build_log', default='build_log')
@click.option('--sample', help = 'number of messages simulated in each repetition. Default = 100', type=int, default=100)
@click.option('--events', help = 'number of events per request. Sent as NDJSON in the body. Default = 50', type=int, default=50)
@click.option('--repeat', type=int, default=1)
@click.option('--silent', is_flag=True, default=False)
@click.option('--d_from', help = 'used along d_to to simulate data from the past. d_from lets you select the number of days previous to today for starting the simulation. Default = 0', type=int, default=0)
@click.option('--d_to', help = 'used along d_from to simulate data from the past. d_to lets you select the number of days previous to today for ending the simulation. Default = 0', type=int, default=0)
def send_hfi(datasource,
             sample,
             events,
             repeat,
             silent,
             d_from,
             d_to
             ):
 
  with open ("./.tinyb") as tinyb:
    token = json.load(tinyb)['token']
   
  id_event = random.randint(0, 1000000000)
  build_id = random.randint(0, 1000000000)
  for _ in range(repeat):
      
    #projectId = 'prj_' + ''.join(random.choices(string.ascii_letters + string.digits, k = 30))
    #deploymentId = 'dpl_' + ''.join(random.choices(string.ascii_letters + string.digits, k = 30))
    projectId = random.choices(['prj_BDqTqm81F4l6rtC0zhTujXOsqk5igr','prj_7p28UEeoDR533iYE79FOpF0JQmsh2Q','prj_JrevsvR1WgGaICCMDSpOOvyR8gsHF7','prj_785sDMqcq9qjreGsnYinoKMOulAnGw','prj_17sfKwWvGkRwqeY8Wifh6hwtxDojJ4'],k=events)
    deploymentId = random.choices(['dpl_UOZqbYsJvjbGiScsfAE43P2C92wu7C','dpl_doOhm4IGNFB7jMZOeIQi9FaHaELnfQ','dpl_TRsVuLI2StYcyXneoqx1KBneXDYsqy','dpl_wlwpJriCKrgSqCyXVjzTflx6CFnA9z','dpl_SVPY6RrsolCMQzSMdYGvl9KsPVmbeu','dpl_hKpVdorWlllc4tx3wwJw7lgktxxhwJ','dpl_qjdzP0Oe7q4StDtM4lG37Tfj5Dc1cr','dpl_HGb13aLJHpO4IqN1T6UIEcP12CEHTM','dpl_wWwHycmpZhjjPN78s5VBLYCLL3rJF2','dpl_1sGqOZwb9ksNnkk33jrMB7Mp4TKuSu'],k=events)
    logLevel = random.choices(['WARNING','DEBUG','ERROR'],k=events)
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
    destination = random.choices(['http','https'],k=events)
    body_message = random.choices(['Package Deployed','Loading File into database','Running Instance','Cleaning Memory Buffer'],k=events)
  
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

        if (d_from != 0):
            delta_days=random.randint(d_to,d_from)
            delta_seconds=random.randint(1,3600*24)

        message = {
        'timestamp': (datetime.utcnow() - timedelta(days=delta_days, seconds=delta_seconds)).isoformat() if (d_from != 0) else datetime.utcnow().isoformat(),
        'projectId':  projectId[i%events],
        'id': str(id_event),
        'deploymentId': deploymentId[i%events],
        'message': (f"{logLevel[i%events]}: {body_message[i%events]} RequestId: {requestId} Version: LATEST\n Init Duration: {initDuration} ms Duration: {duration} ms Memory Used: {memoryUsed} MB"),
        'logLevel': logLevel[i%events]
        }
        if(datasource == 'build_log'):
            message.update(
            {'buildId': str(build_id),
            'entrypoint': entrypoint[i%events]
            })
        if(datasource == 'lambda_log' or datasource == 'rewrite_log'):
            message.update(
            { 'requestId': requestId,
            'requestPath': request_path[i%events],
            'region': region[i%events],
            'cacheId': cacheId,
            'scheme': scheme[i%events],
            'httpMethod': http_method[i%events],
            'edgeStatusCode': status_code[i%events],
            'userAgent': userAgent[i%events],
            'duration': duration,
            'initDuration': initDuration,
            'memoryUsed': memoryUsed,
            'clientIp': clientIp,
            'referer': (f"https://{referer[i%events]}.vercel.app/")
            })
            if(datasource == 'rewrite_log'):
                message.update({ 'destination': destination[i%events]})

        nd.append(message) 
        if len(nd) == events:
            send_event(datasource, token, nd)
            nd = []
        if not(silent):
            print(message) 
        #if ((i % (sample /12)) == 0):
        #    deploymentId = 'dpl_' + ''.join((random.choice(string.ascii_letters) for x in range(30)))
        #if ((i % (sample /7)) == 0):
            #projectId = 'prj_' + ''.join(random.choices(string.ascii_letters + string.digits, k = 30))
    send_event(datasource, token, nd)
    nd = []


if __name__ == '__main__':
    send_hfi()