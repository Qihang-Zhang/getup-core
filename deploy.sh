python generate_csv.py
python generate_md.py
# mkdocs gh-deploy --force
mkdocs gh-deploy

git add .
git commit -m "$(date +%Y-%m-%d) update"
git push