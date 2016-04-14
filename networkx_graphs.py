%load TwitterEval.py

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from collections import Counter

# %matplotlib inline

#####################################################
# 
# Graph network of user_mentions
#

BASE_NODE_SIZE = 300
NODE_SIZE_MULTIPLIER = 200

#for every mention, adds an edge between the mentioner and mentionee
def add_mention(row, g):
    for mention in row['user_mentions']:
        if not (mention in g.nodes()):
            g.add_node(mention, edges=0)
        g.add_edge(row['from_user'], mention)
        g.node[mention]['edges'] += 1

#creating the graph
g = nx.DiGraph()

#populating with nodes
g.add_nodes_from(df.from_user.unique(), edges=0)

#add edges from mentions
df.apply(lambda row: add_mention (row, g), axis=1)

#scale node size based on number of edges (mentions)
node_sizes = [BASE_NODE_SIZE + NODE_SIZE_MULTIPLIER * g.node[s]['edges'] for s in g.nodes()]

#draw the graph
plt.figure(1, figsize=(100,100))
nx.draw_random(g, 
		node_size=node_sizes, 
		font_size=12, 
		alpha=0.5, 
		edge_color="blue",
		with_labels=True)


#####################################################
# 
# Graph of hashtag cloud
#



#sets the 'count' attribute of each node based on the number in the row tuple
def add_count(g, rows):
    for row in rows:
        g.node[row[0]]['count'] = row[1]

hashtags_all = [ht for ht in df.hashtags]
hashtags_flat = [ht for sublist in hashtags_all for ht in sublist]
count_all = Counter()
count_all.update(map(str.lower, hashtags_flat))

#top 20 used hashtags 
most_popular = count_all.most_common(20)

#create graph
hashtag_cloud = nx.DiGraph()

#populate graph with nodes
hashtag_cloud.add_nodes_from([row[0] for row in most_popular], count=0)

#set the hashtag count as attirbutes of the nodes
add_count(hashtag_cloud, most_popular)

#scale node sizes based on count
hashtag_cloud_sizes = [10 + hashtag_cloud.node[s]['count'] for s in hashtag_cloud.nodes()]

#set some colour scale
node_colours = [size/12517 for size in node_sizes]

#draw graph
nd.draw_random(hashtag_cloud,
		node_size = hashtag_cloud_sizes,
		alpha = 0.7
		font_size = 12,
		with_labels = True,
		cmap = plt.get_cmap('jet'),
		node_color = node_colours)