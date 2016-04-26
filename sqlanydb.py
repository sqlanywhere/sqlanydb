# Copyright 2016 SAP SE or an SAP affiliate company.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# 
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# While not a requirement of the license, if you do modify this file, we
# would appreciate hearing about it.   Please email sqlany_interfaces@sap.com


"""SQLAnydb - A DB API v2.0 compatible interface to SQL Anywhere.

This package provides a DB API v2.0 interface
    http://www.python.org/dev/peps/pep-0249
to the sqlanywhere dbcapi library.

"""

__version__ = '1.0.8'

import os
import sys
import atexit
import time
import logging



try:
    import exceptions
    # pre 3.0
    Exception = exceptions.StandardError
    bytes = str
    str = unicode
    v3list = lambda x: x
except:
    # 3.0 or later
    xrange = range
    v3list = list
import codecs
from ctypes import *
from struct import pack, unpack, calcsize

lg = logging.getLogger(__name__)

API_VERSION = 1
API_VERSION_EX = 2

# NB: The following must match those in sacapi.h for the specified API_VERSION!

A_INVALID_TYPE  = 0
A_BINARY        = 1
A_STRING        = 2
A_DOUBLE        = 3
A_VAL64         = 4
A_UVAL64        = 5
A_VAL32         = 6
A_UVAL32        = 7
A_VAL16         = 8
A_UVAL16        = 9
A_VAL8          = 10
A_UVAL8         = 11

DT_NOTYPE       = 0
DT_DATE         = 384
DT_TIME         = 388
DT_TIMESTAMP    = 392
DT_VARCHAR      = 448
DT_FIXCHAR      = 452
DT_LONGVARCHAR  = 456
DT_STRING       = 460
DT_DOUBLE       = 480
DT_FLOAT        = 482
DT_DECIMAL      = 484
DT_INT          = 496
DT_SMALLINT     = 500
DT_BINARY       = 524
DT_LONGBINARY   = 528
DT_TINYINT      = 604
DT_BIGINT       = 608
DT_UNSINT       = 612
DT_UNSSMALLINT  = 616
DT_UNSBIGINT    = 620
DT_BIT          = 624
DT_LONGNVARCHAR = 640

DD_INVALID      = 0x0
DD_INPUT        = 0x1
DD_OUTPUT       = 0x2
DD_INPUT_OUTPUT = 0x3

class DataValue(Structure):
    """Must match a_sqlany_data_value."""

    _fields_ = [("buffer",      POINTER(c_char)),
                ("buffer_size", c_size_t),
                ("length",      POINTER(c_size_t)),
                ("type",        c_int),
                ("is_null",     POINTER(c_int))]


class BindParam(Structure):
    """Must match a_sqlany_bind_param."""

    _fields_ = [("direction",   c_int),
                ("value",       DataValue),
                ("name",        c_char_p)]


class ColumnInfo(Structure):
    """Must match a_sqlany_column_info."""

    _fields_ = [("name",        c_char_p),
                ("type",        c_int),
                ("native_type", c_int),
                ("precision",   c_short),
                ("scale",       c_short),
                ("max_size",    c_size_t),
                ("nullable",    c_int32)]


class DataInfo(Structure):
    """Must match a_sqlany_data_info."""

    _fields_ = [("index",       c_int),
                ("type",        c_int),
                ("is_null",     c_int),
                ("data_size",   c_size_t)]

