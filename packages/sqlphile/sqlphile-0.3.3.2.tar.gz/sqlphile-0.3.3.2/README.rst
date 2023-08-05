==========
SQLPhile
==========

.. contents:: Table of Contents

Introduce
=============

SQLPhile is a SQL template engine and Python style SQL generator. It looks like Django ORM but it hasn't any relationship with Django or ORM.

But it is inspired by Django ORM and iBATIS SQL Maps.

SQLPhile might be useful for keeping clean look of your app script. It can make hide SQL statements for your script by using Python functions or/and writing SQL templates to seperated files.

For Example,

.. code:: python
  
  conn = psycopg2.connect (...)
  cursor = conn.cursor ()
  
  cursor.execute ("""
    SELECT type, org, count(*) cnt FROM tbl_file
    WHERE org = {} AND filename LIKE '%{}'
    GROUP BY {}    
    ORDER BY {}
    LIMIT {}
    OFFSET {}
  """.format (1, 'OCD', 'type', 'org, cnt DESC', 10, 10))

This codes can be written with SQLPhile:

.. code:: python

  sp = SQLPhile ()
  
  conn = psycopg2.connect (...)
  cursor = conn.cursor ()
  
  q = sp.select ("tbl_file").get ("type", "count(*) cnt")
  q.filter (org = 1, name__endswith = 'OCD')
  q.group_by ("type").order_by ("org", "-cnt")[10:20]
  cursor.execute (q.as_sql ())

Or you can use SQL template file: sqlmaps/file.sql:

.. code:: html

  <sql name="get_stat">
    SELECT type, org, count(*) cnt FROM tbl_file
    WHERE {_filters} {_group_by} {_order_by} {_limit} {_offset}
  </sql>

Your app code is,
  
.. code:: python
  
  sp = SQLPhile ("sqlmaps")
  
  conn = psycopg2.connect (...)
  cursor = conn.cursor ()
  
  q = sp.file.get_stat.filter (org = 1, name__endswith = 'OCD')
  q.group_by ("type").order_by ("org", "-cnt")[10:20]
  cursor.execute (q.as_sql ())


SQLPhile
===========

SQLPhile is main class of this package.

.. code:: python
  
  from sqlphile import SQLPhile
  
  sp = SQLPhile (dir = None, auto_reload = False, engine = "postgresql")
  
Once SQLPhile is created, you can reuse it through entire your app.


Simple Query
--------------

SQLPhile provide select(), update(), insert() and delete() for generic SQL operation.

.. code:: python
  
  q = sp.insert ("tbl_file")
  q.data (_id = 1, score = 1.3242, name = "file-A", moddate = datetime.date.today ())
  cursor.execute (q.as_sql ())
  
  q = sp.update ("tbl_file")
  q.data (name = "Jenny", modified = datetime.date.today ())
  q.filter (...)
  
  q = sp.select ("tbl_file")
  q.get ("id", "name", "create", "modified")
  q.filter (...)
    
  q = sp.delete ("tbl_file")
  q.filter (...)

If you want to insert or update to NULL value, give None.

.. code:: python  
  
  q = sp.insert ("tbl_file", score = None)  

  
Templating For Complex and Highly Customized Query
------------------------------------------------------

For simple example,

.. code:: python
  
  from sqlphile import SQLPhile
  
  sp = SQLPhile ()
  
  q = sp.tempate ("SELECT {columns} FROM tbl_file WHERE {_filters} {_order_by}")
  q.feed (columns = "id, name").filter (id__eq = 6).order_by ("-id")
  q.as_sql () # OR q.render ()
  >> SELECT id, name FROM tbl_file WHERE id = 6 ORDER BY id DESC
  
If you create SQL templates in specific directory,

.. code:: python

  from sqlphile import SQLPhile
  
  sp = SQLPhile (dir = "./sqlmaps", auto_reload = True)

SQLPhile will load all of your templates in ./sqlmaps.

If you are under developing phase, set auto_reload True.

Assume there is a template file named 'file.sql':

.. code:: html

  <sqlmap version="1.0">
  
  <sql name="get_stat">
    SELECT type, org, count(*) cnt FROM tbl_file
    WHERE {_filters}
    GROUP BY type    
    ORDER BY org, cnt DESC
    {_limit} {_offset}
  </sql>

