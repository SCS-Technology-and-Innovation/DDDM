import networkx as nx
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.cluster import KMeans
from math import sqrt, fabs

G = None
tones = None
roles = None
sizes = None
groups = None

def update(xy, magnitude = 0.1):
  xy += np.random.uniform(-magnitude, magnitude, 2)
  return (np.clip(xy, 0, 1))

def leadersmove():
  global G
  for i in range(n, n + k):
    G.nodes[i]['pos'] = update(G.nodes[i]['pos'])

def followersmove(ideal = 0.15, threshold = 0.02, prop = 0.2): 
  global G
  moved = 0
  for f in range(n):
    fp = G.nodes[f]['pos']
    lp = G.nodes[n + groups[f]]['pos']
    d = lp - fp # the position difference of the follower towards its leader 
    eucl = sqrt(np.sum(d * d)) 
    adj = eucl - ideal
    speed = prop * adj # bigger movements when further away
    if fabs(adj) > threshold: 
      G.nodes[f]['pos'] += speed * d
      moved += 1
  return moved
    

n = 100
k = 7
size = 25
    
def reset():
  global G, tones, roles, sizes, groups
  pos = np.random.random((n, 2)) # x and y 
  clustering = KMeans(n_clusters = k, n_init = 'auto').fit(pos)
  leaders = clustering.cluster_centers_
  groups = clustering.labels_
  G = nx.DiGraph()
  for f in range(n): #  followers 0, 1, ..., n - 1 
    G.add_node(f, pos = pos[f])
  for l in range(k):
   G.add_node(n + l, pos = leaders[l]) # leaders n, n + 1, n + k - 1
  for f in range(n): 
    l = n + groups[f] 
    G.add_edge(f, l) 
  tones = sns.color_palette('husl', k)
  roles = [ tones[groups[i]] if i < n else tones[i - n] for i in range(n + k)]
  sizes = [ size if i < n else 3 * size for i in range(n + k) ]

def twostep(t = 0):
  plt.clf()
  if followersmove() < n / 2:
    leadersmove() # the majority is caught up, leaders can move again
  nx.draw(G, nx.get_node_attributes(G, 'pos'),
          node_size = sizes,
          node_color = roles,
          width = 2, # thicker edges
          arrowstyle = '-') # no arrowheads, we know the direction anyhow
  
fig = plt.figure(figsize = (5, 5), dpi = 150)
plt.clf()
movie = animation.FuncAnimation(fig, twostep, frames = 200, repeat = False, init_func = reset)

movie.save('formation.avi')

