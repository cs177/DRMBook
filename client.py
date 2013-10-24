#!/usr/bin/env python
'''The completely uncrackable DRMBook client.'''

import sys
import socket
import drm

HOST = "192.35.222.33"
PORT = 31337

if len(sys.argv) != 2:
	print "Welcome to the DRMBook Streaming Book Service! You may read a book by executing:"
	print "# %s title" % (sys.argv[0],)
	exit(0)

title = sys.argv[1]
userkey = drm.get_userkey()

print "Connecting to DRMBook server..."
s = socket.create_connection((HOST, PORT))

print "Sending userkey..."
s.send(userkey + title)

print "Receiving ebook..."
encrypted = s.makefile().read()
if len(encrypted) < 64:
	print "Received streaming error:", encrypted
	exit(0)

print "Decrypting ebook..."
book = drm.decrypt_drm_book(encrypted, userkey)

print "Writing ebook..."
open(title + ".pdf", "w").write(book)
print "Your book has been written to %s.pdf and may now be viewed." % title
print "Thank you for using DRMBook! Remember, if it's not copy-protected, we don't like it!"
