import random
import socketserver
import re
import logging
import string
import io
from typing import Dict, Callable, Optional
import qrcode  # type:ignore

log = logging.getLogger(__name__)


PARSE_REGEX = r"(?![A-Za-z0-9,\-])"


###########################################
################ QUESTIONS ################
###########################################

Q_WANNA_PLAY = b"Do you wanna play a game?\n"
A_WANNA_PLAY = ["yes", "y"]

Q_42 = b"What is the meaning of life, the universe, and everything, according to Deep Thought?\n"
A_42 = ["42"]


Q_EASY = """Easy question, Which letter comes {position} : {letter}\n"""


Q_RGB = """Can you tell me what color is : {color}\n"""
Q_RGB_VALUES = {
    "black": "0,0,0",
    "red": "255,0,0",
    "green": "0,255,0",
    "blue": "0,0,255",
    "white": "255,255,255",
}

Q_FORGOT = b"I forgot everything. Send me back your answers to questions 1 to 4, separated by commas.\n"


Q_REPEAT = """I did not understand. Can you repeat your previous answers for question(s) {questions} using the same format ?\n"""

Q_RANDOM = """Just to be sure it wasn't luck, random question time : {question}"""

Q_ENCODE = """Send me back the following word : {word}"""

Q_STEGA = """Answer the following question : {question}"""

QUESTIONS = [
    "question_wanna_play",
    "question_42",
    "question_easy",
    "question_rgb",
    "question_forgot",
    "question_repeat",
    "question_random",
    "question_encode",
    "question_qr",
    "question_final",
]


###########################################
############# CLASS QUESTIONS #############
###########################################


