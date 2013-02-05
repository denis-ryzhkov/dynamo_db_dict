'''
Simple Python interface to Amazon DynamoDB,
adding some dict-like sugar to boto.dynamodb.layer2.

See also:
* http://aws.amazon.com/dynamodb/
* http://boto.cloudhackers.com/en/latest/ref/dynamodb.html#module-boto.dynamodb.layer2

Usage:

    pip install dynamo_db_dict
    from dynamo_db_dict import dynamo_db

    db = dynamo_db(aws_access_key_id='YOUR KEY HERE', aws_secret_access_key='YOUR SECRET KEY HERE') # or via: os.environ, ~/.boto, /etc/boto.cfg
    # Set table_name_prefix='YOUR_PROJECT_NAME_' if you use the same DynamoDB account for several projects.

    # Either create table "user" with hash_key "email" via AWS concole, or via inherited db.create_table(...).
    db.user['john@example.com'] = dict(first_name='John', last_name='Johnson') # Put. No need to repeat "email" in dict(...).
    john = db.user['john@example.com'] # Get.
    assert john == dict(email='john@example.com', first_name='John', last_name='Johnson') # Complete item, with "email".
    assert john['first_name'] == 'John' # Key access.
    assert john.first_name == 'John' # Attr access.
    del db.user['john@example.com'] # Delete.

dynamo_db_dict version 0.2.1
Copyright (C) 2012 by Denis Ryzhkov <denis@ryzhkov.org>
MIT License, see http://opensource.org/licenses/MIT
'''

#### requirements

from adict import adict
from boto.dynamodb.layer2 import Layer2
from boto.dynamodb.table import Table

#### dynamo_db

class dynamo_db(Layer2):

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, table_name_prefix='', **kwargs):
        '''
        Configures boto Layer2 connection to DynamoDB, creates cache for repeated access to tables:
            db = dynamo_db(aws_access_key_id='YOUR KEY HERE', aws_secret_access_key='YOUR SECRET KEY HERE') # or via: os.environ, ~/.boto, /etc/boto.cfg
        '''
        self.tables = {}
        self.table_name_prefix = table_name_prefix
        super(dynamo_db, self).__init__(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, **kwargs)

    def __getattr__(self, table_name):
        '''
        Simple access to a table:
            db.user

        For table names conflicting with Layer2 attributes, e.g. db.scan(), use:
            db.get_table('scan')
        '''
        table_name = self.table_name_prefix + table_name
        table = self.tables.get(table_name)
        if not table:
            table = self.tables[table_name] = dynamo_table(layer2=self, response=self.describe_table(table_name))
        return table

    get_table = __getattr__ # See __getattr__ docstring.

#### dynamo_table

class dynamo_table(Table):

    def __setitem__(self, hash_key, attrs):
        '''
        Puts item to db:
            db.user[email] = dict(first_name='...', ...)

        TODO: range_key support:
            db.message[topic][date] = dict(text='...', ...)
        '''
        self.layer2.put_item(item=self.new_item(hash_key=hash_key, attrs=attrs))

    def __getitem__(self, hash_key):
        '''
        Gets item from db:
            user = db.user[email]

        TODO: range_key support:
            message = db.message[topic][date]

        TODO: Option to control consistent_read.
        '''
        return adict(self.get_item(hash_key=hash_key, consistent_read=True))

    def __delitem__(self, hash_key):
        '''
        Deletes item from db:
            del db.user[email]

        TODO: range_key support:
            del db.message[topic][date]
        '''
        self.layer2.delete_item(item=adict(table=self, hash_key=hash_key, range_key=None))
        # NOTE: Do not change `adict` to `dict` here. It emulates Item object with attr access.

#### test

def test():
    print('Please copy the Usage above and test it with your own AWS keys and existing tables. TODO: Use `ddbmock` package.')

if __name__ == '__main__':
    test()
