#!/bin/bash

# Skript, um TiKZ Bilder (im PNG Format) aus LaTeX-Dateien zu erstellen.

# LaTeX-Dateien kompilieren und in PNG umwandeln:
for FILE in *tex
do
  pdflatex ${FILE}

  BASE=$(basename ${FILE} .tex)

  convert -density 600x600 -flatten ${BASE}.pdf \
          -quality 90 -resize 800x600 ${BASE}.png

  rm ${BASE}.aux
  rm ${BASE}.log
  rm ${BASE}.pdf
done

# Spezielle Nachbereitung von Figuren:

# Zwei Figuren zur Verzechnisbaum-Navigation zusammenfuegen:
convert Shell_Befehle_Dateisystem_fig4.png \
        Shell_Befehle_Dateisystem_fig5.png \
	+append Shell_Befehle_Dateisystem_fig4_und_5.png 
