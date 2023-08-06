from ScopusWp.extend import DataSink

from ScopusWp.wordpress.wordpress import WordpressPublicationController
from ScopusWp.wordpress.reference import PublicationReference


class Wordpress(DataSink):

    def __init__(self, controller):
        DataSink.__init__(self, controller)

        self.reference = PublicationReference()
        self.wordpress_controller = WordpressPublicationController()

    def run(self):
        # Selecting all the publications from scopus
        general_publications = self.register.select_origin('scopus', '')

        # Posting all the publications, that are not yet in the system to the web page
        for general_publication in general_publications:
            if not self.reference.contains_publication(general_publication.id):
                post_reference_dict = self.wordpress_controller.post(general_publication)
                self.reference.insert(post_reference_dict)

    @property
    def name(self):
        return 'wordpress'
