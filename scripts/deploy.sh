python generate_md.py --cutoff 5 \
                      --getup_threshold 7.75 \
                      --recent_days 30 \
                      --name Qihang
                      
mkdocs gh-deploy --force

# git add .
# git commit -m "$(date +%Y-%m-%d) update"
# git push