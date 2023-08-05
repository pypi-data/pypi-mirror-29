# coding=utf-8
"""
Jason <peter.waynechina@gmail.com>  2018/01/18

LHD implementation


Expensive in fully-associative cache N^2logN
expensive without hardware support
magic number comes from the drop pos in EVA curve
age updating complicated off 1
when there is no EVA ready, need to random evict, cannot use LRU (otherwise converge problem)
    random will cause some problem in classification, it can be trapped into local minimal, for example,
    if an element from small array gets evicted then it becomes non-reused class and gets evicted every time comes in

self.reused_class.hit_probability[0] can be 1 in classification
"""


import sys
import socket
import math
from collections import deque
from PyMimircache.cache.abstractCache import Cache
from PyMimircache.utils.linkedList import LinkedList
from heapdict import heapdict
# from numba import jit
from functools import reduce

from concurrent.futures import ProcessPoolExecutor, as_completed

import os
import matplotlib.pyplot as plt
from PyMimircache.utils.timer import MyTimer
from PyMimircache.cache.lru import LRU
from PyMimircache import CLRUProfiler
from PyMimircache.profiler.pyGeneralProfiler import PyGeneralProfiler

from PyMimircache.profiler.cGeneralProfiler import CGeneralProfiler
from PyMimircache.cacheReader.vscsiReader import VscsiReader
from PyMimircache.cacheReader.binaryReader import BinaryReader
from PyMimircache import PlainReader


def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

def argsort_dict(d):
    return sorted(d.keys(), key=d.__getitem__)


