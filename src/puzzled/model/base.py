'''
Created on Feb 23, 2013

@author: peterb
'''
from sqlalchemy.engine import create_engine, reflection
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import MetaData, ForeignKeyConstraint, DropConstraint,\
    DropTable, Table
from sqlalchemy.ext.declarative.api import declared_attr, has_inherited_table,\
    declarative_base
import re


class _Base_(object):
    '''
        This class allows us to base the tablename off the class name.
        We also check for has_inherited_table, so as not to redeclare.
        We make the table name to lower case and underscored.
        
        We don't implement the primary key in base as some classes will use
        a foreign key to a parent table as their primary key.
        
        see: http://docs.sqlalchemy.org/en/rel_0_7/orm/extensions/declarative.html#augmenting-the-base
    '''


    @declared_attr
    def __tablename__(self):
        if has_inherited_table(self):
            return None
        name = self.__name__
        return (
            name[0].lower() +
            re.sub(r'([A-Z])', lambda m:"_" + m.group(0).lower(), name[1:])
        )
        
    __table_args__ = {'mysql_engine': 'InnoDB'}


Base = declarative_base(cls=_Base_)


def connect(url):
    engine = create_engine(url)
    Session = sessionmaker(autocommit=False,
                           autoflush=False,
                           bind=engine)
    return Session
    
    
def create_all(engine):
    Base.metadata.create_all(engine)
    

def drop_all(session):

    inspector = reflection.Inspector.from_engine(session.bind)
    
    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in 
    # a transaction.
    
    metadata = MetaData()
    
    tbs = []
    all_fks = []
    
    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((),(),name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)
    
    for fkc in all_fks:
        session.execute(DropConstraint(fkc))
    
    for table in tbs:
        session.execute(DropTable(table))
    
    session.commit()
