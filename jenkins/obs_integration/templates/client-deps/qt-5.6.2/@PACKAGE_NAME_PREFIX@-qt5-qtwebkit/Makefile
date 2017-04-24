#
# generate meta files from their *.in using prjconf 
# 
# jw, 20170207 initial draught
# jw, 20170213 added /g
#
## convert %define variables from prjconf into sed substitute expressions.

metafiles:
	chmod +w *
	for file in *.in; do \
  	  mv $$file $$(basename $$file .in); \
	done \
