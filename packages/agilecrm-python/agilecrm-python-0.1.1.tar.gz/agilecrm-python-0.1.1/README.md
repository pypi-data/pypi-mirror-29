# agilecrm-python

agilecrm is an API wrapper for Agile CRM written in Python

## Installing
```
pip install agilecrm-python
```

## Usage
```
from agilecrm.client import Client

client = Client('API_KEY', 'EMAIL', 'DOMAIN')
```

Create contact
```
contact_data = {
    "star_value": "4",
    "lead_score": "92",
    "tags": [
        "Lead",
        "Likely Buyer"
    ],
    "properties": [
        {
            "type": "SYSTEM",
            "name": "first_name",
            "value": "Los "
        },
        {
            "type": "SYSTEM",
            "name": "last_name",
            "value": "Bruikheilmer"
        },
        {
            "type": "SYSTEM",
            "name": "company",
            "value": "steady.inc"
        },
        {
            "type": "SYSTEM",
            "name": "title",
            "value": "VP Sales"
        },
        {
            "type": "SYSTEM",
            "name": "email",
            "subtype": "work",
            "value": "akrambakram@yabba.com"
        },
        {
            "type": "SYSTEM",
            "name": "address",
            "value": "{\"address\":\"225 George Street\",\"city\":\"NSW\",\"state\":\"Sydney\",\"zip\":\"2000\",\"country\":\"Australia\"}"
        },
        {
            "type": "CUSTOM",
            "name": "My Custom Field",
            "value": "Custom value"
        }
    ]
}

response = client.create_contact(contact_data)
```

Get contact by id
```
response = client.get_contact_by_id('5685265389584384')
```

Get contact by email
```
response = client.get_contact_by_email('akrambakram@yabba.com')
```

Update contact
```
update_contact_data = {
    "id": "5685265389584384",
    "properties": [
        {
            "type": "SYSTEM",
            "name": "last_name",
            "value": "Chan"
        },
        {
            "type": "CUSTOM",
            "name": "My Custom Field",
            "value": "Custom value chane"
        }
    ]
}
response = client.update_contact(update_contact_data)
```

Search contacts
```
import json

myjson = {
    "rules": [{"LHS": "created_time", "CONDITION": "BETWEEN", "RHS": 1510152185.779954, "RHS_NEW": 1510238585.779877}],
    "contact_type": "PERSON"}
    
response = client.search(
    {'page_size': 25,
    'global_sort_key': '-created_time',
    'filterJson': json.dumps(myjson)
})
```


## Requirements
- requests

## Tests
```
python tests/test_client.py
```