def init_sacapi(api):
    sacapi_i32 = c_int32
    sacapi_bool = sacapi_i32
    sacapi_u32 = c_uint32
    p_sacapi_u32 = POINTER(sacapi_u32)
    p_sqlany_interface_context = c_void_p
    p_sqlany_connection = c_void_p
    p_sqlany_stmt = c_void_p
    p_sqlany_bind_param = c_void_p
    p_sqlany_bind_param_info = c_void_p
    p_sqlany_data_value = c_void_p
    p_sqlany_data_info = c_void_p
    p_sqlany_column_info = c_void_p

    def defun(name, *types):
        try:
            setattr(api, name, CFUNCTYPE(*types)((name, api),))
        except:
            pass

    defun("sqlany_init",
          sacapi_bool, c_char_p, sacapi_u32, p_sacapi_u32)
    defun("sqlany_init_ex",
          p_sqlany_interface_context, c_char_p, sacapi_u32, p_sacapi_u32)
    defun("sqlany_fini",
          None)
    defun("sqlany_fini_ex",
          None, p_sqlany_interface_context)
    defun("sqlany_new_connection",
          p_sqlany_connection)
    defun("sqlany_new_connection_ex",
          p_sqlany_connection, p_sqlany_interface_context)
    defun("sqlany_free_connection",
          None, p_sqlany_connection)
    defun("sqlany_make_connection",
          p_sqlany_connection, c_void_p)
    defun("sqlany_make_connection_ex",
        p_sqlany_connection, p_sqlany_interface_context, c_void_p)
    defun("sqlany_connect",
        sacapi_bool, p_sqlany_connection, c_char_p)
    defun("sqlany_disconnect",
          sacapi_bool, p_sqlany_connection)
    defun("sqlany_cancel",
          None, p_sqlany_connection)
    defun("sqlany_execute_immediate",
        sacapi_bool, p_sqlany_connection, c_char_p)
    defun("sqlany_prepare",
        p_sqlany_stmt, p_sqlany_connection, c_char_p)
    defun("sqlany_free_stmt",
          None, p_sqlany_stmt)
    defun("sqlany_num_params",
          sacapi_i32, p_sqlany_stmt)
    defun("sqlany_describe_bind_param",
        sacapi_bool, p_sqlany_stmt, sacapi_u32, p_sqlany_bind_param)
    defun("sqlany_bind_param",
        sacapi_bool, p_sqlany_stmt, sacapi_u32, p_sqlany_bind_param)
    defun("sqlany_send_param_data",
        sacapi_bool, p_sqlany_stmt, sacapi_u32, c_void_p, c_size_t)
    defun("sqlany_reset",
        sacapi_bool, p_sqlany_stmt)
    defun("sqlany_get_bind_param_info",
        sacapi_bool, p_sqlany_stmt, sacapi_u32, p_sqlany_bind_param_info)
    defun("sqlany_execute",
        sacapi_bool, p_sqlany_stmt)
    defun("sqlany_execute_direct",
        p_sqlany_stmt, p_sqlany_connection, c_char_p)
    defun("sqlany_fetch_absolute",
        sacapi_bool, p_sqlany_stmt, sacapi_i32)
    defun("sqlany_fetch_next",
        sacapi_bool, p_sqlany_stmt)
    defun("sqlany_get_next_result",
        sacapi_bool, p_sqlany_stmt)
    defun("sqlany_affected_rows",
        sacapi_i32, p_sqlany_stmt)
    defun("sqlany_num_cols",
        sacapi_i32, p_sqlany_stmt)
    defun("sqlany_num_rows",
        sacapi_i32, p_sqlany_stmt)
    defun("sqlany_get_column",
        sacapi_bool, p_sqlany_stmt, sacapi_u32, p_sqlany_data_value)
    defun("sqlany_get_data",
        sacapi_i32, p_sqlany_stmt, sacapi_u32, c_size_t, c_void_p, c_size_t)
    defun("sqlany_get_data_info",
        sacapi_bool, p_sqlany_stmt, sacapi_u32, p_sqlany_data_info)
    defun("sqlany_get_column_info",
        sacapi_bool, p_sqlany_stmt, sacapi_u32, p_sqlany_column_info)
    defun("sqlany_commit",
        sacapi_bool, p_sqlany_connection)
    defun("sqlany_rollback",
        sacapi_bool, p_sqlany_connection)
    defun("sqlany_client_version",
        sacapi_bool, c_void_p, c_size_t)
    defun("sqlany_client_version_ex",
        sacapi_bool, p_sqlany_interface_context, c_void_p, c_size_t)
    defun("sqlany_error",
        sacapi_i32, p_sqlany_connection, c_void_p, c_size_t)
    defun("sqlany_sqlstate",
        c_size_t, p_sqlany_connection, c_void_p, c_size_t)
    defun("sqlany_clear_error",
        None, p_sqlany_connection)
    return api
 

