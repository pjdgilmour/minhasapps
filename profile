export QT_QPA_PLATFORMTHEME=qt5ct
export GTK_CSD=0
export LD_PRELOAD=/usr/local/lib/libgtk3-nocsd.so.0
export GTK_THEME=Irixium
export XAPPLRESDIR="$HOME/.app-defaults"

/usr/libexec/polkit-gnome-authentication-agent-1 &
/usr/bin/gnome-keyring-daemon --start --components=ssh &
/usr/bin/gnome-keyring-daemon --start --components=pksc11 &
/usr/bin/gnome-keyring-daemon --start --components=secrets &
xset m 20/10 4
/usr/bin/xsettingsd &
xrandr --output DP-5 --rotate left -s 1200x1920
~/.fehbg &
/usr/local/bin/xcompmgr -n -c -C -t-5 -l-5 -r4.2 -o.85 &
setxkbmap -layout us -variant intl
