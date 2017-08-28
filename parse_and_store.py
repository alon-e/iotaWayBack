import os
import transaction

from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, BigInteger , String,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

#can be sqlite for a local DB. or MySQL for more performant queries.
DBEngine = 'sqlite'
folder = './'

###create_db
Base = declarative_base()
class Transactions(Base):
    __tablename__ = 'transactions'
    #the Transactions model - matches transaction.py format
    #many fields are index to allow fast search
    hash = Column(String(81), primary_key=True)
    signature_message_fragment = Column(String(2187))
    address = Column(String(81), index=True)
    value = Column(BigInteger)
    tag = Column(String(81), index=True)
    tagIndex = Column(BigInteger)
    timestamp = Column(Integer, index=True)
    timestampDate = Column(TIMESTAMP, index=True)
    current_index = Column(Integer)
    last_index = Column(Integer)
    bundle_hash = Column(String(81), index=True)
    trunk_transaction_hash = Column(String(81))
    branch_transaction_hash = Column(String(81))
    nonce = Column(String(81))
    if DBEngine.lower() == 'mysql':
        __table_args__ = {"schema": "iotaWayBack"}


engine = None
if DBEngine.lower() == 'sqlite':
    try:
        os.remove('sqlalchemy_IRI.db')
    except:
        pass
    engine = create_engine('sqlite:///sqlalchemy_IRI.db')

if DBEngine.lower() == 'mysql':
    engine = create_engine('mysql+pymysql://user:password@localhost:3306')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.drop_all(engine)   # all tables are deleted
Base.metadata.create_all(engine)
###

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


for file in sorted(os.listdir(folder)):
    counter = 0
    if file.endswith(".dmp"):
        #parse each dump file and add to DB
        with open(folder + file,"r") as f:
            for line in f:
                tx_hash, tx = line.split(",")
                #parse trytes
                trans = transaction.transaction(tx,tx_hash)
                #add to DB
                new_trans = Transactions(**trans.__dict__)
                session.add(new_trans)
                counter += 1
                if counter % 1000 == 0:
                    #in batches
                    session.commit()
                    print "added to DB:", counter, file
        session.commit()