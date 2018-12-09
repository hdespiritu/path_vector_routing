# python 2.7
#
# Node:  name, neighbors, and reachable paths
#
# Program can only acommodate 10 nodes (node0, node1, ..., node 9)
#
class Node:
    def __init__(self, name, neighbors):
        self._name = name
        self._neighbors = neighbors
        self._paths = []
        self._liveNeighbors = dict([[n,True] for n in neighbors])

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def neighbors(self):
        return self._neighbors

    @neighbors.setter
    def neighbors(self, value):
        self._neighbors = value

    @property
    def paths(self):
        return self._paths

    @paths.setter
    def paths(self, value):
        self._paths = value
    
    @property
    def liveNeighbors(self):
        return self._liveNeighbors

    ''' Doesn't work for some reason
    @liveNeighbors.setter
    def liveNeighbors(self, value):
        neighbors, liveness = value
        assert len(neighbors) == len(liveness)
        for idx, elem in enumerate( neighbors ):
            self._liveNeighbors[elem] = liveness[ idx ]
    '''


# Initialize reachable paths for each node
def initialization(num_nodes, node, liveNodes):
    node._paths = []
    for y in range(num_nodes):
        s = []
        #check that node is live, if not we don't include a path to itself
        if node.name == y and  liveNodes[y]: #node is a path to itself
            s.append(node.name)
            node.paths.append(s)
        #check that node is live, if not we don't include a path to its neighbors
        elif liveNodes[node.name] and str(y) in node.neighbors:#node is a neighbor
            #check that the neighbor node and neighbor link is live 
            if liveNodes[y] and node.liveNeighbors[ str(y) ]:
                s.append(node.name)
                s.append(y)
                node.paths.append(s)
            else:
                s.append("")
                node.paths.append(s)
        else:
            s.append("")
            node.paths.append(s)


# Update path from a node to its neighbor
def update(node, neighbor, network):
    path_ys = neighbor.paths
    path_ws = node.paths
    origin = []
    for item in neighbor.paths:
        origin.append(item)
    for i in range(len(path_ys)):
        neighbor.paths[i] = best(path_ys[i], path_ws[i], neighbor)

    if neighbor.paths != origin:
        for i in neighbor.neighbors:
            update(neighbor, network[int(i)], network)
    return network


# Find better path to other nodes for a neighbor node
def best(path_y, path_w, neighbor):
    if path_w == ['']:
        return path_y
    else:
        path_new_w = []
        path_new_w.append(neighbor.name)
        for item in path_w:
            path_new_w.append(item)
        if neighbor.name in path_w:
            return path_y
        elif path_y == ['']:
            neighbor._changed = True
            return path_new_w
        elif len(path_new_w) < len(path_y):
            neighbor._changed = True
            return path_new_w
        else:
            return path_y

def print_live_nodes( liveNodes ):
    print  "Live Nodes\n" 
    output_str = ''
    for idx, val in enumerate( liveNodes ):
        output_str += 'Node {}: {}, '.format(idx,val)
    print(output_str)

def modify_node_liveness( liveNodes, fail_or_rec):
    #
    # liveNodes: list of booleans denoting if node at position idx is live
    # fail_or_rec: if 0, then will set specified nodes to fail
    #              if 1, then will set specified nodes to recover
    #
    num_nodes = len(liveNodes)
    modified_nodes = [None]*num_nodes
    for idx in range(num_nodes):
        modified_nodes[idx] = liveNodes[idx]

    x = raw_input("Nodes: ") 
    print "====================================\n"
    nodes = x.strip().split()
    node_ints = []
    for node in nodes:
        n_int = ord( node )
        #if undefined node specified, return False
        if n_int < ord( '0' ) or n_int > ord( str( num_nodes - 1) ):
            print('Invalid Node. Node values must be 0 through {}\n'.format(num_nodes-1))
            return None
        else:
            node_ints.append( int(node) )

    if fail_or_rec == 0: #make nodes fail
        for node in node_ints:

            modified_nodes[node] = False
        

    if fail_or_rec == 1: #make nodes recover
        for node in node_ints:
            modified_nodes[node] = True
    
    #if modification is successful return new Nodes
    return modified_nodes

def modify_link_liveness( network, fail_or_rec ):
    #
    # network: list of Node objects that define the network
    # fail_or_rec: if 0, then will set specified links to fail
    #              if 1, then will set specified links to recover
    #

    x = raw_input("Links: ") 
    print "====================================\n"
    link_pair_strings = x.strip().split()
    link_ints = [] # array of pairs [ [nodex1, nodex2], ..., [nodexk-1, nodexk]]
    for link_pair_str in link_pair_strings:
        link_pair = link_pair_str.split(",")
        n_int1 = ord( link_pair[0] )
        n_int2 = ord( link_pair[1] )
        #if undefined node specified, return False
        cond1 = n_int1 < ord( '0' ) or n_int1 > ord( str( num_nodes - 1) )
        cond2 = n_int2 < ord( '0' ) or n_int2 > ord( str( num_nodes - 1) )
        if cond1 or cond2:
            print('Invalid Node. Node values must be 0 through {}\n'.format(num_nodes-1))
            return False
        else:
            link_ints.append( [int( link_pair[0] ), int( link_pair[1] )] )


    new_link_val = None
    if fail_or_rec == 0: #make nodes fail
        new_link_val = False
    if fail_or_rec == 1: #make nodes recover
        new_link_val = True

    for link in link_ints:

        node1 = link[0]
        node2 = link[1]

        #set link failure/recovery for node1
        tmp = network[ node1 ].liveNeighbors
        tmp[ str(node2) ] = new_link_val
        network[ node1 ].liveNeighbors = tmp

        #set link failure/recovery for node2
        tmp = network[ node2 ].liveNeighbors
        tmp[ str(node1) ] = new_link_val
        network[ node2 ].liveNeighbors = tmp
    
    #if modification is successful return new Nodes
    return True

