# coding=utf-8
"""
this module provides the pyheatmap ploting engine, it is in Python, so it is very slow
it supports both virtual time (fixed number of trace requests) and
real time
it support using multiprocessing to speed up computation
currently, it only support LRU
the mechanism it works is it gets reuse distance from LRUProfiler
currently supported plot type:

        # 1. hit_ratio_start_time_end_time
        # 2. hit_ratio_start_time_cache_size
        # 3. avg_rd_start_time_end_time
        # 4. cold_miss_count_start_time_end_time
        # 5. rd_distribution

This module hasn't been fully optimized and might not get optimized soon
If you want to use this module instead of cHeatmap and
need optimizations, you can do it yourself or contact the author

Author: Jason Yang <peter.waynechina@gmail.com> 2016/08

"""

import pickle
from collections import deque
from multiprocessing import Array, Process, Queue

# this should be replaced by pure python module
from PyMimircache.const import ALLOW_C_MIMIRCACHE
# from PyMimircache.profiler.cHeatmap import get_breakpoints

if ALLOW_C_MIMIRCACHE:
    import PyMimircache.CMimircache.Heatmap as c_heatmap
from PyMimircache.profiler.pyHeatmapSubprocess import *
from PyMimircache.utils.printing import *
from PyMimircache.const import *

import matplotlib.ticker as ticker
import numpy as np
from matplotlib import pyplot as plt




