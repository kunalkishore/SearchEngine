import elasticsearch
import sys
import os
# Assuming the the data to be a news data
# Assuming that the data is being read from a file which contains the following fields:
# {
# 'title':data
# 'content':content
# 'dop':date of publication
# }
ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'google'
TYPE_NAME = 'news'
#initialize an ES client
client=elasticsearch.Elasticsearch(hosts=[ES_HOST])
if client.indices.exists(INDEX_NAME):
    print("Deleting %s index..." %(INDEX_NAME))
    res=client.indices.delete(index=INDEX_NAME)
    print("Response: %s"%(res))

requestBody = {
    "settings":{
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings":{
        TYPE_NAME:{
            "properties":{
                "title":{
                    "type":"string"
                },
                "article":{
                    "type":"string"
                },
                "date":{
                    "type":"date",
                    "format":"dd-MM-YYYY"
                },
                "newsgenre":{
                    "type":"string"
                },
                "newslink":{
                    "type":"string",
                    "index":"no",
                    "include_in_all":"false"
                }
            }
        }
    }
}

print("creating '%s' index..." % (INDEX_NAME))
res = client.indices.create(index=INDEX_NAME,body=requestBody)
print(" response: '%s'" % (res))

#Read from the file and do bulk uploading
bulkData=[]
with open('data.txt','r') as f:
    rownum=0
    for line in f:
        actionDict={
            "index":{
                "_index":INDEX_NAME,
                "_type":TYPE_NAME,
                "_id":rownum
            }
        }
        dataDict=eval(line.rstrip('\n'))
        bulkData.append(actionDict)
        bulkData.append(dataDict)
        rownum+=1

# bulk index the data
print("bulk indexing...")
res = es.bulk(index = INDEX_NAME, body = bulkData, refresh = True)
