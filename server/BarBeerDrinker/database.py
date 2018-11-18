from sqlalchemy import create_engine
from sqlalchemy import sql

from BarBeerDrinker import config

engine = create_engine(config.database_uri)

def get_bars():
    with engine.connect() as con:
        rs = con.execute("SELECT Name, License, Address, City, State, Phone FROM Bars;")
        return [dict(row) for row in rs]

def find_bar(name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT Name, License, Address, City, State, Phone FROM Bars WHERE Name = :name;"
        )

        rs = con.execute(query, name=name)
        result = rs.first()
        if result is None:
            return None
        return dict(result)

def filter_beers(max_price):
    with engine.connect() as con:
        query = sql.text(
            "SELECT * FROM Sells WHERE Price < :max_price;"
        )

        rs = con.execute(query, max_price=max_price)
        results = [dict(row) for row in rs]
        for r in results:
            r['Price'] = float(r['Price'])
        return results


def get_bar_menu(bar_name):
    with engine.connect() as con:
        query = sql.text(
            'SELECT a.Bar, a.Item, a.Price, b.Manufacturer, coalesce(c.like_count, 0) as likes \
                FROM Sells as a \
                JOIN Items AS b \
                ON a.Item = b.ItemName \
                LEFT OUTER JOIN (SELECT BeerName, count(*) as like_count FROM likes GROUP BY BeerName ) as c \
                ON a.Item = c.BeerName \
                WHERE a.Bar = :bar;  \
            ')
        rs = con.execute(query, bar=bar_name)
        results = [dict(row) for row in rs]
        for i, _ in enumerate(results):
            results[i]['Price'] = float(results[i]['Price'])
        return results


def get_bars_selling(beer):
    with engine.connect() as con:
        query = sql.text('SELECT a.Bar, a.Price, b.customers \
                FROM Sells AS a \
                JOIN (SELECT bar, count(*) AS customers FROM Frequents GROUP BY bar) as b \
                ON a.Bar = b.Bar \
                WHERE a.Item = :beer \
                ORDER BY a.Price; \
            ')
        rs = con.execute(query, beer=beer)
        results = [dict(row) for row in rs]
        for i, _ in enumerate(results):
            results[i]['Price'] = float(results[i]['Price'])
        return results


def get_bar_frequent_counts():
    with engine.connect() as con:
        query = sql.text('SELECT bar, count(*) as frequentCount \
                FROM Frequents \
                GROUP BY bar;  \
            ')
        rs = con.execute(query)
        results = [dict(row) for row in rs]
        return results


def get_bar_cities():
    with engine.connect() as con:
        rs = con.execute('SELECT DISTINCT City FROM Bars;')
        return [row['City'] for row in rs]


def get_beers():
    """Gets a list of beer names from the beers table."""

    with engine.connect() as con:
        rs = con.execute('SELECT name, Manufacturer FROM Beers;')
        return [dict(row) for row in rs]

def get_manufacturers():

    with engine.connect() as con:
        rs = con.execute('SELECT Manufacturer FROM Beers;')
        return [row['Manufacturer'] for row in rs]

        


def get_beer_manufacturers(beer):
    with engine.connect() as con:
        if beer is None:
            rs = con.execute('SELECT DISTINCT Manufacturer FROM Beers;')
            return [row['Manufacturer'] for row in rs]

        query = sql.text('SELECT Manufacturer FROM Beers WHERE Name = :beer;')
        rs = con.execute(query, beer=beer)
        result = rs.first()
        if result is None:
            return None
        return result['Manufacturer']


def get_drinkers():
    with engine.connect() as con:
        rs = con.execute('SELECT Name, Phone, Address, City, State FROM Drinkers;')
        return [dict(row) for row in rs]


def get_likes(drinker_name):
    """Gets a list of beers liked by the drinker provided."""

    with engine.connect() as con:
        query = sql.text('SELECT BeerName FROM likes WHERE Name = :drinker_name;')
        rs = con.execute(query, drinker_name=drinker_name)
        return [row['beer'] for row in rs]


def get_drinker_info(drinker_name):
    with engine.connect() as con:
        query = sql.text('SELECT Name, Phone, Address, City, State FROM Drinkers WHERE Name = :drinker_name;')
        rs = con.execute(query, drinker_name=drinker_name)
        result = rs.first()
        if result is None:
            return None
        return dict(result)


def get_bartenders():
    with engine.connect() as con:
        rs = con.execute('SELECT  distinct BartenderName,BarName FROM Works;')
        return [dict(row) for row in rs]

def get_top_beers_sold(beer):
    with engine.connect() as con:
        query = sql.text('select t1.Bar,cast(sum(t1.Quantity) as unsigned )as beerSold \
                from(Select h.Bar , h.Item as sold,h.Quantity \
                from  HasOrdered h \
                where h.Item = :beer)t1 \
                Group by t1.Bar  \
                Order by beerSold desc \
                Limit 10; \
            ')
            
        rs = con.execute(query, beer=beer)

        if rs is None:
            return None
        return [dict(row) for row in rs]