class LHD(Cache):
    class Class:
        def __init__(self, name, max_age, ewma_decay, dat_name, cache_size):
            self.name = name
            self.max_age = max_age
            self.ewma_decay = ewma_decay
            self.dat_name = dat_name
            self.cache_size = cache_size

            self.reset()

            self.hit_probability   = [0] * self.max_age
            self.expected_lifetime = [0] * (self.max_age + 1)
            self.events = [0] * (self.max_age + 1)

            self.hits_interval = [0] * self.max_age
            self.evicts_interval = [0] * self.max_age

            self._ewma_hits = [0] * self.max_age
            self._ewma_evicts = [0] * self.max_age

            self.hit_density = [0] * self.max_age
            self.eva_plot_count = -1


        def update(self):
            self.events = [0] * self.max_age
            for i in range(self.max_age):
                if i >= len(self._ewma_hits):
                    print("ERROR2 {} {}".format(i, len(self._ewma_hits)))
                self._ewma_hits[i] *= self.ewma_decay
                # self._ewma_hits[i] += self._hits_interval[i]
                self._ewma_hits[i] += (1 - self.ewma_decay) * self._hits_interval[i]
                self._ewma_evicts[i] *= self.ewma_decay
                # self._ewma_evicts[i] += self._evicts_interval[i]
                self._ewma_evicts[i] += (1 - self.ewma_decay) * self._evicts_interval[i]
                self.events[i] = self._ewma_hits[i] + self._ewma_evicts[i]

        # @jit
        def reconfigure(self, line_gain):

            hits_up_to_now = 0
            events_up_to_now = 0

            self.eva = [0] * self.max_age
            self.hit_probability = [0] * (self.max_age)
            self.expected_lifetime = [0] * (self.max_age + 1)

            expected_lifetime_unconditioned = 0

            # first calculate hit_probability, then expected lifetime
            for i in range(self.max_age-1, -1, -1):
                # self.expected_lifetime[i] = expected_lifetime_unconditioned


                # # this can also be put below else
                # events_up_to_now += self.events[i]
                # expected_lifetime_unconditioned += events_up_to_now
                #

                if events_up_to_now >= 1e-2:
                    self.hit_probability[i] = hits_up_to_now / events_up_to_now
                    self.expected_lifetime[i] = expected_lifetime_unconditioned / events_up_to_now

                    self.eva[i] = (self.hit_probability[i] - line_gain * self.expected_lifetime[i])
                else:
                    self.hit_probability[i] = 0
                    self.expected_lifetime[i] = 0
                    self.eva[i] = 0


                # this can also be put above
                events_up_to_now += self.events[i]
                expected_lifetime_unconditioned += events_up_to_now
                hits_up_to_now += self._ewma_hits[i]



            # if socket.gethostname() != "node":
            #     print("{} line gain: {}".format(self.name, line_gain))
            #
            #     print(", ".join(["{:8.2f}".format(i) for i in self._hits_interval]))
            #     print(", ".join(["{:8.2f}".format(i) for i in self._evicts_interval]))
            #     # print(", ".join(["{:8.2f}".format(i) for i in self.events]))
            #     print(", ".join(["{:8.2f}".format(i) for i in self.hit_probability]))
            #     print(", ".join(["{:8.2f}".format(i) for i in self.expected_lifetime]))
            #     print(", ".join(["{:8.2f}".format(i*100) for i in self.eva]))

            self.plot_eva(self.dat_name, self.cache_size)
            self.reset()

        def reset(self):
            self.hits_interval = [0] * self.max_age
            self.evicts_interval = [0] * self.max_age

        def coarsen_age(self, age):
            return age

        # @jit
        def hit(self, age):
            coarse_age = self.coarsen_age(age)
            if coarse_age >= len(self.hits_interval):
                raise RuntimeError("ERROR on class hit: age {} {}".format(coarse_age, len(self.hits_interval)))
            self.hits_interval[coarse_age] += 1

        # @jit
        def evict(self, age):
            coarse_age = self.coarsen_age(age)
            if coarse_age >= len(self.evicts_interval):
                raise RuntimeError("ERROR on class evict: age {} {}".format(coarse_age, len(self.evicts_interval)))
            self.evicts_interval[coarse_age] += 1


        def plot_eva(self, dat_name, cache_size=None):
            if self.eva_plot_count >= 0:
                figname = "1127EVA_Value/{}/eva_{}_{}_{}.png".format(dat_name, self.name, cache_size, self.eva_plot_count)
                if not os.path.exists(os.path.dirname(figname)):
                    os.makedirs(os.path.dirname(figname))

                # print("plot {}".format(self.eva))
                plt.plot(self.eva, label="{}_{}_{}".format(self.name, cache_size, self.eva_plot_count))
                plt.ylabel("EVA")
                plt.xlabel("Age")
                plt.savefig(figname)
                print("eva value plot {} done".format(figname))
                plt.clf()
                self.eva_plot_count += 1


    def __init__(self, cache_size=1000, update_interval=1280, max_age=20000, ewma_decay=0.8,
                 age_scaling=100, enable_classification=False, enable_stat=True, dat_name=None):
        super().__init__(cache_size)

        self.cache_size = cache_size
        self.update_interval = update_interval
        self.max_age = max_age // age_scaling + 1
        self.ewma_decay = ewma_decay
        self.age_scaling = age_scaling
        self.enable_classification = enable_classification
        self.enable_stat = enable_stat
        self.dat_name = dat_name
        self.debugging_mode = True

        print("cache size {}, update interval {}, age_scaling {}, classification {}, decay coefficient {}, max_age {}".format(
                    self.cache_size, self.update_interval, self.age_scaling,
                    self.enable_classification, self.ewma_decay, self.max_age), end="\n")

        self.eva_sorted_age = []
        self.access_time_d = {}
        # self.age_to_elements_dict = {}
        # index using scaled_age
        self.age_to_elements_list = deque()

        self.current_ts = 0
        # this is the oldest ts of elements in the frist element_list in age_to_elements_list
        self.current_element_list_oldest_ts = 1

        if self.enable_classification:
            self.classes = [self.Class("nonReused", self.max_age, self.ewma_decay, self.dat_name, self.cache_size),
                            self.Class("reused", self.max_age, self.ewma_decay, self.dat_name, self.cache_size)]
            self.non_reused_class = self.classes[0]
            self.reused_class = self.classes[1]
            self.classID = {}
            if self.enable_stat:
                self.hit_stat = [[0]*self.max_age, [0]*self.max_age]
                self.evict_stat = [[0]*self.max_age, [0]*self.max_age]
        else:
            self.classes = [self.Class("general", self.max_age, self.ewma_decay, self.dat_name, self.cache_size)]

        self.top_eviction_deque = deque()
        self.top_eviction_set = set()

    # @jit
    def reconfigure(self):
        # get class stat ready for calculation
        for cl in self.classes:
            cl.update()

        # calculate line_gain
        ewma_hits_all = sum([sum(cl.ewma_hits) for cl in self.classes])
        ewma_evicts_all = sum([sum(cl.ewma_evicts) for cl in self.classes])

        if ewma_hits_all + ewma_evicts_all != 0:
            # this can happen when update_interval is very small
            line_gain = ewma_hits_all / (ewma_hits_all + ewma_evicts_all) / self.cache_size
        else:
            line_gain = 0

        # with line_gain, reconfigure each class, calculate EVA with classification
        for cl in self.classes:
            cl.reconfigure(line_gain)
            # cl.reset()

        if self.enable_classification:
            # if self.reused_class.hit_probability[0] == 1:
                # should not happen often
            #     print("self.reused_class.hit_probability[0] = {}, reused eva0 = {}".format(
            #                 self.reused_class.hit_probability[0], self.reused_class.eva[0]))
            #     self.reused_class.hit_probability[0] = 0.99
            # print("self.reused_class.hit_probability[0] = {}, reused eva0 = {}".format(
            #     self.reused_class.hit_probability[0], self.reused_class.eva[0]))


            # eva_reused = self.reused_class.eva[0] / (1 - self.reused_class.hit_probability[0])
            if self.non_reused_class.hit_probability[0] == 0:
                print("size {} h 0".format(self.cache_size))
            eva_non_reused = self.non_reused_class.eva[0] / (self.non_reused_class.hit_probability[0])

            if ewma_hits_all + ewma_evicts_all == 0:
                hit_ratio_overall = 0
            else:
                hit_ratio_overall = ewma_hits_all / (ewma_hits_all + ewma_evicts_all)
            for cl in self.classes:
                for i in range(self.max_age-1, -1, -1):
                    # cl.eva[i] += (cl.hit_probability[i] - hit_ratio_overall) * eva_reused
                    cl.eva[i] += (hit_ratio_overall - cl.hit_probability[i]) * eva_non_reused
            eva_combined = {}
            for cl in self.classes:
                for n, eva in enumerate(cl.eva):
                    eva_combined[(cl.name, n)] = eva
            self.eva_sorted_age = argsort_dict(eva_combined)


        else:
            self.eva_sorted_age = argsort(self.classes[0].eva)


        # print("sorted age {}".format(self.eva_sorted_age))


    def _verify(self, msg=""):
        assert len(self.age_to_elements_list) <= self.max_age
        size = sum( [len(i) for i in self.age_to_elements_list] )
        if msg == "d" or msg == "e" or msg == "f" or \
                msg == "ub" or msg == "uc":
            assert size == len(self.access_time_d) - 1, \
                "msg {}, size different by more than one {} {}".format(
                msg, size, len(self.access_time_d)
            )

        else:
            assert size == len(self.access_time_d), \
                "msg {}, size different {} {}, age list size {}".format(
                msg, size, len(self.access_time_d), len(self.age_to_elements_list)
            )

        if msg != "e":
            assert len(self.access_time_d) + len(self.top_eviction_set) <= self.cache_size, \
                "msg {}, number of items larger than cache size {} {}".format(
                    msg, len(self.access_time_d) + len(self.top_eviction_set), self.cache_size
                )
        else:
            assert len(self.access_time_d) + len(self.top_eviction_set) -1 <= self.cache_size, \
                "msg {}, number of items larger than cache size {} {}".format(
                    msg, len(self.access_time_d) + len(self.top_eviction_set), self.cache_size
                )

        for n, element_list in enumerate(self.age_to_elements_list):
            if element_list:
                for element in element_list:
                    assert element in self.access_time_d, \
                        "cache size {}, msg {}, cannot find {}".format(self.cache_size, msg, element)
                    assert self.current_ts - self.access_time_d[element] - 1 == n, \
                        "age verification failed"


    def _verify2(self, msg=""):
        if self.current_ts == 0: return
        for e, t in self.access_time_d.items():
            current_ts = self.current_ts
            # if msg == "g" or msg == "a":
            #     current_ts = current_ts - 1
            age = self._get_age(e)
            # print("age {}/{} {}/{}/{} {}: {}".format(age, len(self.age_to_elements_list),
            #                                          self.current_element_list_oldest_ts,
            #                                       current_ts, t, e, self.age_to_elements_list))
            assert e in self.age_to_elements_list[age], "{}: {} not in, age {} ({}/{}) {}".\
                format(msg, e, age, current_ts, t, self.age_to_elements_list)

    def _reset(self):
        for c in self.classes:
            c.reset()

    # # not used
    # def _get_id(self, element):
    #     return hash(element) % self.cache_size
    #
    # def _get_timestamp(self, element):
    #     return self.timestamps[self._get_id(element)]

    def _get_age(self, element):
        age = self.current_element_list_oldest_ts - self.access_time_d[element]
        scaled_age = int(math.ceil(age / self.age_scaling))

        if scaled_age < 0:
            scaled_age = 0

        # if left_over_age >= len(self.age_to_elements_list[0]):
        #     scaled_age += 1
        return scaled_age

        # # prev_ts = self.timestamps[ self._get_id(element) ]
        # prev_ts = self._get_timestamp(element)
        # exact_time = self.current_ts - prev_ts
        # coarse_time = (float(exact_time) // self.age_scaling) % self.max_age
        # return coarse_time


    # @jit
    def _update_age(self, element):

        # NOTICE the time order in element list (old->new as left->right) is different
        # from the time order of age_to_elements_list (old->new as right->left)
        # this is for easy traverse the old element in eviction

        # system age begins from 1
        self.current_ts += 1

        if (self.current_ts - self.current_element_list_oldest_ts) % self.age_scaling == 0:
            self.age_to_elements_list.appendleft(deque([element, ]))
            self.current_element_list_oldest_ts = self.current_ts
        else:
            self.age_to_elements_list[0].append(element)

        if self.debugging_mode:
            assert len(self.age_to_elements_list[0]) <= self.age_scaling, \
                "error first element size {} age scaling {}".format(len(self.age_to_elements_list[0]), self.age_scaling)

        if self.enable_stat:
            pass

        # Jason: age wrap up should be avoided
        if len(self.age_to_elements_list) > self.max_age:
            # print("wrap up")
            # element_max_age can be None, this is the situation when the element has been hit
            element_list_max_age = self.age_to_elements_list.pop()
            for element_max_age in element_list_max_age:
                del self.access_time_d[element_max_age]
                self.top_eviction_deque.append(element_max_age)
                self.top_eviction_set.add(element_max_age)


    # @jit
    def has(self, req_id, **kwargs):
        """
        :param **kwargs:
        :param req_id:
        :return: whether the given element is in the cache
        """

        if req_id in self.access_time_d or req_id in self.top_eviction_set:
            return True
        else:
            return False


    # @jit
    def _update(self, req_item, **kwargs):
        """ the given req_item is in the cache, now update it to new location
        :param **kwargs:
        :param req_item:
        """

        # Jason: corner case, how wrap up is handled
        in_top_eviction  = False
        if req_item in self.top_eviction_set:
            in_top_eviction = True
            age = self.max_age - 1
        else:
            # age = (self.current_ts - self.access_time_d[req_item]) // self.age_scaling
            age = self._get_age(req_item)

        if age >= self.max_age:
            raise RuntimeError("cache_size {}, scaled age larger than max age, {}/{}".\
                                format(self.cache_size, age, self.max_age))

        # Jason: corner case if req_item in top_eviction, what is hit age?
        if self.enable_classification:
            self.reused_class.hit(age)
        else:
            self.classes[0].hit(age)

        if not in_top_eviction:
            # req_item should be in age_to_elements_list
            # no need to add a new one to the left to age_to_element_list, which is done in update_age

            # HIGH TIME COMPLEXITY
            element_list = self.age_to_elements_list[age]
            if self.debugging_mode:
                assert req_item in element_list, \
                    "update req_item error, req_item {} not in {}, prev {}, next {}, current ts {}, last access time {}, age {}".\
                        format(req_item, element_list, self.age_to_elements_list[age - 1], self.age_to_elements_list[age + 1],
                               self.current_ts, self.access_time_d[req_item], age)
            element_list.remove(req_item)
            # self.age_to_elements_list[age] = element_list

        else:
            self.top_eviction_set.remove(req_item)
            self.top_eviction_deque.remove(req_item)

        self.access_time_d[req_item] = self.current_ts


    # @jit
    def _insert(self, req_item, **kwargs):
        """
        the given element is not in the cache, now insert it into cache
        ATTENTION: after insert, number of items in age_to_element_list and number of items in access_time_d is different
        adding to age_to_element_list is updated in update_age
        :param **kwargs:
        :param req_item:
        :return: evicted element or None
        """
        self.access_time_d[req_item] = self.current_ts

        if self.enable_classification:
            # Jason: what will be the age of non-reused-class get hit
            self.non_reused_class.hit(self.max_age - 1)


    # @jit
    def evict(self, **kwargs):
        """
        evict one element from the cache line
        :param **kwargs:
        :return: content of evicted element
        """
        # raise RuntimeError("ts {} need to evict, current stack size {} stack {}".format(
        #                     self.current_ts, len(self.access_time_d), self.access_time_d))

        evict_age = -1
        element_to_evict = None
        evict_from = ""
        evict_element_class = None

        # first find the ts of the element that's going to be evicted with EVA
        if len(self.top_eviction_deque):
            # if there are wrap up
            element_to_evict = self.top_eviction_deque.popleft()
            self.top_eviction_set.remove(element_to_evict)
            evict_age = self.max_age -1
            evict_from = "top_eviction_queue"
            if self.enable_classification:
                evict_element_class = self.classID[element_to_evict]
                del self.classID[element_to_evict]
        else:
            if len(self.eva_sorted_age):
                # EVA info is ready
                if self.enable_classification:
                    for (class_name, age) in self.eva_sorted_age:
                        if age >= len(self.age_to_elements_list):
                            continue
                        evict_classID = True if class_name == "reused" else False
                        # HIGH TIME COMPLEXITY
                        element_list = self.age_to_elements_list[age]
                        for element in element_list: # old->new
                            if self.classID[element] == evict_classID:
                                element_to_evict = element
                                evict_age = age
                                element_list.remove(element_to_evict)
                                # self.age_to_elements_list[age] = element_list
                                break

                        if evict_age != -1:
                            # break outer looop
                            evict_from = "sorted age"
                            break

                else:
                    # no classification
                    for age in self.eva_sorted_age:
                        if age >= len(self.age_to_elements_list):
                            continue
                        # HIGH TIME COMPLEXITY
                        element_list = self.age_to_elements_list[age]
                        if len(element_list):
                            element_to_evict = element_list.popleft()
                            evict_age = age
                            # self.age_to_elements_list[age] = element_list
                            evict_from = "sorted age"
                            break

            else:
                # Jason: corner case, handling choice?
                # print("eva_sorted_age have nothing {}".format(self.eva_sorted_age),
                #       file=sys.stderr)

                # use LRU to evict when no info avail
                # element_to_evict = self.age_to_elements_list.pop()
                # while not element_to_evict:
                #     element_to_evict = self.age_to_elements_list.pop()
                # evict_age = len(self.age_to_elements_list)
                # evict_from = "no info"


                # random eviction when no info avail
                for e, t in self.access_time_d.items():
                    element_to_evict = e
                    # evict_age = (self.current_ts - t)//self.age_scaling
                    evict_age = self._get_age(e)
                    evict_from = "no info avail"

                    # HIGH COMPLEXITY
                    element_list = self.age_to_elements_list[evict_age]
                    assert element_to_evict in element_list, \
                        "in eviction, {} not in element list {}".format(element_to_evict, element_list)
                    element_list.remove(element_to_evict)
                    break



        if element_to_evict is None:
            raise RuntimeError("cannot find element to evict {} {}".format(self.age_to_elements_list,
                                                                           self.eva_sorted_age))
        # if socket.gethostname() != "node":
        #     print("evict age {} {} ({}) from {}, age_to_element_list size {}, top_eviction size {}".format(
        #                 evict_age, element_to_evict, self.classID[element_to_evict],
        #                 evict_from, len(self.age_to_elements_list), len(self.top_eviction_deque)))

        try:
            if evict_from != "top_eviction_queue":
                del self.access_time_d[element_to_evict]
                if self.enable_classification:
                    evict_element_class = self.classID[element_to_evict]
                    del self.classID[element_to_evict]
            # self._verify("y {}".format(evict_from))
        except Exception as e:
            print("evict from {} error: {}".format(evict_from, e))
            raise RuntimeError("{} not in {}".format(element_to_evict, self.access_time_d))

        if self.enable_classification:
            if evict_element_class:
                # reused
                self.reused_class.evict(evict_age)
            else:
                self.non_reused_class.evict(evict_age)
        else:
            self.classes[0].evict(evict_age)


    # @jit
    def access(self, req_item, **kwargs):
        """
        :param **kwargs:
        :param req_item: the element in the reference, it can be in the cache, or not
        :return: None
        """

        self._update_age(req_item)
        # self._verify2(msg = "a")

        if self.current_ts > self.cache_size and self.current_ts % self.update_interval == 0:
            self.reconfigure()
        # self._verify2(msg = "b")

        found = False
        if self.has(req_item, ):
            # self._verify2(msg="c")
            found = True
            if self.enable_classification:
                self.classID[req_item] = found
            self._update(req_item, )
            # self._verify2(msg="d")
        else:
            if self.enable_classification:
                self.classID[req_item] = found
            self._insert(req_item, )
            # self._verify2(msg="e")
            if len(self.access_time_d) + len(self.top_eviction_set) >= self.cache_size:
                self.evict()
            # self._verify2(msg = "f")


        # self._update_age(req_item)
        # self._verify2(msg = "g")


        if self.current_ts % 200000 == 0:
            for cl in self.classes:
                cl.plot_eva(self.dat_name, cache_size=self.cache_size)


        return found


    def __len__(self):
        return len(self.access_time_d)


    def __repr__(self):
        return "evaJ, cache size: {}, current size: {}, {}".format(
                    self.cache_size, len(self.access_time_d), super().__repr__())



