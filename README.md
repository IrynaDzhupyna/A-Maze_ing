*This project has been created as part of the 42 curriculum by irdzhupy and glegrand*

# DESCRIPTION

### Rules of the project 

- The project must be written in **Python 3.10**.
- The project must adhere to the **flake8** coding standard.


| **Key** | **Description** | **Example** |
| ------ | ----- | ------ |
| WIDTH | Maze width | WIDTH=20 |
| HEIGHT | Maze height | HEIGHT=15 |
| ENTRY | Entry coordinates (x,y) | ENTRY=0,0 |
| EXIT | Exit coordinates (x,y) | EXIT = 19,14 |
| OUTPUT_FILE | Output filename | OUTPUT_FILE=maze.txt |
| PERFECT | is the maze perfect ? | PERFECT=True |

The maze is basically a grid of the following size : width x height.
We set up the following condition :
- width cannot be over 429 cells long
- height cannot be over 429 cells high
- the grid cannot have more than 32000 cells

In order to be able to set up the '42' pattern in our grid, we added as well :
- width cannot be under 7 cells long
- height cannot be under 9 cells high

And the *entry* cell and the *exit* cell cannot be in the 42 pattern.

Example :

| **Key** | **Value** |
| ------- | --------- |
| WIDTH | 20 |
| HEIGHT | 15 |
| ENTRY | 0,0 |
| EXIT | 19,14 |
| PERFECT | True |



```
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A |   |                       |                       |       |           |
+   +   +   +   +---+---+---+   +   +---+   +---+---+   +   +   +---+---+   +
|   |       |   |               |   |   |       |   |       |   |       |   |
+   +---+---+   +   +---+---+---+   +   +---+   +   +---+---+   +   +   +   +
|           |   |   |           |           |   |                   |       |
+---+---+   +   +   +   +---+   +---+---+   +   +---+   +---+---+---+---+   +
|           |   |   |   |           |       |       |           |       |   |
+   +---+---+   +---+   +   +---+---+   +---+---+   +---+---+---+   +   +---+
|   |           |       |           |   |       |           |       |       |
+   +---+   +   +   +---+---+---+   +   +   +---+---+---+   +   +---+---+   +
|       |   |   |   |           |       |           |   |       |           |
+---+   +   +---+   +   +---+   +---+---+---+   +   +   +---+---+   +---+   +
|       |   |       |   |                       |       |           |   |   |
+   +---+   +   +---+   +   +---+---+---+---+---+---+---+   +---+---+   +   +
|       |   |   |   |   |XXX    |XXX     XXX XXX XXX    |           |       |
+---+   +   +   +   +   +---+   +   +---+---+---+---+   +---+---+   +---+---+
|   |   |       |       |XXX|   |XXX|       |    XXX|           |   |       |
+   +   +   +---+   +---+   +   +   +---+   +   +   +---+---+   +   +   +   +
|   |   |   |   |        XXX|XXX|XXX    |XXX XXX|XXX        |   |       |   |
+   +   +   +   +---+   +---+   +---+   +---+---+---+   +---+   +---+---+   +
|       |   |   |       |        XXX|    XXX        |   |       |           |
+   +---+   +   +   +---+   +---+   +---+---+---+   +   +   +---+   +---+   +
|   |   |   |       |   |   |    XXX|    XXX|XXX XXX|               |   |   |
+   +   +   +---+   +   +   +   +---+   +   +   +---+---+---+---+---+   +   +
|   |           |   |   |   |   |       |   |           |               |   |
+   +---+---+   +   +   +   +   +   +---+   +---+---+   +---+---+   +   +   +
|       |   |   |       |   |   |   |       |       |       |       |   |   |
+---+   +   +   +---+---+   +   +   +   +---+   +   +---+   +   +---+---+   +
|   |   |   |               |   |   |   |       |           |   |           |
+   +   +   +   +---+---+---+   +   +   +   +---+---+---+---+   +   +---+---+
|   |   |       |       |   |   |   |       |       |               |       |
+   +   +---+---+   +   +   +   +   +---+---+   +---+   +---+---+---+---+   +
|   |               |   |   |   |   |                   |               |   |
+   +---+---+---+---+   +   +   +   +---+   +---+---+---+   +---+---+   +   +
|                   |   |       |       |   |           |   |       |       |
+   +---+---+---+   +   +---+---+---+   +   +---+   +   +   +   +---+---+   +
|               |                       |           |       |             B |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The maze must be written in the output file using one hexadecimal digit per cell, where each digit encodes which walls are closed:

| **Bit** | **Direction** |
| ------- | ------------- |
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A wall being closed sets the bit to 1, open means 0. We then have 16 different cases from 0000 (all 4 walls are opened) to 1111 (all 4 walls are closed).

### Thinking and buildings

In this chapter, we will describe our ideas, how we proceed and how we code this project.

First of all, a maze is a grid of x * y cells, with x being the *width* and y the *height* of the grid.

Each cell of this grid has 4 bytes, representing the 4 walls of it : north "N", south "S", east "E" and west "W". Every byte has 2 values : either 0 when it's opened (no wall) or 1 when there is a wall. Every cell has as well a unique location, represented as a tuple (x,y).

We can then define a class simply with a class :
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {
            "N": True,
            "S": True,
            "E": True,
            "W": True
        }


# INSTRCUTIONS

The program must be run with the following command :
    `python3 a_maze_ing.py config.txt`

The Makefile should give the following instructions :

    `make install`      #installs the package editable + dev tools
    `make run`          #runs with config.txt
    `make lint`         #flake8 + mypy
    `make lint-strict`  #flake8 + mypy --strict
    `make build`        #produces mazegen-1.0.0-*.wh1 + .tar.gz in dist/
    `make clean`        #removes caches and generated artefacts



# RESSOURCES

this [GitHub](https://github.com/r3dBust3r/42-a-maze-ing)

this [GitHub](https://github.com/M4F-S/Python-/tree/main/course/amazing-maze) as well 

good [article](https://aryanab.medium.com/maze-generation-recursive-backtracking-5981bc5cc766) about Recursive Backtracking Algorithm 

General [overview](https://jbinternational.co.uk/article/view/1366) git team work 

Very useful artcile about the different Git [commands](https://www.datacamp.com/blog/git-commands?utm_cid=19589720821&utm_aid=152984011134&utm_campaign=230119_1-ps-other~dsa-tofu~all_2-b2c_3-emea_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na&utm_loc=9043091-&utm_mtd=-c&utm_kw=&utm_source=google&utm_medium=paid_search&utm_content=ps-other~emea-en~dsa~tofu~blog~data-engineering&gad_source=1&gad_campaignid=19589720821&gclid=CjwKCAjwhqfPBhBWEiwAZo196g58OT_24cZ07ACLZgSU2a4v6nKhyMlkmBGR6xKwfJAo9rTTRHbs3RoCvawQAvD_BwE)

For a better understanding about uv in Python, we used this [article](https://realpython.com/python-uv/)