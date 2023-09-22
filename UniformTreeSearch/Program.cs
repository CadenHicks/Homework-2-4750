using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace Homework2
{
    public class Node
    {
        public Position State { get; set; }

        public decimal Cost { get; set; }

        public bool Dirty { get; set; }

        public Node Parent { get; set; }

        public string Action { get; set; } = string.Empty;

        public Node(Position state, decimal cost, bool dirty, Node parent, string action)
        {
            State = state;
            Cost = cost;
            Dirty = dirty;
            Parent = parent;
            Action = action;
        }

        public Node()
        {

        }
    }

    public class Position
    {
        public int row { get; set; }

        public int col { get; set; }
    }

    public static class Actions
    {
        public static string[] actions = { "Left", "Right", "Up", "Down", "Suck" };
    }

    public class UniformCostTreeSearch
    {
        public List<Position>? dirt; //list of dirty rooms

        public int Generated = 0;

        public int Expanded = 0;

        public decimal Search(Position initalState, List<Position> dirtyRooms)
        {
            dirt = dirtyRooms; //setting golbal variable

            Node startNode = new Node(initalState, 0, false, null, string.Empty); //inserting inital state

            PriorityQueue<Node, decimal> fringe = new PriorityQueue<Node, decimal>(); //creates a min priority queue

            fringe.Enqueue(startNode, startNode.Cost); //queues the inital state

            int i = 0;

            while (fringe.Count > 0) //runs until fringe is empty
            {
                Node curr = fringe.Dequeue(); //gets node at front of queue

                if(i < 6)
                {
                    Console.WriteLine("(" + curr.State.row + "," + curr.State.col + ")");
                }

                Expanded++;

                if(curr.Action.ToLower() == "suck" && curr.Dirty == true) //if the action is suck and the room is dirty then we have cleaned one room
                {
                    curr.Dirty = false;

                    RemoveDirt(curr.State); //removes it from the list of dirty rooms

                    Console.WriteLine("A dirty room has been cleaned with state: ({0},{1})", curr.State.row, curr.State.col);

                    Generated += fringe.Count;

                    fringe.Clear();//clears the fringe to now start looking for the next goal node
                }

                if (dirt.Count == 0) //returns path cost of final goal node
                {
                    Console.WriteLine("Generated: {0}", Generated);
                    Console.WriteLine("Expanded: {0}", Expanded);
                    return curr.Cost;
                }

                var childNodes = Expand(curr); //gets all the child nodes of the current node

                foreach (var node in childNodes) //puts each childnode in the queue
                {
                    fringe.Enqueue(node, node.Cost);
                }

                i++;
            }

            return 0;//return zero on failure
        }

        private List<Node> Expand(Node node)
        {
            List<Node> successors = new List<Node>(); //list for successor nodes

            for (int i = 0; i < 5; i++)//loop generates the 5 child nodes which represent the 5 actions
            {
                if (Actions.actions[i].ToLower() == "left") //if action is left
                {
                    Position stateNew = new Position();

                    stateNew.col = node.State.col;//sets state
                    stateNew.row = node.State.row;

                    if (stateNew.col - 1 != 0)//then moves the col number down by one since we move left unless it is at boundary
                    {
                        stateNew.col -= 1;
                    }

                    bool isDirty = false;

                    if (InList(stateNew))//checks to see if the room is dirty
                    {
                        isDirty = true;
                    }

                    var n = new Node(stateNew, node.Cost + 1m, isDirty, node, "left"); //creates the new node with the parameters

                    successors.Add(n); //adds to the list
                }
                else if (Actions.actions[i].ToLower() == "right")
                {
                    Position stateNew = new Position();

                    stateNew.col = node.State.col;//sets state
                    stateNew.row = node.State.row;

                    if (stateNew.col + 1 <= 5) //changes state one to the right if not at boundary
                    {
                        stateNew.col += 1;
                    }

                    bool isDirty = false;

                    if (InList(stateNew))//checks if new state is dirty
                    {
                        isDirty = true;
                    }

                    var n = new Node(stateNew, node.Cost + 0.9m, isDirty, node, "right");//creates the node

                    successors.Add(n);//adds it to the list
                }
                else if (Actions.actions[i].ToLower() == "up")
                {
                    Position stateNew = new Position();

                    stateNew.col = node.State.col;//sets state
                    stateNew.row = node.State.row;

                    if (stateNew.row - 1 != 0)//moves state up one row unless at boundary
                    {
                        stateNew.row -= 1;
                    }

                    bool isDirty = false;

                    if (InList(stateNew))//checks if new state is dirty
                    {
                        isDirty = true;
                    }

                    var n = new Node(stateNew, node.Cost + .8m, isDirty, node, "up");//creates node

                    successors.Add(n);//adds to list
                }
                else if (Actions.actions[i].ToLower() == "down")
                {
                    Position stateNew = new Position();

                    stateNew.col = node.State.col; //sets state
                    stateNew.row = node.State.row;

                    if (stateNew.row + 1 <= 5)//sets state to down a row unless at boundary
                    {
                        stateNew.row += 1;
                    }

                    bool isDirty = false;

                    if (InList(stateNew))//checks if new state is dirty
                    {
                        isDirty = true;
                    }

                    var n = new Node(stateNew, node.Cost + .7m, isDirty, node, "down");//creates node

                    successors.Add(n);//adds it to list
                }
                else if (Actions.actions[i].ToLower() == "suck")
                {
                    var n = new Node(node.State, node.Cost + .6m, node.Dirty, node, "suck");//creates new node because state doesn't change

                    successors.Add(n);//adds it to list
                }
            }

            return successors;
        }

        private bool InList(Position position)
        {
            for(int i =0; i<dirt.Count();i++)
            {
                if (dirt[i].row == position.row && dirt[i].col == position.col) return true; //retyrns true if row && col in the dirty list
            }

            return false;
        }

        private void RemoveDirt(Position position)
        {
            for(int i = 0; i < dirt.Count();i++)
            {
                if (dirt[i].row == position.row && dirt[i].col == position.col) 
                {
                    dirt.RemoveAt(i);//removes room from list at specified row and col
                }
            }
        }
    }

    public class Program
    {
        static void Main(string[] args)
        {
            UniformCostTreeSearch search = new UniformCostTreeSearch(); //new instance of the search class

            Position initalState = new Position { col = 2, row = 2 }; //sets inital state for instance 1

            List<Position> dirtyRooms = new List<Position> //sets dirty room list for instance 1
            {
                new Position { row = 1,col = 2},
                new Position { row = 2, col = 4},
                new Position { row = 3, col = 5},
            };

            var watch = new System.Diagnostics.Stopwatch();

            watch.Start();

            var totalCost = search.Search(initalState, dirtyRooms); //Searching Instance 1

            watch.Stop();

            Console.WriteLine("The total Path Cost for Instance 1 was: {0}", totalCost); //print cost of instance 1
            Console.WriteLine("The time taken: {0} miliseconds", watch.ElapsedMilliseconds);

            initalState.row = 3; //change inital state for instance 2
            initalState.col = 2;

            dirtyRooms.Clear();

            dirtyRooms.Add(new Position { row = 1, col = 2 }); //set dirty rooms for instance 2
            dirtyRooms.Add(new Position { row = 2, col = 1 });
            dirtyRooms.Add(new Position { row = 2, col = 4 });
            dirtyRooms.Add(new Position { row = 3, col = 3 });

            watch.Restart();

            var totalCost2 = search.Search(initalState, dirtyRooms); //Searching Instance 2

            watch.Stop();

            Console.WriteLine("The total Path Cost for Instance 2 was: {0}", totalCost2); // print cost of instance 2
            Console.WriteLine("The time taken: {0} miliseconds", watch.ElapsedMilliseconds);

        }
    }
}
