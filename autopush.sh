python generate_csv.py
python generate_md.py
git add .
git commit -m "$(date +%Y-%m-%d) update"
git push
mkdocs gh-deploy --force