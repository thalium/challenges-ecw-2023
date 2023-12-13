import os
import socketserver
import select
import logging
import traceback
import questions as q
import time
import db


log = logging.getLogger(__name__)


WELCOME = b"Welcome ! If you want to leave alive, you'll have to answer correctly to all my questions !\n"

FLAG1 = "ECW{J1GS4W_R3TURNS}"
FLAG2 = "ECW{N0T_SC3R3D_Y3T}"
FLAG3 = "ECW{R4ND0M_ST3G4N0}"

TIMER = 3

QUESTION_FLAG1 = 4
QUESTION_FLAG2 = 7


NEXT = "\n\nNext question\n"
CONGRATULATIONS = f"Congratulations for the first steps. Your first flag is : {FLAG1}\n"
CONGRATULATIONS2 = f"Well done ! Here is your flag : {FLAG2} \n"
CONGRATULATIONS3 = f"You've done it ! The last flag is : {FLAG3}\n"


QUESTION_COUNT = 10

GAME_OVER = b"Wrong answer, bye bye\n"
TIMED_OUT = f"Game over!\nYou did not respond in {TIMER} sec\n"
PARSE_ERROR = b"Banned characters\nbye bye\n"


###########################################
############### TCP HANDLER ###############
###########################################


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        configure_logging()
        log.info(f"Handling player")
        start_time = time.time()
        stage = 0
        log.debug(f"{WELCOME}")
        self.request.sendall(WELCOME)
        questions_handler = q.Questions()
        try:
            while True:
                # give a flag for each flag question passed :
                if stage == QUESTION_FLAG1:
                    self.request.sendall(bytes(CONGRATULATIONS, "utf-8"))
                if stage == QUESTION_FLAG2:
                    self.request.sendall(bytes(CONGRATULATIONS2, "utf-8"))
                if stage == QUESTION_COUNT:
                    self.request.sendall(bytes(CONGRATULATIONS3, "utf-8"))
                    completion_time = time.time() - start_time
                    self.final(completion_time)
                    break
                # Send question
                question = questions_handler.ask(stage)
                log.debug(f"Sending question :\n{question}")
                self.request.sendall(question)
                # Waiting TIMER seconds before timeout-ing the session
                ready_to_read, _, _ = select.select([self.request], [], [], TIMER)

                if ready_to_read:
                    response = self.request.recv(1024)
                    log.info(f"Received {response}")

                    if questions_handler.check(response):
                        log.info(f"Correct answer")
                        stage += 1

                    else:
                        log.info(f"Wrong answer.")
                        raise q.WrongAnswer

                else:
                    raise TimeoutError

        except q.ParseError:
            self.request.sendall(PARSE_ERROR)
        except TimeoutError:
            self.request.sendall(bytes(TIMED_OUT, "utf-8"))
        except q.WrongAnswer:
            self.request.sendall(GAME_OVER)

        except Exception:
            log.error(traceback.format_exc())
        self.request.sendall(db.get_leaderboard())

    def final(self, completion_time: float):
        ask_user = b"Please give your username for the leaderboard\n"
        while True:
            self.request.sendall(ask_user)
            user = self.request.recv(1024).decode().strip("\n")
            log.info(f"Received username : {user}")
            result = db.save_score(user, completion_time)
            if not result:
                self.request.sendall("An error occured. Please retry\n".encode())
                continue
            if result.get("message"):
                log.debug(result.get("message"))
                self.request.sendall(result.get("message").encode() + b"\n")  # type: ignore
            token = result.get("token")
            if token:
                self.request.sendall(f"Your token is {result['token']}\n\n".encode())
                result["retry"] = False

            if not result["retry"]:
                break


class ProcessTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


##########################################
############### Exceptions ###############
##########################################


def configure_logging():
    # Configure the logger

    LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR").upper()
    numeric_level = getattr(logging, LOG_LEVEL, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {LOG_LEVEL}")

    logging.basicConfig(filename="jigsaw.log", level=numeric_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logging.getLogger().addHandler(console_handler)