def mytest1():
    import socket
    CACHE_SIZE = 40000
    NUM_OF_THREADS = os.cpu_count()

    BIN_SIZE = CACHE_SIZE // NUM_OF_THREADS // 4 + 1
    # BIN_SIZE = CACHE_SIZE // NUM_OF_THREADS + 1
    BIN_SIZE = CACHE_SIZE
    MAX_AGE = 20000
    figname = "1127vscsi/vscsiSmall.png"
    figname = "vscsiSmall.png"
    classification = False

    mt = MyTimer()
    reader = VscsiReader("../data/trace.vscsi")
    reader = PlainReader("../data/EVA_test1")
    # reader = plainReader("../data/trace.txt2")
    # eva = EVA(cache_size=2000)

    if "EVA_test" in reader.file_loc and "node" not in socket.gethostname():
        if "EVA_test1" in reader.file_loc:
            CACHE_SIZE = 64
            MAX_AGE = 300
            BIN_SIZE = 1
        elif "EVA_test2" in reader.file_loc:
            CACHE_SIZE = 8
            MAX_AGE = 40

        # BIN_SIZE = CACHE_SIZE
        figname = "eva_HRC.png"

    else:
    # p0 = LRUProfiler(reader, cache_size=20000)
    # p0.plotHRC("LRU.png")
    #     reader = vscsiReader("../data/trace.vscsi")
        reader = BinaryReader("../data/trace.vscsi",
                              init_params={"label": 6, "fmt": "<3I2H2Q"})
    p0 = PyGeneralProfiler(reader, LRU, cache_size=CACHE_SIZE, bin_size=BIN_SIZE, num_of_threads=NUM_OF_THREADS)
    p0.plotHRC(figname="LRUSmall.png", no_clear=True, no_save=True, label="LRU")
    mt.tick()

    print(BIN_SIZE)
    print(reader.file_loc)
    p = PyGeneralProfiler(reader, EVA, cache_size=CACHE_SIZE, bin_size=BIN_SIZE, num_of_threads=NUM_OF_THREADS,
                        cache_params={"update_interval": 20000,
                                      "max_age":MAX_AGE,
                                      "enable_classification": classification,
                                      "age_scaling":10,
                                      "dat_name": "smallTest"})
    p.plotHRC(figname=figname, label="EVA")
    mt.tick()


