for file in `ls -1 phone*.tex`;
do
    pdflatex $file
    pdflatex $file
done

for file in `ls -1 *.pdf`;
do
    fn=`basename $file .pdf`
    convert -density 300 $file -resize 25% $fn.png
done

rm *.aux
rm *.log
rm *.out

git add *.png
git add *.tex
git commit -m 'phone updates'
