c   This FORTRAN program extended from earlier work written by M.E. Larsen

c   This present form was developed in late Oct and earlier Nov 2021'
c   to be compatible with a Goma model formulated by Chance Parrish and 
c   modified by Larsen

c   The four specific parameters needed for DAKOTA are given numerical values
c   in the file 'props.incl'. 'props.xxx' is nearly a copy of 'props.incl' lacking
c   only the four variable parameters. This program reads 'props.xxx' parroting it
c   to 'props.incl' except that upon encountering '$$insert' in 'props.xxx' four lines
c   are substituted which are the search parameters.

c   The four lines that specify the search parameters for Goma's input specify
c   values that are scaled from DAKOTA's search parameter so that DAKOTA is dealing 
c   with a search parameter vector with all entries roughly on the order of one.

c   DAKOTA-specifed values are read from 'PARAMETERS.DAK'

      character*12 valueString(9)
      character*180 commandstring,diffusivitystring
      character*40 ds1
      character*14 f1, f2, f3, f4, f5, f6, f7, f8, f9, hinf
      real xs(9)
      np = 7
      open (unit=14,file='PARAMETERS.DAK',status='UNKNOWN')
      read(14,*)commandstring ! trash line
      do i=1,np
        read(14,*)xs(i)
        print *, xs(i)
      end do
      close(14)
c	(line from dakota file) 'k11overgamma' 'k21-Tg1' 'V1' 'epsilon' 'D01' 'chi' 'chi3'

c     write scaled DAKOTA values to strings...
      write(f1,'(E10.5)')xs(1)*2.21e-3
      write(f2,'(F10.5)')xs(2)*(-103.0)
      write(f3,'(E10.5)')xs(3)*1.0
      write(f4,'(E10.5)')xs(4)*1.0
      write(f5,'(E10.5)')xs(5)*3.988e-4
      write(f6,'(E10.5)')xs(6)*0.738
      write(f7,'(E10.5)')xs(7)*0.738

      f1=adjustl(f1) ! remove the leading blanks
      f2=adjustl(f2)
      f3=adjustl(f3)
      f4=adjustl(f4)
      f5=adjustl(f5)
      f6=adjustl(f6)
      f7=adjustl(f7)

      open (unit=15,file='props.fixed',status='UNKNOWN')
      open (unit=16,file='props.incl',status='UNKNOWN')
      do i=1,600
      read(15,'(a180)',END=200) commandstring
      write(16,'(a180)') commandstring
      if ('$$insert'.eq.commandstring(1:8)) then
 
c     write Aprero-recognized strings specifying the search parameters
      write(16,'(a60)')adjustl('$  {k11_1 = '//f1//'} cm3/g/K')
      write(16,'(a60)')adjustl('$  {k21_1 = '//f2//'} kelvin')
      write(16,'(a60)')adjustl('$  {V1_crit_1 = '//f3//' } cm3/g')
      write(16,'(a60)')adjustl('$  {eps_12 = '//f4//' }')
      write(16,'(a60)')adjustl('$  {D_12 = '//f5//'} cm2/s')
      write(16,'(a60)')adjustl('$  {chi2 = '//f6//'}')
      write(16,'(a60)')adjustl('$  {chi3 = '//f7//'}')      
      endif
      end do
  200 continue
      close(15)
      close(16)
	end

