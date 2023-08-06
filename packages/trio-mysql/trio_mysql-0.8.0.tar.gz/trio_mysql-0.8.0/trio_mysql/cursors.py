# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
from functools import partial
import sys
import re
import warnings

from . import err


#: Regular expression for :meth:`Cursor.executemany`.
#: executemany only suports simple bulk insert.
#: You can use it to load large dataset.
RE_INSERT_VALUES = re.compile(
    r"\s*((?:INSERT|REPLACE)\b.+\bVALUES?\s*)" +
    r"(\(\s*(?:%s|%\(.+\)s)\s*(?:,\s*(?:%s|%\(.+\)s)\s*)*\))" +
    r"(\s*(?:ON DUPLICATE.*)?);?\s*\Z",
    re.IGNORECASE | re.DOTALL)


class Cursor(object):
    """
    This is the object you use to interact with the database.

    Do not create an instance of a Cursor yourself. Call
    connections.Connection.cursor().

    See `Cursor <https://www.python.org/dev/peps/pep-0249/#cursor-objects>`_ in
    the specification.
    """

    #: Max statement size which :meth:`executemany` generates.
    #:
    #: Max size of allowed statement is max_allowed_packet - packet_header_size.
    #: Default value of max_allowed_packet is 1048576.
    max_stmt_length = 1024000

    _defer_warnings = False

    def __init__(self, connection):
        self.connection = connection
        self.description = None
        self.rownumber = 0
        self.rowcount = -1
        self.arraysize = 1
        self._executed = None
        self._result = None
        self._rows = None
        self._warnings_handled = False

    def close(self):
        raise RuntimeError("You need to call 'await .aclose()'")
        
    async def aclose(self):
        """
        Closing a cursor just exhausts all remaining data.
        """
        conn = self.connection
        if conn is None:
            return
        try:
            while await self.nextset():
                pass
        finally:
            self.connection = None

    def __enter__(self):
        raise RuntimeError("You need to use 'async with'")

    def __exit__(self, *tb):
        raise RuntimeError("You need to use 'async with'")

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        del exc_info
        await self.aclose()

    def _get_db(self):
        if not self.connection:
            raise err.ProgrammingError("Cursor closed")
        return self.connection

    def _check_executed(self):
        if not self._executed:
            raise err.ProgrammingError("execute() first")

    def _conv_row(self, row):
        return row

    def setinputsizes(self, *args):
        """Does nothing, required by DB API."""

    def setoutputsizes(self, *args):
        """Does nothing, required by DB API."""

    async def _nextset(self, unbuffered=False):
        """Get the next query set"""
        conn = self._get_db()
        current_result = self._result
        # for unbuffered queries warnings are only available once whole result has been read
        if unbuffered:
            await self._show_warnings()
        if current_result is None or current_result is not conn._result:
            return None
        if not current_result.has_next:
            return None
        await conn.next_result(unbuffered=unbuffered)
        await self._do_get_result()
        return True

    async def nextset(self):
        return await self._nextset(False)

    def _ensure_bytes(self, x, encoding=None):
        if isinstance(x, str):
            x = x.encode(encoding)
        elif isinstance(x, (tuple, list)):
            x = type(x)(self._ensure_bytes(v, encoding=encoding) for v in x)
        return x

    def _escape_args(self, args, conn):
        ensure_bytes = partial(self._ensure_bytes, encoding=conn.encoding)

        if isinstance(args, (tuple, list)):
            return tuple(conn.literal(arg) for arg in args)
        elif isinstance(args, dict):
            return dict((key, conn.literal(val)) for (key, val) in args.items())
        else:
            # If it's not a dictionary let's try escaping it anyways.
            # Worst case it will throw a Value error
            return conn.escape(args)

    def mogrify(self, query, args=None):
        """
        Returns the exact string that is sent to the database by calling the
        execute() method.

        This method follows the extension to the DB API 2.0 followed by Psycopg.
        """
        conn = self._get_db()
        if args is not None:
            query = query % self._escape_args(args, conn)

        return query

    async def execute(self, query, args=None):
        """Execute a query

        :param str query: Query to execute.

        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict

        :return: Number of affected rows
        :rtype: int

        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        while await self.nextset():
            pass

        query = self.mogrify(query, args)

        result = await self._query(query)
        self._executed = query
        return result

    async def executemany(self, query, args):
        # type: (str, list) -> int
        """Run several data against one query

        :param query: query to execute on server
        :param args:  Sequence of sequences or mappings.  It is used as parameter.
        :return: Number of rows affected, if any.

        This method improves performance on multiple-row INSERT and
        REPLACE. Otherwise it is equivalent to looping over args with
        execute().
        """
        if not args:
            return

        m = RE_INSERT_VALUES.match(query)
        if m:
            q_prefix = m.group(1) % ()
            q_values = m.group(2).rstrip()
            q_postfix = m.group(3) or ''
            assert q_values[0] == '(' and q_values[-1] == ')'
            return await self._do_execute_many(q_prefix, q_values, q_postfix, args,
                                         self.max_stmt_length,
                                         self._get_db().encoding)

        cnt = 0
        for arg in args:
            cnt += await self.execute(query, arg)
        self.rowcount = cnt
        return cnt

    async def _do_execute_many(self, prefix, values, postfix, args, max_stmt_length, encoding):
        conn = self._get_db()
        escape = self._escape_args
        if isinstance(prefix, str):
            prefix = prefix.encode(encoding)
        if isinstance(postfix, str):
            postfix = postfix.encode(encoding)
        sql = bytearray(prefix)
        args = iter(args)
        v = values % escape(next(args), conn)
        if isinstance(v, str):
            v = v.encode(encoding, 'surrogateescape')
        sql += v
        rows = 0
        for arg in args:
            v = values % escape(arg, conn)
            if isinstance(v, str):
                v = v.encode(encoding, 'surrogateescape')
            if len(sql) + len(v) + len(postfix) + 1 > max_stmt_length:
                rows += await self.execute(sql + postfix)
                sql = bytearray(prefix)
            else:
                sql += b','
            sql += v
        rows += await self.execute(sql + postfix)
        self.rowcount = rows
        return rows

    async def callproc(self, procname, args=()):
        """Execute stored procedure procname with args

        procname -- string, name of procedure to execute on server

        args -- Sequence of parameters to use with procedure

        Returns the original args.

        Compatibility warning: PEP-249 specifies that any modified
        parameters must be returned. This is currently impossible
        as they are only available by storing them in a server
        variable and then retrieved by a query. Since stored
        procedures return zero or more result sets, there is no
        reliable way to get at OUT or INOUT parameters via callproc.
        The server variables are named @_procname_n, where procname
        is the parameter above and n is the position of the parameter
        (from zero). Once all result sets generated by the procedure
        have been fetched, you can issue a SELECT @_procname_0, ...
        query using .execute() to get any OUT or INOUT values.

        Compatibility warning: The act of calling a stored procedure
        itself creates an empty result set. This appears after any
        result sets generated by the procedure. This is non-standard
        behavior with respect to the DB-API. Be sure to use nextset()
        to advance through all result sets; otherwise you may get
        disconnected.
        """
        conn = self._get_db()
        for index, arg in enumerate(args):
            q = "SET @_%s_%d=%s" % (procname, index, conn.escape(arg))
            await self._query(q)
            await self.nextset()

        q = "CALL %s(%s)" % (procname,
                             ','.join(['@_%s_%d' % (procname, i)
                                       for i in range(len(args))]))
        await self._query(q)
        self._executed = q
        return args

    async def fetchone(self):
        """Fetch the next row"""
        self._check_executed()
        if self._rows is None or self.rownumber >= len(self._rows):
            return None
        result = self._rows[self.rownumber]
        self.rownumber += 1
        return result

    async def fetchmany(self, size=None):
        """Fetch several rows"""
        self._check_executed()
        if self._rows is None:
            return ()
        end = self.rownumber + (size or self.arraysize)
        result = self._rows[self.rownumber:end]
        self.rownumber = min(end, len(self._rows))
        return result

    async def fetchall(self):
        """Fetch all the rows"""
        self._check_executed()
        if self._rows is None:
            return ()
        if self.rownumber:
            result = self._rows[self.rownumber:]
        else:
            result = self._rows
        self.rownumber = len(self._rows)
        return result

    def __iter__(self):
        if self._rows is None or self.rownumber:
            return self
        return iter(self._rows) # optimization

    def __next__(self):
        if self._rows is None or self.rownumber >= len(self._rows):
            raise StopIteration
        res = self._rows[self.rownumber]
        self.rownumber += 1
        return res

    if sys.version_info < (3,5,2):
        async def __aiter__(self):
            return self
    else:
        def __aiter__(self):
            return self

    async def __anext__(self):
        if self._rows is None or self.rownumber >= len(self._rows):
            raise StopAsyncIteration
        res = self._rows[self.rownumber]
        self.rownumber += 1
        return res
        
    async def scroll(self, value, mode='relative'):
        self._check_executed()
        if mode == 'relative':
            r = self.rownumber + value
        elif mode == 'absolute':
            r = value
        else:
            raise err.ProgrammingError("unknown scroll mode %s" % mode)

        if not (0 <= r < len(self._rows)):
            raise IndexError("out of range")
        self.rownumber = r

    async def _query(self, q):
        conn = self._get_db()
        self._last_executed = q
        await conn.query(q)
        await self._do_get_result()
        return self.rowcount

    async def _do_get_result(self):
        conn = self._get_db()

        self.rownumber = 0
        self._result = result = conn._result

        self.rowcount = result.affected_rows
        self.description = result.description
        self.lastrowid = result.insert_id
        self._rows = result.rows
        self._warnings_handled = False

        if not self._defer_warnings:
            await self._show_warnings()

    async def _show_warnings(self):
        if self._warnings_handled:
            return
        self._warnings_handled = True
        if self._result and (self._result.has_next or not self._result.warning_count):
            return
        ws = await self._get_db().show_warnings()
        if ws is None:
            return
        for w in ws:
            msg = w[-1]
            warnings.warn(err.Warning(*w[1:3]), stacklevel=4)

    Warning = err.Warning
    Error = err.Error
    InterfaceError = err.InterfaceError
    DatabaseError = err.DatabaseError
    DataError = err.DataError
    OperationalError = err.OperationalError
    IntegrityError = err.IntegrityError
    InternalError = err.InternalError
    ProgrammingError = err.ProgrammingError
    NotSupportedError = err.NotSupportedError


class DictCursorMixin(object):
    # You can override this to use OrderedDict or other dict-like types.
    dict_type = dict

    async def _do_get_result(self):
        await super()._do_get_result()
        fields = []
        if self.description:
            for f in self._result.fields:
                name = f.name
                if name in fields:
                    name = f.table_name + '.' + name
                fields.append(name)
            self._fields = fields

        if fields and self._rows:
            self._rows = [self._conv_row(r) for r in self._rows]

    def _conv_row(self, row):
        if row is None:
            return None
        return self.dict_type(zip(self._fields, row))


class DictCursor(DictCursorMixin, Cursor):
    """A cursor which returns results as a dictionary"""


class SSCursor(Cursor):
    """
    Unbuffered Cursor, mainly useful for queries that return a lot of data,
    or for connections to remote servers over a slow network.

    Instead of copying every row of data into a buffer, this will fetch
    rows as needed. The upside of this is the client uses much less memory,
    and rows are returned much faster when traveling over a slow network
    or if the result set is very big.

    There are limitations, though. The MySQL protocol doesn't support
    returning the total number of rows, so the only way to tell how many rows
    there are is to iterate over every row returned. Also, it currently isn't
    possible to scroll backwards, as only the current row is held in memory.
    """

    _defer_warnings = True

    def _conv_row(self, row):
        return row

    async def aclose(self):
        conn = self.connection
        if conn is None:
            return

        if self._result is not None and self._result is conn._result:
            await self._result._finish_unbuffered_query()

        try:
            while await self.nextset():
                pass
        finally:
            self.connection = None

    async def _query(self, q):
        conn = self._get_db()
        self._last_executed = q
        await conn.query(q, unbuffered=True)
        await self._do_get_result()
        return self.rowcount

    async def nextset(self):
        return await self._nextset(unbuffered=True)

    async def read_next(self):
        """Read next row"""
        return self._conv_row(await self._result._read_rowdata_packet_unbuffered())

    async def fetchone(self):
        """Fetch next row"""
        self._check_executed()
        row = await self.read_next()
        if row is None:
            await self._show_warnings()
            return None
        self.rownumber += 1
        return row

    async def fetchall(self):
        """
        Fetch all, as per MySQLdb. Pretty useless for large queries, as
        it is buffered. You should async-iterate over the cursor instead.
        """
        res = []
        async for r in self:
            res.append(r)
        return res

    async def fetchall_unbuffered(self):
        """
        Fetch all, implemented as an async iterator. In fact, you can just
        iterate over the cursor itself, so this is a no-op. Included for
        compatibility.
        """
        return self

    def __iter__(self):
        raise RuntimeError("You must use 'async for ...' with %s" % repr(type(self)))

    async def __anext__(self):
        res = await self.fetchone()
        if res is None:
            raise StopAsyncIteration
        return res

    async def fetchmany(self, size=None):
        """Fetch many"""
        self._check_executed()
        if size is None:
            size = self.arraysize

        rows = []
        for i in range(size):
            row = await self.read_next()
            if row is None:
                await self._show_warnings()
                break
            rows.append(row)
            self.rownumber += 1
        return rows

    async def scroll(self, value, mode='relative'):
        self._check_executed()

        if mode == 'relative':
            if value < 0:
                raise err.NotSupportedError(
                        "Backwards scrolling not supported by this cursor")

            for _ in range(value):
                await self.read_next()
            self.rownumber += value
        elif mode == 'absolute':
            if value < self.rownumber:
                raise err.NotSupportedError(
                    "Backwards scrolling not supported by this cursor")

            end = value - self.rownumber
            for _ in range(end):
                await self.read_next()
            self.rownumber = value
        else:
            raise err.ProgrammingError("unknown scroll mode %s" % mode)


class SSDictCursor(DictCursorMixin, SSCursor):
    """An unbuffered cursor, which returns results as a dictionary"""
