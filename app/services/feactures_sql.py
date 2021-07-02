def create_table(connect,cur):
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS animes (
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL
            );
        """
    )

    return (connect, cur,)

def select_all(connect,cur):
    cur.execute(
        """
            SELECT 
                *
            FROM 
                animes;
        """
    )

    return (connect, cur)

def insert(connect,cur, data):
    cur.execute(
        """
            INSERT INTO animes
                (anime,released_date,seasons)
            VALUES
                (%(anime)s,%(released_date)s,%(seasons)s)
            RETURNING *;
        """,
        data,
    )

    return (connect,cur)

def select_one(connect,cur,anime_id):

    cur.execute(
        """
            SELECT
                *
            FROM 
                animes
            WHERE 
                id = %s;
        """
        % anime_id
    )

    return (connect,cur)


def update_anime(connect,cur,anime_id,reponse):
    cur.execute(
        """
            UPDATE 
                animes
            SET
                anime = %s,
                released_date = %s,
                seasons = %s
            WHERE id = %s
            RETURNING *
        """,(reponse['anime'],reponse['released_date'],reponse['seasons'],anime_id)
        # reponse,
        # anime_id
    )

    return (connect,cur)