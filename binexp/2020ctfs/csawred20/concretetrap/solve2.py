import angr

p = angr.Project("./concrete_trap", auto_load_libs=False)

state = p.factory.entry_state()
sm = p.factory.simulation_manager(state)

sm.explore(find=lambda x: b"Amazing" in x.posix.dumps(1))

print(sm.found[0].posix.dumps(0))
