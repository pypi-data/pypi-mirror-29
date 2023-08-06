"""
Test the CosmoHammerSampler module.

Execute with py.test -v

"""
import numpy as np

from cosmoHammer.ChainContext import ChainContext
from cosmoHammer.pso.ParticleSwarmOptimizer import ParticleSwarmOptimizer
from cosmoHammer.pso.ParticleSwarmOptimizer import Particle
from cosmoHammer.pso.CurvatureFitter import CurvatureFitter

class TestCosmoHammerSampler(object):
    ctx = None
    params = np.array([[1,2,3],[4,5,6]])

    def setup(self):
        self.ctx=ChainContext(self, self.params)

    def test_Particle(self):
        particle = Particle.create(2)
        assert particle.fitness == -np.inf

        assert particle == particle.pbest

        particle2 = particle.copy()
        assert particle.fitness == particle2.fitness
        assert particle.paramCount == particle2.paramCount
        assert (particle.position == particle2.position).all()
        assert (particle.velocity == particle2.velocity).all()


        particle.fitness = 1
        particle.updatePBest()

        assert particle.pbest.fitness == 1


    def test_setup(self):
        low = np.zeros(2)
        high = np.ones(2)
        pso = ParticleSwarmOptimizer(None, low, high, 10)

        assert pso.swarm is not None
        assert len(pso.swarm) == 10

        position = [part.position for part in pso.swarm]

        assert (position>=low).all()
        assert (position<=high).all()

        velocity = [part.velocity for part in pso.swarm]
        assert (velocity == np.zeros(2)).all()

        fitness = [part.fitness == 0 for part in pso.swarm]
        assert all(fitness)

        assert pso.gbest.fitness == -np.inf


    def test_optimize(self):
        np.random.seed(0)
        low = np.zeros(2)
        high = np.ones(2)

        def func(p):
            x, y = p
            return - (x - .5) ** 2 - (y - .25) ** 2, None

        pso = ParticleSwarmOptimizer(func, low, high, 10)

        maxIter = 50
        swarms, gbests = pso.optimize(maxIter)
        assert swarms is not None
        assert gbests is not None

        assert len(swarms) == 42
        assert len(gbests) == 42

        assert np.linalg.norm(pso.gbest.position - np.array((.5, .25))) < 3e-4
        assert pso.gbest.fitness != -np.inf

        fitness = [part.fitness != 0 for part in pso.swarm]
        assert all(fitness)

        cf = CurvatureFitter(pso.swarm, pso.gbest)
        pos, cov = cf.fit()
        assert np.linalg.norm(pos - np.array((.5, .25))) < 3e-4

        cov_tobe = np.array([[  2.04223669e+00,  -1.04304597e+02],
                             [ -1.04304597e+02,   5.62094555e+03]])

        assert np.linalg.norm((cov - cov_tobe).flatten()) < 1e-5

