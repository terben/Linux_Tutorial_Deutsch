# script to convert standalone TIkZ PDFs into PNGs with white background:

# $1: The PDF to convert

FILE=$1
BASE=$(basename ${FILE} .pdf)

convert -density 600x600 -flatten ${FILE} \
        -quality 90 -resize 800x600 ${BASE}.png
