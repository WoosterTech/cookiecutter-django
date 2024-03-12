import datetime as dt
import os
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

    from github.PullRequest import PullRequest
    from github.Repository import Repository

import git
from github import Github
from jinja2 import Template

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")
GIT_BRANCH = os.getenv("GITHUB_REF_NAME")


def main() -> None:
    """
    Script entry point.
    """
    # Generate changelog for PRs merged yesterday
    merged_date = dt.date.today() - dt.timedelta(days=1)
    if GITHUB_REPO is None:
        raise RuntimeError("No github repo, please set the environment variable GITHUB_REPOSITORY")
    repo = Github(login_or_token=GITHUB_TOKEN).get_repo(GITHUB_REPO)
    merged_pulls = list(iter_pulls(repo, merged_date))
    print(f"Merged pull requests: {merged_pulls}")
    if not merged_pulls:
        print("Nothing was merged, existing.")
        return

    # Group pull requests by type of change
    grouped_pulls = group_pulls_by_change_type(merged_pulls)
    if not grouped_pulls.has_values:
        print("Pull requests merged aren't worth a changelog mention.")
        return

    # Generate portion of markdown
    release_changes_summary = generate_md(grouped_pulls)
    print(f"Summary of changes: {release_changes_summary}")

    # Update CHANGELOG.md file
    release = f"{merged_date:%Y.%m.%d}"
    changelog_path = ROOT / "CHANGELOG.md"
    write_changelog(changelog_path, release, release_changes_summary)
    print(f"Wrote {changelog_path}")

    # Update version
    setup_py_path = ROOT / "setup.py"
    update_version(setup_py_path, release)
    print(f"Updated version in {setup_py_path}")

    # Commit changes, create tag and push
    update_git_repo([changelog_path, setup_py_path], release)

    # Create GitHub release
    github_release = repo.create_git_release(
        tag=release,
        name=release,
        message=release_changes_summary,
    )
    print(f"Created release on GitHub {github_release}")


def iter_pulls(
    repo: Repository,
    merged_date: dt.date,
) -> Iterable[PullRequest]:
    """Fetch merged pull requests at the date we're interested in."""
    recent_pulls = repo.get_pulls(
        state="closed",
        sort="updated",
        direction="desc",
    ).get_page(0)
    for pull in recent_pulls:
        if not isinstance(pull.merged_at, datetime):
            continue
        if pull.merged and pull.merged_at.date() == merged_date:
            yield pull


@dataclass
class GroupedPulls:
    changed:list[PullRequest] = []
    fixed:list[PullRequest] = []
    documentation:list[PullRequest] = []
    updated:list[PullRequest] = []

    def add_pull(self, pull:PullRequest) -> None:
        """Check for pull type and create lists of different types.
        
        Labels:
        - project infrastructure: not worthy of changelog mention (nothing added)
        - update: added to `updated`
        - bug: added to `fixed`
        - docs: added to `documentation`
        - <no match>: added to `changed`
        """
        label_names = {label.name for label in pull.labels}
        if "project infrastructure" in label_names:
            # Don't mention it in the changelog
            return
        if "update" in label_names:
            self.updated.append(pull)
        elif "bug" in label_names:
            self.fixed.append(pull)
        elif "docs" in label_names:
            self.fixed.append(pull)
        else:
            self.changed.append(pull)
        
        return
    
    @property
    def has_values(self) -> bool:
        """Whether there are any pulls in object."""
        named_attributes = [self.changed, self.fixed, self.documentation, self.updated]
        for attribute in named_attributes:
            if len(attribute) > 0:
                return True
        return False

    
    def to_dict(self) -> dict[str, list[PullRequest]]:
        return {"Changed": self.changed, "Fixed": self.fixed, "Documentation": self.documentation, "Updated": self.updated}

def group_pulls_by_change_type(
    pull_requests_list: list[PullRequest],
) -> GroupedPulls:
    """Group pull request by change type."""
    grouped_pulls = GroupedPulls()
    for pull in pull_requests_list:
        grouped_pulls.add_pull(pull)
    return grouped_pulls


def generate_md(grouped_pulls: GroupedPulls) -> str:
    """Generate markdown file from Jinja template."""
    changelog_template = ROOT / ".github" / "changelog-template.md"
    template = Template(changelog_template.read_text(), autoescape=True)
    return template.render(grouped_pulls=grouped_pulls.to_dict())


def write_changelog(file_path: Path, release: str, content: str) -> None:
    """Write Release details to the changelog file."""
    content = f"## {release}\n{content}"
    old_content = file_path.read_text()
    updated_content = old_content.replace(
        "<!-- GENERATOR_PLACEHOLDER -->",
        f"<!-- GENERATOR_PLACEHOLDER -->\n\n{content}",
    )
    file_path.write_text(updated_content)


def update_version(file_path: Path, release: str) -> None:
    """Update template version in setup.py."""
    old_content = file_path.read_text()
    updated_content = re.sub(
        r'\nversion = "\d+\.\d+\.\d+"\n',
        f'\nversion = "{release}"\n',
        old_content,
    )
    file_path.write_text(updated_content)


def update_git_repo(paths: list[Path], release: str) -> None:
    """Commit, tag changes in git repo and push to origin."""
    if GIT_BRANCH is None:
        raise RuntimeError("No git branch set, please set the GITHUB_REF_NAME environment variable")
    repo = git.Repo(ROOT)
    for path in paths:
        repo.git.add(path)
    message = f"Release {release}"

    user = repo.git.config("--get", "user.name")
    email = repo.git.config("--get", "user.email")

    repo.git.commit(
        m=message,
        author=f"{user} <{email}>",
    )
    repo.git.tag("-a", release, m=message)
    server = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
    print(f"Pushing changes to {GIT_BRANCH} branch of {GITHUB_REPO}")
    repo.git.push(server, GIT_BRANCH)
    repo.git.push("--tags", server, GIT_BRANCH)


if __name__ == "__main__":
    main()
