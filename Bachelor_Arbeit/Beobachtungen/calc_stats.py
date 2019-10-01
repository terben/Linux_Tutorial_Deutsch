# Sehr einfaches Python Programm zur Berechnung von Mittelwert und
# Standardabweichung einer Textdatei mit einer Zahlenspalte
#
# Wir führen keine wirklichen Tests für die Korrektheit der
# Eingangsdaten durch.

import sys
import os.path as op
import numpy as np

# Wir brauchen zwei Argumente: Die Datei und die Spalte
if len(sys.argv) != 2:
    print("SYNOPSIS: %s file" % (sys.argv[0]))
    sys.exit(1)

data_file = sys.argv[1]
data = np.loadtxt(data_file)

if data.ndim > 1:
    print('Only data with a single column can be processed!')
    sys.exit(1)

print("%s %.5f %.5f" % (op.basename(data_file),
                        np.mean(data), np.std(data, ddof=1)))
