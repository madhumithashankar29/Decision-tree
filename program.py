from __future__ import print_function, division
import numpy as np
import csv, math, random, sys, random


def pure_counts(rows):
    pure_count = {}
    pure_count['1'] = 0
    pure_count['0'] = 0
    for row in rows:
        r = row[len(row) - 1]
        pure_count[r] += 1
    return pure_count


def divide_set(rows, column):
    set0 = []
    set1 = []
    for row in rows:
        if (row[column] == '0'):
            set0 = set0 + [row]
        else:
            set1 = set1 + [row]
    return (set0, set1)


def entropy(rows):
    from math import log
    result = pure_counts(rows)
    entropy = 0.0
    for r in result.keys():
        if (len(rows) == 0):
            i = 0.0
        else:
            i = float(result[r]) / float(len(rows))
        if (i == 0):
            entropy = 0.0
        else:
            entropy = entropy - i * log(i, 2)
    return entropy


def Nodes_Total(tree):
    count = 1
    if (tree is None):
        return 0
    if (tree is not None):
        count = count + Nodes_Total(tree.rightchild)
        count = count + Nodes_Total(tree.leftchild)
    return count


def tree_number(tree, count):
    if (tree is None):
        return count
    if (tree.pure is not None):
        tree.keep = 0
        return count
    if (tree is not None):
        count = count + 1;
        tree.keep = count
        count = tree_number(tree.rightchild, count)
        count = tree_number(tree.leftchild, count)
    return count


def count_leaf(tree, count):
    if (tree is None):
        return 0
    if (tree.pure is not None):
        return 1
    else:
        count = count + count_leaf(tree.leftchild, count) + count_leaf(tree.rightchild, count)
        return count


def tree_depth(tree):
    depth_1 = 0
    depth_2 = 0
    if (tree is None):
        return 0
    else:
        depth_1 = 1 + tree_depth(tree.rightchild)
        depth_2 = 1 + tree_depth(tree.leftchild)
        if (depth_1 > depth_2):
            return depth_1
        else:
            return depth_2


def tree_print(tree, bar=''):
    if tree.pure != None:
        if (tree.pure['0'] > tree.pure['1']):
            print(0)
        else:
            print(1)
    else:

        print('\n' + bar, str(tree.col) + ' = ' + str(1), end=": ")
        tree_print(tree.rightchild, bar + '| ')
        if (tree.value == 1):
            val = 0
        else:
            val = 1
        print(bar, str(tree.col) + '=' + str(0), end=": ")
        tree_print(tree.leftchild, bar + '| ')


def classification(newinput, tree):
    if tree.pure != None:

        return tree.pure
    else:
        v = newinput[tree.number]
        branch = None
        if v == '1':
            branch = tree.rightchild
        else:
            branch = tree.leftchild
    return classification(newinput, branch)


def tree_accuracy(data, tree):
    count = 0
    temp = -1
    for row in data:
        temp = temp + 1
        if (classification(row, tree)['1'] >= classification(row, tree)['0']):
            if (row[-1] == '1'):
                count = count + 1
        else:
            if row[-1] == '0':
                count = count + 1

    accuracy = count / len(data)
    return accuracy


def tree_findnode(tree, keep):
    node = None
    if (tree is None):
        return None
    elif (tree.keep == keep):
        return tree

    if (tree is not None):
        node = tree_findnode(tree.rightchild, keep)
        if (node is None):
            node = tree_findnode(tree.leftchild, keep)
    return node


def tree_finddepth(tree, number, tree_depth):
    if (tree is None):
        return 0
    elif (tree.keep == number):
        return tree_depth

    treelevel = tree_finddepth(tree.leftchild, number, tree_depth + 1);
    if (treelevel != 0):
        return treelevel
    treelevel = tree_finddepth(tree.rightchild, number, tree_depth + 1);
    return treelevel

def tree_findparent(tree):
    if (tree is None):
        return None
    elif (tree.parent is not None):
        return tree_findparent(tree.parent)
    else:
        return tree


