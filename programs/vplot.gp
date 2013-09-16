
### size ###

#set size 0.9, 0.9  # makes fonts seem big


### pm3d ###

#set style line 100 lt -1 lw 0.5
#set pm3d solid hidden3d 100
set pm3d 

#set palette rgb 3,5,7
#set palette rgb 30, 31, 32
#set palette defined (0 0 0 1, 1 0.5 0.5 1, 3 1 1 1)  # blue
#set palette rgb 21, 22, 23  # heat colors
#set palette rgb 22,13,-31
set palette rgb 3, 7, 9

### additional pm3d options  ####

set cbrange [5:18]
#unset surface  # surface removes transparency
unset colorbox

### border and orientation ####

#set border 127+256+512  # omit lines at front
set border 4095  # draw a complete box

#set zrange [0:8]
set view 59, 315

### range, title, labels, keys and ticks ###

set xtics 0, 5, 10 # from 0 to 10 by fives
set ytics 0, 5, 10 # from 0 to 10 by fives
set ztics 12, 4, 18 
unset title 
unset key
set xlabel  "X^1" 
set ylabel  "X^2" 


### plot ####

#set term postscript enhanced color
#set output "vfunction.ps"
splot "data.txt" with lines lt -1 lw 0.5

