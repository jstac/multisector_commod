
import scipy

class Iterator:
    """ An iterator object has as data a guess w of the value function.  It
    provides methods to update the guess, and to compute a w-greedy policy.
    """
    def __init__(self, cpwaf, mod):
        """ The argument cpwaf is a cpwaf (piecewise continuous affine
        approximation) object, and mod is a (commodity price) model.
        """
        self.af = cpwaf
        self.mod = mod
        self.iterate_number = 0

    def objective(self, x):
        """ Takes as an argument a point x in the state space and returns the
        w-greedy objective function at x, where the argument of the function
        is the control i.
        """
        def ob(i):
            eval_points = scipy.reshape(self.mod.ALPHA * i, (2,1)) + self.mod.Z
            mean_val = scipy.mean(self.af.approx_val(eval_points))
            return -(self.mod.U(x - i) + self.mod.RHO * mean_val) # minus because we minimize!
        return ob


    def update(self):

        self.iterate_number += 1   

        # initialize Tw, DTw
        Tw = scipy.zeros(self.af.number_of_gridpoints) # update
        DTw = scipy.zeros((2, self.af.number_of_gridpoints))

        last_argmax = scipy.zeros(2)  # the starting point in the optimization
        for k in range(self.af.number_of_gridpoints):
            x = self.af.X[:,k]  # the k-th gridpoint
            ob = self.objective(x)  # the function to be maximized
            # Set up the bound to be [0,(1-e)x], where e a small number.
            # The bound is not [0,x] because of some numerical instability.
            bnds = [(0., 0.95*x[0]), (0., 0.95*x[1])]
            # make sure last_argmax in the bounding box
            if last_argmax[0] >= 0.95*x[0]: last_argmax[0] = 0.95*x[0] 
            if last_argmax[1] >= 0.95*x[1]: last_argmax[1] = 0.95*x[1] 
            # now the optimization
            argmax = scipy.optimize.fmin_l_bfgs_b(ob, 
                    last_argmax, bounds = bnds, approx_grad = True)[0]
            # record the results
            Tw[k] = - ob(argmax)  # minus because ob is minus the objective 
            DTw[0,k] = self.mod.DU0(x - argmax)
            DTw[1,k] = self.mod.DU1(x - argmax)
            # and let last_argmax store the current maximizer
            last_argmax = argmax

        self.af.function_vals = Tw
        self.af.derivatives = DTw
        #datafile = "data%d.txt" % counter
        #current_iterate.write_data_for_plot(ALPHA, datafile)


    def policy(self, x, init = scipy.zeros(2)):  
        """ 
        Computes the greedy policy corresponding to the current guess
        of the value function.  The 'x' argument is value of the state
        where the policy is computed, while 'init' is a starting point
        for the optimization search.
        """
        ob = self.objective(x)  # the function to be maximized
        bnds = [(0., 0.95 * x[0]), (0., 0.95 * x[1])]
        if init[0] >= 0.95* x[0]: init[0] = 0.95* x[0] # init must be mutable
        if init[1] >= 0.95* x[1]: init[1] = 0.95* x[1] 
        argmax = scipy.optimize.fmin_l_bfgs_b(ob, 
                    init, bounds = bnds, approx_grad = True)[0]
        return argmax

    def plot(self, datafile):
        self.af.plot(self.mod.ALPHA, datafile)
 
    def time_series(self, init_cond, series_length):
        """
        Generates a simulated time for the price when investment is determined
        by the current greedy policy.
        """
        pass

