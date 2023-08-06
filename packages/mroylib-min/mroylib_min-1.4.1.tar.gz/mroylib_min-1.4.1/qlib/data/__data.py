import sqlite3,time, os, logging
import xlwt, xlrd
import contextlib 
from tempfile import TemporaryFile, NamedTemporaryFile

DEBUG = False
# DEBUG = True
BACK_PATH = "/tmp/back_dirs"
if not os.path.exists(BACK_PATH):
    os.mkdir(BACK_PATH)


"""
# example:
# use:
from data import  *
c = Cache("/tmp/test.db")
w = list(c.query(File, "like",file="dat"))

# expend:
# don't overwrite function: '__init__' !!!!
# don't overwrite function: '__init__' !!!!
# don't overwrite function: '__init__' !!!!
create table test22 as select Infos.reg_time, Users.name, Infos.email, Infos.ip from Infos left outer join Users on Infos.uid == Users.uid ;
class XXX(dbobj):
    ...

c = Cache(db_path)

## insert
e = XXX(k=v, k2=v2)
e.save(c)

## query

c.query(XXX, id=2)                  #id=2 's XXX 
c.query(XXX,'<', id=2)              #id < 2 's XXX 


## query by time , if there be , which like:
c.query(XXX, '<', time='2017-12-1 18:37:23')   # time before 2017-12-1 18:37:23's XXX
c.query(XXX, '<', time='18:37:23')   # time before 2017-12-1 18:37:23's XXX
c.query(XXX, '<', time='18:37')   # time before 2017-12-1 18:37:00's XXX
c.query(XXX, '~2', time='18:37')   # time before 2017-12-1 18:37:00 +- 2 sec 's XXX

c.query(XXX, '<', time=1512124620.0)   # time before 2017-12-1 18:37:00's XXX
c.query(XXX, '>', time=1512124620.0)   # time before 2017-12-1 18:37:00's XXX
c.query(XXX, '~1', time=1512124620.0)   # time before 2017-12-1 18:37:00 +- 1 sec 's XXX
c.query(XXX, '~2', time=1512124620.0)   # time before 2017-12-1 18:37:00 +- 2 sec 's XXX


"""


