speed=100 # slow ones

for file in `ls -1 *.tex`;
do
    pdflatex $file
    label=`basename $file .tex`
    convert -density 300 -delay $speed -loop 0 -background white -alpha remove ${label}.pdf ${label}.gif
done
rm *.aux
rm *.log
rm *.out
rm *.snm