# NB: The preceding must match those in sacapi.h for the specified API_VERSION!


class DBAPISet(frozenset):

    """A special type of set for which A == x is true if A is a
    DBAPISet and x is a member of that set."""

    def __eq__(self, other):
        if isinstance(other, DBAPISet):
            return frozenset.__eq__(self, other)
        else:
            return other in self

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return frozenset.__hash__(self)

STRING    = DBAPISet([DT_VARCHAR,
                      DT_FIXCHAR,
                      DT_LONGVARCHAR,
                      DT_STRING,
                      DT_LONGNVARCHAR])
BINARY    = DBAPISet([DT_BINARY,
                      DT_LONGBINARY])
NUMBER    = DBAPISet([DT_DOUBLE,
                      DT_FLOAT,
                      DT_DECIMAL,
                      DT_INT,
                      DT_SMALLINT,
                      DT_TINYINT])
DATE      = DBAPISet([DT_DATE])
TIME      = DBAPISet([DT_TIME])
TIMESTAMP = DBAPISet([DT_TIMESTAMP])
DATETIME  = TIMESTAMP
ROWID     = DBAPISet()

ToPyType = {DT_DATE         : DATE,
            DT_TIME         : TIME,
            DT_TIMESTAMP    : TIMESTAMP,
            DT_VARCHAR      : STRING,
            DT_FIXCHAR      : STRING,
            DT_LONGVARCHAR  : STRING,
            DT_STRING       : STRING,
            DT_DOUBLE       : NUMBER,
            DT_FLOAT        : NUMBER,
            DT_DECIMAL      : NUMBER,
            DT_INT          : NUMBER,
            DT_SMALLINT     : NUMBER,
            DT_BINARY       : BINARY,
            DT_LONGBINARY   : BINARY,
            DT_TINYINT      : NUMBER,
            DT_BIGINT       : NUMBER,
            DT_UNSINT       : NUMBER,
            DT_UNSSMALLINT  : NUMBER,
            DT_UNSBIGINT    : NUMBER,
            DT_BIT          : NUMBER,
            DT_LONGNVARCHAR : STRING}


class Error(Exception):
    def __init__(self,err,sqlcode=0):
        self._errortext = err
        self._errorcode = sqlcode
    @property
    def errortext(self): return self._errortext
    @property
    def errorcode(self): return self._errorcode
    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self.errortext),
                               repr(self.errorcode))
    def __str__(self):
        return repr((self.errortext, self.errorcode))

class Warning(Exception):
    """Raise for important warnings like data truncation while inserting."""
    def __init__(self,err,sqlcode=0):
        self._errortext = err
        self._errorcode = sqlcode
    @property
    def errortext(self): return self._errortext
    @property
    def errorcode(self): return self._errorcode
    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self.errortext),
                               repr(self.errorcode))
    def __str__(self):
        return repr((self.errortext, self.errorcode))

class InterfaceError(Error):
    """Raise for interface, not database, related errors."""
    def __init__(self, *args):
        super(InterfaceError,self).__init__(*args)

class DatabaseError(Error):
    def __init__(self, *args):
        super(DatabaseError,self).__init__(*args)

class InternalError(DatabaseError):
    """Raise for internal errors: cursor not valid, etc."""
    def __init__(self, *args):
        super(InternalError,self).__init__(*args)

class OperationalError(DatabaseError):
    """Raise for database related errors, not under programmer's control:
    unexpected disconnect, memory allocation error, etc."""
    def __init__(self, *args):
        super(OperationalError,self).__init__(*args)

