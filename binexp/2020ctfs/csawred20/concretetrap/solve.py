import angr
import claripy

p = angr.Project("./concrete_trap")

state = p.factory.entry_state()

sm = p.factory.simulation_manager(state)

sm.explore(find=0x400dcf, avoid=0x400d05)

print(sm.found[0].posix.dumps(0))
