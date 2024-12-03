import psycopg2

conn = psycopg2.connect(host = "localhost", port = "5432", database = "myduka", password = "williammurage", user = "postgres")

print("Databse connected")

cur = conn.cursor()