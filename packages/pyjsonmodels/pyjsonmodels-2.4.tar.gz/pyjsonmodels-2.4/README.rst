===========
pyJSON models
===========

.. image:: https://badge.fury.io/py/jsonmodels.png
    :target: http://badge.fury.io/py/jsonmodels

.. image:: https://travis-ci.org/beregond/jsonmodels.png?branch=master
    :target: https://travis-ci.org/beregond/jsonmodels

.. image:: https://img.shields.io/pypi/dm/jsonmodels.svg
    :target: https://pypi.python.org/pypi/jsonmodels

.. image:: https://coveralls.io/repos/beregond/jsonmodels/badge.png
    :target: https://coveralls.io/r/beregond/jsonmodels


`jsonmodels` 是一个能够方便得处理json格式数据和模型数据转化的工具

* Free software: GPL3
* Documentation: http://jsonmodels.rtfd.org
* Source: https://gitee.com/huichengip_chenxf/jsonmodels

特性
--------

* 完全支持 Python 2.7, 3.3, 3.4, 3.5, 3.6.

* 支持 PyPy (see implementation notes in docs for more details).

* 创建类似Django一样的models:

  .. code-block:: python

    from jsonmodels import models, fields, errors, validators


    class Cat(models.Base):

        name = fields.StringField(required=True)
        breed = fields.StringField()
        love_humans = fields.IntField(nullable=True)


    class Dog(models.Base):

        name = fields.StringField(required=True)
        age = fields.IntField()


    class Car(models.Base):

        registration_number = fields.StringField(required=True)
        engine_capacity = fields.FloatField()
        color = fields.StringField()


    class Person(models.Base):

        name = fields.StringField(required=True)
        surname = fields.StringField(required=True)
        nickname = fields.StringField(nullable=True)
        car = fields.EmbeddedField(Car)
        pets = fields.ListField([Cat, Dog], nullable=True)

* 通过属性访问值:

  .. code-block:: python

    >>> cat = Cat()
    >>> cat.populate(name='Garfield')
    >>> cat.name
    'Garfield'
    >>> cat.breed = 'mongrel'
    >>> cat.breed
    'mongrel'

* 验证模型:

  .. code-block:: python

    >>> person = Person(name='Chuck', surname='Norris')
    >>> person.validate()
    None

    >>> dog = Dog()
    >>> dog.validate()
    *** ValidationError: Field "name" is required!

* 转化模型为python的格式或者json:

  .. code-block:: python

    >>> cat = Cat(name='Garfield')
    >>> dog = Dog(name='Dogmeat', age=9)
    >>> car = Car(registration_number='ASDF 777', color='red')
    >>> person = Person(name='Johny', surname='Bravo', pets=[cat, dog])
    >>> person.car = car
    >>> person.to_struct()
    {
        'car': {
            'color': 'red',
            'registration_number': 'ASDF 777'
        },
        'surname': 'Bravo',
        'name': 'Johny',
        'nickname': None,
        'pets': [
            {'name': 'Garfield'},
            {'age': 9, 'name': 'Dogmeat'}
        ]
    }

    >>> import json
    >>> person_json = json.dumps(person.to_struct())

* 你不想写json元数据? pyjsonmodels能为你做这件事:

  .. code-block:: python

    >>> person = Person()
    >>> person.to_json_schema()
    {
        'additionalProperties': False,
        'required': ['surname', 'name'],
        'type': 'object',
        'properties': {
            'car': {
                'additionalProperties': False,
                'required': ['registration_number'],
                'type': 'object',
                'properties': {
                    'color': {'type': 'string'},
                    'engine_capacity': {'type': ''},
                    'registration_number': {'type': 'string'}
                }
            },
            'surname': {'type': 'string'},
            'name': {'type': 'string'},
            'nickname': {'type': ['string', 'null']}
            'pets': {
                'items': {
                    'oneOf': [
                        {
                            'additionalProperties': False,
                            'required': ['name'],
                            'type': 'object',
                            'properties': {
                                'breed': {'type': 'string'},
                                'name': {'type': 'string'}
                            }
                        },
                        {
                            'additionalProperties': False,
                            'required': ['name'],
                            'type': 'object',
                            'properties': {
                                'age': {'type': 'number'},
                                'name': {'type': 'string'}
                            }
                        },
                        {
                            'type': 'null'
                        }
                    ]
                },
                'type': 'array'
            }
        }
    }

