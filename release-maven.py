import os

if not os.path.exists("./repos"):
    print("Please run check-repos script first")
    exit()


def release_repo(repository, release_version,development_version,release_branch,branch_removal,branch_state,release_profile):
    init_dir = os.getcwd()
    short_repo = repository.rsplit('/', 2)[-1]
    name = short_repo.rsplit('.', 1)[-2]
    print("Releasing " + name + "...")
    os.chdir(f"repos/{name}")

    if branch_state == "new-branch":
        os.system(f"git checkout -b {release_branch}")
    elif branch_state == "existing-branch":
        os.system(f"git checkout {release_branch}")

    if release_profile:
        release_profile = "-P" + release_profile

    os.system("mvn -B versions:use-dep-version -DforceVersion=true -Dincludes=com.bombardier.* -DdepVersion=1.0.0")
    os.system("mvn -B versions:use-latest-versions -Dincludes=com.bombardier.* -DallowSnapshots=false versions:update-parent")
    os.system("mvn -B versions:commit")
    os.system('git commit -am "[pre-release] Using latest release dependencies and parent"')

    if name == "master":
        os.system(f"mvn -B -Dtag=MDC-TEST-SA-{release_version} -DreleaseVersion={release_version} -DdevelopmentVersion={development_version} release:prepare release:perform")
    elif name == "gp":
        os.system(f"mvn -B -Dtag=mdc-{release_version} -DreleaseVersion={release_version} -DdevelopmentVersion={development_version} release:prepare release:perform")
    os.system(f"mvn -B -DreleaseVersion={release_version} -DdevelopmentVersion={development_version} release:prepare release:perform")

    os.system(f"mvn -B versions:use-dep-version -DforceVersion=true -Dincludes=com.bombardier.* -DdepVersion=1.0.0-SNAPSHOT")
    os.system(f"mvn -B versions:use-latest-versions -Dincludes=com.bombardier.* -DallowSnapshots=true")
    os.system(f" mvn -B versions:update-parent -DallowSnapshots=true -DparentVersion=1.1.0-SNAPSHOT")
    os.system(f"mvn -B versions:commit &> /dev/null")
    os.system(f'git commit -am "[post-release] Restoring SNAPSHOT dependencies and parent back"')

    if name == "authentication-service":
        os.system("mvn -B clean deploy -Dtests.skip -Dmaven.install.skip=true -Dmaven.test.skip=true -Pansible,adapter-native,adapter-jms,broadcast-jms,broadcast-jca")
    elif name == "notification-gateway":
        os.system("mvn -B deploy -Dtests.skip -Dmaven.install.skip=true -Dmaven.test.skip=true -Pansible")
    os.system("mvn -B deploy - Dtests.skip - Dmaven.install.skip = true - Dmaven.test.skip = true")


    os.system(f"git push --set-upstream origin {release_branch}")

    os.system(f'git checkout master && git merge -m "Merge {release_branch} branch into master" {release_branch}')
    os.system(f'git checkout develop && git merge -m "Merge {release_branch} branch into develop" {release_branch}')

    if branch_removal == "branch-delete":
        os.system(f"git branch -D {release_branch}")
        os.system(f"git push --all && git push --tags && git push --delete origin {release_branch}")
        print("Pushed - Release branch removed.")
    os.system("git push --all && git push --tags")
    print("Pushed - Release branch not removed.")

    print("released.")
    os.chdir(f"{init_dir}")


release_repo("git@gitlab.xyz.net/abc.git", "1.0.6", "1.1.0-SNAPSHOT", "release/7.7", "no-branch-delete", "new-branch")