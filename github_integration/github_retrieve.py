import github as pygit
import datetime

#to be replaced by data from db
USER_LOGIN="kargamant"
USER_TOKEN="ghu_8HBjRtbYWaiFBRP9Zbac70xiZvmPL43zejrx"
REPO_NAME="kargamant/tst_gh_app"

#activation
auth=pygit.Auth.Token(USER_TOKEN)
user_github=pygit.Github(auth=auth)

user_activity_data={
    'commits_on_previous_week': 0,
    'pull_requests_on_previous_week': 0
    #'code_reviews_on_previous_week': 0
}
today=datetime.datetime.now()
user_name=user_github.get_user(USER_LOGIN).name
repo=user_github.get_repo(REPO_NAME)

for br in repo.get_branches():
    for commit in repo.get_commits(sha=br.commit.sha):
        if commit.committer is None:
            continue
        if commit.commit.author.name==user_name:
            commit_date = commit.commit.committer.date.replace(tzinfo=None)
            user_activity_data['commits_on_previous_week']+=((today-commit_date).days<=7)
for pull in repo.get_pulls():
    if pull.user is None:
        continue
    if pull.user.name==user_name:
        pull_date=pull.created_at.replace(tzinfo=None)
        user_activity_data['pull_requests_on_previous_week']+=((today-pull_date).days<=7)
print(user_activity_data)
user_github.close()
