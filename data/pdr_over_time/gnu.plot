# time
set xdata time
set timefmt "%s"
set format x "%y-%m-%d %H:%M:%S"

# legend
set ylabel "PDR"
set xlabel "time (UTC)"
set title "00-17-0d-00-00-60-03-82 to 00-17-0d-00-00-38-0f-66 PDR"

# style
set grid
set key font ",15"

# plot
plot "0f-66_03-82" u 1:2 w l notitle
pause -1
