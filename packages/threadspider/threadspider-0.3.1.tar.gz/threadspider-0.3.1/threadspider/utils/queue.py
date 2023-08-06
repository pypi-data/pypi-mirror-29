# coding:utf-8
# write  by  zhou

from Queue import PriorityQueue as _Q


class QueueElement(object):
    def __init__(self, priority, obj):
        self.priority = priority
        self.obj = obj

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)


class PriorityQueue(_Q):
    def put_priority(self, item, priority, block=True, timeout=None):
        _Q.put(self, QueueElement(priority, item), block, timeout)
