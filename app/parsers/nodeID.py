from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

from re import compile


class Parser(BaseParser):

    def parse(self, blob):
        relationships = []
        for match in self.line(blob):
            nodeID = self._locate_NodeID(match)
            if nodeID:
                for mp in self.mappers:
                    source = self.set_value(mp.source, nodeID, self.used_facts)
                    target = self.set_value(mp.target, nodeID, self.used_facts)
                    relationships.append(
                        Relationship(source=Fact(mp.source, source),
                                     edge=mp.edge,
                                     target=Fact(mp.target, target))
                    )
        return relationships

    @staticmethod
    def _locate_NodeID(line):
        if 'Id: ' in line:
            return line.split('Id: ')[1]