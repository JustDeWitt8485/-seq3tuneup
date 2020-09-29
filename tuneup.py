#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = """Tracy DeWitt,
https://docs.python.org/3/library/timeit.html,
https://youtu.be/FsAPt_9Bf3U,
https://youtu.be/KlBPCzcQNU8,
https://docs.python.org/3/library/profile.html,
Manuel Velasco
"""

import cProfile
import pstats
import timeit
from collections import Counter


# raise NotImplementedError("Complete this decorator function")
# Decorator func
def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    # Be sure to review the lesson material on decorators.
    # You need to understand how they are constructed and used.

    # Inner func
    def wrapper_func(*args, **kwargs):
        pro = cProfile.Profile()
        pro.enable()
        result = func(*args, **kwargs)
        pro.disable()
        pro_stats = pstats.Stats(pro).sort_stats("cumulative")
        pro_stats.print_stats()
        return result

    return wrapper_func


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    # Not optimized
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates

#
# Students: write a better version of find_duplicate_movies
#


def optimized_find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    # Optimized
    # movies = read_movies(src)
    # movie_dict = {}
    # duplicates = []
    # for movie in movies:
    #     if movie not in movie_dict:
    #         movie_dict[movie] = 1
    #     else:
    #         duplicates.append(movie)
    # return duplicates

    movies = read_movies(src)
    movie_counter = Counter(movies)
    duplicates = [movie for movie, x in movie_counter.items() if x > 1]
    return duplicates


def timeit_helper(func_name, func_param):
    """Part A: Obtain some profiling measurements using timeit"""
    assert isinstance(func_name, str)
    stmt = func_name + "('"+func_param+"')"
    setup = "from __main__ import  find_duplicate_movies,\
            optimized_find_duplicate_movies"
    t = timeit.Timer(stmt, setup)
    runs_per_repeat = 3
    num_repeats = 5
    result = t.repeat(repeat=num_repeats, number=runs_per_repeat)
    # print(result)
    avg = map(lambda x: x/3, result)
    min_list = list(avg)
    # print(min_list)
    time_cost = min(min_list)
    print(f"func={func_name}  num_repeats={num_repeats}\
        runs_per_repeat={runs_per_repeat} time_cost={time_cost:.3f} sec")
    return t


def main():
    """Computes a list of duplicate movie entries."""
    # Students should not run two profiling functions at the same time,
    # e.g. they should not be running 'timeit' on a function that is
    # already decorated with @profile

    filename = 'movies.txt'

    print("--- Before optimization ---")
    result = find_duplicate_movies(filename)
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))

    print("\n--- Timeit results, before optimization ---")
    timeit_helper('find_duplicate_movies', filename)

    print("\n--- Timeit results, after optimization ---")
    timeit_helper('optimized_find_duplicate_movies', filename)

    print("\n--- cProfile results, before optimization ---")
    profile(find_duplicate_movies)(filename)

    print("\n--- cProfile results, after optimization ---")
    profile(optimized_find_duplicate_movies)(filename)


if __name__ == '__main__':
    main()
    print("Completed.")
