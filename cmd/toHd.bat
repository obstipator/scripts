
echo "%*"
set filepath=%*
set filepath=%filepath:"=""%
winscp.exe /console /command "option batch abort" "option confirm off" "open s@192.168.1.180" "lcd %cd%" "put %filepath%" "close" "exit"
