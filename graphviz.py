import networkx as nx
from collections import Counter
import graphviz

%load TwitterEval.py

#create tuples of (from_user, user_mentions) and append to tuple_list
def populate_tuple(row, tuple_list):
	for mention in row['user_mentions']:
		tuple_list.append((row['from_user'], mention))


amount = 1000
ms = [m for m in df.head(amount).user_mentions]
flat_ms = [m for sublist in ms for m in sublist]
mention_count = Counter(flat_ms)

#tuple_list is used to add edges to the graph
tuple_list = []
df.head(amount).apply(lambda row: populate_tuple (row, tuple_list), axis=1)

#create a networkx digraph and convert into an Agraph
mention_graph = nx.DiGraph()
mention_agraph = nx.drawing.nx_agraph.to_agraph(mention_graph)

#for every mention add a node and make its 'edges' equal to number of mentions
for mention in mention_count:
	count = mention_count[mention]
	length = len(mention_count)
	    mention_agraph.add_node(mention, label=mention, edges=count, fontsize=12+count/7, 
            height=1+count/(length/2), width=1+count/(length/3), color='firebrick1')

#connect the nodes using the tuple list
mention_agraph.add_edges_from(tuple_list)

#change settings of the graph and nodes
mention_agraph.graph_attr['overlap'] = 'false'
mention_agraph.graph_attr['splines'] = 'true'
mention_agraph.node_attr['style'] = 'filled'
mention_agraph.node_attr['color'] = 'firebrick1'
mention_agraph.node_attr['fontname'] = 'Helvetica'


mention_agraph.draw("graphviz.png", prog='sfdp')