import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="ydh0114", db="stackoverflow201503")
cur = db.cursor()

pl = ['java', 
	   'javascript', 
	   'c#', 
	   'php', 
	   'android', 
	   'jquery', 
	   'python', 
	   'html', 
	   'c++', 
	   'ios' ] 
	   # 'objective-c', 
	   # 'mysql', 
	   # 'c', 
	   # 'ruby']
for name in pl:
	exe_str = "SELECT Id FROM posts where Tags like '%<" + name + ">%'"
	row_count = cur.execute(exe_str)
	if row_count > 0: 
		f = open(name + 'postid.txt', 'w') 
		postid = cur.fetchall()
		for row in postid:
			f.write(str(row[0]) + '\n')
		f.close()
