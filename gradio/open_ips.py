def archive():
    try:
        with open('ip.txt', 'r') as arquivo:
            ip = arquivo.read()
            ip = ip.splitlines()
    except:
        ip = ["sem arquivo"]
    return ip


