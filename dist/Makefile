ELMANDIR=src/elman/
ELMAN=ext/elman
WAPITIDIR=src/wapiti/
WAPITI=ext/wapiti
PREFIX=/usr/local/
BIN=$(PREFIX)bin/

all : elephant elephant-train

$(ELMAN) :
	cd $(ELMANDIR) ; make
	cp $(ELMANDIR)elman $@
	
$(WAPITI) : 
	cd $(WAPITIDIR) ; make
	cp $(WAPITIDIR)wapiti $@

elephant : src/elephant $(ELMAN) $(WAPITI)
	cp src/elephant .

elephant-train : src/elephant-train elephant
	cp src/elephant-train .
	
install : elephant
	cp elephant $(WAPITI) $(ELMAN) $(BIN)
	
clean :
	rm -f elephant
	rm -rf $(ELMANDIR)elephant $(WAPITIDIR)wapiti
	rm -f ext/*

uninstall :
	rm -f $(BIN)elephant $(BIN)elman $(BIN)wapiti
