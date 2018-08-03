import nltk


def lines(a, b):
    """Return lines in both a and b"""
    eq = list()

    """ Apply split method excluding \n """
    """ Then convert to set to discard repeated values """
    f1 = set(a.split('\n'))
    f2 = set(b.split('\n'))

    """ If values from f1 equals f2, append them to eq list"""
    for n in f1:
        for m in f2:
            if n == m:
                eq.append(n)
    return eq


def sentences(a, b):
    """Return sentences in both a and b"""

    """ Use sent_tokenize method to divide in sentences the texts in 'a' and 'b'
        (http://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.sent_tokenize) """

    list1 = nltk.tokenize.sent_tokenize(a, language='english')
    list2 = nltk.tokenize.sent_tokenize(b, language='english')
    list3 = list()

    list1 = set(list1)
    list2 = set(list2)
    """ Iterate through sentences in list1 and list2, comparing each other and, if equal, appending
        to list3, then returned as an output """

    for m in list1:
        for n in list2:
            if m == n:
                list3.append(n)
            else:
                continue
    return list3


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    """ Initialize values (Must optimize) """
    slic = n
    slic2 = n
    list1 = list()
    list2 = list()
    list3 = list()

    """ Iterate over a's len and then use 'i/j' as the pivot for slicing to slic/slic2
        All this while saving the slices in a different list for each text
    """

    for i in range(len(a)):
        curPos = i
        list1.append(a[curPos:slic-1])
        slic += 1

    for j in range(len(b)):
        curPos = j
        list2.append(b[curPos:slic2-1])
        slic2 += 1

    """ Convert lists to set to remove repeated values"""  # Need to find a better way

    list1 = set(list1)
    list2 = set(list2)

    """ Iterate over slices in list1 and list2 comparing each one
        and saving the coincidental values in list3"""

    for k in list1:
        for l in list2:
            if k == l:
                list3.append(k)
            else:
                continue
    return list3
""" TODO """

# Make fancier form
# Review substrings function
# Check