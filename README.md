## To make the project for your own:
```shell
pip install mkdocs
pip install mkdocs-material
```

1. fork the project to your own github account
2. **delete** the `docs/data` folder
3. modify the `mkdocs.yml` file to change the `site_name` and `repo_url` to your own
4. modify the parameter in deploy.sh `cutoff` to what you want, for `generate_md.py`it should be the upper bound of the time you get-up.
```shell
python generate_md.py --cutoff $a float number
```
1. for `generate_csv.py` it should be the lower bound of the time you get-up.
```shell
python generate_csv.py --cutoff $a float number
```
1. run the following command to generate html and push to github

```shell
bash deploy.sh
```
7. set the github page to the `gh-pages` branch

## Frequent Command for MkDocs

### to preview website locally:

```shell
mkdocs serve --watch-theme
```

### to kill preview program:
```shell
ps -fA | grep python
```

### to release website:
```shell
mkdocs gh-deploy
```



