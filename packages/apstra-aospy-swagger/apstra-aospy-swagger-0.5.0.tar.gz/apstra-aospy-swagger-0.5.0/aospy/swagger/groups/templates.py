from aospy.swagger.indexer import Indexer

class Templates(Indexer):
    def __init__(self, aos):
        super(Templates, self).__init__(
            rqst=aos.request.design.all_templates,
            name_from='display_name')
        self.run()
