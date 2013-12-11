# -*- coding: utf-8 -*-
import http.client,json,os
import codecs

#proxy sans schema
proxy=None
noproxy=0
host = "www.irem.sciences.univ-nantes.fr"
user=None
#host='localhost:8080'

service = '/mathinfo/x3m0080'

def get_proxy() :
    global proxy
    if proxy : return 
    proxy=os.getenv('http_proxy')
    if not proxy : proxy = os.getenv('HTTP_PROXY')
    if proxy and proxy[:7] == "http://" :
        proxy =  proxy[7:]

def do_request(method, host, path, **args) :
    if not noproxy : get_proxy()
    if proxy :
        h = http.client.HTTPConnection(proxy)
        h.request(method, 'http://' + host + path, **args)
    else:
        h = http.client.HTTPConnection(host)
        h.request(method, path,**args)
    resp   = h.getresponse()
    status = resp.status
    reason = resp.reason
    bd     = resp.read().decode('utf-8')
    h.close()
    return status,reason,bd

def show_example(taskid) :
    path = service + '/example/' + taskid
    status,r,bd = do_request('GET',host,path)
    if status == 200:
        bd = json.loads(bd)
        print("Input   :" , bd['input'])
        print("Result  :" , bd['result'])
    elif status == 404:
        print(bd)
        print(taskid,"not found")
    else:
        print("Error:",status,r,bd)

def get_user() :
    global user
    if user != None:
        etud = user
    else:
        etud = os.getenv("LOGNAME").upper()
    if etud[0] == 'E' : etud = etud[1:]
    print("Identifiant :", etud)
    return etud

def set_user(usr):
    global user
    user = str(usr)

def get_task(taskid) :
    path = service + '/task/' + taskid
    status,r,bd = do_request('GET',host,path)
    if status == 200:
        bd = json.loads(bd)
        return bd['hash'], bd['input']
    if status ==  404 :
        print(bd)
        print(taskid, "not found")
    else:
        print("Error:",status,r,bd)

def check_task(taskid,h,result) :
    path = service + '/task/' + taskid
    body = {'user': get_user(), 'hash':h, 'result': result}
    status,r,bd = do_request('PUT',host,path,body=json.dumps(body))
    if status == 202:
        print("Input accepté")
        return True
    elif status == 406:
        print("Input refusé")
        return False
    elif status == 410:
        print("Hash gone : please retry")
    elif status == 404:
        print("Resource not found :", bd)
    else:
        print("Error:",status,r)
        print("EMsg :",bd)

def hello(etud=None) :
    if not etud : etud = get_user()
    path = service + '/hello/' + etud
    status,r,bd = do_request('GET',host,path)
    if status == 302:
        print("User ", etud, "found")
    elif status == 404:
        print("User ", etud, "not found")
    else:
        print ("Error :", status, r, bd)

def tasklist() :
    hello()
    path   = service + "/tasklist"
    s,r,bd = do_request("GET",host,path)
    if s == 200 :
        print("Tasks :", bd)


def accepted_tasks() :
    user = get_user()
    path = service + '/users/' + user
    s,r,bd = do_request("GET",host,path)
    if s == 200 :
        print("Accepted tasks :",bd)
    elif s == 404 :
        print(s,r,"User not found\n",bd)
    else :
        print("Error :",s,r,bd)


__help = """
Ce module définit trois fonctions :

hello()                   : Est-ce que le serveur vous connait ?

tasklist()                : List des exos.

show_example(exo)         : Cette fonction affiche des exemples pour
                            l'exercice spécifié par l'entier exo.

get_task(exo)             : Cette fonction prend comme argument
                            un entier qui est un numéro d'exercice.
                            Elle renvoie un couple (id,param) où
                            id est un numéro identifiant le dataset
                            param est l'argument pour la fonction
                            client.

check_task(exo,id,result) : Cette fonction envoie le resultat de la
                            fonction client.

accepted_tasks()          : Liste des taches acceptees.

set_user(user)            : Définir le nom d'utilisateur.

valid_<task>()            : Valider un exercice.

valid_tasks()             : Valider l'ensemble des exercices.

generate_primes(n,ppath)  : Génère la liste des nombres premiers
                            inférieurs à n et enregistre cette liste
                            dans le fichier ppath au format json.

Alexis Giraudet
"""

def info() : print(__help)
        
if __name__ == "__main__" :
    info()

# Alexis Giraudet

import math, json

def trivialtask(ls):
    ls.reverse()
    return ls

def valid_trivialtask():
    print("valid trivialtask...")
    (idt, paramt) = get_task("trivialtask")
    print("id =", idt)
    print("param =", paramt)
    result = trivialtask(paramt)
    print("result =", result)
    check_task("trivialtask", idt, result)