# Print the network
def print_network(network, liveNodes):
    print('\nlive nodes: {}'.format(liveNodes))
    print("\nThe list of nodes, their neighbors and theirs reachable paths:")
    for node in network:
            print("\nnode name: {}".format(node._name))
            print("node neighbors: {}".format(node._neighbors))
            print("node paths: {}".format(node._paths))
            print("live neighbors: {}".format(node._liveNeighbors))


if __name__ == '__main__':

    num_nodes = None
    networkInit = False
    liveNodes = None

    # user input for graph definition
    while True:
        try:
            if not num_nodes:
                num_nodes = int(input("Number of nodes in network: "))
                break
        except ValueError:
            print("Invalid Number. Specify number of nodes in network: ")
    # exit the program by entering 0
    if num_nodes > 0:

        if (not networkInit):
            network = []  # Create network
            liveNodes = [True]*num_nodes

            # Build the network
            for i in range(num_nodes):
                s = raw_input("Input neighbors of node number {} (separated by spaces): ".format(i)) 
                s_arr = s.strip().split(" ")
                network.append(Node(i, s_arr))  # Add nodes to the network
                initialization(num_nodes, network[i], liveNodes)  # Initializing reachable paths for each node of the network
            # Update paths in the network
            for item in network:
                    for i in item.neighbors:
                        network = update(item, network[int(i)], network)

            networkInit = True
            print("Network Initialized\n\n")
     
        if networkInit:
            while True:
                print "======================================================\n" \
                    "\tInput a command\n" \
                    "======================================================\n" \
                    "\t0 - Exit Program\n" \
                    "\t1 - Print the network\n" \
                    "\t2 - Simulate Node Failure\n" \
                    "\t3 - Simulate Link Failure\n" \
                    "\t4 - Simulate Node Recovery\n" \
                    "\t5 - Simulate Link Recovery\n" \
                    "\t6 - Re-compute Node Paths\n" \
                    "======================================================\n" 
                x = raw_input("Command: ") 
                print "======================================================\n" 
                input_cmd = int( x.strip().split()[0] )

                if input_cmd is 0:   #0 - Exit Program             
                    print("Exiting program")
                    break        
                elif input_cmd is 1:  #1 - Print the network
                    print_network(network, liveNodes)
                    print('\n')
                elif input_cmd is 2:  #2 - Simulate Node Failure
                   
                    print_live_nodes( liveNodes )

                    print "======================================================\n" \
                    "\tSpecify nodes to fail (separated by spaces)\n" \
                    "======================================================\n" \
                
                    new_live_nodes = modify_node_liveness( liveNodes, 0)
                    
                    if new_live_nodes:
                        liveNodes = new_live_nodes
                        print_live_nodes( liveNodes )


                elif input_cmd is 3: #3 - Simulate Link Failure
                    
                    print_network( network, liveNodes )

                    print "======================================================\n" \
                    "\tSpecify links to fail (node comma pairs separated by spaces)\n\t eg 1,2 2,0\n" \
                    "======================================================\n" \
                
                    new_network = modify_link_liveness( network, 0)
                    
                    if new_network:
                        print_network( network, liveNodes )
                    
                elif input_cmd is 4: #4 - Simulate Node Recovery

                    print_live_nodes( liveNodes )

                    print "======================================================\n" \
                    "\tSpecify nodes to recover (separated by spaces)\n" \
                    "======================================================\n" \
                
                    new_live_nodes = modify_node_liveness( liveNodes, 1)
                    

                    if new_live_nodes:
                        liveNodes = new_live_nodes
                        print_live_nodes( liveNodes )

                elif input_cmd is 5: #5 - Simulate Link Recovery
                    
                    print_network( network, liveNodes )

                    print "======================================================\n" \
                    "\tSpecify links to recover (node comma pairs separated by spaces)\n\t eg 1,2 2,0\n" \
                    "======================================================\n" \
                
                    new_network = modify_link_liveness( network, 1)
                    
                    if new_network:
                        print_network( network, liveNodes )

                elif input_cmd is 6: #6 - Re-compute node paths
                    
                    
                    num_nodes = len( network )
                    # Initialization checks if node and its links are reachable???
                    for i in range( num_nodes ):
                        initialization(num_nodes, network[i], liveNodes)  # Initializing reachable paths for each node of the network

                    #DEBUGGING
                    continue 
                        
                    # Update paths in the network
                    for item in network:
                            for i in item.neighbors:
                                network = update(item, network[int(i)], network)
    else:
        print("Exiting program")
        pass  