MAKE    =       gmake
SHELL   =       /bin/sh
APREPRO =       aprepro
EXO1EXO2=       ex1ex2v2
FASTQ   =       fastq
GJOIN   =       gjoin
GEN3D   =       gen3d
GREPOS  =       grepos
GROPE   =       grope
RM      =       rm -f

RANLIB  =       /bin/true
CODENAME=	goma

all:
	@echo "Go ahead... make my day."

default:	update

update:
		@$(MAKE) -$(MAKEFLAGS) \
		exec

exec: $(CODENAME)


$(CODENAME):    $(CODENAME).o $(LIBS)
	$(CC) $(CODENAME).o $(LIBS) $(EXO2) $(NETCDF) $(XTRALIBS) -o $@


$(CODENAME).o:
	cp ../src/coyote.o .


elo_dom1.gen: dom1.gen dom1.g3d Defs
	gen3d -aprepro dom1.gen elo_dom1.gen <dom1.g3d

elo_dom2.gen: dom2.gen dom2.g3d Defs
	gen3d -aprepro dom2.gen elo_dom2.gen <dom2.g3d

elo_domain.gen: elo_dom1.gen elo_dom2.gen gjoin.inp
	gjoin < gjoin.inp

dom1.fas: Defs
dom2.fas: Defs

clean:
	-rm -f *~ *.BAK *.o core *FNT nc* tmp* stderr stdout


realclean:
	$(MAKE) clean
	-rm -f input *.ps *.exoII *_o.*


# Ought to use "makedepend" with APREPRO instead of cpp...

geom1d.fas:	Defs
	touch $@

.gen.exoII:
	$(EXO1EXO2) $*.gen $*.exoII

.fas.exoII: 
	$(RM) $@
	$(FASTQ) -aprepro -mesh=$*.gen $*.fas
	$(EXO1EXO2) $*.gen $*.exoII

.fas.gen:
	$(RM) $@
	$(FASTQ) -aprepro -mesh=$*.gen $*.fas

.apj.fas:
	aprepro $*.apj > $*.fas
	
.sia.sin:
	aprepro $*.sia > $*.sin

.gap.gmi:
	$(APREPRO) $*.gap >$*.gmi

#.defs.fas:
#	touch $@
#	$(MAKE) $*.exoII


.SUFFIXES: .exoII .gen .input .fas .gmi .gap .apj .sin .sia
