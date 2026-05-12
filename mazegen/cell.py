# Cell class
# internal building blocks

class Cell:
    """Represents a single cell in the maze grid.

    Attributes:
        x (int): Colum position of the cell
        y (int): Row position of the cell.
        visited (bool): Whether the cell has been visited during generation.
        walls (dict): Dictionary of wall states
        for each directions (N, E, S, W).
    """

    def __init__(self, x: int, y: int) -> None:
        """Initializes the cell and set all walls to True (closed)

        Args:
            x (int): Colum position of the cell
            y (int): Row position of the cell.
        """
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }

    def cell_to_hex(self) -> str:
        """Converts cell wall states to a hexadecimal character.

        Returns:
            str: A single hex char representing the cell's wall configuration
        """
        cell_hex = 0

        if self.walls["N"]:
            cell_hex += 2**0
        if self.walls["E"]:
            cell_hex += 2**1
        if self.walls["S"]:
            cell_hex += 2**2
        if self.walls["W"]:
            cell_hex += 2**3
        cell_hex_str = format(cell_hex, "X")

        return cell_hex_str
