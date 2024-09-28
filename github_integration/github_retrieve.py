import github as pygit

auth=pygit.Auth.Token("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")

user_github=pygit.Github(auth=auth)

repo=user_github.get_repo("kargamant/Python_lessons_basic")

commits=repo.get_commits()
for i in commits:
    print(i.commit.committer.date, i.commit.message, i.commit.author.name)
user_github.close()
