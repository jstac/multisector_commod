
import scipy
import scipy.stats

class Model1:

    def __init__(self):
        # parameters
        self.RHO = 0.95
        self.ALPHA = 0.95
        self.mean1 = 1
        self.mean2 = 4
        self.gamma = 0.9  # with prob gamma, mean1 shock
        # next we provide a fixed collection of shocks
        # for computing the integrals via monte carlo
        self.MC_SIZE = 1000  # number of observations
        self.Z = self.rshock(self.MC_SIZE)
 
    # utility function and its two partial derivatives
    def U(self, x): return (x[0] * x[1])**0.4
    def DU0(self, x): return 0.4 * (x[0]**(-0.6)) * (x[1]**0.4)
    def DU1(self, x): return 0.4 * (x[0]**0.4) * (x[1]**(-0.6))

    # a function to draw 1 shock from the harvest distribution
    def r_one_shock(self):
        Z = scipy.zeros(2)
        U = scipy.stats.uniform.rvs(size = 2)
        if U[0] <= self.gamma: Z[0] = scipy.stats.norm.rvs(loc = self.mean1)
        else: Z[0] = scipy.stats.norm.rvs(loc = self.mean2)
        if U[1] <= self.gamma: Z[1] = scipy.stats.norm.rvs(loc = self.mean1)
        else: Z[1] = scipy.stats.norm.rvs(loc = self.mean2)
        return scipy.exp(Z)

    # a function to draw n shocks from the harvest distribution
    def rshock(self, n):
        Z = scipy.zeros((2, n))  
        for i in range(n): Z[:,i] = self.r_one_shock()
        return Z

    # density of the shock: expects
    # a 2xn matrix zmat, and returns a vector of evaluations at
    # each point zmat[:,k]
    def phi(self, zmat):
        pass


class Model2:

    def __init__(self):
        # parameters
        self.RHO = 0.95
        self.ALPHA = 0.95
        self.mean = -10.0
        self.sigma = 1.0  
        # next we provide a fixed collection of shocks
        # for computing the integrals via monte carlo
        self.MC_SIZE = 1000  # number of observations
        self.Z = self.rshock(self.MC_SIZE)
 
    # utility function and its two partial derivatives
    
    def U(self, x): return 100*(x[0] * x[1])**0.4
    def DU0(self, x): return 100*0.4 * (x[0]**(-0.6)) * (x[1]**0.4)
    def DU1(self, x): return 100*0.4 * (x[0]**0.4) * (x[1]**(-0.6))

    # a function to draw n shocks from the harvest distribution
    def rshock(self, n):
        Z = scipy.zeros((2, n))
        Z[0,:] = scipy.stats.norm.rvs(loc = self.mean, scale = self.sigma, size = n)
        Z[1,:] = scipy.stats.norm.rvs(loc = self.mean, scale = self.sigma, size = n)
        return scipy.exp(Z)

    # density of the shock: expects
    # a 2xn matrix zmat, and returns a vector of evaluations at
    # each point zmat[:,k]
    def phi(self, zmat):
        pass


