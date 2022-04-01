# Using Tinybird with a Demo Log

This repository contains the data project —[datasources](./datasources), and [endpoints](./endpoints)— and [data-generator](./data-generator) scripts for a log example of using Tinybird.

To clone the repository:

`git clone git@github.com:tinybirdco/demo_logs.git`

`cd demo_logs`

## Working with the Tinybird CLI

To start working with data projects as if they were software projects, let's install the Tinybird CLI in a virtual environment.
Check the [CLI documentation](https://docs.tinybird.co/cli.html) for other installation options and troubleshooting.

```bash
virtualenv -p python3 .e
. .e/bin/activate
pip install tinybird-cli
tb auth --interactive
```

Choose your region: __1__ for _us-east_, __2__ for _eu_

Go to your workspace, copy a token with admin rights and paste it. A new `.tinyb` file will be created.  

## Project description

```bash
├── datasources
│   ├── build_log.datasource
│   ├── lambda_log.datasource
│   └── rewrite_log.datasource
├── endpoints
│   ├── count_log.pipe
│   ├── get_filter_values.pipe
│   └── query_logs.pipe  
```

In the `/datasources` folder we have three Data Sources:

- build_log: where we'll be sending build log events.
- lambda_log: where we'll be sending lambda log events.
- rewrite_log: where we'll be sending rewrite log events.

And five .pipe files in the `/endpoints` folder:

- query_logs: Retrieve timestamp and message data every events filtered by channel, project_id, deployment_id and log_level.
- count_log: Retrieve the number of rows in all the logs.
- get_filter_values_channel: Retrieve distinct values for channel, project, deploymert and log level.

Note:
Typically, in big projects, we split the .pipe files across two folders: /pipes and /endpoints

- `/pipes` where we store the pipes ending in a datasource, that is, [materialized views](https://guides.tinybird.co/guide/materialized-views)
- `/endpoints` for the pipes that end in API endpoints.

## Authentication

You'll need cli-authentication before executing the next steps [cli-authenticate](https://docs.tinybird.co/cli/workspaces.html#authenticate), given that the token will be readed from the file .tinyb.

```bash
tb auth
Copy the admin token from https://ui.tinybird.co/tokens and paste it here: <pasted token>
** Auth successful!
** Configuration written to .tinyb file, consider adding it to .gitignore
```

Here you must paste your Tinybird token.

## Pushing the data project to your Tinybird workspace

Push the data project —datasources, pipes and fixtures— to your workspace.

```bash
tb push
```

Your data project is ready for realtime analysis. You can check the UI's Data flow to see how it looks.

![Data_flow](https://user-images.githubusercontent.com/51535157/161029357-bed71b97-0900-469c-8653-17169b7b57e3.png)

## Ingesting data using high-frequency ingestion (HFI)

Let's add some data through the [HFI endpoint](https://www.tinybird.co/guide/high-frequency-ingestion).

To do that we have created a python script to generate and send dummy events.

```bash
python3 data_generator/demo_log_events.py --datasource build_log --sample 100000 --events 100 --silent
```

Feel free to play with the parameters. You can check them with `python3 data_generator/demo_log_events.py --help`

## Advanced Token security

You now have your Data Sources and pipes that end in API endpoints.

The endpoints need a [token](https://www.tinybird.co/guide/serverless-analytics-api) to be consumed. You should not expose your admin token, so let's create one with more limited scope.

```bash
pip install jq

TOKEN=$(cat .tinyb | jq '.token'| tr -d '"')
HOST=$(cat .tinyb | jq '.host'| tr -d '"')

curl -H "Authorization: Bearer $TOKEN" \
-d "name=endpoints_token" \
-d "scope=PIPES:READ:query_logs" \
-d "scope=PIPES:READ:count_log" \
-d "scope=PIPES:READ:get_filter_values" \
$HOST/v0/tokens/
```

You will receive a response similar to this:

```json
{
    "token": "<the_newly_ceated_token>",
    "scopes": [
        {
            "type": "PIPES:READ",
            "resource": "query_logs",
            "filter": ""
        },
        {
            "type": "PIPES:READ",
            "resource": "count_log",
            "filter": ""
        },
        {
            "type": "PIPES:READ",
            "resource": "get_filter_values",
            "filter": ""
        }
    ],
    "name": "endpoints_token"
}
```

If you want to create a token to share just `query_logs` with, let's say, the channel with value build, you can do so with the __row level security__:

```bash
curl -H "Authorization: Bearer $TOKEN" \
-d "name=build_logs_token" \
-d "scope=PIPES:READ:query_logs" \
-d "scope=DATASOURCES:READ:query_logs:channel=build" \
$HOST/v0/tokens/
```

This project shows just some of the features of Tinybird. If you have any questions, come along and join our community [Slack](https://join.slack.com/t/tinybird-community/shared_invite/zt-yi4hb0ht-IXn9iVuewXIs3QXVqKS~NQ)!
