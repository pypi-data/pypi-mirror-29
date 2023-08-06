##Installation
1. Get the code: pip install uidgenerator-utils
2. Add "uidgenerator" to your INSTALLED_APPS


##Usage

* To use it in your model class:

```
	from django.db import models
	from uidgenerator.models import UIDField
	
	class Tag(models.Model):
		tag_id = UIDField(primary_key=True)
		....
```

* if you want to change the default configuration, alter the parameter in settings:

```
UIDGENERATOR_START_TIMESTAMP = 1514736000000 #2018-1-1 0:0:0
UIDGENERATOR_REGIONIDBITS = 3
UIDGENERATOR_WORKERIDBITS = 10
UIDGENERATOR_SEQUENCEBITS = 10

UIDGENERATOR_REGIONID = 1
UIDGENERATOR_WORKERID = 1
```
