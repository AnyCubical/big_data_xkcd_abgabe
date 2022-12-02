import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import desc
import pandas
import sqlite3

if __name__ == '__main__':
    con = sqlite3.connect("/home/airflow/mnt/xkcd.db")

    sc = pyspark.SparkContext()
    spark = SparkSession(sc)
    test = spark.read.format('json')\
        .option('recursiveFileLookup',True)\
        .load('/user/hadoop/xkcd/raw/*')

    xkcd = test.drop("alt").drop("day").drop("link").drop("month").drop("news").drop("transcript").drop("extra_parts").drop("title")

    xkcd.printSchema()
    xkcd.write.format('csv')\
        .mode('overwrite')\
        .option('path', '/user/hadoop/xkcd/final')\
        .saveAsTable('default.xkcd_partitioniert')\

    df = xkcd.toPandas()
    
    df.to_sql("xkcd", con, if_exists="replace")
    con.close()
