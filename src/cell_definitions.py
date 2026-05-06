class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y  # x and y are the position of the cell in the maze
        self.visited = False
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }

    # From subject:
    #     Bit 0(LSB) = North
    #     Bit 1 = East
    #     Bit 2 = South
    #     Bit 3 = West
    #
    # So ?:

    def cell_to_hex(self):
        cell_hex = 0
        if self.walls["N"]:
            cell_hex += 2**0
        if self.walls["E"]:
            cell_hex += 2**1
        if self.walls["S"]:
            cell_hex += 2**2
        if self.walls["W"]:
            cell_hex += 2**3
        cell_hex = format(cell_hex, "X")
        return cell_hex
    # old version
    # def cell_to_hex(self):
    #     cell_hex = 0
    #     if self.walls["N"] == True:
    #         cell_hex += 2**3
    #     if self.walls["E"] == True:
    #         cell_hex += 2**2
    #     if self.walls["S"] == True:
    #         cell_hex += 2**1
    #     if self.walls["W"] == True:
    #         cell_hex += 2**0
    #     cell_hex = format(cell_hex, "X")
    #     # print(cell_hex)
    #     return cell_hex
