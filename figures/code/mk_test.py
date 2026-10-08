import re,sys
s=open('parallel_xs_zan4.cpp').read()
parts=re.split(r'^//---- (\w+)\n',s,flags=re.M)
secs={parts[i]:parts[i+1] for i in range(1,len(parts),2)}
out="#include <bits/stdc++.h>\nusing namespace std;\n"
for k,v in secs.items(): out+=f"namespace {k} {{\n{v}\n}}\n"
open(sys.argv[1],'w').write(out)
