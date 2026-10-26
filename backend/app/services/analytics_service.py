from pyspark.sql.functions import avg, count, desc, explode, split
from app.services.spark_service import get_anime, json_number

def get_stats():
    anime = get_anime()
    average = anime.filter(anime.rating.isNotNull()).select(avg('rating')).first()[0]
    return {'total_anime': anime.count(), 'average_rating': round(float(average), 2) if average is not None else None,
            'total_types': anime.filter(anime.type.isNotNull()).select('type').distinct().count()}

def top_anime(limit=10):
    a = get_anime()
    rows = a.filter(a.rating.isNotNull()).orderBy(desc('rating')).select('name','rating','type','episodes').limit(limit).collect()
    return [{'name':r['name'],'rating':json_number(r['rating']),'type':r['type'],'episodes':r['episodes']} for r in rows]

def type_analysis():
    a=get_anime(); rows=a.filter(a.type.isNotNull()).groupBy('type').agg(count('*').alias('count')).orderBy(desc('count')).collect()
    return [{'type':r['type'],'count':int(r['count'])} for r in rows]

def genre_analysis():
    a=get_anime(); rows=(a.filter(a.genre.isNotNull()).withColumn('genre',explode(split(a.genre, r',\s*')))
        .groupBy('genre').agg(count('*').alias('count')).orderBy(desc('count')).limit(10).collect())
    return [{'genre':r['genre'],'count':int(r['count'])} for r in rows if r['genre']]

def popular_anime(limit=10):
    a=get_anime(); rows=a.filter(a.members.isNotNull()).orderBy(desc('members')).select('name','members','rating','type').limit(limit).collect()
    return [{'name':r['name'],'members':int(r['members']),'rating':json_number(r['rating']),'type':r['type']} for r in rows]

def search_anime(query,limit=20):
    a=get_anime(); rows=(a.filter(a.name.isNotNull() & a.name.contains(query)).select('name','genre','type','episodes','rating','members').limit(limit).collect())
    return [{'name':r['name'],'genre':r['genre'],'type':r['type'],'episodes':r['episodes'],'rating':json_number(r['rating']),
             'members':int(r['members']) if r['members'] is not None else None} for r in rows]
