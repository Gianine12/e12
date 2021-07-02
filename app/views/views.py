from ..services.services import connection, close_connection, check_key
from ..services.feactures_sql import create_table ,select_all, select_one, insert, update_anime
from datetime import datetime
from psycopg2 import errors

from flask import request, Blueprint, jsonify

import ipdb

bp = Blueprint('bp_animes',__name__)

campos_tabela = ["id","anime","released_date","seasons"]
available_keys = ["anime","released_date","seasons"]

@bp.route("/animes", methods=["GET", "POST"])
def get_create():

    if request.method == "GET":
        try:
            connect,cur = connection()
            connect,cur = select_all(connect,cur)

            query = cur.fetchall()

            close_connection(connect,cur)

            reponse = [dict(zip(campos_tabela,retorno)) for retorno in query]

            #fazer tratamente de data
            # reponse['released_date'] = reponse['released_date'].strftime("%d/%m/%y")

            return ({"data": reponse},200)

        except:
            return ({"data": []}, 400)

    else:
        try:
            data = request.get_json()
            data["anime"] = data["anime"].title()

            connect,cur = connection()
            connect,cur = create_table(connect,cur)

            key = check_key(data,available_keys)

            if key:
                raise KeyError(
                    {
                        'available_keys': available_keys,
                        'wrong_keys_sended':key
                    }
                )

            connect,cur = insert(connect,cur,data)

            query = cur.fetchone()
            reponse = dict(zip(campos_tabela,query))

            close_connection(connect,cur)

            return ({'data': data}, 200)

        except errors.UniqueViolation as _:
            return ({'error': "anime is already  exists"}, 422)

        except KeyError as k:
            return (k.args[0],422)

@bp.route("/animes/<int:anime_id>", methods=["GET"])
def filter(anime_id):
    try:
        connect,cur = connection()

        connect,cur = select_one(connect,cur,anime_id)    
        
        query = cur.fetchone()

        close_connection(connect,cur)
        
        data = dict(zip(campos_tabela,query))

        return ({'data':data},200)
    except:
        return ({'error':"Not Found"},404)

@bp.route("/animes/<int:anime_id>", methods=["PATCH"])
def update(anime_id):

    try:
        data = request.get_json()
        connect,cur = connection()

        chaves_validas = ["anime","seasons"]
        key = check_key(data,chaves_validas)

        if key:
            raise KeyError(
                {
                    'available_keys': chaves_validas,
                    'wrong_keys_sended':key
                }
            )

        connect,cur = select_one(connect,cur,anime_id)    
        
        query = cur.fetchone()

        reponse = dict(zip(campos_tabela,query))
        reponse.update(data)

        reponse['released_date'] = reponse['released_date'].strftime("%d/%m/%y")
        reponse['anime'] = reponse['anime'].title()
    
        connect,cur = update_anime(connect,cur,anime_id,reponse)   

        query = cur.fetchone()

        result = dict(zip(campos_tabela,query))

        close_connection(connect,cur)

        return ({'data':result},200)

    except KeyError as k:
            return (k.args[0],422)

@bp.route("/animes/<int:anime_id>", methods=["DELETE"])
def delete(anime_id):   
    connect,cur = connection()

    connect,cur = select_one(connect,cur,anime_id)  
    query = cur.fetchone()
    if not query:
        return {'error': "Not Found"},404

    cur.execute(
        """
            DELETE FROM
                animes
            WHERE id = %s
        """
        % anime_id
    )

    close_connection(connect,cur)

    return 'no content',204