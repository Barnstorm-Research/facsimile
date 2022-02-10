import facsimile.framework as F
import facsimile.SIRexample as sirex

def test_get_ABM_dynamics_factor():
    sirex.get_ABM_dynamics_factor()

def test_distribute_to_abm():
    abm = F.Distribute_to_ABM(
        sirex.get_ABM_dynamics_factor(),
        sirex.get_space_factor(3),
        sirex.get_parameters_factor()
    )
    x = 10
    assert True
