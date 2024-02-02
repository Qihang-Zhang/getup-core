## To make the project for your own:
1. delete the `docs/data` folder

2.modify the `mkdocs.yml` file to change the `site_name` and `repo_url` to your own

3. run the following command to generate html and push to github
```shell
bash deploy.sh
```

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



