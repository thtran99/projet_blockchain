

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

mk = MerkleRoot([0,1,2,3,4])
mk.show_tree()