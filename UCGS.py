import numpy as np
from copy import deepcopy
import time

# 0 clean
# 1 dirty
class State:

    def __init__(self, state_space, agent_loc = np.array([0,0])):
        self.state_space = deepcopy(state_space)
        self.agent_loc = deepcopy(agent_loc)

    def __eq__(self, other):
        return np.array_equal(self.state_space, other.state_space) and np.array_equal(self.agent_loc, other.agent_loc)
    
    def __hash__(self):
        return hash((str(self.state_space), str(self.agent_loc)))

    def set_agent_loc(self, agent_loc):
        self.agent_loc = agent_loc
    

class Node:

    def __init__(self, parent, move):
        if (parent != None):
            self.parent = parent
            # Initialize state to parent's state (before applying move)
            self.state = State(deepcopy(parent.state.state_space))
            self.state.agent_loc = deepcopy(parent.state.agent_loc)
            # Initialize cost to parent's (before applying move)
            self.total_cost = parent.total_cost
            self.move_cost = 0
            self.move = move

        # Initialize children as an empty list
        self.children = []

        # Apply move to parent's state space/total cost

        # Left move
        if (move == "Left"):
            self.state.agent_loc += np.array([0, -1])
            self.total_cost += 1.0
            self.move_cost = 1.0
        # Right move
        elif (move == "Right"):
            self.state.agent_loc += np.array([0, 1])
            self.total_cost += 0.9
            self.move_cost = 0.9
        # Up move
        elif (move == "Up"):
            self.state.agent_loc += np.array([-1, 0]) 
            self.total_cost += 0.8
            self.move_cost = 0.8
        # Down move
        elif (move == "Down"):
            self.state.agent_loc += np.array([1, 0])
            self.total_cost += 0.7
            self.move_cost = 0.7
        # Suck move
        elif (move == "Suck"):
            if (self.state.state_space[tuple(self.state.agent_loc)] == 1):
                self.state.state_space[tuple(self.state.agent_loc)] = 0
            self.total_cost += 0.6
            self.move_cost = 0.6

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    # Creates all possible children from a node
    def Expand(self):
        # Left
        if (self.state.agent_loc[1] != 0):
            self.children.append(Node(self, "Left"))
        # Right
        if (self.state.agent_loc[1] != 4):
            self.children.append(Node(self, "Right"))
        # Up
        if (self.state.agent_loc[0] != 0):
            self.children.append(Node(self, "Up"))
        # Down
        if (self.state.agent_loc[0] != 3):
            self.children.append(Node(self, "Down"))
        # Suck
        self.children.append(Node(self, "Suck"))

# If the entire state space is 0 (clean), return True
def Goal_Test(node):
    if (np.all(node.state.state_space == 0)):
        return True
    else:
        return False

import heapq

def UCGS(state_space, agent_loc):
    closed = set()
    fringe = []  # Now an empty list, but will be used as a heap
    total_nodes_generated = 0

    # Create initial node
    initial_node = Node(None, None)
    initial_node.state = State(state_space, agent_loc)
    initial_node.total_cost = 0
    initial_node.move_cost = 0

    heapq.heappush(fringe, initial_node)  # Insert into heap
    total_nodes_generated += 1

    total_nodes_expanded = 0
    first_five_expand = []

    while True:
        if len(fringe) == 0:
            return None

        node = heapq.heappop(fringe)  # Pop node with lowest move_cost

        if Goal_Test(node):
            print(f"\nTotal Nodes Generated: {total_nodes_generated}")
            print(f"Total Nodes Expanded: {total_nodes_expanded}")
            for i in range(len(first_five_expand)):
                print(f"Node {i + 1}:")
                print(f"{first_five_expand[i].state.state_space}")
                print(f"{first_five_expand[i].state.agent_loc}")
            return node 

        # Add to closed set
        closed.add(node.state)
        
        # Expand node
        node.Expand()
        total_nodes_expanded += 1
        if (total_nodes_expanded <= 5):
            first_five_expand.append(node)

        # Add children to fringe
        for child in node.children:
            if child.state not in closed:
                heapq.heappush(fringe, child)
                total_nodes_generated += 1

def print_path(node):
    if (node.total_cost == 0):
        return
    else:
        print(node.move)
        print_path(node.parent)


def main():
    # Test 1
    print("---------------- Test 1 ----------------")

    state_space = np.zeros((4,5))
    state_space[0][1] = 1
    state_space[1][3] = 1
    state_space[2][4] = 1

    agent_loc = np.array([1,1])

    start_time = time.time()

    goal_node = UCGS(state_space, agent_loc)

    end_time = time.time()

    print(f"Execution time: {end_time - start_time} seconds")

    print(f"\nSolution cost: {goal_node.total_cost}")

    print("\nSolution Sequence (Last move on top)")
    print_path(goal_node)

    # Test 2
    print("---------------- Test 2 ----------------")

    state_space = np.zeros((4,5))
    state_space[0][1] = 1
    state_space[1][0] = 1
    state_space[1][3] = 1
    state_space[2][2] = 1

    agent_loc = np.array([2,1])

    start_time = time.time()

    goal_node = UCGS(state_space, agent_loc)

    end_time = time.time()

    print(f"Execution time: {end_time - start_time} seconds")

    print(f"\nSolution cost: {goal_node.total_cost}")

    print("\nSolution Sequence (Last move on top)")
    print_path(goal_node)


main()

        

