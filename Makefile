# Compiler stuff
CXX = g++
CFLAGS = -g -Wall -std=c++17
PYTHON = python


# Get all necessary files
SRCDIR = src
SRCS = $(wildcard $(SRCDIR)/*.cpp)

OBJDIR = obj
OBJS = $(patsubst $(SRCDIR)/%.cpp, $(OBJDIR)/%.o, $(SRCS))

BINDIR = bin
BIN = $(BINDIR)/main

LIBDIR = /Users/francescomarchisotti/Documents/Uni/Magistrale/Algoritmi/Libs
LIBNAME = algo

DATADIR = data

IMAGESDIR = images


.PHONY: all
all: $(BIN)  ## Build all

# Build binaries
$(BIN): $(OBJDIR) $(OBJS) $(BINDIR)  ## Build binaries
	$(MAKE) -C $(LIBDIR)
	$(CXX) $(CFLAGS) $(OBJS) -L$(LIBDIR)/lib -l$(LIBNAME) -o $@


$(OBJDIR)/%.o: $(SRCDIR)/%.cpp  ## Build object files from sources
	$(CXX) $(CFLAGS) -c $< -o $@


.PHONY: run
run: $(DATADIR)  ## Run all
	@$(BIN)


.PHONY: plot
plot: $(IMAGESDIR)  ## Create plot
	@echo "Making plot"
	@$(PYTHON) $(SRCDIR)/plot.py


# Create directories
$(OBJDIR):  ## Create object files directory
	mkdir $@

$(BINDIR):  ## Create binaries directory
	mkdir $@

$(DATADIR): ## Create output data directory
	mkdir $@

$(IMAGESDIR): ## Create images directory
	mkdir $@


.PHONY: lib
lib:  ## Build library
	$(MAKE) -C $(LIBDIR)


.PHONY: test
test:  ## Build and run tests
	$(MAKE) test -C $(LIBDIR)


# clang-format: https://gist.github.com/dtoma/61468552bbc7c0114b2e700f9247a310
.PHONY: style
style:  ## Run clang-format
	@for src in $(SRCS) ; do \
		echo "Formatting $${src}..." ; \
		clang-format -i "$${src}" ; \
	done
	@echo "Done"

.PHONY: check-style
check-style:  ## Check clang-format
	@for src in $(SRCS) ; do \
		var=`clang-format "$${src}" | diff "$${src}" - | wc -l` ; \
		if [ $${var} -ne 0 ] ; then \
			echo "$${src} does not respect the coding style (diff: $${var} lines)" ; \
			exit 1 ; \
		fi ; \
	done
	@echo "Style check passed"


.PHONY: clean
clean:  ## Clean
	$(RM) -r $(OBJDIR) $(BINDIR) $(DATADIR) $(IMAGESDIR)
	@echo make clean: done


.PHONY: cleanlib
cleanlib:  ## Clean library
	@$(MAKE) clean -C $(LIBDIR)


.PHONY: help
help:  ## Show this message
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)## \(.*\)/\1|||\3/p' \
	| column -t  -s '|||'
