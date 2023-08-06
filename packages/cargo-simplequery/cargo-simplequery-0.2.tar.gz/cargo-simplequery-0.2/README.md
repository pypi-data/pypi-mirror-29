# Cargo SimpleQuery

## Why?

This basically started as a simple experiment. Obviously the go-to tool in the Python world for database interactions is SQLAlchemy. I'm aware and I started building the first service based on it. But in my opinion there are two problems with it:

1. It is a heavy abstraction layer. Migrating from PostgreSQL to another SQL database is a highly unlikely scenario.
2. Postgres-specific features are not well supported. Just take the UUID column type as an example. As of now it supports being selected as part of a SELECT statement but as soon as you want to filter with it, the support is not sufficient.

## What then?

The most widely used Postgres Python adapter is called [psycopg2](http://initd.org/psycopg/). SQLAlchemy uses psycopg2 internally to connect against Postgres. psycopg2 supports big parts of the Postgres feature set and is compliant with the Python DB API specification.

## So SimpleQuery does what?

The biggest trouble when working with SQL databases in general in your code is to assemble SQL queries dynamically. Psycopg2 brings [SQL string composition features](http://initd.org/psycopg/docs/sql.html) to build your SQL strings step by step in a secure fashion. While that works great and we are using exactly this feature to build complicated queries, there is a whole range of simpler queries where the process could be more straight forward. That's where SimpleQuery comes in.

SimpleQuery is a query builder that can support you in building most SELECT, INSERT, UPDATE and DELETE statements.

```python3
q = SelectQueryBuilder('users', ['*'])
cursor.execute(q.get_query())
users = cursor.fetchall()
```

This would result in the simple query `SELECT * FROM users`. A query object can be converted to an sql.SQL object, executed through a database cursor and then the results can be fetched.

The true power of SimpleQuery comes into play as soon as you build queries conditionally.

```python3
q = SelectQueryBuilder('users u', ['*'])
q.order_by('created_at', 'ASC')

if request.email_filter != '':
  q.where().like('email', request.email_filter+'%')

if request.group_filter != '':
  q.inner_join('groups g').on_eq('u.group_id', 'g.id')
  q.where().eq('g.name', request.group_filter)
```

Building the SQL query by hand with all the different conditions is doable but a lot slower than just throwing a few functions together and let the small library piece it together for you. Again, if you have a very complicated query, the library will not be able to support it and the effort to implement the functionality into SimpleQuery would most likely outweigh the effort to write the specific query yourself.

## Escaping

As you can see in the example above, there is no explicit escaping happening in the query. SimpleQuery makes certain assumptions about your input and you have to explicitly overwrite it in case you want a different behavior. Let's assume I want to create the SQL query `SELECT * FROM users WHERE id = 'abc'`. The code would look like this:

```python3
s = SelectQueryBuilder('users', ['*'])
s.where().eq('id', 'abc')
``` 

In this scenario SimpleQuery assumes that `'id'` is a SQL identifier and `'abc'` is a SQL literal which needs to be escaped. We can supress escaping of a literal by passing a [sql.SQL](http://initd.org/psycopg/docs/sql.html#psycopg2.sql.SQL) object. Whenever you use an SQL object, you signal to the library that you are taking care of everything yourself. The library will only apply magic if you are using plain strings.

## SQL Identifiers

In a lot of situations in order to make the standard scenarios as easy as possible, the library expects an identifier. If you pass a string, it will try to treat the string correctly. A few examples:

```python3
q = SelectQueryBuilder('users u', ['*'])
q.where().eq('u.id', 'abc)
```

SimpleQuery expects an identifier as the table name. The wrapping algorithm will convert `users u` to `"users" AS "u"`. In the WHERE clause however, it will recognize the dot syntax and will produce `"u"."id"` out of `u.id`. You can find all the supported cases in the wrap_identifier function. When in doubt, you can always use sql.SQL, sql.Identifier or sql.Literal and handle the situation yourself.