# Winter Palace - lab 1 - variant 3

## Description

Lab 1: Mutable Algorithms and Data Structure Implementation

Objectives:

* Use development tools:
  Python 3, IDE/source code editor, git, Github Actions, and laboratory work process.
* Design algorithms and data structures in mutable styles.
* Develop unit and property-based tests.

Variant 3:

Set based on binary-tree

* You need to check that you implementation corectly works with None value.

## Group Information

Group Name: Winter Palace

Group members information as follows.

| HDU Number | Name            |
| ---------- | --------------- |
| 212320024  | Chen Chongzhong |
| 212320025  | Zuo Yuexin      |

## Project structure

- `mutable_BTree.py` -- implementation of `BTree` class with all features.
- `mutable_Tree_test.py` -- unit and PBT tests for `mutable_BTree`.

## Changelog

The first lab of CPO
HDU-ID: 212320025
Name: Zuo Yuexin
Date: 2022/04/12

1.Completed the general part of the lab. Such as add,remove,size and so on.
2.Iteration and merging still have some problems to be solved.

---

The first lab of CPO
HDU-ID: 212320025
Name: Zuo Yuexin
Date: 2022/04/13

1.Fixed some problems and finished the set_element method.

2.Still have some problems about empty method.

---

The first lab of CPO
HDU-ID: 212320024
Name: Chen Chongzhong
Date: 2022/04/14

1.Fixed one function's problem.

2.Completed the unittest and PBT tests in the Design Notes section.

---

The first lab of CPO
HDU-ID: 212320025
Name: Zuo Yuexin
Date: 2022/04/18

1.Add a class named Value which is used to provide static value.
Before I used this method, lot of ways had been tried.
I want to get the same effect as static in Java. Unfortunately.
I'm not that familiar with Python syntax.

2.I tested different way to test undefined behavior.
In C++ it's can be very easy, such as f(i++,i++) can cause undefined behavior.
So I tried the same idea.It proved that it can be a source of undefined behavior.
An example is shown in `mutable_test.py`.

---

The first lab of CPO
HDU-ID: 212320024
Name: Chen Chongzhong
Date: 2022/04/18

1.Fixed iterator tests in `mutable_test.py`.

2.Fixed test function `test_monoid_properties` about monoid property.

---

The first lab of CPO

HDU-ID: 212320025

Name: Zuo Yuexin

Date: 2022/04/25

1.Same as above test, I passed the absolute value function to the map() and
tested a set of data to be its inverse.
In the function, I wrote to construct the tree, I did not judge how
to construct a tree based on the size of the value passed in.
So the result is definitely certain. If it means Can you provide data, whether
result is not determined?
When changed whether to where, i can't understand what that means.

2.Update the map function.

---

The first lab of CPO

HDU-ID: 212320024

Name: Chen Chongzhong

Date: 2022/04/25

1.Add much more assertions for checking behaviour in function `test_iter`.

## Design notes

We implement the Binary Tree's mutable algorithms and data structure Implementation.

The running result screenshot of unittests is the image named `image/img.png`.

We write two python files, `mutable_BTree.py` and `mutable_BTree_test.py`.

And successfully implement some operations about Binary Tree.

For example, add and remove element, concat  the trees to the new tree, etc.

The unittest and PBT tests provides us with great convenience.

