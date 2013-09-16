import scipy
import scipy.weave
import grid

class CPWAF:
    """
    A continuous piecewise affine approximator.
    Initialized with an array of 2D grid points, a vector of values taken by a
    function at each of the grid points, and the partials at the same points.
    The evaluate method gives the approximation and is vectorized.  To exploit
    the speed of the C code it should be called with arrays of input values.
    """

    def __init__(self, number_of_gridpoints, gridpoints, function_vals, derivatives):
        """
        Notation: X, W, DW = gridpoints, function_vals, derivatives.
        X is 2XK matrix of grid points (x_0,...x_K) with each x_k a point in
        the plane.  W is K-vector of function values (w(x_0),...,w(x_K)), and
        DW is a 2xK Jacobian matrix (Dw(x_0),...,Dw(x_K)).
        """
        self.number_of_gridpoints = number_of_gridpoints
        self.X = gridpoints
        self.function_vals = function_vals
        self.derivatives = derivatives

    def approx_val(self, Y):
        """
        Given a 2xK array Y of K points in the plane, find corresponding
        approximate values.
        """

        # first prepare the input arrays:

        X0 = self.X[0,] # first row of X
        X1 = self.X[1,] # second row
        W = self.function_vals  # the function W evaluated on the grid 
        DW0 = self.derivatives[0,] # first row of DW
        DW1 = self.derivatives[1,] # second row
        Y0 = Y[0,] # first row of Y
        Y1 = Y[1,] # second row

        # and a output array:

        R = scipy.zeros(len(Y0))

        # next the C code.

        code = r"""
        double tmp;
        double running_min = pow(10,100);  /* large double */
        int k; int j; 
        int K = NX0[0];  /* length of vector X0 */
        int J = NY0[0];  /* length of vector Y0 */

        for (j=0; j<J; j++) {

            for(k=0; k<K; k++) {
                tmp = W[k] + DW0[k] * (Y0[j] - X0[k]) 
                    + DW1[k] * (Y1[j] - X1[k]);
                if (tmp < running_min) running_min = tmp;
            }

            R[j] = running_min;
            running_min = pow(10, 100);
        }
        """

        scipy.weave.inline(code, ['Y0', 'Y1', 
                                  'X0', 'X1', 
                                  'DW0', 'DW1',
                                  'R', 'W'], compiler = 'gcc')
        return R



    def plot(self, alpha, datafile):
        """
        The affine approximation knows how to plot itself.  This method
        produces a 3D plot of the function surface.  The constant alpha
        distorts the grid so that points are close together near the origin
        """
        f = open(datafile, "w")
        last = self.X[0,0]
        for j in range(self.number_of_gridpoints):
            if self.X[0,j] != last: f.write("\n") # for gnuplot format
            f.write("%f, %f, %f\n" % (self.X[0,j], self.X[1,j], self.function_vals[j]))
            last = self.X[0,j]
        f.close()
