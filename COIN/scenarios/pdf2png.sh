for file in `ls -1 *.pdf`;
do
    fn=`basename $file .pdf`
    convert -density 300 $file -resize 25% $fn.png
done
