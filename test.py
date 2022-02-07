s = 'foo-bar#baz?qux@127_/\\9]'
print(s)
t = "".join(i for i in s if i not in "\/:*?<>|")
print(t)

import string
import time
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
print(valid_chars)
filename = "This Is a (valid) - filename%$&$ .txt"
print(''.join(c for c in filename if c in valid_chars))

print(s + s)

t = time.asctime()
print(time.strftime("%Y%m%j",time.localtime()))

an_array = [[1, 2], [3, 4]]

print(len(an_array))