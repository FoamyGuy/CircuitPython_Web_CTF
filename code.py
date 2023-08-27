# SPDX-FileCopyrightText: 2023 Tim C (Foamyguy)
#
# SPDX-License-Identifier: MIT
import json
import os
from binascii import unhexlify

import socketpool
import wifi
import aesio

from adafruit_httpserver import (
    Server,
    REQUEST_HANDLED_RESPONSE_SENT,
    Request,
    Response,
    FileResponse,
    Basic,
    Bearer,
    require_authentication,
    NOT_FOUND_404,
    METHOD_NOT_ALLOWED_405,
    POST,
    GET,
    Redirect,
    JSONResponse
)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/ctf_static", debug=True)

auths = [
    Basic("admin", "admin"),
    Bearer("#CTF{ERV0Ja1_u0MNXHDfeMN339CR0hqQx1c8cRhdtby4pH5M}"),
]

strict_auths = [
    Bearer("#CTF{ERV0Ja1_u0MNXHDfeMN339CR0hqQx1c8cRhdtby4pH5M}"),
]
def get_db_obj():
    def decrypt_string(keystring, inpstring):
        # SPDX-FileCopyrightText: 2022 Mark McGookin
        #
        # SPDX-License-Identifier: MIT
        # https://github.com/markmcgookin/circuitpython-easycrypt/tree/main
        # Slight modifications by foamyguy

        # Convert our string key to a byte array
        key = bytearray(keystring)

        # Unhex the input string, then convert it into a byte array
        inp = bytes(unhexlify(inpstring))

        # Create a byte array to store the output in
        outp = bytearray(len(inp))

        # Create our cypher
        cipher = aesio.AES(key, aesio.MODE_CTR)

        # Decrypt the data into the output array
        cipher.decrypt_into(inp, outp)

        # Conver the unencrypted bytes into a string to return
        trans = outp.decode()

        return trans

    f = open("ctf_static/encrypted_lazy_hosts_db.txt", 'rb')
    encrypted_data = f.read()
    f.close()
    f = open("ctf_static/db_key.txt", "rb")
    key = f.read()
    f.close()
    decrypted_data = decrypt_string(key, encrypted_data)
    return json.loads(decrypted_data)

@server.route("/")
def base(request: Request):
    """
    Serve the default index.html file.
    """
    # headers={"Set-Cookie": "is_admin=false;"}
    return FileResponse(request, "index.html" )


@server.route("/login/", [GET, POST])
def login(request: Request):
    """

    """
    if request.method == GET:
        return FileResponse(request, "login.html" )
    elif request.method == POST:
        #print(request.form_data)
        #print(f'{request.form_data.get('username')}")
        inc_username = request.form_data.get('username')
        inc_password = request.form_data.get('password')
        db_obj = get_db_obj()
        if inc_username not in db_obj['users'].keys():
            return Response(request, "User Not Found", status=NOT_FOUND_404)

        user_obj = db_obj['users'][inc_username]
        stored_password = user_obj['password']
        if stored_password != inc_password:
            return Response(request, "Invalid Password", status=NOT_FOUND_404)

        #return Redirect(request, f"/profile/{inc_username}/")
        #return profile(request, inc_username)
        #return FileResponse(request, "pr")

        return Response(request, "", status=(302, "Found"), headers={
            "Location": f"/profile/{inc_username}/",
            "Set-Cookie": [f"is_admin={'false' if not user_obj['is_admin'] else 'true'}; Path=/",
                           f"user={inc_username}; Path=/"]
        })
    else:
        return Response(request, "Invalid Method", status=METHOD_NOT_ALLOWED_405)


