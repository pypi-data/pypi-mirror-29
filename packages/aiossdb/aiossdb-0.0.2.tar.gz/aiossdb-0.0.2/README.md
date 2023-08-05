# aiossdb
aiossdb is a library for accessing an ssdb database from AsyncIO

[![Coverage Status](https://coveralls.io/repos/github/Microndgt/aiossdb/badge.svg?branch=master)](https://coveralls.io/github/Microndgt/aiossdb?branch=master)
![https://travis-ci.org/Microndgt/aiossdb.svg?branch=master](https://travis-ci.org/Microndgt/aiossdb.svg?branch=master)

Requirements
------------

- Python 3.6+

DONE and TODO
-------------

- [x] base async ssdb connection
- [x] async ssdb parser
- [x] async ssdb connection pool
- [x] easy using ssdb async client
- [x] tests
- [ ] detailed docs
- [ ] suppress ReplyError as a choice
- [ ] releasing...
- [ ] and more...

Quick Start
-----------

- Client

Client will create a connection pool, each time you execute the command will be from the available connection pool to get the connection, and then execute the command, and then release  
Client会创建一个连接池，在每次执行命令的时候都会去从可用连接池中拿到连接，然后执行命令，然后释放

```
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def just_look():
    c = Client(loop=loop)
    await c.set('a', 1)
    res = await c.get('a')
    print(res)
    await c.close()
    return res

loop.run_until_complete(just_look())
loop.close()
```

- ConnectionPool

```
import asyncio
from aiossdb import create_pool

loop = asyncio.get_event_loop()


async def connect_tcp():
    pool = await create_pool(('localhost', 8888), loop=loop, minsize=5, maxsize=10)

    # Use the direct implementation of the command pool
    # 使用pool直接执行命令
    await pool.execute('set', 'a', 2)
    val = await pool.execute('hget', 'hash_name', 'hash_key')
    print(val)

    # Use the pool to get the connection
    # 使用pool获取连接
    conn, addr = await pool.get_connection()
    await conn.execute('set', 'a', 2)
    val = await conn.execute('hget', 'hash_name', 'hash_key')
    print(val)
    
    # Get the final connection to be released
    # 获取的连接最后一定要release
    await pool.release(conn)

    pool.close()
    await pool.wait_closed()

loop.run_until_complete(connect_tcp())
loop.close()
```

If you request a non-existent key, a `ReplyError` will be raised and the type of error may be: `not_found`, `error`, `fail`, `client_error`  
如果获取不存在的键等情况会引发`ReplyError`, 错误类型可能有: `not_found`, `error`, `fail`, `client_error`

```
try:
    val = await conn.execute('hget', 'hash_name', 'hash_key')
except ReplyError as e:
    print("Error type: {}".format(e.etype))
    print("Executed command: {}".format(e.command))
```

- Connection

```
import asyncio
from aiossdb import create_connection, ReplyError


loop = asyncio.get_event_loop()


async def connect_tcp():
    conn = await create_connection(('localhost', 8888), loop=loop)
    await conn.execute('set', 'a', 2)
    val = await conn.execute('hget', 'hash_name', 'hash_key')
    print(val)

    conn.close()
    await conn.wait_closed()

loop.run_until_complete(connect_tcp())
loop.close()
```

Exceptions
----------

- SSDBError
    - ConnectionClosedError
    - ReplyError
    - ProtocolError
    - PoolClosedError

NOTES
-----

- The preliminary test shows that `aiossdb` is 25 times fast than [pyssdb](https://github.com/ifduyue/pyssdb)

Contributor
===========

Kevin Du
--------

- Email: `dgt_x@foxmail.com`
- Site: `http://skyrover.me`