* 验证模型和用验证器, 最终影响生成的json元数据:

  .. code-block:: python

    >>> class Person(models.Base):
    ...
    ...     name = fields.StringField(
    ...         required=True,
    ...         validators=[
    ...             validators.Regex('^[A-Za-z]+$'),
    ...             validators.Length(3, 25),
    ...         ],
    ...     )
    ...     age = fields.IntField(
    ...         nullable=True,
    ...         validators=[
    ...             validators.Min(18),
    ...             validators.Max(101),
    ...         ]
    ...     )
    ...     nickname = fields.StringField(
    ...         required=True,
    ...         nullable=True
    ...     )
    ...

    >>> person = Person()
    >>> person.age = 11
    >>> person.validate()
    *** ValidationError: '11' is lower than minimum ('18').
    >>> person.age = None
    >>> person.validate()
    None

    >>> person.age = 19
    >>> person.name = 'Scott_'
    >>> person.validate()
    *** ValidationError: Value "Scott_" did not match pattern "^[A-Za-z]+$".

    >>> person.name = 'Scott'
    >>> person.validate()
    None

    >>> person.nickname = None
    >>> person.validate()
    *** ValidationError: Field is required!

    >>> person.to_json_schema()
    {
        "additionalProperties": false,
        "properties": {
            "age": {
                "maximum": 101,
                "minimum": 18,
                "type": ["number", "null"]
            },
            "name": {
                "maxLength": 25,
                "minLength": 3,
                "pattern": "/^[A-Za-z]+$/",
                "type": "string"
            },
            "nickname": {,
                "type": ["string", "null"]
            }
        },
        "required": [
            "nickname",
            "name"
        ],
        "type": "object"
    }

  想知道更多的内容请访问文档.

* 对于循环引用,可以支持懒加载:

  .. code-block:: python

    >>> class Primary(models.Base):
    ...
    ...     name = fields.StringField()
    ...     secondary = fields.EmbeddedField('Secondary')

    >>> class Secondary(models.Base):
    ...
    ...    data = fields.IntField()
    ...    first = fields.EmbeddedField('Primary')

* 用定义的方式也可以处理循环引用:

  .. code-block:: python

    >>> class File(models.Base):
    ...
    ...     name = fields.StringField()
    ...     size = fields.FloatField()

    >>> class Directory(models.Base):
    ...
    ...     name = fields.StringField()
    ...     children = fields.ListField(['Directory', File])

    >>> class Filesystem(models.Base):
    ...
    ...     name = fields.StringField()
    ...     children = fields.ListField([Directory, File])

    >>> Filesystem.to_json_schema()
    {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
            "children": {
                "items": {
                    "oneOf": [
                        "#/definitions/directory",
                        "#/definitions/file"
                    ]
                },
                "type": "array"
            }
        },
        "additionalProperties": false,
        "definitions": {
            "directory": {
                "additionalProperties": false,
                "properties": {
                    "children": {
                        "items": {
                            "oneOf": [
                                "#/definitions/directory",
                                "#/definitions/file"
                            ]
                        },
                        "type": "array"
                    },
                    "name": {"type": "string"}
                },
                "type": "object"
            },
            "file": {
                "additionalProperties": false,
                "properties": {
                    "name": {"type": "string"},
                    "size": {"type": "number"}
                },
                "type": "object"
            }
        }
    }

* 比较json元数据:

  .. code-block:: python

    >>> from jsonmodels.utils import compare_schemas
    >>> schema1 = {'type': 'object'}
    >>> schema2 = {'type': 'array'}
    >>> compare_schemas(schema1, schema1)
    True
    >>> compare_schemas(schema1, schema2)
    False

更多
----

文档中已经描述很详细:
http://jsonmodels.rtfd.org.