class Questions:
    def __init__(self) -> None:
        self.answers: list[str] = []
        self.question: bytes
        self.answer: list[str]

    def ask(self, stage: int):
        log.info(f"Serving stage {stage}")
        if stage >= 0 and stage < len(QUESTIONS):
            question_function = f"{QUESTIONS[stage]}"
            try:
                self.question, self.answer = self._get_question(
                    eval(f"self.{question_function}")
                )

            except AttributeError:
                log.critical(f"Question function not found")
                raise

        else:
            raise InvalidStageError(f"Invalid stage number: {stage}")

        return bytes(f"{stage+1}. ", "utf-8") + self.question

    def check(self, received: bytes):
        response = self.parsing(received)
        log.debug(f"Expected: {self.answer}")

        if response in self.answer:
            self.answers.append(response)
            return True

        else:
            return False

    @staticmethod
    def parsing(data: bytes):
        """Input parsing and injection prevention"""
        log.debug(f"Before parsing : {data}")
        data_str = data.decode()
        data_str = data_str.replace("\n", "")
        if re.match(PARSE_REGEX, data_str):
            log.warning("Parsing error")
            raise ParseError()
        log.debug(f"after parsing : {data_str}")
        return data_str

    ###########################################
    ################ FUNCTIONS ################
    ###########################################

    def question_wanna_play(self):
        self.question = Q_WANNA_PLAY
        self.answer = A_WANNA_PLAY

    def question_42(self):
        self.question = Q_42
        self.answer = A_42

    def question_easy(self):
        letter = random.choice(string.ascii_lowercase)
        if letter == "a":
            direction = "after"
        elif letter == "z":
            direction = "before"
        else:
            direction = random.choice(["before", "after"])

        ascii_value = ord(letter)

        if direction.lower() == "before":
            next_or_before = ascii_value - 1

        else:  # direction is "after"
            next_or_before = ascii_value + 1

        self.question = bytes(Q_EASY.format(letter=letter, position=direction), "utf-8")
        answer = chr(next_or_before)
        self.answer = [answer, answer.lower(), answer.upper()]

    def question_rgb(self):
        color = random.choice(list(Q_RGB_VALUES.keys()))
        self.question = bytes(Q_RGB.format(color=Q_RGB_VALUES[color]), "utf-8")
        self.answer = [color, color.lower(), color.upper()]

    def question_forgot(self):
        self.question = Q_FORGOT
        self.answer = [",".join(self.answers[0:4])]

    def question_repeat(self):
        questions = []
        while not len(questions):
            questions = [str(x + 1) for x in range(0, 3) if random.randint(0, 1)]

        self.question = bytes(Q_REPEAT.format(questions=",".join(questions)), "utf-8")

        selected_answers: list[str] = []
        for x in [int(x) - 1 for x in questions]:
            selected_answers.append(self.answers[x])
        self.answer = [",".join(selected_answers)]

    def question_random(self):
        question_function = random.choice(QUESTIONS[0:5])
        try:
            self.question, self.answer = self._get_question(
                eval(f"self.{question_function}")
            )
        except AttributeError:
            log.critical(f"Random question function not found")
        choosen_question = self.question.decode()
        self.question = bytes(Q_RANDOM.format(question=choosen_question), "utf-8")

    def question_encode(self):
        random.choice([self.question_morse, self.question_braille])()

    def question_morse(self, word: Optional[str] = None):
        if not word:
            word = Questions._get_random_word()
            question = Q_ENCODE.format(word=word).upper()
        else:
            question = Q_STEGA.format(question=word).upper()
        self.answer = [word, word.lower(), word.upper()]

        encoded_question = self._encode_morse(question)
        self.question = bytes(encoded_question, "utf-8") + b"\n"

    def question_braille(self, word: Optional[str] = None):
        if not word:
            word = self._get_random_word()
            question = Q_ENCODE.format(word=word).upper()
        else:
            question = Q_STEGA.format(question=word).upper()

        self.answer = [word, word.lower(), word.upper()]
        encoded_question = self._encode_braille(question)
        self.question = bytes(encoded_question, "utf-8") + b"\n"

    def question_qr(self):
        word = self._get_random_word()
        self.answer = [word, word.lower(), word.upper()]
        question = Q_ENCODE.format(word=word)
        self.question = self._create_qr(question)

    def question_final(self):
        random.choice([self.question_easy, self.question_rgb])()
        answer = self.answer
        log.debug(self.question)
        random.choice([self.question_morse, self.question_braille])(
            self.question.decode()
        )
        log.debug(self.question)
        question = self._create_qr(self.question.decode())
        self.question = question
        self.answer = answer

    def _get_question(self, function: Callable[[], None]):
        function()
        log.info(f"Question : {self.question}\nAnswer : {self.answer}")
        return self.question, self.answer

    @staticmethod
    def _get_random_word(filename: str = "words.txt") -> str:
        with open(filename, "r") as file:
            words = file.read().splitlines()  # splitlines() is used to remove newlines
        return random.choice(words)

    @staticmethod
    def _encode(char_dict: Dict[str, str], message: str):
        return " ".join(char_dict[i] for i in message.upper() if i in char_dict)

    @staticmethod
    def _encode_morse(message: str):
        morse_code_dict = {
            "A": ".-",
            "B": "-...",
            "C": "-.-.",
            "D": "-..",
            "E": ".",
            "F": "..-.",
            "G": "--.",
            "H": "....",
            "I": "..",
            "J": ".---",
            "K": "-.-",
            "L": ".-..",
            "M": "--",
            "N": "-.",
            "O": "---",
            "P": ".--.",
            "Q": "--.-",
            "R": ".-.",
            "S": "...",
            "T": "-",
            "U": "..-",
            "V": "...-",
            "W": ".--",
            "X": "-..-",
            "Y": "-.--",
            "Z": "--..",
            "0": "-----",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            " ": "/",
            ":": "---...",
            ",": "--..--",
        }
        return Questions._encode(morse_code_dict, message)

    @staticmethod
    def _encode_braille(message: str):
        braille_alphabet = {
            "A": "\u2801",
            "B": "\u2803",
            "C": "\u2809",
            "D": "\u2819",
            "E": "\u2811",
            "F": "\u280b",
            "G": "\u281b",
            "H": "\u2813",
            "I": "\u280a",
            "J": "\u281a",
            "K": "\u2805",
            "L": "\u2807",
            "M": "\u280d",
            "N": "\u281d",
            "O": "\u2815",
            "P": "\u280f",
            "Q": "\u281f",
            "R": "\u2817",
            "S": "\u280e",
            "T": "\u281e",
            "U": "\u2825",
            "V": "\u2827",
            "W": "\u283a",
            "X": "\u282d",
            "Y": "\u283d",
            "Z": "\u2835",
            " ": "\u2800",
            ":": ":",
            ",": ",",
            "0": "\u2834",
            "1": "\u2802",
            "2": "\u2806",
            "3": "\u2812",
            "4": "\u2832",
            "5": "\u2822",
            "6": "\u2816",
            "7": "\u2836",
            "8": "\u2826",
            "9": "\u2814",
        }
        return Questions._encode(braille_alphabet, message)

    @staticmethod
    def _create_qr(question: str):
        qr = qrcode.make(question)  # type: ignore
        img = io.BytesIO()
        qr.save(img)  # type: ignore
        return img.getvalue()


############################################
################ EXCEPTIONS ################
############################################


class InvalidStageError(Exception):
    """Exception raised for invalid stage numbers."""

    pass


class ParseError(Exception):
    """Exception raised for invalid stage numbers."""

    pass


class WrongAnswer(Exception):
    """Exception raised for invalid stage numbers."""

    pass
