# -*- coding:utf-8 -*-


from elasticsearch import Elasticsearch
import sys

client = Elasticsearch(hosts=["172.16.39.231","172.16.39.232","172.16.39.233","172.16.39.234"],timeout=5000)

def scan_task():
    try:
        operation = sys.argv[1]
        task_name = sys.argv[2]
        ipv4_index_name = task_name +"_ipv4"
        websites_index_name = task_name + "_websites"
        if operation == "delete":
            client.indices.delete(index=ipv4_index_name)
            client.indices.delete(index=websites_index_name)
            print "Successful deletion of the task"
        elif operation == "create":
            client.indices.create(index=ipv4_index_name)
            client.indices.create(index=websites_index_name)
            print "Successful creation of a task"
        else:
            print "format:scantask create/operate taskname"
    except:
        print "format:scantask create/operate taskname"