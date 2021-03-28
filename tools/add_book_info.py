import os

import nbformat
from nbformat.v4.nbbase import new_markdown_cell
import notebook_utils as nu

# script to add an advertisement for the Linux book to the lecture
# notebook

# implicit assumptions:
# - the source notebooks are in the parent directory of pwd
# - result notebooks go to pwd

def add_book_info():
    for nb_name in nu.get_lecture_notebooks():
        nb_file = os.path.join(nu.NOTEBOOK_DIR, nb_name)
        nb = nbformat.read(nb_file, as_version=nbformat.NO_CONVERT)

        is_comment = lambda cell: cell.source.startswith(nu.BOOK_COMMENT)

        if is_comment(nb.cells[0]):
            print('- amending comment for {0}'.format(nb_name))
            nb.cells[0].source = nu.BOOK_INFO
        else:
            print('- inserting comment for {0}'.format(nb_name))
            nb.cells.insert(0, new_markdown_cell(nu.BOOK_INFO))

        nbformat.write(nb, nb_name)


if __name__ == '__main__':
    add_book_info()
