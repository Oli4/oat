#!/bin/bash
for i in *.ui; do
	[ -f "$i" ] || break
	pyuic5 --from-imports $i --output ${i/.ui/.py};
done
