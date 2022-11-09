# python-adt

## What are Algebraic Data Types (ADT) ?
ADTs are very popular in functional programming languages. They are a type of composite data type that combine the features of union and enum data types.   
   
A union allows you to capture different data types within a single type. An instance of the union will be an object of one of the pre-defined list of data types from the union. An enum allows you to define a set of named values. An ADT enables you to combine both features, you can define a set of named data types. An instance of the ADT will be an object of one of the named data types from the pre-defined set.    
    
For example   

We can have a Tree data type, where it is either empty, has nodes, where each node has left and right child. Each left and right child can either be empty or be a leaf node.

Most functional programming languages leverage the power of ADTs with pattern matching!!!

ADTs allow you to quickly and concisely define rich data structues and then capture the behavior using pattern matching. 

## Python based ADT
Refer to the previous work    
Several previous attempts have been made to bring the goodness of ADTs to python. <1>, <2>, ...

However, all these python mechanisms were developed prior to the introduction of pattern matching to python. The addition of pattern matching to python gives us the flexibility of building ADTs on top of python classes. We use a combination of python classes and python dataclasses to capture the definition of an ADT, and then we can directly use python pattern matching since our python ADT is a class under the hood.

Pattern matching was introduced in python 3.10 in October'21.

### Examples