It looks like XML file, BUT IT'S NOT. All tags - <sqlmap>, <sql></sql> should be started at first of line. But SQL of inside is at your own mind but I recommend give some indentation.

Now you can access each sql temnplate via filename without extension and query name attribute:
  
.. code:: python

  # filename.query name
  q = sp.file.get_stat
  q.filter (...).order_by (...)
  
  # or
  q = sp.file.get_stat.filter (...).order_by (...)

Note: filename is *default.sql*, you can ommit filename.

.. code:: python

  q = sp.get_stat
  q.filter (...).order_by (...)

Note 2: SHOULD NOT use starts with "select", "update", "insert", "delete" or "template" as template filename.

Filtering & Excluding
======================

First of all, 

.. code:: python

  q.filter (id__eq = 1, name = None)
  >> id = 1

Please give your attention that *name* will be ignored. It makes reducing 'if' statements.

Otherwise, filter () is very similar with Django ORM.

.. code:: python

  q = sp.get_stat
  
  q.filter (__all = True)
  >> 1 = 1
  
  q.filter (id__all = True)
  >> 1 = 1
  
  q.filter (id__all = False)
  >> 1 = 0

  q.filter (id = 1)
  >> id = 1
  
  q.filter (t1__id = 1)
  >> t1.id = 1
  
  q.filter (id__exact = 1)
  >> id = 1
  
  q.filter (id__eq = 1)
  >> id = 1
  
  q.exclude (id = 1)
  >> NOT (id = 1)
  
  q.filter (id__neq = 1)
  >> id <> 1
  
  q.filter (t1__id__neq = 1)
  >> t1.id <> 1
  
  q.filter (id__gte = 1)
  >> id >= 1
  
  q.filter (id__lt = 1)
  >> id < 1

  q.filter (id__between = (10, 20))
  >> id BETWEEN 10 AND 20
  
  q.filter (name__contains = "fire")
  >> name LIKE '%fire%'
  
  q.exclude (name__contains = "fire")
  >> NOT name LIKE '%fire%'
  
  q.filter (name__startswith = "fire")
  >> name LIKE 'fire%'
  
  # escaping %
  q.filter (name__startswith = "fire%20ice")
  >> name LIKE 'fire\%20ice%'
  
  q.filter (name__endswith = "fire")
  >> name LIKE '%fire'
  
  q.filter (name__isnull = True)
  >> name IS NULL
  
  q.filter (name__isnull = False)
  >> name IS NOT NULL
  
Also you can add multiple filters:

.. code:: python

  q.filter (name__isnull = False, id = 4)
  >> name IS NOT NULL AND id = 4

All filters will be joined with "AND" operator.

Q Object
----------
  
How can add OR operator?

.. code:: python

  from sqlphile import Q
  
  q.filter (Q (id = 4) | Q (email__contains = "org"), name__isnull = False)
  >> name IS NOT NULL AND (id = 4 OR email LIKE '%org%')
  
Note that Q objects are first, keywords arguments late. Also you can add seperatly.

.. code:: python

  q.filter (name__isnull = False)
  q.filter (Q (id = 4) | Q (email__contains = "org"))
  >> (id = 4 OR email LIKE '%org%') AND name IS NOT NULL

If making excluding filter with Q use tilde(*~*),

.. code:: python

  q.filter (Q (id = 4) | ~Q (email__contains = "org"))
  >> (id = 4 OR NOT email LIKE '%org%')


F Object
----------
  
All value will be escaped or automatically add single quotes, but for comparing with other fileds use *F*.

.. code:: python

  from sqlphile import F
  
  Q (email = F ("b.email"))
  >> email = b.email
  
  Q (email__contains = F ("org"))
  >> email LIKE '%' || org || '%'
  
F can be be used for generic operation methods.

.. code:: python

  q = sp.update (tbl, n_view = F ("n_view + 1"))
  q.filter (...)
  cursor.execute (q.as_sql ())

Ordering & Grouping
====================

For ordering,

.. code:: python

  q = sp.select (tbl).get ("id", "name", "create", "modified")
  q.filter (...)
  q.order_by ("id", "-modified")
  >> ORDER BY id, modified DESC

For grouping,  

.. code:: python

  q = sp.select (tbl).get ("name", "count(*) cnt")
  q.filter (...)
  q.group_by ("name")
  >> GROUP BY name
  
  q.having ("count(*) > 10")
  >> GROUP BY name HAVING count(*) > 10

