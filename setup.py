from distutils.core import setup

setup(
    name='dynamo_db_dict',
    version='0.2.4',
    description='Simple Python interface to Amazon DynamoDB, adding some dict-like sugar to boto.dynamodb.layer2.',
    long_description='''

Usage::

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

See also:

* `Amazon DynamoDB <http://aws.amazon.com/dynamodb/>`_
* `boto.dynamodb.layer2 <http://boto.cloudhackers.com/en/latest/ref/dynamodb.html#module-boto.dynamodb.layer2>`_

''',
    url='https://github.com/denis-ryzhkov/dynamo_db_dict',
    author='Denis Ryzhkov',
    author_email='denisr@denisr.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    py_modules=['dynamo_db_dict'],
    install_requires=[
        'adict',
        'boto',
    ],
)
