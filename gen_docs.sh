#!/bin/bash

pdoc --html ./ --force
pdoc --pdf ./ > docs.md
pandoc --metadata=title:"FTC-Music-Player Documentation"            \
           --from=markdown+abbreviations+tex_math_single_backslash   \
           --pdf-engine=xelatex --variable=mainfont:"DejaVu Sans"     \
           --toc --toc-depth=4 --output=docs.pdf  docs.md
