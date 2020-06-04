#!/bin/bash
for i in ui/*.qrc; do
	[ -f "$i" ] || break
	pyrcc5 $i -o ${i/.qrc/_rc.py};
done
