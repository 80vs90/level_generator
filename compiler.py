from array import array
import argparse
import sys


class LevelSyntaxError(Exception):
    pass


class Block(object):
    def __init__(self, char):
        self.char = char

    def to_bin(self):
        return ord(self.char)

    def __repr__(self):
        return "Block: %s" % self.char


def cleanup_rows(rows):
    """
    Remove blank rows and strip all whitespace from the rest.
    """
    new_rows = []

    for row in rows:
        stripped_row = row.replace(' ', '')
        if len(stripped_row) == 0:
            continue

        new_rows.append(stripped_row)

    return new_rows


def parse_level(level):
    rows = level.splitlines()
    try:
        [x, y, z] = [int(dim) for dim in rows.pop(0).split()]
    except ValueError:
        raise LevelSyntaxError("x y and z dimensions must be specified at top of file")

    level_ast = []  # More of an abstract syntax array, really...

    current_layer = []
    for i, row in enumerate(cleanup_rows(rows), start=1):
        if len(row) != x:
            raise LevelSyntaxError("All rows must be the specified %d blocks wide" % x)

        row_array = []
        for char in row:
            row_array.append(Block(char))

        current_layer.append(row_array)

        if i % y == 0:  # time to start a new layer
            level_ast.append(current_layer)
            current_layer = []

    if len(level_ast[len(level_ast) - 1]) != y:
        raise LevelSyntaxError("All layers must be the specified %d blocks tall" % y)

    if len(level_ast) != z:
        raise LevelSyntaxError("There must be the specified % layers" % z)

    return {'x': x, 'y': y, 'z': z, 'ast': level_ast}


def compile_level(ast):
    binary_out = []
    binary_out.extend([76, 86, 76])  # Magic bytes: LVL
    binary_out.extend([ast['x'], ast['y'], ast['z']])
    for layer in ast['ast']:
        binary_out.append(76)
        for row in layer:
            binary_out.append(82)
            for block in row:
                binary_out.append(block.to_bin())
    return array('i', binary_out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse levels into binary representation.')
    parser.add_argument('infile', type=str, nargs=1)
    parser.add_argument('outfile', type=str, nargs=1)

    args = parser.parse_args()

    with open(args.infile[0], 'r') as level:
        try:
            level_ast = parse_level(level.read())
        except LevelSyntaxError as e:
            print "Error: %s" % e
            sys.exit(1)

    with open(args.outfile[0], 'wb') as bin_file:
        compile_level(level_ast).tofile(bin_file)
