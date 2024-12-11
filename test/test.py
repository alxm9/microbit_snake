id = 'this'
try:
    with open('seen.txt','r') as seen:
        temp = seen.read()
        temp += id+','
except:
    temp = id+','

with open('seen.txt','w') as seen:
    seen.write(temp)

print(temp)