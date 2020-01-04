import time
email = "john_smith-bla.33@example.org"
local, at, domain = email.rpartition('@')
print(local)
print(domain)

now= time.time()
print(time.strftime('%Y%m%d'))
year= time.strftime('%Y')
month = time.strftime('%m')
day = time.strftime('%d')
print(day)
print(month)
print(year)

print(time.strftime('%H%M%S'))