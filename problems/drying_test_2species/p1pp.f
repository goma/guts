c   This FORTRAN program extended from earlier work written by M.E. Larsen

c   This present form was developed in late Oct and earlier Nov 2021'
c   to be compatible with a Goma model formulated by Chance Parrish and modified by Larsen

c   This program calculates the rms difference between the measured residual
c   solvent mass per area and that calculated by the last Goma run in the directory

c   The 'time.txt' and 'weight.txt' files are those provided by Parrish from experimental
c   measurements except that a few data entries were at at an odd number of seconds in the 
c   the original files. Those data points were eliminated from the data.  The Goma calculation
c   writes every 2 seconds. So odd times do not occur in Goma's output. 

c   'caseStats.dat' is a short file added to each experiment directory that tells the program
c   the duration of the experimental data and the duration of the calculated data (the rms
c   difference can only be calculated up to the lesser of these two so that each 'time.txt'
c   time is guaranteed to be in the calculated file. 'caseStats.dat' also includes the
c   initial film thickness, the initial solvent mass fraction, and the width of the mesh
c   because these all needed to calculate remaining solvent per unit area. 'caseStats.dat'
c   contents were developed by inspecting all the relevant files. In principle, this could
c   be automated by reading everthing from model inputs (but it was simpler just to compile
c   these things by inspection and consolidate them in this file.

c   The only file produced by this code and needed by DAKOTA is 'error.dat' to which
c   the rms disagreement between measurement and calculation is written.  However, 
c    'plotFile.dat' is also produced for convenience. If gnuplot is operable, the residual
c   solvent mass from the most recent version of 'plotFile.dat' can be displayed by executing 
c   the command 'gnuplot -p gplot.plt'.  This can be done while DAKOTA is operating to keep an
c   eye on progress.  The 'remainingSolvent.out' Goma output file is sufficient to generate
c   'error.dat'. But 'plotFile.dat' includes the face temperatures and solvent concentrations.


      program scoreDry
      character*80  sline(6)
      character*16 head1
      character*10 head2
      real calcVals(5000),weights(5000),texps(5000)

      rhoPolymer=1.17 ! gm/cc
      rhoSolvent1=0.866 ! gm/cc
      rhoSolvent2=0.789 ! gm/cc
      nmass=4 ! nmass is a file unit number kind of a hangover from past work
              ! usually unit numbers are just explicit in the open statements

      open(file='caseStats.dat',status='unknown',unit=nmass)
      read(nmass,*) texpmax, tcalcmax
      read(nmass,*) filmThick, solMF1, solMF2, widthMesh
      close(nmass)
      Area=17.34944543
      polyMF=1.0-solMF1-solMF2
      rhoMix=1.0/(solMF1/rhoSolvent1+solMF2/rhoSolvent2
     1 +polyMF/rhoPolymer)
      PolymerMass=filmThick*Area*rhoMix*polyMF
      tbothmax=min(texpmax, tcalcmax)
      open(file='time.txt',status='unknown',unit=nmass)
      do i=1,5000
      read(nmass,*) texps(i)
      if (texps(i).ge.tbothmax)then
      imax=i-1
      goto 100
      end if
      end do
  100 continue
c      print *, imax,texps(i)
      close(nmass)
     
      open(file='weight.txt',status='unknown',unit=nmass)
      do i=1,imax
      read(nmass,*) weights(i)
      end do
      close(nmass)

      rmserror=0.0

c     write out a file convenient for plotting..

      open(file='plotFile.dat',status='unknown',unit=7)
      write(7,*) 'Time Prediction Experiment Tbase Tsurf Cbase  Csurf'

      open(file='remainingSolvent0.out',status='unknown',unit=nmass)
      open(file='remainingSolvent1.out',status='unknown',unit=nmass+1)

      open(file='faceTemps.dat',status='unknown',unit=11)

      open(file='faceCs.dat',status='unknown',unit=12)

      do i=2,imax
      call getVatTime(nmass,texps(i),calcVals(i))
      solventMassPred1=calcVals(i)/widthMesh ! gm / cm ^ 2  predicted sol 1

      call getVatTime(nmass+1,texps(i),calcVals(i))
      solventMassPred2=calcVals(i)/widthMesh ! gm / cm ^ 2  predicted sol 2
      solventMassPred = solventMassPred1+solventMassPred2 ! gm / cm^2 predicted total

      solventMassExp=(weights(i)-PolymerMass)/Area
      rmserror=rmserror+(1.0-solventMassPred/solventMassExp)**2

      call getFaceValues(11,texps(i),Tbase, Tsurf)
      call getFaceValues(12,texps(i),Cbase, Csurf)

      write(7,*)texps(i),solventMassPred,solventMassExp
     1 ,Tbase, Tsurf,Cbase, Csurf
c      print *, rmserror, calcVals(i), weights(i),texps(i)
      end do

      close(nmass)
      close(nmass+1)
      close(7)
     
      open(file='goma_err.dat',status='unknown',unit=nmass)
      write(nmass,*) sqrt(rmserror/(imax-1.0))
      close(nmass)
     
      end
     
      subroutine getVatTime(nunit,t,fval)
      character*80 sline,waste
      logical notFoundYet,timeLine,rightTime
      notFoundYet=.true.
      do while (notFoundYet)
      read(nunit,'(a80)') sline

      timeLine=(sline(1:14).eq.'Time/iteration')
      if (timeLine) then
      read(sline(17:35),*)tval
      rightTime=(tval.eq.t)
      notFoundYet=.not.rightTime
      end if
      end do
c     at this point sline should be the time line at t
      read(nunit,'(a80)') waste
      read(nunit,'(a80)') waste
      read(waste(12:25),*)fval
      end

      subroutine getFaceValues(nfile,xtime,fbase, fsurf)
c     read from nfile until record at xtime is found and return the value at both faces
c     note that the outputs for the face temperatures and face concentrations are identical
c     formats
      timeRecord=-1.0
      do while (timeRecord.lt.xtime)
      call getAFaceRecord(nfile,timeRecord,fbase, fsurf)
      enddo
      return
      end

      subroutine getAFaceRecord(nfile,xtime,fbase, fsurf)
      character*60 rlines(8)
      do i=1,8
      read(nfile,'(a60)') rlines(i)
      enddo
      read(rlines(1)(18:len(rlines(1))),*)xtime
      read(rlines(4),*)x,y,z,fbase
      read(rlines(8),*)x,y,z, fsurf
      return
      end




