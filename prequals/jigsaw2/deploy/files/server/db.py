import base64
import sqlite3
import traceback
import logging
from typing import Any, Dict

log = logging.getLogger(__name__)


def db_connect(name: str = "jigsaw2.db"):
    return sqlite3.connect(name)


def create_table():
    create_sql = (
        """CREATE TABLE IF NOT EXISTS leaderboard (user TEXT, completion_time REAL)"""
    )
    db_connect().cursor().execute(create_sql)


def check_username(user: str):
    conn = db_connect()
    c = conn.cursor()
    c.execute(
        """
        SELECT COUNT(*) FROM leaderboard 
        WHERE user = ?
    """,
        (user,),
    )

    result = c.fetchone()

    # If the count is 0, then the user does not exist and we return True
    if result[0] == 0:
        return True
    else:
        return False


def generate_identifier(user: str):
    try:
        identifier = repr({"user_name": user})
        identifier = base64.b64encode(bytes(identifier, "utf-8")).decode()
    except Exception:
        raise

    return identifier


def unserialize_identifier(identifier: str):
    identifier = base64.b64decode(bytes(identifier, "utf-8")).decode()
    log.debug(f"{identifier} : {len(identifier)}")

    # So that the attacker can leak size limit and blocked words with locals()
    token_len_max = 27
    token_len = len(identifier)
    forbidden_words = ["import", "exec", "eval", "os", "sys", "popen"]

    if token_len > token_len_max:
        raise UsernameTooLarge
    if any(word in identifier for word in forbidden_words):
        raise Blocked

    unserialized: Dict[str, str] = {}

    # Vulnerable !
    exec(f"unserialized.update({identifier})")

    log.debug(f"Unserialized : {unserialized} ({type(unserialized)})")
    return unserialized


def update_user(user_name: str, user_time: float, return_dict: Dict[str, Any] = {}):
    conn = db_connect()
    c = conn.cursor()
    try:
        # Get the current score
        c.execute(
            "SELECT completion_time FROM leaderboard WHERE user = ?", (user_name,)
        )
        result = c.fetchone()

        if result is None:
            raise UsernameNotFound

        current_score = result[0]

        # If the new score is lower, update the current score
        if user_time < current_score:
            c.execute(
                """
                UPDATE leaderboard 
                SET completion_time = ? 
                WHERE user = ?
            """,
                (user_time, user_name),
            )
            conn.commit()

            return_dict["message"] = f"Score for {user_name} updated to {user_time}"

        else:
            return_dict[
                "message"
            ] = f"New score {user_time} is not better than current score {current_score}"

    except UsernameNotFound as e:
        return_dict["message"] = f"No existing score for {user_name}"
        return_dict["retry"] = True

    except Exception as e:
        return_dict["message"] = f"An error occurred: {e}"

    log.info(return_dict["message"])
    return return_dict


def save_score(user_name: str, user_time: float):
    return_dict: Dict[str, Any] = {"retry": False}
    try:
        identifier = unserialize_identifier(user_name)
        user_name = identifier["user_name"]
    except UsernameTooLarge:
        log.info(f"Username too large")
        return_dict["message"] = "token too large"
        return_dict["retry"] = True
    except Blocked:
        log.info(f"str blocked")
        return_dict["message"] = "blocked str"
        return_dict["retry"] = True
    except KeyError:
        log.info(f"Username not found")
        return_dict["message"] = "username not found"
        return_dict["retry"] = True

    except Exception as e:
        return_dict["message"] = e
        log.info(traceback.format_exc())
        return_dict["retry"] = True

        if not check_username(user_name) or not len(user_name):
            return_dict["message"] = f"Token not valid / User already exists"
        else:
            return_dict = create_user(user_name, user_time, return_dict)

    else:
        return_dict = update_user(user_name, user_time, return_dict)

    return return_dict


def create_user(user_name: str, user_time: float, return_dict: Dict[str, Any] = {}):
    insert_sql = "INSERT INTO leaderboard VALUES (?,?)"
    # insert_sql = f"INSERT INTO leaderboard VALUES ('{user_name}','{user_time}')"
    conn = db_connect()
    conn.cursor().execute(insert_sql, (user_name, user_time))
    # conn.cursor().execute(insert_sql)
    conn.commit()

    return_dict["message"] = f"Welcome {user_name}. Your score is saved !"
    return_dict["token"] = generate_identifier(user_name)
    return return_dict


def get_leaderboard():
    select_sql = """SELECT * FROM leaderboard ORDER BY completion_time ASC"""
    conn = db_connect()
    c = conn.cursor()
    c.execute(select_sql)

    rows = c.fetchall()
    leaderboard: str = "Leaderboard :\nUser |\t Completion time\n"
    for row in rows:
        user, completion_time = row
        user_row = f"{user}:\t {completion_time} seconds"
        leaderboard += user_row + "\n"

    return bytes(leaderboard + "\n\n", "utf-8")


def save_globals():
    return globals().copy()


def restore_globals(saved_globals: Dict[str, Any]):
    globals().clear()
    globals().update(saved_globals.copy())


class UsernameNotFound(Exception):
    """Exception raised for invalid stage numbers."""

    pass


class UsernameTooLarge(Exception):
    """Exception raised for invalid stage numbers."""

    pass


class Blocked(Exception):
    """Exception raised for invalid stage numbers."""

    pass
