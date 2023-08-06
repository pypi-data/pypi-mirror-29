<h1 align="center">AWS Client Bot for Python</h1>

<div align="center">

[![Documentation Status](https://readthedocs.org/projects/awsclientbot/badge/?version=latest)](http://awsclientbot.readthedocs.io/en/latest/?badge=latest)

</div>

Use this library to push messages from AWS EC2 instance to Telegram via [@aws_client_bot](https://t.me/aws_client_bot).

Step 1. Get AWS Client Bot token
* Go to [@aws_client_bot](https://t.me/aws_client_bot),
* Set AWS credentials (this allows start/stop instances from [@aws_client_bot](https://t.me/aws_client_bot)),
* Send "Get token",
* Use token on step 2

Step 2. Set logger
Typical usage looks like this::

    #!/usr/bin/env python

    from awsclientbot import AWSClientBot

    acb = AWSClientBot(token)
    acb.push("Started")
    my_long_running_function() <-- Replace this with your own function
    acb.push("Done")
