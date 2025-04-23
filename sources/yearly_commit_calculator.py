from asyncio import sleep, Semaphore, gather
from json import dumps
from datetime import datetime
from typing import Dict, Tuple

from manager_download import DownloadManager as DM
from manager_environment import EnvironmentManager as EM
from manager_github import GitHubManager as GHM
from manager_file import FileManager as FM
from manager_debug import DebugManager as DBM


async def calculate_commit_data(repositories: Dict) -> Tuple[Dict, Dict]:
    """
    Calculate commit data by years.
    Commit data includes contribution additions and deletions in each quarter of each recorded year.

    :param repositories: user repositories info dictionary.
    :returns: Commit quarter yearly data dictionary.
    """
    DBM.i("Calculating commit data...")
    if EM.DEBUG_RUN:
        content = FM.cache_binary("commits_data.pick", assets=True)
        if content is not None:
            DBM.g("Commit data restored from cache!")
            return tuple(content)
        else:
            DBM.w("No cached commit data found, recalculating...")

    yearly_data, date_data = dict(), dict()

    # limit concurrency to 10 repos at once with a semaphore
    sem = Semaphore(10)  # keep well below the 100-request cap

    async def _safe_update(r):
        if r["name"] not in EM.IGNORED_REPOS:
            repo_name = "[private]" if r["isPrivate"] else f"{r['owner']['login']}/{r['name']}"
            DBM.i(f"\tRetrieving repo: {repo_name}")
            async with sem:
                await update_data_with_commit_stats(r, yearly_data, date_data)

    await gather(*[_safe_update(r) for r in repositories])
    DBM.g("Commit data calculated!")

    if EM.DEBUG_RUN:
        FM.cache_binary("commits_data.pick", [yearly_data, date_data], assets=True)
        FM.write_file("commits_data.json", dumps([yearly_data, date_data]), assets=True)
        DBM.g("Commit data saved to cache!")
    return yearly_data, date_data


async def update_data_with_commit_stats(repo_details: Dict, yearly_data: Dict, date_data: Dict):
    """
    Updates yearly commit data with commits from given repository.
    Skips update if the commit isn't related to any repository.

    :param repo_details: Dictionary with information about the given repository.
    :param yearly_data: Yearly data dictionary to update.
    :param date_data: Commit date dictionary to update.
    """
    owner = repo_details["owner"]["login"]
    code_weeks = await DM.get_repo_code_freq(owner, repo_details["name"])
    if not code_weeks:
        DBM.w("\t\tStats not (yet) available, skipping repo.")
        return

    # code_weeks -> [ts, add, del]  | convert to your quarterly structure
    for week_ts, add, delete in code_weeks:
        dt = datetime.utcfromtimestamp(week_ts)
        curr_year = dt.year
        quarter = (dt.month - 1) // 3 + 1
        lang = (repo_details["primaryLanguage"] or {}).get("name", "Unknown")
        yearly_data \
            .setdefault(curr_year, {}) \
            .setdefault(quarter, {}) \
            .setdefault(lang, {"add": 0, "del": 0})
        yearly_data[curr_year][quarter][lang]["add"] += add
        yearly_data[curr_year][quarter][lang]["del"] += abs(delete)

        date = dt.strftime("%Y-%m-%d")
        if repo_details["name"] not in date_data:
            date_data[repo_details["name"]] = dict()
        if lang not in date_data[repo_details["name"]]:
            date_data[repo_details["name"]][lang] = dict()
        date_data[repo_details["name"]][lang][dt.strftime("%Y-%m-%d")] = dt.strftime("%Y-%m-%d")
