rodCount = 3
diskCount = 7
rods = [ [] for rod in range(rodCount) ]
disks = [ size for size in range(diskCount) ]

import seaborn as sns
colors = sns.color_palette('bright', diskCount)

rods[0] = disks # put all disks on the first rod, listed from top to bottom

def validate(rods):
  for rod in rods:
      previous = 0
      for disk in rod:
        if disk < previous:
          return False # a disk is smaller than the one above it
        previous = disk
  return True # all disks were larger than the ones above them

import matplotlib.pyplot as plt 
fig = None
ax = None

def setup():
  global fig, ax
  r = len(rods)
  d = max( [ max(rod) if len(rod) > 0 else 0 for rod in rods ] ) + 1
  if fig is None:
    fig = plt.figure(figsize = (3 * r, 1 + d), dpi = 120)
    ax = plt.subplot(111)
  plt.axis('off')
  plt.xlim(-2 * d, r * (2 * d) + 4 * d)
  plt.ylim(-1, d)
  print('the figure has been set up')

drawings = [] # will need this later to make an animation of the stages

def draw(configuration):
  global drawings
  r = len(configuration)
  d = max( [ max(rod) if len(rod) > 0 else 0 for rod in rods ] ) + 1
  x = 0
  for rod in configuration:
    h = 0
    ax.axvline(x, color = 'gray', linestyle = '-', lw = 5 * r) # bars for where the rods are 
    for disk in rod[::-1]: # from bottom to top
      s = disk + 1 # the size 0 gets drawn with width 2, the size 1 with width 4 etc
      drawings.append(ax.plot([x - s, x + s], [h, h], color = colors[disk], linestyle = '-', lw = 5 * d)) # draw the disks
      h += 1
    x += 3 * d

counter = 0
track = [ [ r[:] for r in rods ] ]

def move(configuration, target = diskCount - 1, destination = rodCount - 1, store = True):
  global counter
  counter += 1
  source = None
  for r in range(len(configuration)):
    if target in configuration[r]:
      source = r # located the current rod
      break
  top = None
  for disk in configuration[source]:
    if disk == target:
      break
    if disk != target:
      top = disk
  auxiliary = None
  if top is not None: # something is on top of it 
    # we have to move the one on top of it elsewhere
    # it cannot go on the source itself nor on the target rod
    for aux in range(len(configuration)):
      if aux == source or aux == destination:
        continue
      elif len(configuration[aux]) == 0 or rods[aux][0] > target: # any other rod that does not have smaller disks on top works
        auxiliary = aux
        break # done
    if auxiliary is None:
      print('we are unfortunately at an impasse') # this should not happen
      return
    else:
      move(configuration, top, auxiliary)
  assert configuration[source][0] == target # make sure it is now on top 
  configuration[source].pop(0) # remove it
  configuration[destination].insert(0, target) # put it at the top of the target rod
  if store: # take a snapshot after every disk movement
    track.append([ r[:] for r in configuration ])
  assert validate(configuration) # make sure the current configuration is valid
  # put the other one back on it, if there was one there before
  if top is not None:
    move(configuration, top, destination)

def clear():
  # erase old disks, if any (needed when we animate later on)
  global drawings
  for old in drawings:
    bar = old.pop(0)
    bar.remove()
  drawings = []

  
    
move(rods)

import matplotlib.animation as animation
  
def step(t):
  clear() # clean up the old disks
  draw(track[t])

setup()
result = animation.FuncAnimation(fig, step, frames = len(track),
                                 interval = 500, repeat = False)

result.event_source.stop()
result.save('towers.gif')

