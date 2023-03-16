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
            self.cur.execute('''SELECT bidderID,highestbid FROM auctions WHERE listingID = ?''',(currentlistingID,))
            result = self.cur.fetchall()
            if result:
                result = result[0]
                self.cur.execute('''
                                INSERT INTO basket
                                (userID,
                                listingID,
                                quantity,
                                purchased,
                                creationdate)
                                VALUES (?,?,1,1,DATE('now'))
                                ''',(result[0],currentlistingID))
                basketID = self.cur.lastrowid


                ##Fetch buyer's address
                self.cur.execute('SELECT addressID FROM usad WHERE userID = ?',(result[0],))
                buyerAddressID = self.cur.fetchone()[0]
                self.cur.execute('SELECT * FROM address WHERE addressID = ?',(buyerAddressID,))
                buyerAddress = self.cur.fetchall()[0]

                # concatenate first two indexes with a space
                first_part = buyerAddress[1] + ' ' + buyerAddress[2]
                # concatenate the rest of the indexes with a new line
                second_part = '\n'.join(buyerAddress[3:])
                # concatenate the two parts and store in a new variable
                s_buyerAddress = f"{first_part}\n{second_part}"
                # print the concatenated address

                self.cur.execute('''
                                INSERT INTO invoice
                                (couponID,
                                buyerID,
                                purchasedate,
                                buyeraddress)
                                VALUES (NULL,?,DATE('now'),?)
                                ''',(result[0],s_buyerAddress))
                invoiceID = self.cur.lastrowid


                self.cur.execute('''
                                INSERT INTO binv
                                (basketID,invoiceID)
                                VALUES (?,?)
                                ''',(basketID,invoiceID))

                self.cur.execute('''
                                UPDATE listings
                                SET active=0
                                WHERE listingID = (?)
                                ''', (currentlistingID,))