#!/usr/bin/bash
current=$(xrandr --current --verbose | grep -i brightness | sed 's/.*rightness: //g';)
if  [ $(echo "$current > 0" | bc) -eq 1 ]
then    
    xrandr --output eDP-1 --brightness $(echo "$current - 0.1"| bc)
fi
