#!/usr/bin/python

import os

NODES_NUMBER = 2**14

def calculate_parent(id):
	parent = ""
	while (id != 0):
		parent = ("/%d" + parent) % (id)
		id /= 2
	return parent


def generate_body(id):
	parent = calculate_parent(id)
	node = "{\"name\": \"Text%d\", \"path\": \"%s\"}" % (id, calculate_parent(id))
	return node

def generate_id(id):
	return "{\"index\": {\"_id\":\"%d\"}}" % (id)

def generate_node(id):
	index = generate_id(id)
	node = generate_body(id)
	return index + "\n" + node

def main():
	for i in range(1, NODES_NUMBER):
		print generate_node(i)

if __name__ == '__main__':
	main()

# Generate this structure 
# {
# >  "name": "1",
# >  "path": "/a/b/c"
# > }

# Useful commands
# -- create index
# curl -XPUT 'localhost:9200/tree' -d '{
# 	"settings" : {
# 		"index" : {
# 			"analysis" : {
# 				"analyzer" : {
# 					"path_analyzer" : { "tokenizer" : "path_hierarchy" }
# 				}
# 			}
# 		}
# 	},
# 	"mappings" : {
# 		"bst" : {
# 			"properties" : {
# 				"bst" : {
# 					"type" : "string",
# 					"fields" : {
# 						"name" : { 
# 							"type" : "string",
# 							"index" : "not_analyzed" 
# 						},
# 						"path" : { 
# 							"type" : "string",
# 							"analyzer" : "path_analyzer",
# 							"store" : true 
# 						}
# 					}
# 				}
# 			}
# 		}
# 	}
# }'

# -- upload batch
# curl -XPOST 'localhost:9200/tree/bst/_bulk?pretty&refresh' --data-binary "@bst.json"

# -- get indeces
# curl -XGET 'localhost:9200/_cat/indices?v&pretty'

# curl -XGET 'localhost:9200/tree/_search?pretty' -H 'Content-Type: application/json' -d'
# {
#   "query": { "match": {"path": "/4" } }
# }
# '

# curl -XGET 'localhost:9200/tree/_search?pretty' -H 'Content-Type: application/json' -d'
# {
#   "query": { "match_all": {} }
# }
# '

# curl -XGET 'localhost:9200/tree/_search?pretty' -H 'Content-Type: application/json' -d'
# {
# 	"filter": {
# 		"term" : { "bst.path" : "/4" }
# 	}
# }
# '


# curl -XGET 'localhost:9200/_search?pretty' -H 'Content-Type: application/json' -d'
# {
#     "query": {
#     	"term" : { "bst.path" : "/4"}
#     }
# }
# '
# --analyze path
# curl -XGET 'localhost:9200/tree/_analyze?field=bst.path&pretty' -d'/4/8/16'