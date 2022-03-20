import enum


class Status(enum.Enum):
    """
    Enum representing the Status of a position on a goban
    """

    WHITE = 1
    BLACK = 2
    EMPTY = 3
    OUT = 4


class Goban(object):
    def __init__(self, goban):
        self.goban = goban

    def get_status(self, x, y):
        """
        Get the status of a given position

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            a Status
        """
        if (
            not self.goban
            or x < 0
            or y < 0
            or y >= len(self.goban)
            or x >= len(self.goban[0])
        ):
            return Status.OUT
        elif self.goban[y][x] == ".":
            return Status.EMPTY
        elif self.goban[y][x] == "o":
            return Status.WHITE
        elif self.goban[y][x] == "#":
            return Status.BLACK

    def adjacents(self, x, y):
        """
        Get the adjacent positions of (x, y).

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            a list of positions
        """
        positions = (
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1),
        )
        adjacents = [
            pos
            for pos in positions
            if self.get_status(*pos) != Status.OUT
        ]
        return adjacents

    def sibilings(self, x, y):
        """
        Get the adjacents of the same color.

        Args:
            x: the x coordinate
            y: the y coordinate
            stones : internal state, shouldn't be provided

        Returns:
            a set of positions
        """
        color = self.get_status(x, y)
        sibilings = {
            pos
            for pos in self.adjacents(x, y)
            if self.get_status(*pos) == color
        }
        return sibilings

    def shape(self, x, y, stones=None):
        """
        Get all the stones belonging to the shape of the given position.

        Args:
            x: the x coordinate
            y: the y coordinate
            stones : internal state, provided only by recursive calls

        Returns:
            a set of the shape's positions
        """
        if stones is None: stones = set()
        stones.add((x, y))
        for a, b in self.sibilings(x, y) - stones:
            stones |= self.shape(a, b, stones)
        return stones

    def is_free(self, x, y):
        """
        Tells if the stone at (x, y) is free.

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            True if the stone is free, False otherwise.
        """
        free = any(
            self.get_status(*pos) == Status.EMPTY
            for pos in self.adjacents(x, y)
        )
        return free

    def is_taken(self, x, y):
        """
        Tells if the stone at (x, y) is taken.

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            True if the stone is taken, False otherwise.
        """
        taken = not any(
            self.is_free(*pos)
            for pos in self.shape(x, y)
        )
        return taken

