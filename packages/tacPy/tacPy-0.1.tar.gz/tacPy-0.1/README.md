tacPy
=====

I don't know about you, but some things about the Talend Administration
Center UI are obnoxious to do, or at least monotonous.

Fortunately there's an API, so I figure I'd cook up a Python library
to work with it.

This thing isn't exactly polished, but it seems to do the trick.

## API Documentation ##
This is what I got my start with:

* [Invocation](https://help.talend.com/reader/rJGzSCBb8MvnaZHhs978KQ/ulwkupQQphDnbxaUbGscNg)
* [Command List](https://help.talend.com/reader/oYf9gKhmYrkWCiSua4qLeg/SLiAyHyDTjuznLR_F~MiQQ)

Note that these reference version 6.3

## Usage ##

### Quick Example ###
Let's get a list of tasks:
```
tac = tacPy.Client(tac_host='your.tachost.com', tac_name='org.talend.administrator', auth_user='user@company.com', auth_pass='p4ssw0rd')

r = tac.endpoint.listTasks()

for r.json()['result']:
    print('Project: {project} Task: {label} taskId: {id}'.format(project=task['projectName'], label=task['label'], id=task['id']))
```

### The Details ###

When a `Client` object is initiated, the "help" output is processed. This
library ships with a copy that I generated, which is used by default. If
you want to supply your own copy (see the reference docs), specify the
location to the file by way of the `help_file_location` argument.

This builds a list of attributes under the `endpoint` attribute of the
`Client` object that represent the various methods available. Which can
then be called as shown in the example above.

Calling the `Method` object returns the `response` object that the
`requests` library emits. This also gets stored in the `last_response`
attribute for that particular object.

Specific parameters for the method are passed as arguments like so:
```
r = tac.endpoint.taskLog(taskId=25, lastExecution=True)
```