README.txt

Index
================================
1. Folder Organization.
2. How to run.
3. Understanding output.
4. Understanding map.
================================


1. Folder Organization.

    The submit folder contain "README.txt", "ai.py", "map",
    "output", "teamwork.xlsx", "report.pdf", "visual".

    The "README.txt" is a text file contain some clarify, 
    reduce your spending time to understanding what it is
    and how it works.

    The "report.pdf" is a pdf file contain all contents of
    the group report.

    The "visual" is a directory contain gif file visualize
    the solution for each algorithms.

    The "ai.py" is a python file,   is a core   of this 
    submission, is implemented all needed data structures 
    and algorithms.

    The "map" is a directory contain coded-map-file from 
    stage 1 to 33. Example: map01.txt  is coded for stage 1,
    map22.txt is coded for stage 22,..

    The "output" contain sample output.

    The "teamwork.xlsx" is a file contain list of task and
    who got that job done.


2. How to run.

    In linux, you need to change dir to this folder (contain
    ai.py file),    and be sure that your machine have  been 
    installed python3, for details, I use Python 3.6.3.

    The command is "python3 ai.py <stagenum> <algorithm>"
    without quotes symbol.

    <stagenum>: is number of stage you want to play, it is 
                2-number aligned from 01 to 33
    
    <algorithm>: is a flag of algorithms you want to play
                with, there are three type of algorithms 
                have been implementation.  It is Breadth
                First Search (flag is BFS),  Depth First
                Search (flag is DFS) and Best First Search
                (flag is BEST).
    
    Example:
        - Run stage 01 with Breadth-First-Search algorithm:
            "python ai.py 01 BFS"
        
        - Run stage 02 with Depth-First-Search algorithm:
            "python ai.py 02 DFS"

        - Run stage 03 with Best-First-Search algorithm:
            "python ai.py 03 BEST"

    
3. Understanding output.

    Output contain the map of specified stage and start
    coordinates. ManaBoa is short for ManagedBoard is list
    of special location like "teleport" or "brigdes switch"
    , so on, it will show nothing if this is normal map. 
    After that is a flag specify what algorithms have been
    requested, in case of Breadth-First-Search, it will be
    "Solve BFS". Follow by the Success Road, it visualize 
    how to we get target. In the bottom, it show number 
    step be consumed to be win, and the number of virtual 
    step (is number of traversed nodes/steps).



4. Understanding map.
    
    Map file is introduced in report.pdf

