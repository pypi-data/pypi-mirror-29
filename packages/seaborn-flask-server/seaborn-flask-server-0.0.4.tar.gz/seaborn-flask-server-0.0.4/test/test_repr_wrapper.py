def smoke_test():
    print(str(ReprListList([['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                            ['a', 1, 0.0, 1.0, 2.12, 3.123, 4.1234]],
                           digits=3)))

    test_str = "[(0, {'a': 'A', 'c': 'C', 'b': 'B'}), \n " \
               "(1, {'a': 'A', 'c': 'C', 'b': 'B'}), \n " \
               "(2, {'a': 'A', 'c': 'C', 'b': 'B'})]"
    ans_str = rep(test_str)
    print(repr(ans_str) + '\n')

    test_dict = {'key': [(0, {'a': 'A', 'c': 'C', 'b': 'B'}),
                         (1, {'a': 'A', 'c': 'C', 'b': 'B'}),
                         (2, {'a': 'A', 'c': 'C', 'b': 'B'})]}
    ans_dict = rep(test_dict)
    print(repr(ans_dict) + '\n')

    test_list = [(0, {'a': 'A', 'c': 'C', 'b': 'B'}),
                 (1, {'a': 'A', 'c': 'C', 'b': 'B'}),
                 (2, {'a': 'A', 'c': 'C', 'b': 'B'})]
    ans_list = rep(test_list)
    print(repr(ans_list) + '\n')

    test_unicode = u"[(0, {'a': 'A', 'c': 'C', 'b': 'B'}), \n " \
                   u"(1, {'a': 'A', 'c': 'C', 'b': 'B'}), \n " \
                   u"(2, {'a': 'A', 'c': 'C', 'b': 'B'})]"
    ans_unicode = rep(test_unicode)
    print(repr(ans_unicode) + '\n')

    test_tuple = (
        (0, {'a': 'A', 'c': 'C', 'b': 'B'}),
        (1, {'a': 'A', 'c': 'C', 'b': 'B'}),
        (2, {'a': 'A', 'c': 'C', 'b': 'B'}))
    ans_tuple = rep(test_tuple)
    print(repr(ans_tuple) + '\n')

    test_list_list = [range(i, i + 10) for i in range(10)]
    ans_list_list = rep(test_list_list, _type='list_list')
    print(repr(ans_list_list) + '\n')

    col_names = [l for l in 'abcdefghi'] + ['hello']
    ans_list_list.repr_setup(col_names=col_names)
    print(repr(ans_list_list))


if __name__ == '__main__':
    smoke_test()