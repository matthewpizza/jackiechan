#!/usr/bin/env python

import csv
import itertools
import os

"""
Filtering TSVs from IMDB for an actor
https://www.imdb.com/interfaces/
"""

primary_name = 'Jackie Chan'
birth_year = '1954'
category = 'actor'

path = os.path.dirname(os.path.abspath(__file__))
data_path = path + '/data'
filtered_path = path + '/filtered'

names_basics_path = data_path + '/name.basics.tsv'
title_principals_path = data_path + '/title.principals.tsv'
title_basics_path = data_path + '/title.basics.tsv'

nconsts = []

def get_nconst_from_name_and_year(primary_name, birth_year):
    """
    Find a row in the names document for an actor

    Columns:
        nconst primaryName birthYear deathYear primaryProfession knownForTitles

    Args:
        primary_name (str)
        birth_year (str)

    Returns:
        row (str)
    """
    with open(names_basics_path, 'r') as names:
        names = csv.reader(names, delimiter = '\t')
        for row in names:
            if \
                row[1] == primary_name and \
                row[2] == birth_year:

                print 'Found row for ' + primary_name + \
                      ' (' + birth_year + ')'
                print row
                return row

def write_title_principals_with_nconst(nconst, input_path, output_path):
    """
    Filter titles for an actor nconst

    Columns:
        tconst ordering nconst category "job characters"

    Args:
        nconst (str)
        output_path (str)
    """
    with \
        open(input_path, 'r') as principals, \
        open(output_path, 'wb') as out:

        principals = csv.reader(principals, delimiter = '\t')
        out = csv.writer(out, delimiter = '\t')

        # adds column names
        out.writerow(next(principals))

        for principal in principals:
            if \
                principal[2] == nconst and \
                principal[3] == category:
                out.writerow(principal)
    print 'Wrote title.principals for ' + nconst

def get_tconsts_from_filtered_title_principals(input_path):
    """
    Gets the tconsts only

    Args:
        input_path (str)

    Returns:
        tconsts (list)
    """
    tconsts = []

    with open(input_path, 'r') as principals:
        principals = csv.reader(principals, delimiter = '\t')
        for principal in principals:
            tconsts.append(principal[0])

    print 'Found ' + str(len(tconsts) - 1) + ' tconsts'
    return tconsts

def write_title_basics_for_tconsts(tconsts, input_path, output_path):
    """
    Columns:
        tconst titleType primaryTitle originalTitle isAdult startYear endYearruntimeMinutes genres

    Args:
        tconsts (list)
        input_path (str)
        output_path (str)
    """
    with \
        open(input_path, 'r') as basics, \
        open(output_path, 'wb') as out:

        basics = csv.reader(basics, delimiter = '\t')
        out = csv.writer(out, delimiter = '\t')

        # adds column names
        out.writerow(next(basics))

        for row in basics:
            if row[0] in tconsts:
                out.writerow(row)

    print 'Wrote title.basics for ' + str(len(tconsts) - 1) + ' tconsts'

def write_title_principals_for_tconsts(tconsts, input_path, output_path):
    """
    Columns:
        tconst ordering nconst category "job characters"

    Args:
        nconst (str)
        input_path (str)
        output_path (str)
    """
    with \
        open(input_path, 'r') as principals, \
        open(output_path, 'wb') as out:

        principals = csv.reader(principals, delimiter = '\t')
        out = csv.writer(out, delimiter = '\t')

        out.writerow(next(principals))

        for principal in principals:
            if principal[0] in tconsts:
                out.writerow(principal)
                nconsts.append(principal[2])

def write_name_basics_for_nconsts(nconsts, input_path, output_path):
    """
    Columns:
        nconst primaryName birthYear deathYear primaryProfession knownForTitles

    Args:
        nconsts (list)
        input_path (str)
        output_path (str)

    Returns:
        row (str)
    """
    with \
        open(input_path, 'r') as names, \
        open(output_path, 'wb') as out:

        names = csv.reader(names, delimiter = '\t')
        out = csv.writer(out, delimiter = '\t')

        out.writerow(next(names))

        for name in names:
            if (name[0] in nconsts):
                out.writerow(name)

actor = get_nconst_from_name_and_year(primary_name, birth_year)
nconst = actor[0]
nconsts.append(nconst)

filtered_title_principals_path_for_nconst = filtered_path + '/title.principals.' + nconst + '.tsv'
filtered_title_basics_path = filtered_path + '/title.basics.' + nconst + '.tsv'
filtered_name_basic_path = filtered_path + '/name.basics.tsv'
filtered_title_principals_path = filtered_path + '/title.principals.tsv'

write_title_principals_with_nconst(
    nconst,
    title_principals_path,
    filtered_title_principals_path_for_nconst
)

tconsts = get_tconsts_from_filtered_title_principals(filtered_title_principals_path_for_nconst)

write_title_basics_for_tconsts(
    tconsts,
    title_basics_path,
    filtered_title_basics_path
)

write_title_principals_for_tconsts(
    tconsts,
    title_principals_path,
    filtered_title_principals_path
)

write_name_basics_for_nconsts(
    nconsts,
    names_basics_path,
    filtered_name_basic_path
)

print 'Found ' + str(len(list(set(nconsts))) - 1) + ' collaborators'
