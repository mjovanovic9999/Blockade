def h_calculate(src,dst):
    return abs(src[0]-dst[0])+abs(src[1]-dst[1])

def get_children(node):
    return list(filter(
        lambda x: not(x[0]<0 or x[0]>5 or x[1]<0 or x[1]>5 
        ),
    ((node[0]-1,node[1]),(node[0],node[1]-1),(node[0]+1,node[1]),(node[0],node[1]+1)) ) )

def find_best_path(start:tuple[int,int],end:tuple[int,int],dimensions:tuple[int,int])->list[tuple[int,int]]:
    if start[0]<0 or start[0]>5 or end[0]<0 or end[0]>5 or start[1]<0 or start[1]>5 or end[1]<0 or end[1]>5:
        return "Losi parametri"
    if start[0]==end[0] and start[1]==end[1]:
        return []

    found_end = False        
    open_set = set([start])  
    closed_set = set() 
    g = {}                   
    prev_nodes = {}          
    g[start] = 0          
    prev_nodes[start] = None 
    while len(open_set) > 0 and (not found_end): 
        node = None 
        for next_node in open_set: 
            if node is None or g[next_node] + h_calculate(next_node,end) < g[node] + h_calculate(node,end): 
                node = next_node
        if node == end: 
            found_end = True 
            break
        # print(node,end="")
        for m in get_children(node): 
            cost=1
            if m not in open_set and  m not in closed_set: 
                open_set.add(m) 
                prev_nodes[m] = node 
                g[m] = g[node] + cost 
            elif m not in closed_set and g[m] > g[node] + cost: 
                g[m] = g[node] + cost 
                prev_nodes[m] = node 
        open_set.remove(node) 
        closed_set.add(node)
    path = [] 
    if found_end: 
        prev = end 
        while prev_nodes[prev] is not None: 
            path.append(prev) 
            prev = prev_nodes[prev] 
        path.append(start) 
        path.reverse()       
    return path
    

print(find_best_path((2,2),(0,5)))
print('\n')

for i in range(0,6):
    for j in range(0,6):
        print("("+str(i)+","+str(j)+")", end=" ")
    print('\n')
