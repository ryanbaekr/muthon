# Mutyping

Static code analysis for mutable object safety in Python

## Table of Contents

- [Motivation](#motivation)
- [The Problem with Mutable Objects](#the-problem-with-mutable-objects)
- [How to use Mutyping](#how-to-use-mutyping)
- [How to Contribute](#how-to-contribute)
- [How to Support](#how-to-support)

## Motivation

The Mutyping authors are both senior SWEs with professional experience in Python.  Between the two of them, they agree on three shortcomings of Python: They wish it was strictly typed, they wish it had true multithreading, and they wish it had better checking for the safety issues related to passing around mutable objects.

The first two are getting solved by others, but Mutyping aims to solve the issue of safety with mutable objects.

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

## How to use Mutyping

Mutyping relies largely on mypy's existing handling of typing.Sequence, typing.MutableSequence, typing.Mapping, typing.MutableMapping, typing.Set, and typing.MutableSet. Mypy's analysis largely handles all the issues with mutability just by using these types.

Here is an example of mypy's analysis:

```python
def my_func(my_list: MutableSequence[int]):
    my_list.append(5)
    print(my_list)

x: Sequence[int] = [0, 1, 2]
my_func(x)
print(x)
```

At runtime, this still produces the following output:

```
[0, 1, 2, 5]
[0, 1, 2, 5]
```

However, mypy analysis produces the following error:

```
error: Argument 1 to "my_func" has incompatible type "Sequence[int]"; expected "MutableSequence[int]"  [arg-type]
```

This is fantastic, but it does require developers to be diligent with type annotations. When a type annotation is not provided for `x`, mypy infers the type as `List[int]` which produces no errors when passed into `my_func`.

It would be great if mypy could be configured to infer immutable types by default, but there is a pretty good alternative.

The `flake8-strict-types` plugin can be used to require all variable instantiations to have a type annotation. If a developer is commited to the idea of immutable by default, simply using mypy, flake8, and this plugin together will prevent the basic mistakes that often come with using mutable types.

There is even a way to temporarily allow an otherwise immutable object to be mutated with typing.cast:

```python
def my_func(my_list: MutableSequence[int]):
    my_list.append(5)
    print(my_list)

x: Sequence[int] = [0, 1, 2]
my_func(cast(MutableSequence[int], x))
print(x)
```

This is almost like borrowing in Rust.

Beyond that, Mutyping just offers some syntax sugar so `Mut[Sequence]` can be used in place of `MutableSequence`, for example.

## How to Contribute

To contribute to Mutyping please fork the repository, branch off of main, and then make a merge request from your branch back to Mutyping's main branch.

You will be added to the contributors section of the authors file if your merge request is accepted.

## How to Support

The best ways to help are to [contribute](#how-to-contribute), open issues, star the project, and TODO buy me a coffee.
