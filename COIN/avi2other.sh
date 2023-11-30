# mp4 video
ffmpeg -i formation.avi -c:v mpeg4 formation.mp4

# animated GIF
ffmpeg -i formation.avi -t 10 tmp%02d.gif
gifsicle --delay=5 --loop tmp*.gif > formation.gif
rm tmp*.gif