def Information_Gain(rows, columncount):
    entropy_old = entropy(rows)
    max_info = 0.0
    Info = 0.0
    flag = 0
    for i in range(0, columncount):
        set0, set1 = divide_set(rows, i)
        if (len(set0) > 0 and len(set1) > 0):
            rowslength = len(rows)
            p = float(len(set0)) / float(len(rows))
            Info = entropy_old - (p * entropy(set0) + (1 - p) * entropy(set1))

            if (Info > max_info):
                max_info = Info
                attribute = i
                flag = 1
    if (flag == 1):

        return attribute
    else:
        return -2


def Variance_Impurity(rows, columncount):
    Vimp = float(pure_counts(rows)['0'] * pure_counts(rows)['1'] / len(rows))
    gain_max = 0.0
    flag = 0
    for i in range(0, columncount):
        set0, set1 = divide_set(rows, i)
        if (len(set0) > 0 and len(set1) > 0):
            rowslength = len(rows)
            pr0 = float(len(set0)) / float(len(rows))
            pr1 = (1 - pr0)
            Vimp0 = (pure_counts(set0)['0'] * pure_counts(set0)['1']) / len(set0) ** 2
            Vimp1 = (pure_counts(set1)['0'] * pure_counts(set1)['1']) / len(set1) ** 2
            vi_gain = Vimp - float((pr0 * Vimp0) + (pr1 * Vimp1))
            if (vi_gain > gain_max):
                gain_max = vi_gain
                attribute = i
                flag = 1
    if (flag == 1):

        return attribute
    else:
        return -2


class Decision_Node:
    def __init__(self, col=-1, pure=None, value=None, leftchild=None, rightchild=None, number=None, name=None,
                 count=None, keep=None, noof0=0, noof1=0, parent=None):
        self.pure = pure
        self.value = value
        self.leftchild = leftchild
        self.rightchild = rightchild
        self.number = number
        self.name = name
        self.keep = keep
        self.col = col
        self.noof1 = noof1
        self.noof0 = noof0
        self.parent = parent


def tree_build(rows, attributelength, val):
    global keep
    global leafcount
    if len(rows) == 0:
        keep = keep + 1
        return Decision_Node()
    Index = Information_Gain(rows, attributelength)
    if (Index == -2):
        if (pure_counts(rows)['0'] > pure_counts(rows)['1']):
            value = 0
            keep = keep + 1
            leafcount = leafcount + 1
            return Decision_Node(pure=pure_counts(rows), value=value, keep=keep, noof0=pure_counts(rows)['0'])
        else:
            value = 1
            keep = keep + 1
            leafcount = leafcount + 1
            return Decision_Node(pure=pure_counts(rows), value=value, keep=keep, noof1=pure_counts(rows)['1'])
    else:

        set0, set1 = divide_set(rows, Index)
        rightchild = tree_build(set1, attributelength, 1)
        leftchild = tree_build(set0, attributelength, 1)
        keep = keep + 1
        temp = Decision_Node(col=attributes[Index], value=val, leftchild=leftchild, rightchild=rightchild, number=Index,
                             keep=keep, noof0=pure_counts(rows)['0'], noof1=pure_counts(rows)['1'])
        rightchild.parent = temp
        leftchild.parent = temp
        return temp


def tree_build1(rows, attributelength, val):
    global keep
    global leafcount
    if len(rows) == 0:
        keep = keep + 1
        return Decision_Node()
    Index = Variance_Impurity(rows, attributelength)
    if (Index == -2):
        if (pure_counts(rows)['0'] > pure_counts(rows)['1']):
            value = 0
            keep = keep + 1
            leafcount = leafcount + 1
            return Decision_Node(pure=pure_counts(rows), value=value, keep=keep, noof0=pure_counts(rows)['0'])
        else:
            value = 1
            keep = keep + 1
            leafcount = leafcount + 1
            return Decision_Node(pure=pure_counts(rows), value=value, keep=keep, noof1=pure_counts(rows)['1'])
    else:

        set0, set1 = divide_set(rows, Index)
        rightchild = tree_build(set1, attributelength, 1)
        leftchild = tree_build(set0, attributelength, 1)
        keep = keep + 1
        temp = Decision_Node(col=attributes[Index], value=val, leftchild=leftchild, rightchild=rightchild, number=Index,
                             keep=keep, noof0=pure_counts(rows)['0'], noof1=pure_counts(rows)['1'])
        rightchild.parent = temp
        leftchild.parent = temp
        return temp


