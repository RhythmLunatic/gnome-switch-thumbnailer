# gnome-switch-thumbnailer
add thumbnails to Switch games

Only use your own games, don't do illegal stuff, yadda yadda you know the rules.

Edit nintendo-switch-thumbnailer.py if you want it to run slightly faster at the expense of your precious HDD space.

Run as root shell:
```bash
cp nintendo-switch.xml /usr/share/mime/packages/
cp nintendo-switch.thumbnailer /usr/share/thumbnailers/
cp nintendo-switch-thumbnailer.py /usr/bin/nintendo-switch-thumbnailer
update-mime-database /usr/share/mime
nautilus -q #if you already had nautilus open
```
