from dataclasses import dataclass


@dataclass
class SpecialChars:
    SPACE: str = " "
    QUOT: str = '"'
    ESCAPE: str = "\\"


class Parser:
    """Argument parser from string"""

    def __init__(self, text: str, separator: str = None):
        self.text = text
        self.separator = separator

        self._current = ""
        self._char = None
        self._quot = False
        self._escape = False
        self._index = -1
        self._arguments = list()

    def advance(self):
        self._index += 1
        self._char = self.text[self._index]

    def parse(self):
        if self.separator:
            args = [
                arg.strip()
                for arg in self.text.strip().split(self.separator)
                if arg.strip()
            ]
            return args

        while self._index < len(self.text) - 1:
            self.advance()
            if self._escape:
                self._current += self._char
                self._escape = False
                continue

            if self._char == SpecialChars.ESCAPE:
                self._escape = True
                continue

            if self._quot:
                if self._char == SpecialChars.QUOT:
                    self._arguments.append(self._current)
                    self._current = ""
                    self._quot = False
                else:
                    self._current += self._char
                continue

            if self._char == SpecialChars.QUOT:
                if self._current:
                    self._arguments.append(self._current)
                    self._current = ""

                self._quot = True
                continue

            if self._char == SpecialChars.SPACE:
                self._quot = False
                if self._current:
                    self._arguments.append(self._current)
                self._current = ""
            else:
                self._current += self._char

        if self._current:
            if self._quot:
                self._current = SpecialChars.QUOT + self._current

            rest_args = [arg for arg in self._current.split(" ") if arg.strip()]
            self._arguments += rest_args

        return self._arguments


with open("content.txt") as f:
    content = f.read()
    print(content)

    parser = Parser(content)
    args = parser.parse()
    print(args)
