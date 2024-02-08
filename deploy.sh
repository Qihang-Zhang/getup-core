python main.py --cutoff 5 \
               --getup_threshold 7.75 \
               --recent_days 30 \
               --name Qihang
mkdocs gh-deploy --force

git add .
git commit -m "$(date +%Y-%m-%d) update"
git push

# below is to print some interesting message, feel free to delete or modify it
clear
echo "==========================================================================="
echo "Morning! Have a nice day!"
echo "==========================================================================="
figlet Morning!
figlet Have a nice day!
echo "==========================================================================="
sleep 2
sl -h
