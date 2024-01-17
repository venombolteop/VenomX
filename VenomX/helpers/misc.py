import asyncio
import shlex
import socket
from typing import Tuple

import dotenv
import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from config import BRANCH, GIT_TOKEN, HEROKU_API_KEY, HEROKU_APP_NAME, REPO_URL
from VenomX import LOGGER

HAPP = None

XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "my heroku",
    "push",
    str(HEROKU_API_KEY),
    "https",
    str(HEROKU_APP_NAME),
    "HEAD",
    "play",
]

def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())

def git():
    REPO_LINK = REPO_URL
    if GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{GIT_USERNAME}:{GIT_TOKEN}@{TEMP_REPO}"
    else:
        UPSTREAM_REPO = REPO_URL

    try:
        repo = Repo()
        LOGGER("VenomX").info(f"Git Client Found")
    except GitCommandError:
        LOGGER("VenomX").info(f"Invalid Git Command")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(
            BRANCH,
            origin.refs[BRANCH],
        )
        repo.heads[BRANCH].set_tracking_branch(origin.refs[BRANCH])
        repo.heads[BRANCH].checkout(True)
        try:
            repo.create_remote("origin", REPO_URL)
        except BaseException:
            pass
        nrs = repo.remote("origin")
        nrs.fetch(BRANCH)
        try:
            nrs.pull(BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        install_req("pip3 install --no-cache-dir -U -r requirements.txt")
        LOGGER("VenomX").info("Fetched Latest Updates")

def is_my_hero():
    return "heroku" in socket.getfqdn()

def heroku():
    global HAPP
    if is_my_hero():
        if HEROKU_API_KEY and HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(HEROKU_API_KEY)
                HAPP = Heroku.app(HEROKU_APP_NAME)
                LOGGER("VenomX").info(f"Heroku App Configured")
            except BaseException as e:
                LOGGER("My Heroku").error(e)
                LOGGER("My Heroku").info(
                    f"Make sure your HEROKU_API_KEY and HEROKU_APP_NAME are configured correctly in the heroku config vars."
                )
async def in_heroku():
     return "heroku" in socket.getfqdn()

async def create_botlog(client):
    if HAPP is None:
        return

    LOGGER("VenomX").info(
        "WAIT A MOMENT. I'M CREATING A USERBOT LOG GROUP FOR YOU"
    )
    desc = "Group Log for VenomX-UserBot.\n\nPLEASE DO NOT LEAVE THIS GROUP.\n\n✨ Powered By ~ @venomowners ✨"
    try:
        loggroup = await client.create_supergroup("UserBot Log", desc)
        if await in_my_hero():
            heroku_var = HAPP.config()
            heroku_var["BOTLOG_CHATID"] = grouplog.id
        else:
            path = dotenv.find_dotenv("config.env")
            dotenv.set_key(path, "BOTLOG_CHATID", loggroup.id)
    except Exception:
        LOGGER("VenomX").warning(
            "Your BOTLOG_CHATID var has not been filled in. Create a telegram group and enter the bot @MissRose_bot then type /id. Enter the group ID in var BOTLOG_CHATID"
        )
