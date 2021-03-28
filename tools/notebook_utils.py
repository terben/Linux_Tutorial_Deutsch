import os
import re
import itertools
import nbformat
from nbformat.v4.nbbase import new_markdown_cell

# module for utility functions used by add_navigation_to_lectures.py
# and add_book_info.py

# directory for the lexture and review-question notebooks:
NOTEBOOK_DIR = os.path.join(os.path.dirname(__file__), '..')

# regular expression for lecture notebooks:
LECTURE_REG = re.compile(r'(\d\d)_Shell_(.*)\.ipynb')

# if you change the naming scheme for lecture or review question
# notebooks, you need to modify the variable above and also the
# function 'get_review_notebook'.

# variables for texts in the navigation bars:
PREV_TEMPLATE = "< [Vorherige Lektion]({url}) |"
REV_TEMPLATE = "| [Verständnisfragen zu dieser Lektion]({url}) |"
CURR_TEMPLATE = "| [zur Lektion]({url}) |"
NEXT_TEMPLATE = "| [Nächste Lektion]({url}) >"
NAV_COMMENT = "<!--NAVIGATION-->\n"

# variables to advertise the Linux book:
BOOK_COMMENT = "<!--BOOK_INFORMATION-->"
BOOK_INFO = BOOK_COMMENT + """
<img align="left" style="padding-right:10px;" src="figuren/book_cover_small.jpg"> Dieses Notebook ist Teil eines Begleit-Kurses zu dem im Springer-Verlag erschienenem Buch [Einführung in Unix/Linux für Naturwissenschaftler](http://www.springer.com/de/book/9783662503003)

Das Material wird Ihnen unter der [CC BY  4.0 Lizenz](http://creativecommons.org/licenses/by/4.0/deed.de) zur Verfügung gestellt. Wenn Ihnen der Kurs weiterhilft und Sie mich bei der Erstellung weiterer kostenloser Tutorials unterstützen möchten, überlegen Sie sich bitte, [das Buch zu kaufen](http://www.springer.com/de/book/9783662503003)."""

def prev_this_next(it):
    """
    iterator to gradually return three consecutive elements of
    another iterable. If at the beginning or the end of the iterable,
    None is returned for corresponding elements.
    """
    a, b, c = itertools.tee(it, 3)
    next(c)
    return zip(itertools.chain([None], a), b, itertools.chain(c, [None]))

def get_lecture_notebooks():
    """
    return sorted list of all available lecture notebooks
    """
    return sorted(nb for nb in os.listdir(NOTEBOOK_DIR)
                  if LECTURE_REG.match(nb))

def get_review_notebook(lecture_nb):
    """
    return corresonding review question notebook for
    a given lecture notebook.
    Return 'None' if no revire question notebook is available

    We implicitely assume that there is either no or one
    review question notebook.
    """

    # In the following, we implicitely use the outlined naming schemes
    # for lexture and review question notebooks.

    # The [9:] cuts away the 'xx_Shell_'-part of a notebook name
    lecture_name = lecture_nb[9:]
    review_regex = "Verstaendnisfragen_(.*)_%s" % (lecture_name)

    review_nb = None

    for nb in os.listdir(NOTEBOOK_DIR):
        if(re.search(review_regex, nb)):
           review_nb = nb

    return review_nb

def get_notebook_title(nb_file):
    """
    return the title (main heading) of a given notebook
    """
    nb = nbformat.read(os.path.join(NOTEBOOK_DIR, nb_file), as_version=4)

    for cell in nb.cells:
        if cell.source.startswith('#'):
            return cell.source[1:].splitlines()[0].replace('`', '').strip()

def iter_navbars():
    """
    generator function for the navigation bars for lecture and
    review question notebooks
    """

    for prev_nb, nb, next_nb in prev_this_next(get_lecture_notebooks()):
        lec_navbar = NAV_COMMENT

        # build navigation bar for lecture notebook
        if prev_nb:
            lec_navbar += PREV_TEMPLATE.format(url=prev_nb)

        rev_nb = get_review_notebook(nb)
        if rev_nb:
            lec_navbar += REV_TEMPLATE.format(url=rev_nb)

        if next_nb:
            lec_navbar += NEXT_TEMPLATE.format(url=next_nb)

        # build navigation bar for review question notebook:
        rev_navbar = None
        if rev_nb:
            rev_navbar = NAV_COMMENT

            rev_navbar += CURR_TEMPLATE.format(
                title=get_notebook_title(nb),
                url=nb)

        yield nb, rev_nb, lec_navbar, rev_navbar
