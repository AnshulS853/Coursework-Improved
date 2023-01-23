import sqlite3

class refreshLists:
    def __init__(self,app):
        self.app = app
        self.conn = sqlite3.connect("auc_database.db", isolation_level=None)
        self.cur = self.conn.cursor()
        self.refreshall()

    def refreshall(self):
        self.cur.execute("SELECT listingID FROM listings WHERE dateofend<=DATE('now') AND active=1 AND format = 'Buy Now'")
        buynowresult = self.cur.fetchall()

        self.cur.execute("SELECT listingID FROM listings WHERE dateofend<=DATE('now') AND active=1 AND format = 'Auction'")
        auctionresult = self.cur.fetchall()

        buynowlist = []
        auctionlist = []

        for i in buynowresult:
            if i is not None:
                i = i[0]
                buynowlist.append(i)

        for j in auctionresult:
            if j is not None:
                j = j[0]
                auctionlist.append(j)

        self.updatebuynow(buynowlist)
        self.updateauctions(auctionlist)

    def updatebuynow(self, list):
        for i in list:
            currentlistingID = i
            self.cur.execute('''
                            UPDATE listings
                            SET active=0
                            WHERE listingID = (?)
                            ''',(currentlistingID,))

    def updateauctions(self, list):
        for i in list:
            currentlistingID = i
            self.cur.execute('''SELECT bidderID,highestBid FROM auctions WHERE listingID = ?''',(currentlistingID,))
            result = self.cur.fetchall()
            if result:
                result = result[0]
                self.cur.execute('''
                                INSERT INTO invoice
                                (listingID,
                                buyerID,
                                total,
                                purchasedate)
                                VALUES (?,?,?,DATE('now'))
                                ''',(currentlistingID,result[0],result[1]))

            self.cur.execute('''
                            UPDATE listings
                            SET active=0
                            WHERE listingID = (?)
                            ''', (currentlistingID,))


