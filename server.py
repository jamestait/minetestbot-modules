#!/usr/bin/env python
"""
server.py - Phenny Minetest Server Module
Copyright 2013, Sfan5
"""

import web, json, random

def by_random(tbl, arg):
    return [random.randrange(0, len(tbl))]

def by_address(tbl, arg):
    results = []
    for i in range(0, len(tbl)):
        e = tbl[i]
        if arg.lower().strip() in e["address"].lower().strip():
            results.append(i)
    return results

def by_name(tbl, arg):
    results = []
    for i in range(0, len(tbl)):
        e = tbl[i]
        if arg.lower().strip() in e["name"].lower().strip():
            results.append(i)
    return results

def by_players(tbl, arg):
    results = []
    if arg.startswith("<"): # less comparing
        try:
            nu = int(arg[1:])
        except:
            return []
        for i in range(0, len(tbl)):
            if int(tbl[i]["clients"]) < nu:
                results.append(i)
    elif arg.startswith(">"): # more comparing
        try:
            nu = int(arg[1:])
        except:
            return []
        for i in range(0, len(tbl)):
            if int(tbl[i]["clients"]) > nu:
                results.append(i)
    elif arg == "most": # most
        ranking = (-1, None)
        for i in range(0, len(tbl)):
            if int(tbl[i]["clients"]) > ranking[0]:
                ranking = (int(tbl[i]["clients"]), i)
        if ranking[1]: results.append(ranking[1])
    elif arg == "least": # least
        ranking = (9999, None)
        for i in range(0, len(tbl)):
            if int(tbl[i]["clients"]) < ranking[0]:
                ranking = (int(tbl[i]["clients"]), i)
        if ranking[1]: results.append(ranking[1])
    elif arg.startswith("!"): # not comparing
        try:
            nu = int(arg[1:])
        except:
            return []
        for i in range(0, len(tbl)):
            if int(tbl[i]["clients"]) != nu:
                results.append(i)
    else:
        if arg.startswith("="): # support "3" and "=3"
            arg = arg[1:]
        try:
            nu = int(arg)
        except:
            return []
        for i in range(0, len(tbl)):
            if int(tbl[i]["clients"]) == nu:
                results.append(i)
    return results

def by_ping(tbl, arg):
    results = []
    if arg.startswith("<"): # less comparing
        try:
            nu = float(arg[1:])
        except:
            return []
        for i in range(0, len(tbl)):
            if float(tbl[i]["ping"]) < nu:
                results.append(i)
    elif arg.startswith(">"): # more comparing
        try:
            nu = float(arg[1:])
        except:
            return []
        for i in range(0, len(tbl)):
            if float(tbl[i]["ping"]) > nu:
                results.append(i)
    elif arg == "most": # most
        ranking = (-1, None)
        for i in range(0, len(tbl)):
            if float(tbl[i]["ping"]) > ranking[0]:
                ranking = (float(tbl[i]["ping"]), i)
        if ranking[1]: results.append(ranking[1])
    elif arg == "least": # least
        ranking = (9999, None)
        for i in range(0, len(tbl)):
            if float(tbl[i]["ping"]) < ranking[0]:
                ranking = (float(tbl[i]["ping"]), i)
        if ranking[1]: results.append(ranking[1])
    elif arg.startswith("!"): # not comparing
        try:
            nu = float(arg[1:])
        except:
            return []
        for i in range(0, len(tbl)):
            if float(tbl[i]["ping"]) != nu:
                results.append(i)
    else:
        if arg.startswith("="): # support "0.6" and "=0.6"
            arg = arg[1:]
        try:
            nu = float(arg)
        except:
            return []
        for i in range(0, len(tbl)):
            if float(tbl[i]["clients"]) == nu:
                results.append(i)
    return results

def by_index(tbl, arg):
    if arg == "last":
        return [len(tbl) - 1]
    else:
        try:
            if int(arg) < len(tbl) - 1:
                return [int(arg)]
        except:
            return []

def by_port(tbl, arg):
    results = []
    if arg.startswith("<"): # less comparing
        try:
            nu = int(arg[1:])
        except:
            return []
        for i in range(0, len(tbl)):
            if int(tbl[i]["port"]) < nu:
                results.append(i)
    elif arg.startswith(">"): # more comparing
        try:
            nu = int(arg[1:])
        except:
            return []
        for i in range(0, len(tbl)):
            if int(tbl[i]["port"]) > nu:
                results.append(i)
    elif arg.startswith("!"): # not comparing
        try:
            nu = int(arg[1:])
        except:
            return []
        for i in range(0, len(tbl)):
            if int(tbl[i]["port"]) != nu:
                results.append(i)
    else:
        if arg.startswith("="): # support "3" and "=3"
            arg = arg[1:]
        try:
            nu = int(arg)
        except:
            return []
        for i in range(0, len(tbl)):
            if int(tbl[i]["port"]) == nu:
                results.append(i)
    return results

def server(phenny, input):
    for x in phenny.bot.commands["high"].values():
       if x[0].__name__ == "aa_hook":
           if x[0](phenny, input):
               return # Abort function

    arg = input.group(2)
    if not arg:
        cfuncs = [by_random]
        cargs = [None]
    else:
        arg = arg.split(" ")
        cfuncs = []
        cargs = []
        for a in arg:
            if a.startswith("addr:"):
                choicefunc = by_address
                carg = a[len("addr:"):]
            elif a.startswith("name:"):
                choicefunc = by_address
                carg = a[len("name:"):]
            elif a.startswith("players:"):
                choicefunc = by_players
                ca = a[len("players:"):]
            elif a.startswith("ping:"):
                choicefunc = by_ping
                carg = a[len("ping:"):]
            elif a.startswith("i:"):
                choicefunc = by_index
                carg = a[len("i:"):]
            elif a.startswith("port:"):
                choicefunc = by_port
                carg = a[len("port:"):]
            elif a == "random":
                choicefunc = by_random
                carg = ""
            else:
                choicefunc = by_name
                carg = a
            cfuncs.append(choicefunc)
            cargs.append(carg)

    text = web.get("http://servers.minetest.net/list")
    server_list = json.loads(text)["list"]
    prep_table = server_list
    for i in range(0, len(cfuncs)):
        choicefunc = cfuncs[i]
        carg = cargs[i]

        choices = choicefunc(prep_table, carg)
        if len(choices) == 0:
            return phenny.reply("No results")
        prep_table = []
        for idx in range(0, len(server_list)):
            if idx in choices:
                prep_table.append(server_list[idx])

    choice = choices[0]
    name = server_list[choice]["name"]
    address = server_list[choice]["address"]
    if server_list[choice]["port"] != "30000":
        address += ":" + server_list[choice]["port"]
    clients = server_list[choice]["clients"]
    try:
        version = server_list[choice]["version"] + " " + server_list[choice]["gameid"]
    except:
        version = server_list[choice]["version"]
    ping = server_list[choice]["ping"]
    clients_max = server_list[choice]["clients_max"]

    phenny.reply("%s | %s | Clients: %s/%s | Version: %s | ping: %s" % (name, address, clients, clients_max, version, ping))

server.commands = ['sv', 'server']
server.thread = True

if __name__ == '__main__':
   print __doc__
