import bottle
import pymongo
from bottle import response, request
import json
from bson import ObjectId
import os
import random
import time
import requests
from loremipsum import generate_paragraphs
import urllib2
import threading


class JSONEncoder1(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    @staticmethod
    def apply(fn, context):
        def _enable_cors(*args, **kwargs):
            # print context
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, DELETE'
            response.headers[
                'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
            response.headers['Content-type'] = 'application/json'
            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


app = bottle.app()
app.install(EnableCors())

print "START"
coll_name = 'documents'


def get_database_host():
    try:
        host = os.environ.get('DATABASE_HOST')
    except Exception, e:
        print e
        host = None
        print "ERROR"
    if host:
        pass
    else:
        host = 'arkismongopersistent'
    return host


def get_database_port():
    try:
        port = int(os.environ.get('DATABASE_PORT'))
    except Exception, e:
        print e
        port = None
        print "ERROR"
    if port:
        pass
    else:
        port = 27017
    return port


def get_connection(user, option, replica):
    conn_cluster = "mongodb://mongo-0.mongo"
    hosts = []
    for i in range(0, replica):
        a = "mongo-" + str(i) + ".mongo:27017"
        hosts.append(a)
        if i != 0:
            conn_cluster += ",mongo-" + str(i) + ".mongo"
    conn_cluster += ":27017/?replicaSet=rs0"
    try:
        # conn = pymongo.MongoClient(conn_cluster, read_preference=ReadPreference.NEAREST)
        conn = pymongo.MongoClient(conn_cluster)
    except Exception, e:
        a2 = {"mongos": e}
        print e
        conn = None
    return conn


def get_database(conn, option, user):
    if user:
        user = str(user)
    if option == 'A':
        return conn['arkis']
    elif option == 'B':
        return conn['arkis']
    elif option == 'C':
        return conn['arkis']
    elif option == 'E':
        return conn['arkis']
    elif option == 'D':
        return conn['arkis' + str(user)]
    else:
        return conn['arkis']


def get_collection(option, db, user, coll):
    if option == 'B':
        return db[str(coll) + str(user)]
    else:
        return db[str(coll)]


@app.route('/')
def start():
    a2 = {"mongos": "no"}
    conn_cluster = "mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017"
    try:
        conn = pymongo.MongoClient(conn_cluster)
    except Exception, e:
        a2 = {"mongos": e}
        print e
        conn = None
    a3 = {"conn": str(conn)}
    conn.close()
    # host = get_database_host()
    # port = get_database_port()
    a1 = {"conn_cluster": conn_cluster}
    try:
        a2 = {"mongos": conn.is_mongos}
    except Exception, e:
        print e

    res = [a1, a2, a3]
    return JSONEncoder1().encode(res)


@app.route('/check')
def check():
    a1 = {"conn": "error"}
    res = [a1]
    return JSONEncoder1().encode(res)


@app.route('/connection/<user>/<option>')
def connection(user, option):
    user = int(user)
    try:
        replicas = 3
        conn = get_connection(user, option, replicas)
    except Exception, e:
        collection_names = ["error connection", e]
        return JSONEncoder1().encode({"collections": collection_names})
    try:
        db = get_database(conn, option, user)
    except Exception, e:
        collection_names = ["error database", e]
        return JSONEncoder1().encode({"collections": collection_names})
    collection_names = db.collection_names()
    conn.close()
    return JSONEncoder1().encode({"collections": collection_names})


def get_blob():
    res = ''
    for p in generate_paragraphs(10, False):
        res += p[2]
    return res


def create_aux_json(prefix_name, multi_tenant_option, count, user):
    blob = get_blob()
    name = blob[:5]
    path = '/data/blobs/' + prefix_name + '_' + multi_tenant_option + '_' + str(count) + '_' + name + '.txt'
    number_aux = random.randint(1, 100)
    aux_json = {'title': name,
                'tenant': user,
                'user': user,
                'name': name,
                'tenant_option': multi_tenant_option,
                'other_id': count,
                'path': path,
                'blob': blob,
                'number': number_aux}
    return aux_json


def get_max_row_id(coll):
    try:
        a = int(coll.find_one(sort=[("other_id", -1)])['other_id'])
        return a
    except Exception, e:
        print e
        return -2


@app.get('/test/insert/<tenant_start>/<tenant_end>/<docs>/<option>/<user>/<replicas>')
def test_insert(tenant_start, tenant_end, docs, option, user, replicas):
    if option == 'D':
        counts = []
        conn = get_connection(user, option, int(replicas))
        for i in range(int(tenant_start), int(tenant_end)):
            db = get_database(conn, 'D', i)
            coll = get_collection(option, db, i, 'documents')
            for j in range(0, int(docs)):
                json_data = create_aux_json('arkis', option, j, int(i))
                coll.insert_one(json_data)
            coll.create_index([('blob', pymongo.TEXT)])
            counts.append(str(coll.count()))
        conn.close()
        return JSONEncoder1().encode({"counts": counts})


def get_documents_host():
    try:
        host = str(os.environ.get('DOCUMENTS_HOST'))
    except Exception, e:
        print e
        host = None
        print "ERROR"
    if host:
        pass
    else:
        host = '130.211.221.192'
    return host


def get_number_database(replica1, tenant_max1, tenant1):
    number_db1 = -1
    for k in range(0, int(replica1)):
        a1 = (k * int(tenant_max1)) / int(replica1)
        b1 = ((k + 1) * int(tenant_max1)) / int(replica1)
        if tenant1 in range(a1, b1):
            number_db1 = k
    return str(number_db1)


@app.get('/test/selects/<tenant_start>/<tenant_end>/<tenant_max>/<option>/<replica>/<loop>/<lim>/<word>')
def test_selects(tenant_start, tenant_end, tenant_max, option, replica, loop, lim, word):

    host_name = get_documents_host()
    if option == 'D':
        time_total_start = time.time()
        times = []

        for i in range(int(tenant_start), int(tenant_end)):
            time_start = time.time()

            number_db = get_number_database(replica, tenant_max, i)
            for j in range(0, int(loop)):
                url1 = 'http://' + host_name + ':30000/documents/search/' + str(i) + '/D/' + number_db + '/' + str(word)
                url2 = 'http://' + host_name + ':30000/documents/' + str(i) + '/D/' + number_db + '/lim/' + str(lim)
                url3 = 'http://' + host_name + ':30000/documents/' + str(i) + '/D/' + number_db + '/last'
                url4 = 'http://' + host_name + ':30000/documents/' + str(i) + '/D/' + number_db + '/4'
                print JSONEncoder1().encode(urllib2.urlopen(url1).read())
                print JSONEncoder1().encode(urllib2.urlopen(url2).read())
                print JSONEncoder1().encode(urllib2.urlopen(url3).read())
                print JSONEncoder1().encode(urllib2.urlopen(url4).read())
            time_end = time.time()
            time_iteration = time_end - time_start
            key_aux = "tenant_" + str(i)
            aux = {key_aux: time_iteration}
            times.append(aux)
        time_total_end = time.time()
        time_total = time_total_end - time_total_start
        times.append(time_total)
        return JSONEncoder1().encode({"times": times})


def select_test_1(a, b, loop, replica, word, lim, times):
    host_name = get_documents_host()
    for i in range(a, b):
        time_start = time.time()
        for j in range(0, int(loop)):
            url1 = 'http://' + host_name + ':30000/documents/search/' + str(i) + '/D/' + replica + '/' + str(word)
            url2 = 'http://' + host_name + ':30000/documents/' + str(i) + '/D/' + replica + '/lim/' + str(lim)
            url3 = 'http://' + host_name + ':30000/documents/' + str(i) + '/D/' + replica + '/last'
            url4 = 'http://' + host_name + ':30000/documents/' + str(i) + '/D/' + replica + '/4'
            print JSONEncoder1().encode(urllib2.urlopen(url1).read())
            print JSONEncoder1().encode(urllib2.urlopen(url2).read())
            print JSONEncoder1().encode(urllib2.urlopen(url3).read())
            print JSONEncoder1().encode(urllib2.urlopen(url4).read())
        time_end = time.time()
        time_iteration = time_end - time_start
        key_aux = "tenant_" + str(i)
        aux = {key_aux: time_iteration}
        times.append(aux)
    return times


@app.get('/test/selects/thread/<tenant_start>/<tenant_end>/<tenant_per_thread>/<option>/<replica>/<loop>/<lim>/<word>')
def test_selects_thread(tenant_start, tenant_end, tenant_per_thread, option, replica, loop, lim, word):
    if option == 'D':
        time_total_start = time.time()
        times = []
        threads = []
        a = int(tenant_start)
        c = int(tenant_end)
        len_times = c - a
        while a < c:

            b = min(c, a + int(tenant_per_thread))
            t = threading.Thread(target=select_test_1, args=(a, b, loop, replica, word, lim, times))
            a += int(tenant_per_thread)
            threads.append(t)

        count = 0
        for t in threads:
            t.start()
            count += 1
            time.sleep(0.5)

        while count != len(threads):
            pass

        print "started"
        for t in threads:
            t.join()

        print "ended"
        time_total_end = time.time()
        time_total = time_total_end - time_total_start

        while len(times) < len_times:
            pass

        key_aux = "tenant_total"
        aux = {key_aux: time_total}
        times.append(aux)
        key_times = "times_" + str(tenant_start) + "_" + str(tenant_end)
        return JSONEncoder1().encode({key_times: times})


app.run(host='0.0.0.0', port=55555, debug=True)