@server.route("/profile/<username>/")
def profile(request: Request, username):
    f = open("ctf_static/profile.html", 'r')
    profile_html = f.read()
    f.close()

    profile_html = profile_html.replace("{{ username }}", username)

    db_obj = get_db_obj()

    if username not in db_obj['users'].keys():
        return Response(request, "User Not Found", status=NOT_FOUND_404)

    file_lis = []
    for file in db_obj['users'][username]['files']:
        file_lis.append(f'<li>{file}</li>')

    lis_str = "\n".join(file_lis)
    ul_str = f"<ul>{lis_str}</ul>"

    profile_html = profile_html.replace("{{ filelist }}", ul_str)
    admin_visible_val = "none" if not db_obj['users'][username]['is_admin'] else "block"
    profile_html = profile_html.replace("{{ admin_visible }}", admin_visible_val)

    return Response(request, profile_html, content_type="text/html")
    #return FileResponse(request, "index.html", headers={"Set-Cookie": "is_admin=false;"})


@server.route("/admin/v3/")
def admin_v3(request: Request):
    print(request.headers)
    if "Cookie" not in request.headers:
        return Response(request, "Not on my watch.")

    cookies = (dict(i.split('=', 1) for i in request.headers['Cookie'].split('; ')))
    print(cookies)

    if 'is_admin' not in cookies:
        return Response(request, "Not on my watch.")

    if cookies['is_admin'] != "true":
        return Response(request, "Not on my watch.")

    return Response(request, "#CTF{BrokenAccessControl}")


@server.route("/admin/")
def admin(request: Request):
    require_authentication(request, auths)

    resp_str = """Page not found: /admin/

Did you mean?
/admin/dashboard/
/admin/files/
/admin/v3/

#CTF{OverlyInformativeErrorMessages}
"""

    return Response(request, resp_str)

@server.route("/admin/dashboard/")
def admin_dashboard(request: Request):
    require_authentication(request, auths)

    return Response(request, "#CTF{BadPassword}")

@server.route("/dev/delete_all/", [POST])
def dev_delete_all(request: Request):
    print(request.headers)
    require_authentication(request, strict_auths)

    return JSONResponse(request, {
        "success": True,
        "flag": "#CTF{Zer0_Cool;MessWithTheBest.DieLikeTheRest.}",
        "message": "Congratulations on finding the BossFlag 🎉. Many of the flags in this exercise are based on OWASP Top 10 vulnerabilities. Learn more about them here: https://owasp.org/www-project-top-ten/"
    })

@server.route("/admin/files/")
def admin_dashboard(request: Request):
    require_authentication(request, auths)
    file = request.query_params.get("file")
    print(f"file: {file}.")
    if file == ".env":
        f = open("fake_env.env", 'r')
        fake_env_content = f.read()
        f.close()
        return Response(request, fake_env_content)
    elif file == "/etc/passwd":
        f = open("fake_passwd", 'r')
        fake_passwd_content = f.read()
        f.close()
        return Response(request, fake_passwd_content)
    elif file in os.listdir("ctf_static"):
        return FileResponse(request, file)
    elif file.startswith("../"):
        return Response(request, "#CTF{../PathTraversal}")
    elif file == 'None':
        f = open("ctf_static/filelist_template.html", 'r')
        filelist_template = f.read()
        f.close()

        file_lis = []
        for file in os.listdir("ctf_static"):
            file_lis.append(f'<li><a href="/admin/files/?file={file}">{file}</a></li>')

        file_lis.append("<li>#CTF{SecurityMisconfiguration}</li>")
        lis_str = "\n".join(file_lis)
        files_ul = f"<ul>{lis_str}</ul>"
        filelist_template = filelist_template.replace("{{ files_ul }}", files_ul)
        return Response(request, filelist_template, content_type="text/html")
    else:
        return Response(request, "File Not Found", status=NOT_FOUND_404)


# Start the server.
server.start(str(wifi.radio.ipv4_address))

while True:
    try:
        # Process any waiting requests
        pool_result = server.poll()

        if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
            # Do something only after handling a request
            pass

        # If you want you can stop the server by calling server.stop() anywhere in your code
    except OSError as error:
        print(error)
        continue