def base_ecriture(ls):
    res = list()
    for i in ls:
        n = list()
        quo = i[0]
        base = i[1]
        while quo > 0:
            n.insert(0, quo % base)
            quo = quo // base
        res.append(n)
    return res

def valid_base_ecriture():
    print("valid base_ecriture...")
    (idt, paramt) = get_task("base_ecriture")
    print("id =", idt)
    print("param =", paramt)
    result = base_ecriture(paramt)
    print("result =", result)
    check_task("base_ecriture", idt, result)

def primes(ls):
    res = list()
    for i in ls:
        if i < 2:
            res.append(False)
        else:
            for n in range(2, int(math.sqrt(i))+1):
                if (i % n) == 0:
                    res.append(False)
                    break
            else:
                res.append(True)
    return res

def valid_primes():
    print("valid primes...")
    (idt, paramt) = get_task("primes")
    print("id =", idt)
    print("param =", paramt)
    result = primes(paramt)
    print("result =", result)
    check_task("primes", idt, result)

def factors(ls, ppath="./prime_numbers.json"):
    res = list()
    pr = list()
    try:
        with open(ppath, "r") as pfile:
            print("load prime numbers from file...")
            pr = json.load(pfile)
            print(len(pr), "prime numbers loaded from file")
            pfile.close()
    except IOError:
        pr = [2,3]
    for i in ls:
        print("number =", i)
        if primes([i]) == [True]:
            res.append([[i,1]])
        else:
            fa = list()
            dcc = i
            for p in pr:
                if (dcc % p) == 0:
                    acc = 0
                    while ((dcc % p) == 0) and (dcc > 1):
                        acc += 1
                        dcc = dcc // p
                    fa.append([p,acc])
                if dcc == 1:
                    break
            else:
                print("generate new prime numbers...")
                for j in range(pr[-1]+2,i,2):
                    if primes([j]) == [True]:
                        pr.append(j)
                        if (dcc % j) == 0:
                            acc = 0
                            while ((dcc % j) == 0) and (dcc > 1):
                                acc += 1
                                dcc = dcc // j
                            fa.append([j,acc])
                        if dcc == 1:
                            break
            res.append(fa)
    return res

def valid_factors():
    print("valid factors...")
    (idt, paramt) = get_task("factors")
    print("id = ", idt)
    print("param =", paramt)
    result = factors(paramt)
    print("result = ", result)
    check_task("factors", idt, result)

def stirling_rec(ls):
    def stirling(m, n):
        if m < n:
            return 0
        elif m == n:
            return math.factorial(m)
        elif n == 1:
            return 1
        elif n == 2:
            return (2**m)-2
        else:
            return n*(stirling(m-1, n) + stirling(m-1, n-1))
    return stirling(ls[0], ls[1])

def stirling(ls):
    if ls[0] < ls[1]:
        return 0
    elif ls[0] == ls[1]:
        return math.factorial(m)
    elif ls[1] == 1:
        return 1
    else:
        lm0 = dict()
        lm0[1] = 1
        lm1 = dict()
        for m in range(1,ls[0]-1):
            for n in range(1,ls[1]+1):
                try:
                    sm1n = lm0[n]
                except:
                    sm1n = 0
                try:
                    sm1n1 = lm0[n-1]
                except:
                    sm1n1 = 0
                lm1[n] = n*(sm1n+sm1n1)
            lm0 = lm1
            lm1 = dict()
        return ls[1]*(lm0[ls[1]]+lm0[ls[1]-1])

def valid_stirling():
    print("valid stirling...")
    (idt, paramt) = get_task("stirling")
    print("id = ", idt)
    print("param =", paramt)
    result = stirling(paramt)
    print("result = ", result)
    check_task("stirling", idt, result)

def bezout(ls):
    a = ls[0]
    b = ls[1]
    def bezout(u,v,r,uu,vv,rr):
        if rr == 0:
            return [r, u, v]
        else:
            q = r//rr
            return bezout(uu,vv,rr,u-q*uu,v-q*vv,r-q*rr)
    return bezout(1,0,a,0,1,b)

def valid_bezout():
    print("valid bezout...")
    (idt, paramt) = get_task("bezout")
    print("id = ", idt)
    print("param =", paramt)
    result = bezout(paramt)
    print("result = ", result)
    check_task("bezout", idt, result)

def valid_tasks():
    tasklist()
    print()
    valid_trivialtask()
    print()
    valid_base_ecriture()
    print()
    valid_primes()
    print()
    valid_factors()
    print()
    valid_stirling()
    print()
    valid_bezout()
    print()
    accepted_tasks()

def generate_primes(n=50000000, ppath="./prime_numbers.json"):
    with open(ppath, "w") as pfile:
        pr = list()
        pr.append(2)
        for i in range(3,n,2):
            if primes([i]) == [True]:
                pr.append(i)
        json.dump(pr,pfile)
        pfile.close()
