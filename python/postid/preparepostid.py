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
	   'c', 
	   'ruby', 
	   'ios', 
	   'objective-c', 
	   'mysql']
for name in pl:
	exe_str = "SELECT Id FROM posts where Tags like '%<" + name + ">%'"
	row_count = cur.execute(exe_str)
	if row_count > 0: 
		f = open(name + 'postid.txt', 'w') 
		postid = cur.fetchall()
		for row in postid:
			f.write(str(row[0]) + '\n')
		f.close()
