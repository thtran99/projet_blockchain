import math
import hashlib
import json


class Node:
    def __init__(self, value: str, left_child=None, right_child=None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child


def compute_tree_depth(number_of_leaves: int) -> int:
    return math.ceil(math.log2(number_of_leaves))


def is_power_of_2(number_of_leaves: int) -> bool:
    return math.log2(number_of_leaves).is_integer()


def fill_set(list_of_nodes: list):
    current_number_of_leaves = len(list_of_nodes)
    if is_power_of_2(current_number_of_leaves):
        return list_of_nodes
    total_number_of_leaves = 2**compute_tree_depth(current_number_of_leaves)
    if current_number_of_leaves % 2 == 0:
        for i in range(current_number_of_leaves, total_number_of_leaves, 2):
            list_of_nodes = list_of_nodes + [list_of_nodes[-2], list_of_nodes[-1]]
    else:
        for i in range(current_number_of_leaves, total_number_of_leaves):
            list_of_nodes.append(list_of_nodes[-1])
    return list_of_nodes


def hash(block):
        # hashes a block
        # also make sure that the transactions are ordered otherwise we will have insonsistent hashes!
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

def build_merkle_tree(node_data):
    complete_set = fill_set(node_data)
    old_set_of_nodes = [Node((data)) for data in complete_set]
    tree_depth = compute_tree_depth(len(old_set_of_nodes))

    for i in range(0, tree_depth):
        num_nodes = 2**(tree_depth-i)
        new_set_of_nodes = []
        for j in range(0, num_nodes, 2):
            child_node_0 = old_set_of_nodes[j]
            child_node_1 = old_set_of_nodes[j+1]
            new_node = Node(
                
                value=(f"{child_node_0.value}{child_node_1.value}"),
                left_child=child_node_0,
                right_child=child_node_1
            )
            new_set_of_nodes.append(new_node)
        old_set_of_nodes = new_set_of_nodes
    return new_set_of_nodes[0]


""" 

class MerkleRoot:

    def __init__(self, hash_list):
        self.hash_list = hash_list
        racine = Node(hash_list, father = None, isRightNode = False)
        self.init_merkle_rec(racine)
        self.root = racine

    def init_merkle_rec(self, current_node):

        if current_node == None:
            return

        hash_current_node = current_node.get_value()
        len_hash = len(hash_current_node)

        if len_hash % 2 == 1 :
            stop_index = (len_hash // 2) + 1
        else :
            stop_index = len_hash // 2

        if len_hash > 1:
            current_node.init_sons(hash_current_node[:stop_index], hash_current_node[stop_index:])

            self.init_merkle_rec(current_node.left_node())
            self.init_merkle_rec(current_node.right_node())

    def show_tree(self):
        self.show_tree_rec(self.root)

    def show_tree_rec(self, node):
        if node != None:
            print(node.get_value())
            self.show_tree_rec(node.left_node())
            self.show_tree_rec(node.right_node())


class Node:

    def __init__(self, value, father, isRightNode):
        self.value = value
        self.father = father 
        self.isRightNode = isRightNode
        self.left = None
        self.right = None

    def init_sons(self, left_value, right_value):
        self.left = Node(value = left_value, father = self, isRightNode = False)
        if len(right_value) > 0:
            self.right = Node(value = right_value, father = self, isRightNode = True)

    def get_value(self):
        return self.value

    def left_node(self):
        return self.left

    def right_node(self):
        return self.right


def get_path(node, k):
    if node.value == k:
        return [node.value]
    res = get_path(node.left_node(), k)
    if res:
        return [node.value] + res
    res = get_path(node.right_node(), k)
    if res:
        return [node.value] + res
    return []

mk = MerkleRoot([0,1,2,3,4,5])
mk.show_tree() """


