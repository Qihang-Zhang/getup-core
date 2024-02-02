python generate_csv.py
python generate_md.py --cut_off 7.75
mkdocs gh-deploy --force

git add .
git commit -m "$(date +%Y-%m-%d) update"
git push
echo "===================================="
echo "Congratulations! Have a nice day!"
echo "===================================="