Offset & Limit
================

For limiting record set,

.. code:: python

  q = sp.select (tbl).get ("id", "name", "create", "modified")
  q [:100]
  >> LIMIT 100

  q [10:30]
  >> LIMIT 20 OFFSET 10
  
Be careful for slicing and limit count.

Returning
============

For Returning columns after insertinig or updating data,

.. code:: python

  q = sp.insert (tbl).data (name = "Hans", created = datetime.date.today ())  
  q.returning ("id", "name")
  >> RETURNING id, name

Joining
============

For joining tables,

.. code:: python

  q = sqlmaps.select ("tbl_file", "t1").join ("names", "t2", t1__name = F ("t2.name"))
  q.filter (id__gt > 100)
  q.get ("score", "t2.name")
  
  >> SELECT score, t2.name FROM tbl_file AS t1
     INNER JOIN names AS t2 ON t1.name = t2.name
     WHERE id > 100

For joining with sub query,

.. code:: python

  subq = sqlmaps.select ("tbl_project").get ("name")  
  q = sqlmaps.select ("tbl_file", "t1").join (subq, "t2", t1__name = F ("t2.name"))
  q.filter (id__gt = 100)
  q.get ("score", "t2.name")
  
  >> SELECT score, t2.name FROM tbl_file AS t1
     INNER JOIN (SELECT * FROM tbl_project) AS t2 ON t1.name = t2.name
     WHERE id > 100

You can use 'from\_()' for update query,

.. code:: python
     
  q = sqlmaps.update ("tbl_file", "t1")
  q.from_ ("tbl_record", "t2", t1__id = F ("t2.id"))
  q.data (score = F ("t2.score"))
  q.filter (id = 1)
  
  >> UPDATE tbl_file AS t1 SET score = t2.score
     FROM tbl_record AS t2 ON t1.id = t2.id
     WHERE id = 1
    
Also available,

- left_join ()
- right_join ()
- full_join ()
     
Using Template
=================

Template is like this,

.. code:: html

  <sqlmap version="1.0">
  
  <sql name="get_stat">
    SELECT type, org, count(*) cnt FROM tbl_file
    WHERE {_filters}
    GROUP BY type
    ORDER BY org, cnt DESC
    {_limit} {offset}
  </sql>
  
  <sql name="get_file">
    SELECT * cnt FROM tbl_file
    WHERE {_filters}
    {_order_by}
    {_limit} 
    {_offset}
  </sql>

You just fill variables your query reqiures,

.. code:: python

  q = sp.file.get_file.filter (id__gte = 1000)[:20]
  q.order_by ("-id")

Current reserved variables are,

- _filters
- _group_by
- _order_by
- _limit
- _offset
- _having
- _returning


Adding Data
--------------

data () also creates 3 variables automatically for inserting and updating purpose,

- _pairs
- _columns
- _values

.. code:: html
  
  <sql name="update_profile">
    UPDATE tbl_profile SET {_pairs} WHERE {_filters};
    INSERT INTO tbl_profile ({_columns}) VALUES ({_values});
  </sql>

.. code:: python
  
  q = sp.update_profile
  q.data (name = "Hans Roh", birth_year = 2000)
  q.data (email = None, age = 20)

Will be rendered:
  
.. code:: python

  {_columns} : name, birth_year, email, age
  {_values} : 'Hans Roh', 2000, NULL, 20
  {_pairs} : name='Hans Roh', birth_year=2000, email=NULL, age=20


