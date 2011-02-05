import codeop
import git

class CoreRepo(object):
    def __init__(self, path):
        self.repo = git.Repo(path)

    def getClass(self, class_name, ref_age = 0):
        return self.repo.commits(class_name, max_count=1, skip=ref_age)[0]

    def getBranch(self, class_name, branch_name):
        return self.getClass(class_name).tree[branch_name + ".py"]

    def getMethod(self, class_name, method_name):
        source = self.getBranch(class_name, method_name).data
        return codeop.compile_command(source)
