---
title: "Encryption configuration"
sub_link: "Encryption"
meta_title: "Encryption configuration in Polyaxon - Configuration"
meta_description: "Polyaxon's Encryption configuration."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - docker-compose
sidebar: "configuration"
---

Polyaxon might need to save some sensitive information other than passwords in the database. 
By default Polyaxon uses Kubernetes secrets for accessing all users provided secrets, but sometime it might need to also store some additional information. 
The way Polyaxon does it is by obfuscating the data and then applying an encryption to the values based on Fernet before saving the information.

## Enable encryption

In order to enable the encryption, the user must provide an encryption secret, 
you need to provide a secret containing a key `POLYAXON_ENCRYPTION_SECRET`.

You can use this to generate a valid secret:

```python
Fernet.generate_key()
```

> N.B. Please you should know that changing the secret will lock access to any previously saved value in the DB, 
You need to delete previous values and set new ones