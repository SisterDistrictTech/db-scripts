# Logic relating to the pres_races db table.

class PresRaces:
    @staticmethod
    def setup(cur):
        """
        Initial setup of the pres_races table.
        WARNING: destroys any data present in pres_races.

        Args:
          cur - a database cursor
        """
        cur.execute('DELETE FROM pres_races')
        sql = ('INSERT INTO pres_races ' +
               ' (race_year, dem_candidate, rep_candidate, winning_party) ' +
               ' VALUES (%s, %s, %s, %s)')
        cur.executemany(sql,
                        [(2016, "Hillary Clinton", "Donald Trump", "R"),
                         (2012, "Barack Obama", "Mitt Romney", "D"),
                         (2008, "Barack Obama", "John McCain", "D"),
                         (2004, "John Kerry", "George W. Bush", "R"),
                         (2000, "Al Gore", "George W. Bush", "R"),
                         (1996, "Bill Clinton", "Bob Dole", "D"),
                         (1992, "Bill Clinton", "George H. W. Bush", "D"),
                         (1988, "Michael Dukakis", "George H. W. Bush", "R"),
                         (1984, "Walter Mondale", "Ronald Reagan", "R"),
                         (1980, "Jimmy Carter", "Ronald Reagan", "R")])
