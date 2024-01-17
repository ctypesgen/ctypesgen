from ctypesgen.parser.datacollectingparser import DataCollectingParser


class MyParser(DataCollectingParser):
    def __init__(self, headers, options):
        super(MyParser, self).__init__(headers=headers, options=options)
        self.parse()
        self.data = self.data()
