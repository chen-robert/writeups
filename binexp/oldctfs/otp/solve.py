import angr
import claripy

pw = claripy.BVS('pw', 100 * 8)
p = angr.Project("./otp", auto_load_libs=False)

state = p.factory.entry_state(addr=0x40080e, args=["./otp", pw], add_options={ angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY })

def AND1(c):
  return claripy.Or(claripy.And(48 <= c , c <= 57), claripy.And(97 <= c, c <= 102))

for i in range(100):
  state.solver.add( AND1(pw.get_byte(i)) ) 

sm = p.factory.simulation_manager(state)



sm.explore(find=lambda x: b"congrats!" in x.posix.dumps(1))
#sm.explore(find=0x4009e0)

print(sm.found[0].posix.dumps(0))