class ProgrammingError(DatabaseError):
    """Raise for programming errors: table not found, incorrect syntax, etc."""
    def __init__(self, *args):
        super(ProgrammingError,self).__init__(*args)

class IntegrityError(DatabaseError):
    """Raise for database constraint failures:  missing primary key, etc."""
    def __init__(self, *args):
        super(IntegrityError,self).__init__(*args)

class DataError(DatabaseError):
    def __init__(self, *args):
        super(DataError,self).__init__(*args)

class NotSupportedError(DatabaseError):
    """Raise for methods or APIs not supported by database."""
    def __init__(self, *args):
        super(NotSupportedError,self).__init__(*args)
 
def standardErrorHandler(connection, cursor, errorclass, errorvalue, sqlcode=0):
    error=(errorclass, errorvalue)
    if connection:
        connection.messages.append(error)
        if cursor:
            cursor.messages.append(error)
    if errorclass != Warning:
        raise errorclass(errorvalue,sqlcode)


# format types indexed by A_* values
format = 'xxxdqQiIhHbB'

def mk_valueof(raw, char_set):
    def valueof(data):
        if data.is_null.contents:
            return None
        elif data.type in raw:
            return data.buffer[:data.length.contents.value]
        elif data.type in (A_STRING,):
            return data.buffer[:data.length.contents.value].decode(char_set)
        else:
            fmt = format[data.type]
            return unpack(fmt, data.buffer[:calcsize(fmt)])[0]
    return valueof


def mk_assign(char_set):
    def assign(param, value):
        is_null = value is None
        param.value.is_null = pointer(c_int(is_null))
        if is_null and param.direction == DD_INPUT:
            value = 0
        if param.value.type == A_INVALID_TYPE:
            if isinstance(value, int):
                if abs(value) > 4294967295:
                    param.value.type = A_VAL64
                else:
                    param.value.type = A_VAL32
            elif isinstance(value, float):
                param.value.type = A_DOUBLE
            elif isinstance(value, Binary):
                param.value.type = A_BINARY
            else:
                param.value.type = A_STRING
        fmt = format[param.value.type]
        if fmt == 'x':
            if isinstance(value, bytes):
                pass
            elif isinstance(value, str):
                value = value.encode(char_set)
            else:
                value = str(value).encode(char_set)
            size = length = len(value)
            if param.direction != DD_INPUT:
                if size < param.value.buffer_size:
                    size = param.value.buffer_size
            buffer = create_string_buffer(value)
        else:
            buffer = create_string_buffer(pack(fmt, value))
            size = length = calcsize(fmt)
        param.value.buffer = cast(buffer, POINTER(c_char))
        param.value.buffer_size = c_size_t(size)
        param.value.length = pointer(c_size_t(length))
    return assign


threadsafety = 1
apilevel     = '2.0'
paramstyle   = 'qmark'

__all__ = [ 'threadsafety', 'apilevel', 'paramstyle', 'connect'] 

def load_library(*names):

    for name in names:
        if name is None or name == '':
            continue
        try:
            dll = cdll.LoadLibrary(name)
            lg.debug("Successfully loaded dbcapi library '%s' with name '%s'", dll, name)
            return init_sacapi(dll)
        except OSError as ose:
            continue
    raise InterfaceError("Could not load dbcapi.  Tried: " + ','.join(names))