def run_data(dat, LRU_hr=None, cache_size=-1, update_interval=2000, max_age=20000, age_scaling=1, num_of_threads=os.cpu_count()):
    from PyMimircache.bin.conf import get_reader
    # reader = get_reader(dat, dat_type)
    reader = BinaryReader("/home/cloudphysics/traces/{}_vscsi1.vscsitrace".format(dat),
                          init_params={"label":6, "fmt":"<3I2H2Q"})

    CACHE_SIZE = cache_size
    NUM_OF_THREADS = num_of_threads
    # BIN_SIZE = CACHE_SIZE // NUM_OF_THREADS + 1
    BIN_SIZE = CACHE_SIZE // 40 + 1

    if os.path.exists("1127vscsi/{}/EVA_{}_ma{}_ui{}_as{}.png".format(dat, dat, max_age, update_interval, age_scaling)):
        return

    mt = MyTimer()

    if LRU_hr is None:
        profiler_LRU = PyGeneralProfiler(reader, LRU, cache_size=CACHE_SIZE, bin_size=BIN_SIZE, num_of_threads=NUM_OF_THREADS)
        profiler_LRU.plotHRC(figname="1127vscsi/{}/LRU_{}.png".format(dat, dat), no_clear=True, no_save=False, label="LRU")
    else:
        plt.plot(LRU_hr[0], LRU_hr[1], label="LRU")
        plt.legend(loc="best")
    mt.tick()

    p = PyGeneralProfiler(reader, EVA, cache_size=CACHE_SIZE, bin_size=BIN_SIZE, num_of_threads=NUM_OF_THREADS,
                        cache_params={"update_interval": update_interval,
                                      "max_age":max_age,
                                      "enable_classification": False,
                                      "age_scaling":age_scaling,
                                      "dat_name": "noclass_{}_{}_{}".format(dat, update_interval, max_age)})
    p.plotHRC(no_clear=True, figname="1127vscsi/{}/EVA_{}_ma{}_ui{}_as{}_no_class.png".
              format(dat, dat, max_age, update_interval, age_scaling), label="EVA_noclass")
    mt.tick()

    p = PyGeneralProfiler(reader, EVA, cache_size=CACHE_SIZE, bin_size=BIN_SIZE, num_of_threads=NUM_OF_THREADS,
                        cache_params={"update_interval": update_interval,
                                      "max_age":max_age,
                                      "enable_classification": True,
                                      "age_scaling":age_scaling,
                                      "dat_name": "class_{}_{}_{}".format(dat, update_interval, max_age)})
    p.plotHRC(figname="1127vscsi/{}/EVA_{}_ma{}_ui{}_as{}_classification.png".
                format(dat, dat, max_age, update_interval, age_scaling), label="EVA_class")
    mt.tick()




