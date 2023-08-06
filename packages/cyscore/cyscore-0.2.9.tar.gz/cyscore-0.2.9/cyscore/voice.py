from itertools import accumulate
from typing import Iterator, List

from .note import Note
from .utility import number_format, str_format


class Voice:
    def __init__(self, instr: str, notes: List[Note], starttime: float=0) -> None:
        assert(len(notes) > 0)
        assert(starttime >= 0)
        self.__instr = instr
        self.__notes = notes
        self.__starttime = starttime

    @property
    def instr(self) -> str:
        return self.__instr

    @property
    def notes(self) -> List[Note]:
        return list(self.__notes)

    @property
    def starttime(self) -> float:
        return self.__starttime

    def __iter__(self) -> Iterator[Note]:
        return self.notes.__iter__()

    def __getitem__(self, index: int) -> Note:
        return self.notes[index]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__eq(other)
        else:
            False

    def duration(self):
        return sum([n.delay for n in self.notes])

    def __eq(self, other: 'Voice') -> bool:
        i = self.instr == other.instr
        n = self.notes == other.notes
        return i and n

    def __line(self, time: float, note: Note, mutefunc) -> str:
        line = "i\t{0}\t{1}\t".format(str_format(self.instr),
                                      number_format(time))
        if mutefunc(note):
            result = line + str(note)
        else:
            result = ''
        return result

    def repr(self, mutefunc) -> str:
        times = accumulate(map(lambda x: x.delay, self.notes))
        times = [time + self.starttime for time in times]
        block = self.__line(self.starttime, self.notes[0], mutefunc)
        for n, time in zip(self.notes[1:], times):
            block += '\n'
            block += self.__line(time, n, mutefunc)
        return block

    def __repr__(self) -> str:
        return self.repr(lambda x: True)
