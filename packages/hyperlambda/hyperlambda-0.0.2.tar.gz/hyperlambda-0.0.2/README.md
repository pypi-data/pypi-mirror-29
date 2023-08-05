
hyperlambda: A low-level client representing AWS Lambda
======================

**hyperlambda** helps you to execute your script on aws instances .

Creates a new Lambda function. The function metadata is created from the request parameters, and the code for the function is provided by a .zip file in the request body. 

Installation
============

Using pip:

    $ pip install hyperlambda

PyPi package page https://pypi.python.org/pypi/hyperlambda/

From source:

    $ git clone https://github.com/SenseHawk/HyperLambda.git
    $ cd hyperlambda
    $ python setup.py install

Note that this program requires Python 2.7 or higher.

Command Line Interface
======================


    $ hyperlambda --help
    usage: hyperlambda <command> [<args>]
            The most commonly used hyperlambda commands are:
            configure     Configure the settings
            invoke_function      create and execute lambda function

    Create a Hyper Lambda Instance to Execute Script

    positional arguments:
      command     Subcommand to run

    optional arguments:
      -h, --help  show this help message and exit
  

    >>>hyperlambda configure:
        The Hyperlambda will prompt you for four pieces of information. AWS Access Key ID and AWS Secret Access Key are your account credentials.

      AWS Access Key ID : AKIAIOSFODNN7EXAMPLE
      AWS Secret Access Key : wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
      Default region name : us-west-2
      Security Group Ids<list> : list<>
      key Name : 'string'
      Volume Size(GiB): 8
      Instance Type : string
      Spot Price: float


    >>>hyperlambda invoke_function:
        Create a Hyper Lambda Instance and execute the script given.

      arguments:
        --runtime RUNTIME     The runtime environment for the Lambda function you are uploading. Defaults to python2.7
        --role ROLE           The Amazon Resource Name (ARN) of the IAM role that Lambda assumes when it executes your function 
                              to access any other Amazon Web Services (AWS) resources.
        --timeout TIMEOUT     The function execution time at which Lambda should terminate the function. The Default is 180 seconds
        --handler HANDLER     The function within your code that Lambda calls to begin execution.
        --code CODE           The code for the Lambda function.
        --zip-file ZIP_FILE   The URL to the zip file of the code you are uploaded
        --data DATA           A dictionary that you want to provide to your Lambda function as input
        --environment ENVIRONMENT
                              The parent object that contains your environment's configuration settings.
        --userdata USERDATA   The location of the userdata file for the instance. eg: userdata.txt
        --tags [TAGS [TAGS ...]]
                              The list of tags (key-value pairs) assigned to the new function.

      instance arguments:
        --instance-type INSTANCE_TYPE
                              The type of the instance to be created
        --key-name KEY_NAME   The name of the key pair
        --security-group-ids SECURITY_GROUP_IDS
                              One or more security group ids
        --callback-url CALLBACK_URL
                              Optional URL to be called after execution.
    
    example: hyperlambda invoke_function --function-name string --runtime python2.7 --handler filename.function_name --zip-file url --timeout seconds --environment '{"Variables": {string: string}}' --data '{key: value, key: value}' --userdata userdata.txt            


BasicUsage
------------

    from hyperlambda import client
    obj = client.lamda()
  
    response = obj.invoke_function(
      function_name='string',
      runtime='python2.7'|'python3.6'
      role='string',
      handler='string',
      zip_file= b'url',
      timeout=123,
      environment={
          'Variables': {
            'string': 'string'
          }
      },
      userdata='string',
      data={
        'string': 'string'
      },
      security_group_ids=[
            'string',
          ],
      key_name='string',
      tags={
        'string': 'string'
      },
      callback_url = 'string'
    )

    

Reporting bugs and submitting patches
=====================================

Please check our `issue tracker`_ for known bugs and feature requests.

We accept pull requests for fixes and new features.

