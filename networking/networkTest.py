from network import Networking

e = Networking("https://spring-codefest-server.frankanator433.repl.co")
print(e.post("join", {"name":"fernk"}))
print(e.post("createGame", {"name":"gam", "settings":{"players":2}}))
print(e.get("getGames"))