def run2(parallel=True):
    CACHE_SIZE = 80000
    BIN_SIZE = CACHE_SIZE//os.cpu_count()+1
    LRU_HR_dict = {}

    for dat in ["w78", "w92", "w106"]:
        reader = BinaryReader("/home/cloudphysics/traces/{}_vscsi1.vscsitrace".format(dat),
                              init_params={"label":6, "fmt":"<3I2H2Q"})
        profiler_LRU = PyGeneralProfiler(reader, LRU, cache_size=CACHE_SIZE, bin_size=BIN_SIZE,
                                       num_of_threads=os.cpu_count())
        # hr = [1]
        hr = profiler_LRU.get_hit_ratio()
        LRU_HR_dict[dat] = ([i*BIN_SIZE for i in range(len(hr))], hr)

    if not parallel:
        for ma in [20000, 2000, 200000, 2000000]:
            for ui in [2000, 20000, 200000]:
                for age_scaling in [1, 2, 5, 10, 20, 100, 200]:
                    for dat in ["w92", "w106", "w78"]:
                        run_data(dat, LRU_HR_dict[dat], CACHE_SIZE,
                                 update_interval=ui, max_age=ma, age_scaling=age_scaling, num_of_threads=os.cpu_count())
    else:
        max_workers = 12
        with ProcessPoolExecutor(max_workers=max_workers) as ppe:
            futures_to_params = {}
            for ma in [20000, 2000, 200000, 2000000]:
                for ui in [2000, 20000, 200000]:
                    for age_scaling in [1, 2, 5, 10, 20, 100, 200]:
                        for dat in ["w92", "w106", "w78"]:
                            futures_to_params[ppe.submit(run_data, dat, LRU_HR_dict[dat], CACHE_SIZE,
                                        ui, ma, age_scaling, os.cpu_count()//max_workers)] = (ma, ui, age_scaling, dat)

            count = 0
            for i in as_completed(futures_to_params):
                result = i.result()
                count += 1
                print("{}/{}".format(count, len(futures_to_params)), end="\n")



def run_small():
    CACHE_SIZE = 40000
    BIN_SIZE = CACHE_SIZE // os.cpu_count() + 1
    NUM_OF_THREADS = os.cpu_count()

    # reader = vscsiReader("../data/trace.vscsi")
    reader = BinaryReader("../data/trace.vscsi",
                          init_params={"label": 6, "fmt": "<3I2H2Q"}, open_c_reader=False)
    p0 = PyGeneralProfiler(reader, LRU, cache_size=CACHE_SIZE, bin_size=BIN_SIZE, num_of_threads=NUM_OF_THREADS)
    p0.plotHRC(no_clear=True, no_save=True, label="LRU")

    for ma in [2000, 5000, 20000, 30000, 40000]:
        for ui in [1000, 2000, 5000, 20000]:
            for age_scaling in [1, 2, 5, 10, 20, 100]:
                for cls in [True, False]:
                    figname = "1127vscsi0/small/small_ma{}_ui{}_as{}_{}.png".format(ma, ui, age_scaling, cls)
                    if os.path.exists(figname):
                        print(figname)
                        continue
                    p0.plotHRC(no_clear=True, no_save=True, label="LRU")
                    p = PyGeneralProfiler(reader, EVA, cache_size=CACHE_SIZE, bin_size=BIN_SIZE, num_of_threads=NUM_OF_THREADS,
                                        cache_params={"update_interval": ui,
                                                      "max_age": ma,
                                                      "enable_classification": cls,
                                                      "age_scaling": age_scaling,
                                                      "dat_name": "smallTest"})
                    plt.legend(loc="best")
                    p.plotHRC(figname=figname, label="EVA")
                    reader.reset()



if __name__ == "__main__":

    mytest1()

    # run_small()
    # run2()

    # when update interval