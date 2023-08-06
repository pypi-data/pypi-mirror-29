# actappliance #

### Use case ###
This repo abstracts the type of connection you are making to an actifio appliance. You can write a test or use case one
way ane execute over SSH or RESTful connections. 

The primary idea being that all sent commands can look like CLI as it is shorter and more people are familiar with it,
while the responses look like the RESTful API's JSON returns as they are easier to parse.
It also allows direct commands using either connection with the same contract of CLI like requests and RESTful like
responses for the case where the call is unreliable unusable for whatever reason (CLI permissions, arbitrary outputs). 

# Functionality of Library #

First create your appliance/sky/uds object:

> a = Appliance(ip_address=<sky or cds ip>, hostname=<sky or cds dns name>) # hostname or ip_address required
> ex. a = Appliance(ip_address=8.8.8.8)

With default settings it will try to send RESTful calls for all cmd methods.

```
>>> a.a.cmd('udsinfo lsversion')
{u'status': 0, u'result': [{u'version': u'7.0.0.68595', u'component': u'CDS', u'installed': u'2016-03-07 12:14:37'}, {u'version': u'7.0.0.68595', u'component': u'psrv-revision', u'installed': u'2016-03-07 12:14:37'}]}
```
Note: You will likely see debug messages if your log levels aren't set!

If you store the return the object has additional methods like parse and raise_for_error.
```
>>> act_response = a.a.cmd('udsinfo lsversion')
>>> act_response.parse()
{u'version': u'7.0.0.68595', u'component': u'CDS', u'installed': u'2016-03-07 12:14:37'}
```

### Parse ###
The parse method tries to simplify interactions with our RESTful responses. It only returns dictionaries and strings. It
will never return a list! In the case above you can see it returned the first relevant dictionary it found. If the info
you desire was the version of the psrv-revision component you would use m_k='component' (search key is component), 
m_v='psrv-revision' (matching value is psrv-revision). Those two inputs in action:
```
>>> act_response.parse(m_k='component', m_v='psrv-revision')
{u'version': u'7.0.0.68595', u'component': u'psrv-revision', u'installed': u'2016-03-07 12:14:37'}
```
However we wanted the version not the whole dicitonary so we would add k='version' (search for key version in the dict 
and return the corresponding value).
The full command and result:
```
>>> act_response
{u'status': 0, 'errorcode': 8675309, 'errormessage': 'Something went wrong', u'result': [{u'version': u'7.0.0.68595', u'component': u'CDS', u'installed': u'2016-03-07 12:14:37'}, {u'version': u'7.0.0.68595', u'component': u'psrv-revision', u'installed': u'2016-03-07 12:14:37'}]}
>>> act_response.parse(m_k='component', m_v='psrv-revision', k='version')
u'7.0.0.68595'
```
Here we can see the use of parse is to simplify basic parsing of appliance responses.

* Advanced example
If you have used parse for a while, you probably have come to understand how it functions. Overreliance on parse may
lead to writing code like the following:

`ids = [act_response.parse(backups, k='id', index=backup) for backup in range(len(backups))]`

The above is considered ugly. When doing something like the above rewriting it to avoid using parse, but instead perform
 it's action. The following has an identical result to the above line:

`ids = [data['id'] for data in backups['result']]`

If you want to avoid list comprehensions you could do the following

```
ids = []
for data in backup['results']:
    ids.append(data['id'])
```

### Raise_for_error ###
The raise_for_error method does self inspection of the dictionary to determine if an Actifio related error occurred.
These errors do not include connection errors like failing to authenticate and get a valid REST sessionid. These are
specifically for errors that are bubbled up to the user when interacting with an Actifio appliance. The response objects
have two attributes "errormessage" and "errorcode" which you can use to handle errors that should not end the test.

* Basic example
```
>>> r = self.a.cmd('udsinfo lsversion -l')
>>> r.raise_for_status()
Response: {u'errorcode': 10010, u'errormessage': u'invalid option: l'}
```

This raised an error because -l is not a valid option for "udsinfo lsversion". The error object itself has direct access
to errorcode and errormessage. You can handle these exceptions as needed:
```
>>> from actappliance.act_errors import ACTError
>>> try:
...     r.raise_for_error()
... except ACTError as e:
...     if e.errorcode == 10010:
...         # handle or allow this error
...         print("I am allowing this error")
...     else:
...         raise
```

An alternative way to handle this would be to catch the specific error:
```
>>> from actappliance.act_errors import act_errors
>>> try:
...     r.raise_for_error()
... except act_errors[10010]:
...     # handle or allow this error
...     print("I am allowing this error")
```


Note: If your command needs to specifically be rest OR ssh and cannot function or is an inaccurate test if sent the 
other way use the specific methods instead of cmd.

### Have fun!
![Lots of fun](http://i.imgur.com/fzhEnP0.png)


