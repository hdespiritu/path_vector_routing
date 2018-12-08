# python 2.7
#
# Node:  name, neighbors, and reachable paths
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

    @liveNeighbors.setter
    def liveNeighbors(self, value):
        neighbors, liveness = value
        assert len(neighbors) == len(liveness)
        for idx, elem in enumerate( neighbors ):
            self._liveNeighbors[elem] = liveness[ idx ]



# Initialize reachable paths for each node
def initialization(num_nodes, node):
    for y in range(num_nodes):
        s = []
        if node.name == y:
            s.append(node.name)
            node.paths.append(s)
        elif str(y) in node.neighbors:
            s.append(node.name)
            s.append(y)
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
            # Build the network
            for i in range(num_nodes):
                s = raw_input("Input neighbors of node number {} (separated by spaces): ".format(i)) 
                s_arr = s.strip().split(" ")
                network.append(Node(i, s_arr))  # Add nodes to the network
                initialization(num_nodes, network[i])  # Initializing reachable paths for each node of the network
            # Update paths in the network
            for item in network:
                    for i in item.neighbors:
                        network = update(item, network[int(i)], network)

            networkInit = True
            liveNodes = [True]*num_nodes
            print("Network Initialized\n\n")
     
        if networkInit:
            while True:
                print "====================================\n" \
                    "\tInput a command\n" \
                    "====================================\n" \
                    "\t0 - Exit Program\n" \
                    "\t1 - Print the network\n" \
                    "\t2 - Simulate Node Failure\n" \
                    "\t3 - Simulate Link Failure\n" \
                    "\t4 - Simulate Node Recovery\n" \
                    "\t5 - Simulate Link Recovery\n" \
                    "====================================\n" 
                x = raw_input("Command: ") 
                print "====================================\n" 
                input_cmd = int( x.strip().split()[0] )

                if input_cmd is 0:                    
                    print("Exiting program")
                    break        
                elif input_cmd is 1:
                    print_network(network, liveNodes)
                    print('\n')
                elif input_cmd is 2:
                    #TODO:
                    print('\nTODO: implement nodefail\n') 
                elif input_cmd is 3:
                    #TODO:
                    print('\nTODO: implement linkfail\n') 
                elif input_cmd is 4:
                    #TODO:
                    print('\nTODO: implement noderecovery\n') 
                elif input_cmd is 5:
                    #TODO:
                    print('\nTODO: implement linkrecovery\n') 

    else:
        print("Exiting program")
        pass  