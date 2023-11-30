speed=150 # slow ones

for file in `ls -1 *.tex`;
do
    if [ "$file" = "alldefs.tex" ]; then
	echo "Skipping the definition file"
    else
	pdflatex $file
	pdflatex $file # twice for internal labels
	label=`basename $file .tex`
	convert -density 300 -delay $speed -loop 0 -background white -alpha remove ${label}.pdf ${label}.gif
    fi
done
rm *.aux
rm *.log
rm *.out
rm *.snm
rm *.nav
rm *.toc
