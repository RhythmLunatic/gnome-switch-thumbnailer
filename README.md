# gnome-switch-thumbnailer
add thumbnails to Switch games

Only use your own games, don't do illegal stuff, yadda yadda you know the rules.

pip3 install requests numpy opencv-python

Edit nintendo-switch-thumbnailer.py if you want it to run slightly faster at the expense of your precious HDD space.

**Test if the thumbnailer works first before putting it in /usr/bin, don't complain to me without testing it.** First argument is the game file, second argument is the image size, third argument is the output file name. Ex. `./nintendo-switch-thumbnailer.py "Sonic Mania [01009AA000FAA000][v0]" 512 output.png`

Run as root shell:
```bash
cp nintendo-switch.xml /usr/share/mime/packages/
cp nintendo-switch.thumbnailer /usr/share/thumbnailers/
cp nintendo-switch-thumbnailer.py /usr/bin/nintendo-switch-thumbnailer
chmod +x /usr/bin/nintendo-switch-thumbnailer
update-mime-database /usr/share/mime
nautilus -q #if you already had nautilus open
```
