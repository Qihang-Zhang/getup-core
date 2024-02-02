python generate_csv.py --cutoff 5
python generate_md.py --cutoff 7.75
mkdocs gh-deploy --force

git add .
git commit -m "$(date +%Y-%m-%d) update"
git push
clear
echo "==========================================================================="
figlet Morning!
figlet Have a nice day!
echo "==========================================================================="
sleep 2
sl -h
