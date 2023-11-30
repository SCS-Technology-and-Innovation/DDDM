# mp4 video
ffmpeg -i formation.avi -c:v mpeg4 formation.mp4

# animated GIF
ffmpeg -r 1 -i formation.mp4 -r 1 "tmp%03d.gif"
gifsicle --delay=5 --loop tmp*.gif > formationLARGE.gif
rm tmp*.gif

# same but with imagemagick (slower, bigger file)
#ffmpeg -r 1 -i formation.mp4 -r 1 "tmp%03d.png"
#convert -delay 5 -loop 0 tmp*.png formation.gif
#rm tmp*.png
