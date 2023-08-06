#!/bin/bash

cd "$(dirname "$0")"

rm parts.*.lst
./make-list -d
mv parts.lst parts.description.lst
./make-list -n
mv parts.lst parts.number.lst

