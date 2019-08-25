#!/bin/bash

# Skript, um TiKZ Bilder (im PNG Format) aus LaTeX-Dateien zu erstellen.

# LaTeX-Dateien kompilieren und in PNG umwandeln:
for FILE in *tex
do
  pdflatex ${FILE}

  BASE=$(basename ${FILE} .tex)

  convert -density 600 -flatten ${BASE}.pdf \
          -quality 100 ${BASE}.png

  rm ${BASE}.aux
  rm ${BASE}.log
  rm ${BASE}.pdf
done

# Spezielle Nachbereitung von Figuren:

# Zwei Figuren zur Verzechnisbaum-Navigation zusammenfuegen:
convert Shell_Befehle_Dateisystem_fig4.png \
        Shell_Befehle_Dateisystem_fig5.png \
	+append Shell_Befehle_Dateisystem_fig4_und_5.png 

# Zwei Figuren fuer Verstaendnisfragen zu Lektion 3:
convert Shell_Dateien_Verzeichnisoperationen_fig3.png \
        Shell_Dateien_Verzeichnisoperationen_fig4.png \
	+append Shell_Dateien_Verzeichnisoperationen_fig3_und_4.png 