class dbobj(object):
    """
# example:
# use:
from data import  *
c = Cache("/tmp/test.db")
w = list(c.query(File, "like",file="dat"))

# expend:
# don't overwrite function: '__init__' !!!!
# don't overwrite function: '__init__' !!!!
# don't overwrite function: '__init__' !!!!

class XXX(dbobj):
    ...

c = Cache(db_path)

## insert
e = XXX(k=v, k2=v2)
e.save(c)

## query

c.query(XXX, id=2)                  #id=2 's XXX 
c.query(XXX,'<', id=2)              #id < 2 's XXX 


## query by time , if there be , which like:
c.query(XXX, '<', time='2017-12-1 18:37:23')   # time before 2017-12-1 18:37:23's XXX
c.query(XXX, '<', time='18:37:23')   # time before 2017-12-1 18:37:23's XXX
c.query(XXX, '<', time='18:37')   # time before 2017-12-1 18:37:00's XXX
c.query(XXX, '~2', time='18:37')   # time before 2017-12-1 18:37:00 +- 2 sec 's XXX

c.query(XXX, '<', time=1512124620.0)   # time before 2017-12-1 18:37:00's XXX
c.query(XXX, '>', time=1512124620.0)   # time before 2017-12-1 18:37:00's XXX
c.query(XXX, '~1', time=1512124620.0)   # time before 2017-12-1 18:37:00 +- 1 sec 's XXX
c.query(XXX, '~2', time=1512124620.0)   # time before 2017-12-1 18:37:00 +- 2 sec 's XXX


    """

    
    def __init__(self, **kargs):
        for k,v in kargs.items():
            setattr(self, k, v)

    def before_save(self):
        """
    do some what you want to, 
    this will run before save
        """
        pass

    @staticmethod
    def str2time(self, str, format="%Y-%m-%d %H:%M:%S"):
        return time.mktime(time.strptime(str, format))

    def sec2date(self, time_sec):
        return time.gmtime(time_sec)

    def gettimezone(self):
        return self.sec2date(self.time)

    def getTime(self):
        return time.ctime(self.time)

    def show(self):
        __dict = self.__dict__
        return [(k,__dict[k]) for k in __dict]

    def search(self, key):
        if isinstance(key, int):
            key = str(key)

        for v in self.get_dict().values():
            if not isinstance(v, str):
                v = str(v)
            if key in v:
                return self, v
            if v in key:
                return self, v
        return '',''

    def change(self,con,  **kargs):
        _change_str = "UPDATE %s SET "
        __dict = self.__dict__
        
        for k in __dict:
            _change_str += "%s=?,"%k

        __change_str = _change_str[:-1] + " WHERE "
        for k2 in kargs:
            __change_str += "%s=?," %k
        ___change_str = __change_str[:-1] + ";"
        
        if not con:
            return ___change_str

    def get_fields(self):
        return self.__dict__.keys()

    def get_dict(self):
        return self.__dict__        
    
    def save(self, con=None):
        self.before_save()
        if not hasattr(self, 'time'):
            self.time = int(time.time())

        __dict = self.__dict__
        _create_str = "CREATE TABLE %s (id INTEGER PRIMARY KEY AUTOINCREMENT, time DATETIME," % self.__class__.__name__
        _insert_str = "INSERT INTO %s (%s) VALUES(" % (self.__class__.__name__, ",".join(__dict.keys()))
        for k in __dict:
            v = __dict[k]
            if k == "time":
                _insert_str += "?,"
                continue

            if isinstance( v, str):
                _create_str += k + " TEXT,"
            elif isinstance( v, bytes):
                _create_str += k + " BLOB,"
            elif isinstance( v, (int, float)):
                if 'time' in k:
                    _create_str += k + " DATETIME,"
                else:
                    if isinstance(v, float):
                        _create_str += k + " FLOAT,"
                    else:
                        _create_str += k + " INTEGER,"

            _insert_str += "?,"
        __create_str = _create_str[:-1] + ");"
        __insert_str = _insert_str[:-1] + ");"
        __values = __dict.values()
        if not con:
            return __create_str, __insert_str, __values

        try:
            con._con.execute(__create_str)
        except sqlite3.OperationalError as e:
            if DEBUG:
                print(e)
            pass
        try:
            if DEBUG:
                print(__create_str,__insert_str, )
            con._con.execute(__insert_str, list(__values))
        except sqlite3.OperationalError as e:
            # print(con._con.execute("select sql from sqlite_master where name=(?)", [self.__class__.__name__]).fetchone()[0])
            raise e
        finally:
            con._con.commit()


class  File(dbobj):
    """docstring for  FileObj"""
    def bak(self):
        if not self.time:
            self.time = int(time.time())

        if not self.link:
            self.link = os.path.join(BACK_PATH, str(self.time))

        try:
            os.rename(self.file, self.link)
        except IOError as e:
            print (e)

    def set_backup_path(self, newpath):
        global BACK_PATH
        BACK_PATH = newpath
    
    def before_save(self):
        self.time = int(time.time())
        self.link = os.path.join(BACK_PATH, str(time.time()))
        assert(hasattr(self, 'file'))


class NetWork(dbobj):
    pass



