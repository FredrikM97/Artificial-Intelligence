# Makefile for markdown report/presentation

# Following is needed:
	# pandoc
	# pandoc-crossref
	# pandoc-citeproc
CC = ${CC}

# Directory for source md files
source := report
# Directory for pdf output
output := report
# Directory for config files
config := config
# Directory for figures
images := image

doc:
	sed 's/\///g' $(source).md | pandoc \
		-V mainfont="DejaVu Sans" \
		-V fontsize=11pt \
		-V geometry:"top=1.5cm, bottom=2.5cm, left=1.5cm, right=1.5cm" \
		-V geometry:a4paper \
		-V date=`date '+%F'` \
		-V docomentclass=report \
		--toc \
		--number-sections \
		--filter pandoc-citeproc --bibliography=refs.bib --csl $(config)/elsevier-vancouver.csl \
		--include-in-header $(config)/titlesec.tex \
		--extract-media=$(images) \
		-o $(output).pdf
		
pres:
	# Not sure if the sed will work but try
	sed 's/\///g' $(source).md | pandoc \
	-t beamer \
	-V classoption="aspectratio=169" \
	-V colortheme=crane \
	-V theme=CambridgeUS \
	-V fonttheme=serif \
	-V date=`date '+%F'` \
	--filter pandoc-citeproc --bibliography=refs.bib --csl $(config)/elsevier-vancouver.csl \
	--extract-media=$(images) \
	-o $(output).pdf

pres_debug:
	sed 's/\///g' $(source).md | pandoc \
	--verbose \
	-t beamer \
	-V classoption="aspectratio=169" \
	-V colortheme=crane \
	-V theme=CambridgeUS \
	-V fonttheme=serif \
	-V date=`date '+%F'` \
	--filter pandoc-citeproc --bibliography=refs.bib --csl $(config)/elsevier-vancouver.csl \
	--extract-media=$(images) \
	-o $(output).pdf

# Remove all pdf files
clean:
	rm -f $(output)*.pdf

# --include-in-header $(config)/titlesec.tex \
