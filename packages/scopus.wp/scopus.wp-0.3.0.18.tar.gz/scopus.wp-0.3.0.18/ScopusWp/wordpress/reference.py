from sqlalchemy import Column, ForeignKey, Integer, String, Text, DATETIME, BigInteger, Table, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from ScopusWp.config import Config

from jutil.database import mysql_database_singleton


class WordpressMySQLDatabase(mysql_database_singleton(
    Config.get_instance()['MYSQL']['username'],
    Config.get_instance()['MYSQL']['password'],
    Config.get_instance()['MYSQL']['host'],
    '__wordpress'
)):
    pass


BASE = declarative_base()


class PostReference(BASE):

    __tablename__ = 'post_reference'

    postID = Column(BigInteger, primary_key=True)
    publicationID = Column(BigInteger)
    published = Column(DATETIME)
    updated = Column(DATETIME)

    comments = relationship(
        'CommentReference',
        back_populates='post'
    )


class CommentReference(BASE):

    __tablename__ = 'comment_reference'

    commentID = Column(BigInteger, primary_key=True)
    publicationID = Column(BigInteger)
    postID = Column(BigInteger, ForeignKey('post_reference.postID'))
    published = Column(DATETIME)

    post = relationship(
        'PostReference',
        back_populates='comments'
    )


class PublicationReference:

    def __init__(self):
        self.session = WordpressMySQLDatabase.get_session()

    def contains_publication(self, publication_id):
        return len(list(self.session.query(PostReference).filter(PostReference.publicationID == publication_id))) != 0

    def insert(self, reference_dict):

        post_reference = PostReference(
            postID=reference_dict['post'],
            publicationID=reference_dict['publication'],
            published=reference_dict['published'],
            updated=reference_dict['published']
        )

        for comment_reference_dict in reference_dict['comments']:
            comment_reference = CommentReference(
                commentID=comment_reference_dict['comment'],
                postID=comment_reference_dict['post'],
                publicationID=comment_reference_dict['publication'],
                published=comment_reference_dict['published']
            )
            post_reference.comments.append(comment_reference)

        self.session.add(post_reference)
        self.session.commit()

    def wipe(self):
        self.session.query(CommentReference).delete()
        self.session.query(PostReference).delete()


if __name__ == '__main__':
    session = WordpressMySQLDatabase.get_session()
    WordpressMySQLDatabase.create_database(BASE)