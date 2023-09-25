import time


class Node:
    def __init__(self, state, dirt, parent=None, action=None, depth=0, cost=0):
        self.state = state
        self.dirt = dirt
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost

# ITDS on the vacuum cleaner world problem in HW2
def iterative_deepening_tree_search(problem):
    depth_limit = 0
    num_expanded = 0
    num_generated = 0
    first_five_exp = []
    while True: # iteratively increase the depth and search the tree until solution - IDTS
        fringe = [Node(problem.initial_state, problem.dirt_locations)]  # starting node
        while fringe:
            # sort the fringe largest to smallest by the sum of the x and y coordinates
            fringe.sort(key=lambda node: (node.state[0] + node.state[1], -node.state[1]), reverse=True)
            # then, sort by depth to maintain IDTS
            fringe.sort(key=lambda node: node.depth)
            node = fringe.pop()
            num_expanded += 1
            if num_expanded <= 5: # save the first 5 nodes expanded to print later
                first_five_exp.append(node)
            if problem.goal_test(node):
                return node, num_expanded, num_generated, first_five_exp  # solution found
            if node.depth < depth_limit:
                # all possible children are added at the next depth
                for action in problem.actions(node.state, node.dirt):
                    child_state, child_dirt = problem.result(node.state, node.dirt, action)
                    child_node = Node(child_state, child_dirt, node, action, node.depth + 1, 
                                      problem.path_cost(node.cost, node.state, action, child_state))
                    fringe.append(child_node)
                    num_generated += 1
        depth_limit += 1

# print function for solution path and CPU execution time
def print_results(problem, solution_node, expanded, generated, first_five_nodes, start_time, end_time, p_num):
    if solution_node is not None:
        total_cost = solution_node.cost
        solution_path = []
        while solution_node.parent is not None:
            solution_path.append(solution_node)
            solution_node = solution_node.parent
        solution_path.reverse()

        # Print the solution path
        print("\nSOLUTION PATH FOR INSTANCE #{}:".format(p_num))
        for node in solution_path:
            print(f"Action: {node.action}, Resulting State: {node.state}")
    else:
        print("\nNo solution found for Instance #{}.".format(p_num))
    print(f"\nCPU execution time: {round((end_time - start_time), 6)} seconds")
    print(f"Total number of moves: {len(solution_path)}")
    print(f"Total cost of solution path: {round(total_cost, 3)}")
    print(f"Total number of nodes expanded: {expanded}")
    print(f"Total number of nodes generated: {generated}")
    print(f"\nFirst 5 nodes expanded:")
    for node in first_five_nodes:
        print(f"Node Depth: {node.depth}, State: {node.state}")
        
class VacuumWorldProblem:
    def __init__(self, initial_state, dirt_locations):
        self.initial_state = initial_state
        self.dirt_locations = dirt_locations

    # return the new state and dirt locations after an action is taken
    def result(self, state, dirt_locs, action):
        x, y = state[0], state[1]
        if state in dirt_locs: # room is dirty
            new_state = state
            new_dirt = [dirt for dirt in dirt_locs if dirt != state]
            return new_state, new_dirt
        elif action == 'Left':
            new_x, new_y = x , y - 1
        elif action == 'Right':
            new_x, new_y = x, y + 1
        elif action == 'Up':
            new_x, new_y = x - 1, y
        elif action == 'Down':
            new_x, new_y = x + 1, y

        new_state = (new_x, new_y)

        return new_state, dirt_locs

    # check if the a room move is valid in our world
    def is_valid(self, x, y):
        return 1 <= x <= 4 and 1 <= y <= 5

    # defines actions for the vacuum cleaner given its current state
    def actions(self, state, dirt_locs):
        actions = []
        x, y = state[0], state[1]
        if state in dirt_locs:
            actions.append(('Suck', (x, y)))
        if self.is_valid(x, y - 1):
            actions.append(('Left', (x, y - 1)))
        if self.is_valid(x, y + 1):
            actions.append(('Right', (x, y + 1)))
        if self.is_valid(x - 1, y):
            actions.append(('Up', (x - 1, y)))
        if self.is_valid(x + 1, y):
            actions.append(('Down', (x + 1, y)))
        actions.sort(key=lambda a: (a[0] != 'Suck', a[1][0], a[1][1]), reverse=True)
        return [a[0] for a in actions]

    # return true if the node has seen all dirty rooms cleaned
    def goal_test(self, node):
        return node.dirt == []
    
    # keep track of the cost of each action
    def path_cost(self, cost_so_far, state_1, action, state_2):
        if action == 'Left':
            return cost_so_far + 1.0
        elif action == 'Right':
            return cost_so_far + 0.9
        elif action == 'Up':
            return cost_so_far + 0.8
        elif action == 'Down':
            return cost_so_far + 0.7
        elif action == 'Suck':
            return cost_so_far + 0.6

# main function - solve both instances of the vacuum cleaner world problem
def main():
    # instance 1 - setup world, run search, print required output info
    initial_state_1 = (2, 2)
    dirt_locations_1 = [(1, 2), (2, 4), (3, 5)]
    problem_1 = VacuumWorldProblem(initial_state_1, dirt_locations_1)
    start_time_1 = time.process_time()
    solution_node_1, expanded_total_1, generated_total_1, first_five_1 = iterative_deepening_tree_search(problem_1)
    end_time_1 = time.process_time()
    print_results(problem_1, solution_node_1, expanded_total_1, generated_total_1, first_five_1, start_time_1, end_time_1, 1)

    # same for instance 2
    initial_state_2 = (3, 2)
    dirt_locations_2 = [(1, 2), (2, 1), (2, 4), (3,3)] 
    problem_2 = VacuumWorldProblem(initial_state_2, dirt_locations_2)
    start_time_2 = time.process_time()
    solution_node_2, expanded_total_2, generated_total_2, first_five_2 = iterative_deepening_tree_search(problem_2)
    end_time_2 = time.process_time()
    print_results(problem_2, solution_node_2, expanded_total_2, generated_total_2, first_five_2, start_time_2, end_time_2, 2)

if __name__ == "__main__":
    main()