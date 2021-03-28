import os
import nbformat
from nbformat.v4.nbbase import new_markdown_cell
import notebook_utils as nu

# script to add navigation information to the Linux
# lecture notebooks.
#
# We implicitely assume:
# - lecture notebooks have the naming scheme:
#   XX_Shell_Lecturename.ipynb
#   where XX is a number. Use explicitely 0X for numbers smaller
#   than 10!
# - review question notebooks have the naming scheme:
#   Verstaendnisfragen_zu_Lektion_XX_lecturename.ipynb
# - the notebooks are in the parent directory of pwd.

# resulting notebooks go the the current working directory.

# Here the main script starts:
for lec_nb, rev_nb, lec_navbar, rev_navbar in nu.iter_navbars():
    for curr_nb in lec_nb, rev_nb:
        if curr_nb:
            source = lec_navbar
            if curr_nb == rev_nb:
                source = rev_navbar

            nb_file = os.path.join(nu.NOTEBOOK_DIR, curr_nb)
            nb = nbformat.read(nb_file, as_version=4)

            is_comment = lambda cell: cell.source.startswith(nu.NAV_COMMENT)

            if is_comment(nb.cells[0]):
                print("- amending navbar for {0}".format(curr_nb))
                nb.cells[0].source = source
            else:
                print("- inserting navbar for {0}".format(curr_nb))
                nb.cells.insert(0, new_markdown_cell(source=source))

            if is_comment(nb.cells[-1]):
                nb.cells[-1].source = source
            else:
                nb.cells.append(new_markdown_cell(source=source))

            nbformat.write(nb, curr_nb)
