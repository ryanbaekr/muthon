# Muthon

Static code analysis for mutable object safety in Python

## Table of Contents

- [Motivation](#motivation)
- [Why not Mojo?](#why-not-mojo)
- [The Problem with Mutable Objects](#the-problem-with-mutable-objects)
- [How to use Muthon](#how-to-use-muthon)
- [How to Contribute](#how-to-contribute)
- [TODO](#todo)
- [FAQ](#faq)
- [How to Support](#how-to-support)

## Motivation

The Muthon authors are both senior SWEs with professional experience in Python.  Between the two of them, they agree on three shortcomings of Python: They wish it was strictly typed, they wish it had true multithreading, and they wish it had better checking for the safety issues related to passing around mutable objects.

The first two are getting solved by others, but Muthon aims to solve the issue of safety with mutable objects.

## Why not [Mojo](https://www.modular.com/mojo)?

"Doesn't Mojo already have a borrow checker?"

The Muthon authors love what Mojo is doing, but have concerns when it comes to adoption.

Mojo does a lot more than Muthon.  If your project needs more features from Mojo, or is likely to need them in the future, you should stop reading and use Mojo.

If your project just needs a borrow checker, then Muthon allows your Python to stay Python.  This offers the following advantages:
- Less development effort to adopt, particularly for large projects
- Less resistance from teammates, management, etc

To give Mojo credit, it is really easy to include Python code in a Mojo project.  But like JSDoc vs TS, Muthon is simply less effort to adopt and doesn't require a full commitment to a new language.

## The Problem with Mutable Objects

Consider the following Python code:

```python
def my_func(my_int):
    my_int = my_int + 2
    print(my_int)

x = 6
my_func(x)
print(x)
```

As expected, this code would produce the following:

```
8
6
```

The behavior is the same for int, float, bool, string, Unicode, and tuple.

Now consider the following Python code:

```python
def my_func(my_list):
    my_list.append(5)
    print(my_list)

x = [0, 1, 2]
my_func(x)
print(x)
```

Unintuitively, perhaps, the contents of x have also changed:

```
[0, 1, 2, 5]
[0, 1, 2, 5]
```

This behavior is the same for all other mutable types.

Most of the time this is actually a good thing, because copying large objects would be costly, but developers should be careful when passing a mutable object into a function and then using it later.

## How to use Muthon

TODO add actual CLI usage

Here are some examples of Muthon's analysis:

### Example 1

```python
def my_func(my_int):
    my_int = my_int + 2
    print(my_int)

x = 6
my_func(x)
print(x)
```

Muthon has no complaints here as no mutable objects are involved.

### Example 2

```python
def my_func(my_list):
    my_list.append(5)
    print(my_list)

x = [0, 1, 2]
my_func(x)
```

In this case, `x` is mutable and modified by `my_func` but `x` is never used again, so again, Muthon has no complaints here.

### Example 3

```python
def my_func(my_list):
    for num in my_list:
        print(num)

x = [0, 1, 2]
my_func(x)
print(x)
```

In this case, `x` is mutable and used again after being passed to `my_func` but `my_func` never modifies the object, so again, Muthon has no complaints here.

### Example 4

```python
def my_func(my_list):
    my_list.append(5)
    print(my_list)

x = [0, 1, 2]
my_func(x)
print(x)
```

In this case, `x` is mutable, modified by `my_func`, and used again after being passed to `my_func`.  Muthon will mark this as a failure unless a comment is added acknowleding `x` as inout.

```python
def my_func(my_list):
    my_list.append(5)
    print(my_list)

x = [0, 1, 2]
my_func(x)  # muthon: inout=x
print(x)
```

Multiple objects can be marked as inout on the same line with the following syntax:

```python
my_func(x, y)  # muthon: inout=x,y
```

## How to Contribute

To contribute to Muthon please fork the repository, branch off of main, and then make a merge request from your branch back to Muthon's main branch.

## TODO

In the future we'd like to have better integration with IDEs/editors, namely special highlighting of Muthon comments, like TODO, and underlining of failures.

## FAQ

Why can't an argument be marked as inout once within the function instead of on every single function call?

There are three good reasons for this:
- If the function you're calling comes from an external library and does an in-place operation, you may have no way to satisfy Muthon
- If you acknowledge an input argument as inout, it doesn't meaen the next person who uses the function knows it will modify the argument
- You may want to selectively keep objects modified by a function around but not everytime

## How to Support

The best ways to help are to [contribute](#how-to-contribute), open issues, star the project, and TODO buy me a coffee.
