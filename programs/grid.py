import scipy
from scipy import *

class Grid:

    def __init__(self, lower, upper, grid_size, distort = 1.0):
        """
        Create a square grid on [lower, upper] x [lower, upper].  The distort
        is a scalar by which all grid points are adjusted: x -> x**distort.
        It can be used to concentrate points near the axes.
        """
        self.distort = distort
        self.lower = lower
        self.upper = upper
        self.grid_size = grid_size  # sqrt should be an integer
        self.X = self.populate_grid()

    def populate_grid(self): 
        """ Creates the grid of points, returning them as a 2 x grid_size
        matrix with X[:,k] the k-th grid point. 
        """
        lwr, upr, gs, d = self.lower, self.upper, self.grid_size, self.distort
        # Grid points will be raised by distort, so adjust upper and lower
        lwr = lwr**(1.0 / d)
        upr = upr**(1.0 / d)

        X = zeros((2, gs))
        J = int(sqrt(gs))
        temp = linspace(lwr, upr, num=J)
        k = 0

        for i in range(J):
            for j in range(J):
                X[0,k], X[1,k] = temp[i], temp[j]
                k += 1

        X = X**d  # finally, transform using distort

        return X


    def eval(self, f):  
        """Evaluates f at each point in the grid and returns the 
        resulting vector.  No real need for speed so uses pure python.
        """
        R = zeros(self.grid_size)
        for k in range(self.grid_size):
            R[k] = f(self.X[:,k])  # f applied to k-th column of X
        return R