class Root(object):
    def __init__(self, name):

        lg.debug("Attempting to load dbcapi library")
        self.api = load_library(os.getenv( 'SQLANY_API_DLL', None ), 'dbcapi.dll', 'libdbcapi_r.so',
                                'libdbcapi_r.dylib')
        ver = c_uint(0)
        try:
            self.api.sqlany_init_ex.restype = POINTER(c_int)
            lg.debug("Attempting to initalize dbcapi context (self.api.sqlany_init_ex) with arguments:" \
                " app name: '%s', api version: '%s'",
                name, API_VERSION_EX)
            context = self.api.sqlany_init_ex(name.encode('utf-8'), API_VERSION_EX, byref(ver))
            if not context:
                lg.error("Failed to initalize dbcapi context (self.api.sqlany_init_ex returned NULL)," \
                    "perhaps you are missing some required sqlanywhere libaries?")

                raise InterfaceError("Failed to initalize dbcapi context, dbcapi version %d required." \
                    " Perhaps you are missing some sqlanywhere libaries?" %
                        API_VERSION_EX)
            else:
                lg.debug("Initalization of dbcapi context successful, max api version supported: %s", ver)

            def new_connection():
                return self.api.sqlany_new_connection_ex(context)
            self.api.sqlany_new_connection = new_connection
            def fini():
                self.api.sqlany_fini_ex(context)
            self.api.sqlany_fini = fini
            def client_version():
                length = 1000
                buffer = create_string_buffer(length)
                ret = self.api.sqlany_client_version_ex(context, buffer, length)
                if ret:
                    vers = buffer.value
                else:
                    vers = None
                return vers
            self.api.sqlany_client_version = client_version
        except InterfaceError:
            raise
        except:
            if (not self.api.sqlany_init(name.encode('utf-8'), API_VERSION, byref(ver))):
                raise InterfaceError("dbcapi version %d required." %
                        API_VERSION)
            self.api.sqlany_new_connection.restype = POINTER(c_int)
        # Need to set return type to some pointer type other than void
        # to avoid automatic conversion to a (32 bit) int.
        self.api.sqlany_prepare.restype = POINTER(c_int)
        atexit.register(self.__del__)

    def __del__(self):

        # if we fail to load the library, then we won't get a chance
        # to even set the 'api' instance variable
        if hasattr(self, "api") and self.api:
            lg.debug("__del__ called on sqlany.Root object, finalizng dbcapi context")
            self.api.sqlany_fini()
            self.api = None


def connect(*args, **kwargs):
    """Constructor for creating a connection to a database."""
    return Connection(args, kwargs)


