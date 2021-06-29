with open("vuln.c") as f:
  data = f.read().strip().split("\n")

  i = 0
  while i < len(data):
    if "int sub_" in data[i]:
      fn = data[i].split("int ")[1].split("()")[0]
    elif "char s[" in data[i]:
      sz = data[i].split("char s[")[1].split("]")[0]
      sz = int(sz)

      #print("loaded %d" % sz)
    elif "fgets(s, " in data[i]:
      rsz = data[i].split("fgets(s, ")[1].split(",")[0]
      rsz = int(rsz)
      if rsz > sz:
        print(i, rsz, sz)
        print("in %s" % fn)

        win_fn = fn
    i += 1

  adj = {}
  cnts = {}

  def valid_fn(name):
    for i in ["sub_814C6CA", "sub_80486B1", "sub_814C6D0"]:
      if i in name:
        return False

    return True

  i = 0
  while i < len(data):
    if "int sub_" in data[i]:
      fn = data[i].split("int ")[1].split("()")[0]

      adj[fn] = list()
      cnts[fn] = list()
    elif "int __cdecl main()" in data[i]:
      fn = "main"

      adj[fn] = list()
      cnts[fn] = list()
    elif "return result" in data[i]:
      fn = None
    elif "sub_" in data[i] and valid_fn(data[i]):
      curr = data[i]
      if "result = " in curr:
        curr = curr.split("result = ")[1]
      curr = curr.strip().split("()")[0]
      if fn != None:
        adj[fn].append(curr)
    elif "result != " in data[i]:
      curr = data[i]
      curr = curr.split("result != ")[1].split(" ")[0]
      curr = int(curr)

      if fn != None:
        cnts[fn].append(curr)


    i += 1

  #for i in adj["main"]:
    #print(i)

  print("searching for %s" % win_fn)

  stack = []
  v = set()
  def bfs(node):
    global stack

    if node == win_fn:
      stack = [node] + stack
      return True

    if node not in v:
      v.add(node)

      for i in adj[node]:
        if bfs(i):
          stack = [node] + stack
          return True

    return False

  bfs("main")

  print(stack)

  goal_nums = []

  for i in adj["main"]:
    if i == stack[1]:
      break

    goal_nums.append(cnts[i][0])
  
  i = 1
  while stack[i] != "sub_8109F08":
    j = 0
    while adj[stack[i]][j] != stack[i+1]:
      goal_nums.append(0)

      nxt_arr = cnts[adj[stack[i]][j]]

      if len(nxt_arr) == 0:
        goal_nums.append(-1)
      else:
        goal_nums.append(cnts[adj[stack[i]][j]][0])
      j += 1
    goal_nums.append(0)

    i += 1

  print(goal_nums)
