python-ldap-simple-search
=========

A python library that provides a simple way to performs synchronous LDAP queries. It wraps python-ldap.

## Install

From dev upstream

```
pip install -e git+git@github.com:chaordic/python-ldap-simple-search.git@master#egg=ldap_simple_search
```

From PyPi

```
pip install ldap_simple_search
```

## Dependencies

* Python 2.7
* python-ldap

## Usage

### Initial setup

```python
from ldap_simple_search import LDAPSearch

uri = 'ldap://ldap.internal:389'
bind_dn = "uid=admin,cn=users,cn=accounts,dc=opensource,dc=org"
password = "yourpassword"
base_dn = "cn=users,cn=accounts,dc=opensource,dc=org"
search_filter = "(&(mail=admin@opensource.org))
search_attribute = ['memberOf']
```

### Perform a query

```python
l = LDAPSearch(uri,bind_dn,password) 
l.search(base_dn, search_filter, search_attribute)
```

### Perform a query with callback

Define a callback:

```python
def LuvCallBacks(dn,record):
   return dn, record
```

Querying with callback to process results on large queries:

```python
l.search(base_dn, search_filter, search_attribute, LuvCallBacks)
```

## Output format

```python
# without callback

[('uid=admin,cn=users,cn=accounts,dc=opensource,dc=org',
  {'mail': ['admin@opensource.org'],
   'memberOf': ['cn=users,cn=groups,cn=accounts,dc=opensource,dc=org',
   'cn=admins,cn=groups,cn=accounts,dc=opensource,dc=org',
   'objectClass': ['posixaccount',
    'person',
    'posixaccount',],
   'uidNumber': ['8228839'],
  }
```