class Cache:
    """
# example:
# use:
from data import  *
c = Cache("/tmp/test.db")
w = list(c.query(File, "like",file="dat"))

# expend:
# don't overwrite function: '__init__' !!!!
# don't overwrite function: '__init__' !!!!
# don't overwrite function: '__init__' !!!!

class XXX(dbobj):
    ...

c = Cache(db_path)

## insert
e = XXX(k=v, k2=v2)
e.save(c)

## query

c.query(XXX, id=2)                  #id=2 's XXX 
c.query(XXX,'<', id=2)              #id < 2 's XXX 


## query by time , if there be , which like:
c.query(XXX, '<', time='2017-12-1 18:37:23')   # time before 2017-12-1 18:37:23's XXX
c.query(XXX, '<', time='18:37:23')   # time before 2017-12-1 18:37:23's XXX
c.query(XXX, '<', time='18:37')   # time before 2017-12-1 18:37:00's XXX
c.query(XXX, '~2', time='18:37')   # time before 2017-12-1 18:37:00 +- 2 sec 's XXX

c.query(XXX, '<', time=1512124620.0)   # time before 2017-12-1 18:37:00's XXX
c.query(XXX, '>', time=1512124620.0)   # time before 2017-12-1 18:37:00's XXX
c.query(XXX, '~1', time=1512124620.0)   # time before 2017-12-1 18:37:00 +- 1 sec 's XXX
c.query(XXX, '~2', time=1512124620.0)   # time before 2017-12-1 18:37:00 +- 2 sec 's XXX


    """

    paths = {}

    def __init__(self, dbpath, driver=sqlite3):
        if hasattr(driver, 'connect'):
            self._driver = driver
            self._con = getattr(driver,'connect')(dbpath)
        else:
            return

    def query(self,obj, eq="=", m='or', timestamp=None,**kargs):
        """
        eq: like
            =
            >
            <

        m:  or
            and
        """
        try:
            keys = [i.split()[0] for i in self._con.execute("select sql from sqlite_master where name=(?)", [obj.__name__]).fetchone()[0].split(",")[1:]]
        except TypeError:
            return 
        
        _query_str = "SELECT * FROM %s WHERE " % obj.__name__
        
        ## 
        # this block is for parse timestamp
        time_sec = None
        if timestamp != None and isinstance(timestamp, str) :
            err_time = 0
            
            while err_time < 3:
                tody = time.gmtime(time.time())
                pre_time = "%d-%d-%d " %(tody.tm_year,tody.tm_mon,tody.tm_mday)
                try:
                    if err_time == 0:
                        time_sec = time.mktime(time.strptime(timestamp.strip(), "%Y-%m-%d %H:%M:%S"))
                    elif err_time == 1:
                        time_sec = time.mktime(time.strptime(pre_time + timestamp.strip(), "%Y-%m-%d %H:%M:%S"))
                    elif err_time == 2:
                        time_sec = time.mktime(time.strptime(pre_time + timestamp.strip()+":0", "%Y-%m-%d %H:%M:%S"))
                    # print(time_sec)
                except ValueError as  e:
                    err_time += 1

                    continue
                
                if time_sec:
                    break
        elif isinstance(timestamp, (int, float,)):
            time_sec = timestamp

        if time_sec:
            kargs['time'] = int(time_sec)

        for k,v  in kargs.items():

            if isinstance(v, int):
                if eq.startswith("~"):
                    may_be = int(eq[1:])
                    ww = ("(" + k + " > %d and " + k + " < %d ) %s") % ( v- may_be,v + may_be, m)
                    
                    _query_str +=   ww
                    continue
                
                _query_str+= k + "%s%d %s" % (eq,v, m)
            elif isinstance(v, str):
                if eq == "like":
                    _query_str+= k + " %s \"%%%s%%\" %s" % (eq,v, m)
                else:
                    _query_str+= k + " %s \"%s\" %s" % (eq,v, m)
        __query_str = _query_str[:-len(m)] + ";"
        if DEBUG:
            print(__query_str)
        try:
            res = self._con.execute(__query_str)
        except sqlite3.OperationalError:
            print(__query_str)
        for v in res.fetchall():
            yield obj(**dict(zip(keys,v[1:])))

    # def execute(self,*args, **kargs): return self._con.execute(*args, **kargs)
    def query_one(self,obj, eq="=", m='or', timestamp=None,**kargs):
        ss = self.query(obj,eq="=", m='or', timestamp=None,**kargs)
        if ss:
            try:
                for i in ss:
                    return i
            except TypeError:
                pass

    def delete(self, obj):
        __dict = obj.__dict__
        __DELETE_STR = "DELETE FROM " + obj.__class__.__name__ + " WHERE "
        for k in __dict:
            __DELETE_STR += "%s=? and " % k
        _delete_str = __DELETE_STR[:-4] + ";"
        vals = __dict.values()
        try:
            self._con.execute(_delete_str, list(vals))
            self._con.commit()
        except sqlite3.OperationalError as e:
            print(_delete_str)
            raise e
        except Exception as e:
            print(_delete_str, vals)



    def __del__(self):
        self._con.close()

    def save_all(self, *Obj):
        create_strs = set()
        insert_strs = {}
        
        for obj in Obj:
            create_str, insert_str, values = obj.save()
            create_strs.add(create_str)
            if insert_str not in insert_strs:
                insert_strs[insert_str] = [tuple(values)]
            else:
                insert_strs[insert_str].append(tuple(values))

            
        try:
            self._con.execute(";\n".join(create_strs))
            self._con.commit()
        except Exception as e:
            logging.warn(e)

        for insert_template in insert_strs:
            try:
                self._con.executemany(insert_template, insert_strs[insert_template])
                self._con.commit()
                logging.info("insert many -> " + insert_template)
            except Exception as e:
                logging.error(e)

    def fuzzy_search(self, Obj, key, printer=print):
        for i in self.query(Obj):
            v,r = i.search(key)
            if r:
                printer(v)
                yield r

    @classmethod
    def load_xlsx(cls, xls_files):
        with NamedTemporaryFile('w+t') as f:
            xlsx_to_sql(xls_files, f.name)
            cl = cls(f.name)
            return cl

    # def from_csv(self, csv_file, create_db_file=None):
    #     if not create_db_file:
    #         with NamedTemporaryFile('w+t') as f:
    #             self._con = getattr(self._driver, 'connect')(f.name)

    #             csv_to_sql(Obj, csv_file)


