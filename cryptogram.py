"""Cryptogram-Flask is a simple web app for creating cryptograms.
"""
# Copyright (c) 2012, Tim Swast
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import os
import random
import string
from flask import Flask, url_for, redirect, request, session

app = Flask(__name__)

def create_ciphertext(plaintext):
    # choose a key
    l = list(string.ascii_uppercase)
    random.shuffle(l)
    # create dictionary
    cipherkey = {}
    for lower, upper in zip(string.ascii_lowercase, l):
        cipherkey[lower] = upper
    # encrypt text
    ciphertext = []
    for letter in plaintext.lower():
        if letter in cipherkey:
            ciphertext.append(cipherkey[letter])
        else:
            ciphertext.append(letter)
    return "".join(ciphertext)


@app.route('/cryptogram')
def view_cryptogram():
    # show the cryptogram make for this request
    return create_ciphertext(session['cryptogram'])

@app.route('/', methods=["GET", "POST"])
def create_cryptogram():
    if request.method == "GET":
        return """<form action="{post}" method="post">
<textarea name="plaintext">Type your message here.</textarea>
<input type="submit" value="Create cryptogram" />
</form>""".format(post=url_for('create_cryptogram'))
    elif request.method == "POST":
        session['cryptogram'] = request.form['plaintext']
        return redirect(url_for('view_cryptogram'))

# set the secret key.  keep this really secret:
app.secret_key = '12345'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

