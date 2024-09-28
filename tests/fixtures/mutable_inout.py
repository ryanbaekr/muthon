def my_func(my_list: list[int]) -> None:
    my_list.append(5)
    print(my_list)

x: list[int] = [0, 1, 2]
my_func(x)
print(x)