@contextlib.contextmanager 
def connect(database):
    try:
        c = Cache(database)
        yield c
    finally:
        del c

def merges(Obj,*files, new_file='new.db'):
    c_new = Cache(new_file)
    ws = []
    for db_f in files:
        c = Cache(db_f)
        for u in c.query(Obj):
            ws.append(u)

    c_new.save_all(*ws)
    return True






def export_xlsx( objs, outputpath):
    
    

    obj = objs[0]
    results = objs

    
    fields = list(obj.get_fields())
    table_name = obj.__class__.__name__
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table_' + table_name , cell_overwrite_ok=True)

    
    for field in range(0,len(fields)):
        sheet.write(0,field,fields[field])

    
    row = 1
    col = 0
    for row in range(1, len(results)+1):
        for col,name in enumerate(fields):
            sheet.write(row,col,u'{}'.format(getattr(results[row-1], name)))

    workbook.save(outputpath)



def csv_to_sql(Obj,csv_file, *fields):

    cs = []
    with open(csv_file) as csv_fp:
        for l in csv_fp:
            l = l.strip()
            if l:
                cs.append(Obj(**dict(zip(fields, l.split(",")))))
    c = Cache(csv_file+".db")
    c.save_all(*cs)
    return True




def open_xlsx(file, granularity=20):
    sheets = xlrd.open_workbook(file)
    for table in  sheets.sheets():
        table_name = table.name
        rows = table.nrows
        cols = table.ncols
        fields = [str(i.value) for i in table.row(0)]
        Obj = type(table_name, (dbobj,), {})
        print(Obj.__name__)
        all_sql_objs = []
        for i in range(1, rows):

            o = Obj(**dict(zip(fields, [i.value for i in table.row(i)])))
            
            all_sql_objs.append(o)
            if len(all_sql_objs) >= granularity:
                yield all_sql_objs
                all_sql_objs = []

        if len(all_sql_objs) != 0:
            yield all_sql_objs



def xlsx_to_sql(excel_file, database):
    with  connect(database) as c:
        for row_objs in  open_xlsx(excel_file):
            c.save_all(*row_objs)