class Connection(object):

    # cache the api object so we don't have to load and unload every single time
    cls_parent = None
    
    def __init__(self, args, kwargs, parent = None):

        # make it so we don't load Root() and therefore the 
        # dbcapi C library just on import
        if parent == None:

            # cache the Root() object so we don't load it every time
            if Connection.cls_parent == None:
                parent = Connection.cls_parent = Root("PYTHON")
            else:
                parent = Connection.cls_parent

        self.Error = Error
        self.Warning = Warning
        self.InterfaceError = InterfaceError
        self.DatabaseError = DatabaseError
        self.InternalError = InternalError
        self.OperationalError = OperationalError
        self.ProgrammingError = ProgrammingError
        self.IntegrityError = IntegrityError
        self.DataError = DataError
        self.NotSupportedError = NotSupportedError

        self.errorhandler = None
        self.messages = []

        self.cursors = set()

        self.parent, self.api = parent, parent.api
        self.c = self.api.sqlany_new_connection();
        params = ';'.join(kw+'='+arg for kw, arg in v3list(list(kwargs.items())))
        char_set = 'utf-8'
        if isinstance(params, str):
            params = params.encode(char_set)
        if self.api.sqlany_connect(self.c, params):
            self.valueof = mk_valueof((A_BINARY, A_STRING), char_set)
            self.assign = mk_assign(char_set)
            self.char_set = char_set
            cur = self.cursor()
            try:
                cur.execute("select connection_property('CharSet')")
                char_set = cur.fetchone()[0]
                if isinstance(char_set, bytes):
                    char_set = char_set.decode()
                if codecs.lookup(char_set):
                    self.valueof = mk_valueof((A_BINARY,), char_set)
                    self.assign = mk_assign(char_set)
                    self.char_set = char_set
            finally:
                cur.close()
        else:
            error = self.error()
            self.api.sqlany_free_connection(self.c)
            self.c = None
            self.handleerror(*error)

    def __del__(self):
        # if we fail to load the library, then we won't get a chance
        # to even set the 'c' instance variable
        if hasattr(self, "c") and self.c:
            self.close()


    def handleerror(self, errorclass, errorvalue, sqlcode):
        if errorclass:
            eh = self.errorhandler or standardErrorHandler
            eh(self, None, errorclass, errorvalue, sqlcode)

    def con(self):
        if not self.c:
            self.handleerror(InterfaceError, "not connected", -101)
        return self.c

    def commit(self):
        self.messages = []
        return self.api.sqlany_commit(self.con())

    def rollback(self):
        self.messages = []
        return self.api.sqlany_rollback(self.con())

    def cancel(self):
        self.messages = []
        try:
            return self.api.sqlany_cancel(self.con())
        except AttributeError:
            self.handleerror(InterfaceError, "cancel not supported", -1965)

    def mk_error():
        buf = create_string_buffer(256)
        buf_size = sizeof(buf)
        def error(self):
            rc = self.api.sqlany_error(self.con(), buf, buf_size)
            if rc == 0:
                return (None, None, 0)
            elif rc > 0:
                return (Warning, buf.value, rc)
            elif rc in (-193,-194,-195,-196):
                return (IntegrityError, buf.value, rc)
            else:
                return (OperationalError, buf.value, rc)
        return error

    error = mk_error()

    def clear_error(self):
        return self.api.sqlany_clear_error(self.con())
    
    def close(self):
        self.messages = []
        c = self.con()
        self.c = None
        for x in self.cursors:
            x.close(remove=False)
        self.cursors = None
        self.api.sqlany_disconnect(c)
        self.api.sqlany_free_connection(c)

    def cursor(self):
        self.messages = []
        x = Cursor(self)
        self.cursors.add(x)
        return x

    def __enter__(self): return self.cursor()
    
    def __exit__(self, exc, value, tb):
        if exc:
            self.rollback()
        else:
            self.commit()