class PyHeatmap:
    def __init__(self):
        # if not os.path.exists('temp/'):
        #     os.mkdir('temp')
        pass

    @staticmethod
    def get_breakpoints(reader, time_mode,
                        time_interval=-1,
                        num_of_pixel_of_time_dim=-1,
                        **kwargs):
        """
        retrieve the breakpoints given time_mode and time_interval or num_of_pixel_of_time_dim,
        break point breaks the trace into chunks of given time_interval

        :param reader: reader for reading trace
        :param time_mode: either real time (r) or virtual time (v)
        :param time_interval: the intended time_interval of data chunk
        :param num_of_pixel_of_time_dim: the number of chunks, this is used when it is hard to estimate time_interval,
                                you only need specify one, either num_of_pixel_of_time_dim or time_interval
        :param kwargs: not used now
        :return: a numpy list of break points begin with 0, ends with total_num_requests
        """

        assert time_interval != -1 or num_of_pixel_of_time_dim != -1, \
            "please provide at least one parameter, time_interval or num_of_pixel_of_time_dim"
        pass


        """
        components down need re-write 
        """


    def _prepare_reuse_distance_and_break_points(self, mode, reader,
                                                 time_interval=-1, num_of_pixels=-1,
                                                 calculate=True, save=False,
                                                 **kwargs):
        reader.reset()

        break_points = []

        if calculate:
            # build profiler for extracting reuse distance (For LRU)
            p = LRUProfiler(reader)
            reuse_dist = p.get_reuse_distance()

            if save:
                # needs to save the data
                if not os.path.exists('temp/'):
                    os.makedirs('temp/')
                with open('temp/reuse.dat', 'wb') as ofile:
                    # pickle.dump(reuse_dist_python_list, ofile)
                    pickle.dump(reuse_dist, ofile)

        else:
            # the reuse distance has already been calculated, just load it
            with open('temp/reuse.dat', 'rb') as ifile:
                # reuse_dist_python_list = pickle.load(ifile)
                reuse_dist = pickle.load(ifile)

            breakpoints_filename = 'temp/break_points_' + mode + str(time_interval) + '.dat'
            # check whether the break points distribution table has been calculated
            if os.path.exists(breakpoints_filename):
                with open(breakpoints_filename, 'rb') as ifile:
                    break_points = pickle.load(ifile)

        # check break points are loaded or not, if not need to calculate it
        if not break_points:
            break_points = CHeatmap.get_breakpoints(reader, mode,
                                                      time_interval=time_interval,
                                                      num_of_pixels=num_of_pixels)
            if save:
                with open('temp/break_points_' + mode + str(time_interval) + '.dat', 'wb') as ifile:
                    pickle.dump(break_points, ifile)

        return reuse_dist, break_points

    def _prepare_multiprocess_params_LRU(self, mode, plot_type, break_points, **kwargs):
        # create the array for storing results
        # result is a dict: (x, y) -> heat, x, y is the left, lower point of heat square

        kwargs_subprocess = {}  # kw dictionary for passing parameters to subprocess
        kwargs_plot = {}  # kw dictionary passed to plotting functions
        if plot_type == "hit_ratio_start_time_cache_size":
            max_rd = max(kwargs['reuse_dist'])
            kwargs_subprocess['max_rd'] = max_rd
            if 'bin_size' in kwargs:
                kwargs_subprocess["bin_size"] = kwargs['bin_size']
            else:
                kwargs_subprocess['bin_size'] = int(max_rd / DEF_NUM_BIN_PROF)

            result = np.zeros((len(break_points) - 1, max_rd // kwargs_subprocess['bin_size'] + 1), dtype=np.float32)
            result[:] = np.nan
            func_pointer = calc_hit_ratio_start_time_cache_size_subprocess
            kwargs_plot['yticks'] = ticker.FuncFormatter(
                lambda x, pos: '{:2.0f}'.format(kwargs_subprocess['bin_size'] * x))
            kwargs_plot['xlabel'] = 'time({})'.format(mode)
            kwargs_plot['ylabel'] = 'cache size'
            kwargs_plot['zlabel'] = 'hit rate'
            kwargs_plot['title'] = "hit rate start time cache size"

            # plt.gca().yaxis.set_major_formatter(
            #     ticker.FuncFormatter(lambda x, pos: '{:2.0f}'.format(kwargs_subprocess['bin_size'] * x)))

        elif plot_type == "hit_ratio_start_time_end_time":
            # (x,y) means from time x to time y
            assert 'reader' in kwargs, 'please provide reader as keyword argument'
            assert 'cache_size' in kwargs, 'please provide cache_size as keyword argument'

            reader = kwargs['reader']
            kwargs_subprocess['cache_size'] = kwargs['cache_size']
            array_len = len(break_points) - 1
            result = np.zeros((array_len, array_len), dtype=np.float32)
            # result[:] = np.nan
            func_pointer = calc_hit_ratio_start_time_end_time_subprocess

            kwargs_plot['xlabel'] = 'time({})'.format(mode)
            kwargs_plot['ylabel'] = 'time({})'.format(mode)
            kwargs_plot['yticks'] = ticker.FuncFormatter(
                lambda x, pos: '{:2.0f}%'.format(x * 100 / len(break_points)))
            kwargs_plot['title'] = "hit_ratio_start_time_end_time"

            last_access = c_heatmap.get_last_access_dist(reader.cReader)
            last_access_array = Array('l', len(last_access), lock=False)
            for i, j in enumerate(last_access):
                last_access_array[i] = j
            kwargs_subprocess['last_access_array'] = last_access_array


        elif plot_type == "avg_rd_start_time_end_time":
            # (x,y) means from time x to time y
            kwargs_plot['xlabel'] = 'time({})'.format(mode)
            kwargs_plot['ylabel'] = 'time({})'.format(mode)
            kwargs_plot['title'] = "avg_rd_start_time_end_time"

            array_len = len(break_points) - 1
            result = np.zeros((array_len, array_len), dtype=np.float32)
            result[:] = np.nan
            func_pointer = calc_avg_rd_start_time_end_time_subprocess

        elif plot_type == "cold_miss_count_start_time_end_time":
            # (x,y) means from time x to time y
            kwargs_plot['xlabel'] = 'time({})'.format(mode)
            kwargs_plot['ylabel'] = 'cold miss count'
            kwargs_plot['title'] = "cold_miss_count_start_time_end_time"
            array_len = len(break_points) - 1
            result = np.zeros((array_len, array_len), dtype=np.float32)
            result[:] = np.nan
            func_pointer = calc_cold_miss_count_start_time_end_time_subprocess

        else:
            raise RuntimeError("cannot recognize plot type")

        kwargs_plot['xticks'] = ticker.FuncFormatter(lambda x, pos: '{:2.0f}%'.format(x * 100 / len(break_points)))

        return result, kwargs_subprocess, kwargs_plot, func_pointer

    def calculate_heatmap_dat(self, reader, mode, plot_type, time_interval=-1, num_of_pixels=-1,
                              algorithm="LRU", cache_params=None, num_of_threads=4, **kwargs):
        """
            calculate the data for plotting heatmap

        :param time_interval:
        :param num_of_pixels:
        :param algorithm:
        :param cache_params:
        :param num_of_threads:
        :param mode: mode can be either virtual time(v) or real time(r)
        :param reader: for reading the trace file
        :param plot_type: the type of heatmap to generate, possible choices are:
        1. hit_ratio_start_time_end_time
        2. hit_ratio_start_time_cache_size
        3. avg_rd_start_time_end_time
        4. cold_miss_count_start_time_end_time
        5. rd_distribution
        6.

        :param kwargs: possible key-arg includes the type of cache replacement algorithms(cache),

        :return: a two-dimension list, the first dimension is x, the second dimension is y, the value is the heat value
        """

        if algorithm == "LRU":
            reuse_dist, break_points = self._prepare_reuse_distance_and_break_points(
                mode, reader, time_interval=time_interval, num_of_pixels=num_of_pixels, **kwargs)

            # create shared memory for child process
            reuse_dist_share_array = Array('l', len(reuse_dist), lock=False)
            for i, j in enumerate(reuse_dist):
                reuse_dist_share_array[i] = j

            result, kwargs_subprocess, kwargs_plot, func_pointer = self._prepare_multiprocess_params_LRU(mode,
                                                                                                         plot_type,
                                                                                                         break_points,
                                                                                                         reuse_dist=reuse_dist_share_array,
                                                                                                         reader=reader,
                                                                                                         **kwargs)

        else:
            assert 'cache_size' in kwargs, "you didn't provide cache_size parameter"
            if isinstance(algorithm, str):
                algorithm = cache_name_to_class(algorithm)

            # prepare break points
            if mode[0] == 'r' or mode[0] == 'v':
                break_points = CHeatmap.get_breakpoints(reader, mode[0],
                                                          time_interval=time_interval,
                                                          num_of_pixels=num_of_pixels)
            else:
                raise RuntimeError("unrecognized mode, it can only be r or v")

            result, kwargs_subprocess, kwargs_plot, func_pointer = self._prepare_multiprocess_params_LRU(mode,
                                                                                                         plot_type,
                                                                                                         break_points,
                                                                                                         reader=reader,
                                                                                                         **kwargs)
            kwargs_subprocess['cache_params'] = cache_params

        # create shared memory for break points
        break_points_share_array = Array('i', len(break_points), lock=False)
        for i, j in enumerate(break_points):
            break_points_share_array[i] = j

        # Jason: memory usage can be optimized by not copying whole reuse distance array in each sub process
        # Jason: change to process pool for efficiency
        map_list = deque()
        for i in range(len(break_points) - 1):
            map_list.append(i)

        q = Queue()
        process_pool = []
        process_count = 0
        result_count = 0
        map_list_pos = 0
        while result_count < len(map_list):
            if process_count < num_of_threads and map_list_pos < len(map_list):
                # LRU related heatmaps
                if algorithm == LRU:
                    p = Process(target=func_pointer,
                                args=(map_list[map_list_pos], break_points_share_array, reuse_dist_share_array, q),
                                kwargs=kwargs_subprocess)
                else:

                    p = Process(target=calc_hit_ratio_start_time_end_time_subprocess_general,
                                args=(map_list[map_list_pos], algorithm, break_points_share_array, reader, q),
                                kwargs=kwargs_subprocess)

                p.start()
                process_pool.append(p)
                process_count += 1
                map_list_pos += 1
            else:
                rl = q.get()
                for r in rl:
                    # print("[{}][{}] = {}".format(r[0], r[1], r[2]))
                    result[r[0]][r[1]] = r[2]
                process_count -= 1
                result_count += 1
            print("%2.2f%%" % (result_count / len(map_list) * 100), end='\r')
        for p in process_pool:
            p.join()

        # old 0510
        # with Pool(processes=self.num_of_threads) as p:
        #     for ret_list in p.imap_unordered(_calc_hit_ratio_subprocess, map_list,
        #                                      chunksize=10):
        #         count += 1
        #         print("%2.2f%%" % (count / len(map_list) * 100), end='\r')
        #         for r in ret_list:  # l is a list of (x, y, hr)
        #             result[r[0]][r[1]] = r[2]

        return result.T, kwargs_plot


    @staticmethod
    def draw_heatmap(xydict, **kwargs):
        if 'figname' in kwargs:
            filename = kwargs['figname']
        else:
            filename = 'heatmap.png'

        masked_array = np.ma.array(xydict, mask=np.isnan(xydict))

        # print(masked_array)
        cmap = plt.cm.jet
        cmap.set_bad('w', 1.)

        if 'fixed_range' in kwargs and kwargs['fixed_range']:
            img = plt.imshow(masked_array, vmin=0, vmax=1, interpolation='nearest', origin='lower',
                             aspect='auto')
        else:
            img = plt.imshow(masked_array, interpolation='nearest', origin='lower', aspect='auto')

        cb = plt.colorbar(img)
        if 'text' in kwargs:
            (length1, length2) = masked_array.shape
            ax = plt.gca()
            ax.text(length2 // 3, length1 // 8, kwargs['text'], fontsize=20)  # , color='blue')

        if 'xlabel' in kwargs:
            plt.xlabel(kwargs['xlabel'])
        if 'ylabel' in kwargs:
            plt.ylabel(kwargs['ylabel'])
        if 'xticks' in kwargs:
            plt.gca().xaxis.set_major_formatter(kwargs['xticks'])
        if 'yticks' in kwargs:
            plt.gca().yaxis.set_major_formatter(kwargs['yticks'])
        if 'title' in kwargs:
            plt.title(kwargs['title'])

        # # # change tick from arbitrary number to real time
        # if 'change_label' in kwargs and kwargs['change_label'] and 'interval' in kwargs:
        #     ticks = ticker.FuncFormatter(lambda x, pos: '{:2.2f}'.format(x * kwargs['interval'] / (10 ** 6) / 3600))
        #     plt.gca().xaxis.set_major_formatter(ticks)
        #     plt.gca().yaxis.set_major_formatter(ticks)
        #     plt.xlabel("time/hour")
        #     plt.ylabel("time/hour")

        # plt.show()
        plt.savefig(filename, dpi=600)
        INFO("plot is saved at the same directory")
        plt.clf()


    @staticmethod
    def draw_3D(xydict, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D

        if 'figname' in kwargs:
            filename = kwargs['figname']
        else:
            filename = 'heatmap_3D.png'

        fig = plt.figure()
        ax = Axes3D(fig)
        # X = np.arange(-4, 4, 0.25)
        X = np.arange(0, len(xydict))
        # Y = np.arange(-4, 4, 0.25)
        Y = np.arange(0, len(xydict[0]))
        X, Y = np.meshgrid(X, Y)
        # R = np.sqrt(X ** 2 + Y ** 2)
        # Z = np.sin(R)
        Z = np.array(xydict).T

        print(X.shape)
        print(Y.shape)
        print(Z.shape)

        # print(X)
        # print(Y)
        # print(Z)

        if 'xlabel' in kwargs:
            ax.set_xlabel(kwargs['xlabel'])
        if 'ylabel' in kwargs:
            ax.set_ylabel(kwargs['ylabel'])
        if 'xticks' in kwargs:
            print("setx")
            ax.xaxis.set_major_formatter(kwargs['xticks'])
        if 'yticks' in kwargs:
            print("sety")
            ax.yaxis.set_major_formatter(kwargs['yticks'])

        ax.plot_surface(X[:, :-3], Y[:, :-3], Z[:, :-3], rstride=10000, cstride=2, cmap=plt.cm.jet)  # plt.cm.hot
        ax.contourf(X, Y, Z, zdir='z', offset=0, cmap=plt.cm.jet)
        ax.set_zlim(0, 1)
        # ax.set_zlim(-2, 2)

        plt.show()
        plt.savefig(filename, dpi=600)

    def __del_manual__(self):
        """
        cleaning
        :return:
        """
        if os.path.exists('temp/'):
            for filename in os.listdir('temp/'):
                os.remove('temp/' + filename)
            os.rmdir('temp/')

    def heatmap(self, reader, mode, plot_type,
                time_interval=-1, num_of_pixels=-1,
                algorithm="LRU", cache_params=None, **kwargs):
        """

        :param time_interval:
        :param num_of_pixels:
        :param algorithm:
        :param cache_params:
        :param plot_type:
        :param mode:
        :param reader:
        :param kwargs: include num_of_threads, figname
        :return:
        """
        reader.reset()

        if mode == 'r' or mode == 'v':
            xydict, kwargs_plot = self.calculate_heatmap_dat(reader, mode, plot_type, algorithm=algorithm,
                                                             time_interval=time_interval, num_of_pixels=num_of_pixels,
                                                             cache_params=cache_params, **kwargs)
        else:
            raise RuntimeError("Cannot recognize this mode, it can only be either real time(r) or virtual time(v), "
                               "but you input %s" % mode)

        kwargs_plot.update(kwargs)
        self.draw_heatmap(xydict, **kwargs_plot)
        reader.reset()

        # self.__del_manual__()



