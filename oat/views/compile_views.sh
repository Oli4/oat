#!/bin/bash
for i in *.ui; do
	[ -f "$i" ] || break
	pyuic5 $i --output ${i/.ui/.py};
done