def Pruning(tree, P):
    copy_tree = tree
    node_select = P
    node_require = tree_findnode(copy_tree, node_select)
    if (node_require is not None):
        if (node_require.pure is None and (tree_depth(copy_tree) - tree_finddepth(copy_tree, node_select, 0)) < 4):
            if (node_require.noof0 > node_require.noof1):
                p = float(node_require.noof0) / (node_require.noof1 + node_require.noof0)
            else:
                p = float(node_require.noof1) / (node_require.noof1 + node_require.noof0)
            if (p > 0.5):
                node_require.rightchild = None
                node_require.leftchild = None
                node_require.pure = {'1': node_require.noof0, '0': node_require.noof1}
                treenew = tree_findparent(node_require)
                copy_tree = treenew
                tree_number(copy_tree, 0)
    return copy_tree


def tree_pruning(L, K, tree, tot, al):
    ValidationAttributes = []
    ValidationCases = []
    with open(sys.argv[4], 'r') as csvfile:
        reader2 = csv.reader(csvfile)
        next(reader2)
        for row in reader2:
            ValidationCases += [row]
    csvfile.close()
    dbest = tree
    for i in range(L):
        d1 = tree_build(tot, al, 1)
        M = np.random.randint(1, K)
        for j in range(M):
            N = tree_number(d1, 0)
            P = np.random.randint(1, N)
            d1 = Pruning(d1, P)
        if tree_accuracy(ValidationCases, d1) > tree_accuracy(ValidationCases, dbest):
            dbest = d1
    return dbest


def main():
    TestCases = []
    TestAttributes = []
    ValidationCases = []
    ValidationAttributes = []
    L = int(sys.argv[1])
    K = int(sys.argv[2])
    with open(sys.argv[4], 'r') as csvfile:
        reader2 = csv.reader(csvfile)
        ValidationAttributes = next(reader2)
        for row in reader2:
            ValidationCases += [row]
        csvfile.close()
    with open(sys.argv[5], 'r') as csvfile:
        reader1 = csv.reader(csvfile)
        TestAttributes = next(reader1)
        for row in reader1:
            TestCases += [row]
        csvfile.close()
    with open(sys.argv[3], 'r') as csvfile:
        reader = csv.reader(csvfile)
        train_cases = []
        firstline = next(reader)
        global attributes
        global keep
        global leafcount
        keep = 0
        leafcount = 0
        attributes = {}
        attribute_values = []
        total_cases = []
        i = 0
        for column in firstline[0:-1]:
            attributes[i] = column
            i = i + 1
        attribute_values = {'0', '1'}
        for row in reader:
            total_cases += [row]
        tree = None
        j = 1
        while (j > 0):
            j = 0
            choice = input("Choose \n 1.Infogain \n 2.Varianceimpurity \n ")
            if (choice == "1"):
                tree = tree_build(total_cases, len(attributes), 1)
            else:
                tree = tree_build1(total_cases, len(attributes), 1)

            print('----------------------------------------------------------------------------------\n')
            print('Pre-Pruned Accuracy')
            print('-------------------')
            TrainAccuracy = tree_accuracy(total_cases, tree)
            print('Accuracy of the model before pruning\n')
        print('training dataset = ', TrainAccuracy * 100, '%\n')
        preValidationAccuracy = tree_accuracy(ValidationCases, tree)
        print('validation dataset = ', preValidationAccuracy * 100,
              '%\n')
        TestAccuracy = tree_accuracy(TestCases, tree)
        print('testing dataset = ', TestAccuracy * 100, '%')
        print('----------------------------------------------------------------------------------\n')
        print('Post-Pruned Accuracy')
        print('--------------------')
        treepruned = tree_pruning(L, K, tree, total_cases, len(attributes))
        TrainAccuracy = tree_accuracy(total_cases, treepruned)
        print('Accuracy of the model after pruning\n')
        print('training dataset = ', TrainAccuracy * 100, '%\n')
        ValidationAccuracy = tree_accuracy(ValidationCases, treepruned)
        print('validation dataset = ', ValidationAccuracy * 100,
          '%\n')
        TestAccuracy = tree_accuracy(TestCases, treepruned)
        print('testing dataset = ', TestAccuracy * 100, '%')
        to_print = sys.argv[6]
        if (to_print == "yes"):
            tree_print(tree)
            tree_print(treepruned)


if __name__ == "__main__":
    main()