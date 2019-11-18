import os
import subprocess


def check_repo(repository, branch):
    init_dir = os.getcwd()
    os.mkdir("repos/")
    os.chdir("repos/")
    releasemsg = "[maven-release-plugin] prepare for next development iteration"
    releasemsg2 = "[post-release] Restoring SNAPSHOT dependencies and parent back"

    short_repo = repository.rsplit('/', 2)[-1]
    name = short_repo.rsplit('.', 1)[-2]
    print(name + ":")
    os.system(f"git clone -b {branch} {repository} &> /dev/null")
    os.chdir(f"{name}")
    lastmsg = os.system("git log --pretty='format:%s' | head -n 1 &> /dev/null")
    if releasemsg == lastmsg:
        answer = "NO"
    elif releasemsg2 == lastmsg:
        answer = "NO"
    else:
        answer = "YES"

    print(f"  needs release: {answer}")

    if answer == "YES":
        subprocess.call("git fetch --tags", shell=True)
        cmd = "git describe --tags --abbrev=0"
        lastmsg = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = lastmsg.communicate()
        print("  last tag: " + out.decode('ascii'))

    os.chdir(f"{init_dir}")


def usage():
    script_name = os.path.basename(__file__)
    print(f"Usage: {script_name} REPOSITORY BRANCH")


os.system("rm ./repos -rf")
check_repo("git@gitlab.xyz.net/abc.git", "develop")