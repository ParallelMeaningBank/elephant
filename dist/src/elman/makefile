#CC = x86_64-linux-g++-4.6
CC = g++
CFLAGS = -lm -O2 -Wall -funroll-loops -ffast-math
#CFLAGS = -lm -O2 -Wall

all: rnnlmlib.o elman

rnnlmlib.o : rnnlmlib.cpp
	$(CC) $(CFLAGS) $(OPT_DEF) -fopenmp -c rnnlmlib.cpp

elman : elman.cpp
	$(CC) $(CFLAGS) $(OPT_DEF) -fopenmp elman.cpp rnnlmlib.o -o elman

clean:
	rm -rf *.o elman