class Cursor(object):
    class TypeConverter(object):
        def __init__(self,types):
            def find_converter(t):
                return CONVERSION_CALLBACKS.get(t, lambda x: x)
            self.converters = v3list(list(map(find_converter, types)))

        def gen(self,values):
            for converter, value in zip(self.converters, values):
                yield converter(value)

    def __init__(self, parent):
        self.messages = []
        self.parent, self.api = parent, parent.api
        self.valueof = self.parent.valueof
        self.assign = self.parent.assign
        self.char_set = self.parent.char_set
        self.errorhandler = self.parent.errorhandler
        self.arraysize = 1
        self.converter = None
        self.rowcount = -1
        self.__stmt = None
        self.description = None

    def handleerror(self, errorclass, errorvalue, sqlcode):
        if errorclass:
            eh = self.errorhandler or standardErrorHandler
            eh(self.parent, self, errorclass, errorvalue, sqlcode)

    def __stmt_get(self):
        if self.__stmt is None:
            self.handleerror(InterfaceError, "no statement")
        elif not self.__stmt:
            self.handleerror(*self.parent.error())
        return self.__stmt

    def __stmt_set(self, value):
        self.__stmt = value

    stmt = property(__stmt_get, __stmt_set)

    def __del__(self):
        self.close()

    def con(self):
        if not self.parent:
            self.handleerror(InterfaceError, "not connected", -101)
        return self.parent.con()

    def get_stmt(self):
        return self.stmt
    
    def new_statement(self, operation):
        self.free_statement()
        self.stmt = self.api.sqlany_prepare(self.con(), operation)

    def free_statement(self):
        if self.__stmt:
            self.api.sqlany_free_stmt(self.stmt)
            self.stmt = None
            self.description = None
            self.converter = None
            self.rowcount = -1

    def close(self, remove=True):
        p = self.parent
        if p:
            self.parent = None
            if remove:
                p.cursors.remove(self)
            self.free_statement()
    
    def columns(self):
        info = ColumnInfo()
        for i in range(self.api.sqlany_num_cols(self.get_stmt())):
            self.api.sqlany_get_column_info(self.get_stmt(), i, byref(info))
            yield ((info.name.decode('utf-8'),
                   ToPyType[info.native_type],
                   None,
                   info.max_size,
                   info.precision,
                   info.scale,
                   info.nullable),
                   info.native_type)
    
    def executemany(self, operation, seq_of_parameters):
        self.messages = []

        def bind(k, col):
            param = BindParam()
            self.api.sqlany_describe_bind_param(self.stmt, k, byref(param))
            (self.assign)(param, col)
            self.api.sqlany_bind_param(self.stmt, k, byref(param))
            return param

        try:
            if isinstance(operation, str):
                operation = operation.encode(self.char_set)
            self.new_statement(operation)
            bind_count = self.api.sqlany_num_params(self.stmt)
            self.rowcount = 0
            for parameters in seq_of_parameters:
                parms = [bind(k, col)
                         for k, col in enumerate(parameters[:bind_count])]
                if not self.api.sqlany_execute(self.stmt):
                    self.handleerror(*self.parent.error())
                
                try:
                    self.description, types = v3list(list(zip(*self.columns())))
                    rowcount = self.api.sqlany_num_rows(self.stmt)
                    self.converter = self.TypeConverter(types)
                except ValueError:
                    rowcount = self.api.sqlany_affected_rows(self.stmt)
                    self.description = None
                    self.converter = None

                if rowcount < 0:
                    # Can happen if number of rows is only an estimate
                    self.rowcount = -1
                elif self.rowcount >= 0:
                    self.rowcount += rowcount
        except:
            self.rowcount = -1
            raise

        return [(self.valueof)(param.value) for param in parms]
    
    def execute(self, operation, parameters = ()):
        self.executemany(operation, [parameters])
    
    def callproc(self, procname, parameters = ()):
        stmt = 'call '+procname+'('+','.join(len(parameters)*('?',))+')'
        return self.executemany(stmt, [parameters])

    def values(self):
        value = DataValue()
        for i in range(self.api.sqlany_num_cols(self.get_stmt())):
            rc = self.api.sqlany_get_column(self.get_stmt(), i, byref(value))
            if rc < 0:
                # print "truncation of column %d"%i
                self.handleerror(*self.parent.error())
            yield (self.valueof)(value)
    
    def rows(self):
        if not self.description:
            self.handleerror(InterfaceError, "no result set", -872)

        while self.api.sqlany_fetch_next(self.get_stmt()):
            self.handleerror(*self.parent.error())
            yield tuple(self.converter.gen(v3list(list(self.values()))))
        self.handleerror(*self.parent.error())

    def fetchmany(self, size=None):
        if size is None:
            size = self.arraysize
        return [row for i,row in zip(range(size), self.rows())]
    
    def fetchone(self):
        rows = self.fetchmany(size=1)
        if rows:
            return rows[0]
        return None
    
    def fetchall(self):
        return list(self.rows())
    
    def nextset(self):
        self.messages = []
        return self.api.sqlany_get_next_result(self.get_stmt()) or None
    
    def setinputsizes(self, sizes):
        self.messages = []
        pass
    
    def setoutputsize(self, sizes, column):
        self.messages = []
        pass


def Date(*ymd):
    return "%04d/%02d/%02d"%ymd

def Time(*hms):
    return "%02d:%02d:%02d"%hms

def Timestamp(*ymdhms):
    return "%04d/%02d/%02d %02d:%02d:%02d"%ymdhms

def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])

def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])

def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])

class Binary( bytes ):
    pass

CONVERSION_CALLBACKS = {}
def register_converter(datatype, callback):
    CONVERSION_CALLBACKS[datatype] = callback
