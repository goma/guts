#!/bin/sh
#
#Problem ldc (linear stability analysis)
#=======================================
#Check Eigenvalues from LSA
#
#    baseline values in BLESSED.SOUT file
#for_testing_only     BLESSED_SOUT='./blessed.sout'
#    current values in GOMA_SOUT file
#for_testing_only     GOMA_SOUT='./sout.lsa'
#
# define some scratch files
     TEMP_FILE1='./baseline_egv.$$'
     TEMP_FILE2='./current_egv.$$'
#
## check number of converged eigenvalues; stop if not equalw
  numEV_stat=0
  numEVb=`grep 'converged eigenvalues' $BLESSED_SOUT | cut -d ' ' -f3`
  numEVc=`grep 'converged eigenvalues' $GOMA_SOUT | cut -d ' ' -f3`
     if [ $numEVb -ne $numEVc ]
         then
         numEV_stat=1
         echo " numEVb = $numEVb; numEVc = $numEVc; numEV_stat = $numEV_stat"
     fi

  if [ $numEV_stat -ne 0 ]
      then
      echo "Number of Converged Eigenvalues Differs."

  ## check eigenvalues when number of converged eigenvalues same
  else
        ev_cnt=$numEVb ; ev_stat_sum=0
        regexsci="[0-9]*\\.\\?[0-9]\\+[eE][+-][0-9]*"
        grep "$regexsci i" $BLESSED_SOUT > TEMP_FILE1
        grep "$regexsci i" $GOMA_SOUT > TEMP_FILE2
        
        n=0; emn=$ev_cnt

        while [ $emn -gt 0 ]
        do
          EV_stat=0; nl=`expr $n + 2`
          EVb=`head -$nl TEMP_FILE1 | tail -1 | cut -d ' ' -f2`
          EVc=`head -$nl TEMP_FILE2 | tail -1 | cut -d ' ' -f2`
          if [ $EVb != $EVc ]
            then
            EV_stat=1
          fi
          echo "blessed = $EVb" >> $custom_tests_file
          echo "current = $EVc" >> $custom_tests_file

          if [ $ev_cnt -eq $numEVb ]
             then
             EVL_stat=$EV_stat
          fi

          ev_stat_sum=`expr $ev_stat_sum + $EV_stat`
          n=`expr $n + 1`; emn=`expr $ev_cnt - $n`
        done

#Notes -
#  strings written to file 'extra_test_code.txt' go to results.html/results.txt
#  strings written to file 'custom_tests_file' go to custTests.txt in data directory
        if [ $ev_stat_sum -ne 0 ]
             then
             echo "EVs_differ" > $extra_test_code.txt
             if [ $ev_stat_sum -eq 1 ]
             then
                 echo "     * Eigenvalue Different"
                 echo "$ev_stat_sum Eigenvalue Different; check file sout.lsa" >> $custom_tests_file
             else
                 echo "     * Eigenvalues Different"
                 echo "$ev_stat_sum Eigenvalues Different; check file sout.lsa" >> $custom_tests_file
             fi
        else
             echo "OK" > $extra_test_code.txt
             echo "     * Eigenvalues Identical"
             echo "All Eigenvalues Identical" >> $custom_tests_file
        fi
  fi

# Clean Up Scratch Files
rm TEMP_FILE*
