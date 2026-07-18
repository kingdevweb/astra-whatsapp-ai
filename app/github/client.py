"""GitHub API client."""
from app.config import settings
from app.utils.logger import logger

class GitHubClient:
    def __init__(self):
        self._c = None
        if settings.github_pat:
            try:
                from github import Github
                self._c = Github(settings.github_pat); logger.info("✅ GitHub ready")
            except Exception as e: logger.warning(f"GitHub: {e}")

    def read_repo(self, repo: str, path: str = "") -> dict:
        if not self._c: return {"error": "PAT not set"}
        try:
            r = self._c.get_repo(repo)
            if path:
                c = r.get_contents(path)
                if isinstance(c, list): return {"type":"dir","files":[x.path for x in c]}
                import base64
                return {"type":"file","path":c.path,"content":base64.b64decode(c.content).decode("utf-8","replace"),"size":c.size}
            return {"type":"dir","files":[x.path for x in r.get_contents("")]}
        except Exception as e: return {"error": str(e)}

    def create_commit(self, repo: str, path: str, content: str, msg: str) -> dict:
        if not self._c: return {"error": "PAT not set"}
        try: self._c.get_repo(repo).create_file(path, msg, content); return {"status":"created","path":path}
        except Exception as e: return {"error": str(e)}

    def create_pr(self, repo: str, title: str, body: str, head: str, base: str = "main") -> dict:
        if not self._c: return {"error": "PAT not set"}
        try: pr = self._c.get_repo(repo).create_pull(title=title, body=body, head=head, base=base); return {"number":pr.number,"url":pr.html_url}
        except Exception as e: return {"error": str(e)}

    def create_issue(self, repo: str, title: str, body: str = "", labels: list = None) -> dict:
        if not self._c: return {"error": "PAT not set"}
        try: i = self._c.get_repo(repo).create_issue(title=title, body=body, labels=labels or []); return {"number":i.number,"url":i.html_url}
        except Exception as e: return {"error": str(e)}

    def create_release(self, repo: str, tag: str, name: str, body: str = "") -> dict:
        if not self._c: return {"error": "PAT not set"}
        try: r = self._c.get_repo(repo).create_git_release(tag=tag, name=name, message=body); return {"tag":r.tag_name,"url":r.html_url}
        except Exception as e: return {"error": str(e)}

github_client = GitHubClient()
