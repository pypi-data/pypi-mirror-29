#funcCollection



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbBase import Base, FlamShow, FlamShot, FlamShotAsset, DATABASE_LOCATION


##session creation for db calls
def makeSession():
    engine = create_engine(DATABASE_LOCATION)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    _session = DBSession()
    
    return _session
'''
def getShot(shotId, showId):
    print "DBQUERIES<-getShow(shotName)"
    session = makeSession()
    show = session.query(FlamShot).filter(FlamShot.id == shotId).join.scalar()
    session.close()
    return show
'''

def getAllShots(showId):
    print "DBQUERIES<-getAllShots(showId)"
    session = makeSession()
    tempShots = session.query(FlamShot).filter(FlamShot.show_id == showId).all()
    session.close()
    return tempShots
    

def getShow(showName):
    print "DBQUERIES<-getShow(showName)"
    session = makeSession()
    show = session.query(FlamShow).filter(FlamShow.name == showName).scalar()
    session.close()
    return show


def getAllShows():
    print "DBQUERIES<-getAllShows()"
    session = makeSession()
    tempShots = session.query(FlamShow).all()
    session.close()
    return tempShots


def addShow(showName):
    session = makeSession()
    FlamShow(name=showName)
    session.add(showName)
    session.commit()
    session.close()

def addShot():
    pass

def addAsset():
    pass




###
def addShotToShow(showName, shotName):
    ###########################
    ###########################
    #########INCOMPLETE########
    ###########################
    ###########################
    ####FOR GUI INGEST FUNCTION
    ###########################

    print "\n\n"
    session = makeSession()
    #curShowName = getCurShow() #Get show currently displayed in GUI
    curShowName = showName
    curShow = session.query(FlamShow).filter(FlamShow.name == curShowName).scalar()

    if curShow:
        print "Found Show: \'%s\'." % curShow.getName()
        print "Adding new shot \'%s\'." % shotName
        curShow.createShot(session, shotName)
        #needs to create default folder structure
    else:
        print "Did not find %s." % curShow

    session.close()