# Coherence API Python Client
### Run code online faster with Coherence API.

Coherence lets you deploy and run your code on a server with only two lines of code.

[Read the Docs.](https://www.coherenceapi.com/docs)

## Install Easily with `pip`

Install the `coherenceapi` python package using `pip`.

```bash
$ pip install coherenceapi
```

## Start with only Two Lines of Code

1. [Sign up for an API key.](https://coherenceapi.com/app)

2. Create `start.py`

```python
import socket
from coherence import coherence

coherence.set_api_key("my-api-key")
serverHostname = coherence.run(lambda: socket.gethostname())

myHostname = socket.gethostname()
print("My Hostname:", myHostname)
print("Server Hostname:", serverHostname)
```

Any lambda passed to `coherence.run()` is serialized, deployed, and run on Coherence API's servers.

## Run Recurring jobs

It's easy to run jobs on a cron schedule, replacing whatever external scheduling system you have with only your code.

```python
from coherence import coherence
from myEmailSender import sendReminder

coherence.set_api_key("my-api-key")

# A cron expression to send a reminder every monday at midnight
schedule = "0 0 0 * * 1"

# Send an email reminder every monday at midnight.
job_id = coherence.run_recurring(schedule,
    lambda: sendReminder("welovedevs@coherenceapi.com")
```

## All the Details are in the Docs

[Read the Docs.](https://www.coherenceapi.com/docs)