def get_top_consumers(beer):
    with engine.connect() as con:
        query = sql.text('select b.Name, b.Item, cast(sum(b.Quantity) as unsigned) as biggestConsumers \
                from (select Name, Item, Quantity from HasOrdered where Item = :beer) as b \
                group by b.Name \
                order By biggestConsumers desc \
                Limit 10; \
            ')
            
        rs = con.execute(query, beer=beer)

        if rs is None:
            return None
        return [dict(row) for row in rs]


def get_top10_dates(beer):
    with engine.connect() as con:
        query = sql.text('select t1.Date, cast(sum(t1.Quantity)as unsigned) as mostselling \
            from (select h.Item, h.Quantity, t.Date, t.ID \
            from HasOrdered h, Transactions t \
            where h.Item=:beer and h.ID=t.ID)t1 \
            group by t1.Date \
            order by mostselling desc \
            limit 10; \
            ')
            
        rs = con.execute(query, beer=beer)

        if rs is None:
            return None
        return [dict(row) for row in rs]

def get_top10_transactions(drinker_name):
    with engine.connect() as con:
        query = sql.text('select h.Name, h.Bar, h.Item, h.price,h.Quantity, h.Amount,t.Date,t.Time,t.ID,t.Tip,t.Total\
                from Transactions t, HasOrdered h\
                where h.Name=:drinker_name and h.ID=t.ID\
                order by t.Date desc;\
                ')
            
        rs = con.execute(query, drinker_name=drinker_name)

        if rs is None:
            return None
        return [dict(row) for row in rs]

def get_top_regions(manufacturer_name):
    with engine.connect() as con:
        query = sql.text('select t3.City, t3.State, cast(sum(itemcount)as unsigned) as sales\
                from\
                (select bb.City,bb.State, t2.itemcount\
                from\
                (select t1.Bar, count(t1.Item) as itemcount\
                from\
                (select h.ID, h.Bar,h.Item,b.Manufacturer\
                from Beers b , HasOrdered h\
                where b.Manufacturer = :manufacturer_name and b.Name= h.Item) t1\
                group by t1.Bar\
                order by itemcount desc) t2, Bars bb\
                where bb.Name= t2.Bar)t3\
                group by t3.City,t3.State\
                order by sales desc \
                limit 10; \
                ')
            
        rs = con.execute(query, manufacturer_name=manufacturer_name)

        if rs is None:
            return None
        return [dict(row) for row in rs]



def get_drinker_region(manufacturer_name):
    with engine.connect() as con:
        query = sql.text('select t2.City, t2.State, cast(count(t2.Name) as unsigned) as liked \
            from (select t1.Name, t1.BeerName, d.City, d.State \
            from (select l.Name, l.BeerName from Beers b, likes l where b.Manufacturer = :manufacturer_name \
            and b.Name= l.BeerName)t1, Drinkers d \
            where t1.Name=d.Name)t2 \
            group by t2.City,t2.State \
            order by liked desc \
            limit 10; \
            ')

            
        rs = con.execute(query, manufacturer_name=manufacturer_name)

        if rs is None:
            return None
        return [dict(row) for row in rs]

def get_top_drinkers(bar_name):
    with engine.connect() as con:
        query = sql.text('select top10.Name,sum(top10.Total) as top10sum \
                from \
                (select distinctrow h.Name,t.ID, t.Total from Transactions t, HasOrdered h \
                where h.Bar = :bar_name and h.ID=t.ID)top10 \
                group by top10.Name \
                order by top10sum DESC \
                limit 10; \
                ')

            
        rs = con.execute(query, bar_name=bar_name)

        if rs is None:
            return None
        return [dict(row) for row in rs]

def get_top_beers(bar_name):
    with engine.connect() as con:
        query = sql.text('select popularbeer.Item,cast(sum(popularbeer.Quantity) as unsigned) as numsold ,popularbeer.Day\
                from \
                (select h.Item,h.quantity,t.ID,t.Date,t.Day \
                from HasOrdered h, Beers b, Transactions t \
                where h.Bar = :bar_name and h.Item=b.Name and h.ID=t.ID )popularbeer \
                group by popularbeer.Item,popularbeer.Day \
                order by numsold desc \
                ')

            
        rs = con.execute(query, bar_name=bar_name)

        if rs is None:
            return None
        return [dict(row) for row in rs]        

def get_bartender_shifts(bartender_name):
    with engine.connect() as con:
        query = sql.text('select w.BarName , w.BartenderName , w.Day, w.ShiftStart , w.ShiftEnd \
                from Works w \
                where w.BartenderName = :bartender_name; \
                ')
         
        rs = con.execute(query, bartender_name=bartender_name)

        if rs is None:
            return None
        return [dict(row) for row in rs]


def get_bartender_beerssold(bartender_name):
    with engine.connect() as con:
        query = sql.text('(select t1.Item,cast(sum(t1.Quantity) as unsigned) as beerssold \
                from \
                (select t.ID, h.Item , h.Quantity \
                from Transactions t , HasOrdered h, BartenderTransaction bt \
                where bt.BartenderName = :bartender_name and bt.ID = t.ID and t.ID=h.ID)t1, Beers b \
                where b.Name = t1.Item \
                group by t1.Item \
                order by beerssold desc); \
                ')
         
        rs = con.execute(query, bartender_name=bartender_name)

        if rs is None:
            return None
        return [dict(row) for row in rs]









        
