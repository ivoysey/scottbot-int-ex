import collections

def maxk (c , k):
    if len (c) < k:
        raise Exception ('can\'t pick ' + str(k) +
                        ' largest elems from collecction of size ' +
                         str(len(c)))

    ## since we didn't raise, we know that there are at least k things in c.
    first_k = c[:k]
    first_k.sort(reverse=True)
    d = collections.deque(first_k, k)

    for elem in c[k:]:
        print "hello! " + str(elem)
        ## see if the new element is larger than all previous maxes
        bt_all = True
        for m in d:
            bt_all = bt_all and (elem > m)

        ## if it is, add it and drop off what ever's smallest
        if bt_all:
                d.appendleft(elem)
    return d

top = maxk ([1,2,5,3,0,4,5],3)
print top
