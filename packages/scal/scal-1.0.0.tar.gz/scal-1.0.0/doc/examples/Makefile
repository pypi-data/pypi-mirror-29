SCL=$(wildcard *.scl)
PDF=$(SCL:.scl=.pdf)

main: $(PDF)

%.tex: %.scl
	../../bin/scal $< > $@

%.pdf: %.tex
	lualatex $<