D Object
```````````
  
D object convert dictionary into SQL column and value format and can feed them into SQL template.

.. code:: python
  
  from sqlphile import D
  
  d = D (name = "Hans", id = 1, email = None)
  d.values
  >> 'Hans', 1, NULL
  
  d.columns
  >> name, id, email
  
  d.pairs
  >> name = 'Hans', id = 1, email = NULL
  
And you can feed to template with prefix.

.. code:: html

  <sql name="get_file">
    INSERT ({_columns}, {additional_columns})
    VALUES ({_valuess}, {additional_values})
    {_returning};
  </sql>

In app,
  
.. code:: python
  
  q = sp.file.get_file.data (area = "730", additional = D (name = 'Hans', id = 1))
  q.returning ("id")
  cursor.execute (q.as_sql ())

In a conclusion, it will be created 3 variables automatically,
  
- additional_pairs
- additional_columns
- additional_values

More About filter()
---------------------

In some cases, filter is tricky.

.. code:: html

  <sqlmap version="1.0">
  
  <sql name="get_stat">
    SELECT type, org, count(*) cnt FROM tbl_file
    WHERE isdeleted is false AND {_filters}    
  </sql>

Above SQL is only valid when {_filters} exists, but what if filter doesn't be provided all the time? You can write like this:

.. code:: python

  q = sp.file.get_file.filter (__all = True, id__gte = None)
  >> WHERE isdeleted is false AND 1 = 1
  
  q = sp.file.get_file.filter (__all = True, id__gte = 1)
  >> WHERE isdeleted is false AND 1 = 1 AND id >= 1


Variablize Your Query
-----------------------

You can add variable on your sql by feed() and data() and both can be called multiple times.

Feeding Variable Key-Value Pairs
``````````````````````````````````````

.. code:: html
  
  <sql name="get_file">
    SELECT {cols} FROM {tbl}
    WHERE {_filters}
  </sql>

Now feed keywords args with feed ():

.. code:: python

  q = sp.file.get_file
  q.feed (cols = "id, name, created", tbl = "tbl_file")
  q.filter (id__gte = 1000)


Also you can feed filter.

.. code:: html
  
  <sql name="get_file">
    SELECT * FROM tbl_file
    WHERE {id} AND {name} AND create BETWEEN {created}
  </sql>

.. code:: python

  q.feed (id = Q (id__in = [1,2,3,4,5]))
  >> id IN (1,2,3,4,5)
  
  q.feed (id = Q (id__in = [1,2,3,4,5]), name = "Hans")
  >> id IN (1,2,3,4,5) AND name = 'Hans'
  
  q.feed (id = Q (id__in = [1,2,3,4,5]), name = Q (name = None), created = B (1, 4))
  # name is ignored by 1 = 1
  >> id IN (1,2,3,4,5) AND 1 = 1

Actually, feed () can be omitable,

.. code:: python
  
  # like instance constructor
  q = sp.file.get_file (cols = "id, name, created", tbl = "tbl_file")
  q.filter (id__gte = 1000)
  
  
Feeding V Object
````````````````````

If V will escape values for fitting SQL. You needn't care about sing quotes, escaping or type casting on date time field.

.. code:: python

  V (1)
  >> 1
  
  V (__eq = 1)
  >> 1
  
  V (datetime.date.today ())
  >> TIMESTAMP '20171224 00:00:00'
  
  V ("Hans")
  >> 'Hans'
  
  V (None)
  >> NULL
  
  V ()
  >> NULL
  
  V (__eq = "Hans")
  >> 'Hans'  
  
  V (__contains = "Hans")
  >> '%Hans%'
  
  V (__in = [1,2])
  >> (1,2)
  
  V (__between = [1,2])
  >> 1 AND 2

For example,
  
.. code:: html
  
  <sql name="get_file">
    UPDATE tbl_profile
    SET {_pairs}
    WHERE id IN (
      SELECT id FROM tbl_member
      WHERE name = {name}
    );    
    UPDATE tbl_stat SET count = count + 1
    WHERE birth_year IN {birth_year};
  </sql>

.. code:: python
  
  q = sp.file.get_file.feed (    
    email = V ("hansroh@email.com"),
    birth_year = V (__in = (2000, 2002, 2004))
  )
  q.data (name = "Hans Roh")


With Connection Helper
==================================

SQLite 3,

.. code:: python

  with sqlphile.db3.open (r"catalops.db3") as db:  
    q = db.select ("photo").get ("id, title, path, user")
    db.execute (q)
    
    for id, title, path, user in db.fetchall ():
      q = db.insert ("photo_bak")
      q.data (id = id, title = title)      
    
    # or getting as dctionary  
    for row in db.fetchall (as_dict = True):
      row ['id'], row ['title']
      q = db.insert ("photo_bak")
      q.data (**row)
 
Same as PostgreSQL,

.. code:: python
  
  with sqlphile.pg2.open ("dbname", "user", "password", "server") as db:
    ...
    

Change Logs
=============
  
  - 0.3.3
  
    - add db3 and pg2
  
	- 0.3.1
		
		- fix datetime type
		- add boolean type casting
		