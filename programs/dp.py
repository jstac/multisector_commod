import scipy
import scipy.io
import cpwaf
import grid
import model
import iterator

# first create an instance of the model
model = model.Model2()

# next set up the grid object
GRIDMIN = 0.000001
GRIDMAX = 1.0 / (1.0 - model.ALPHA)
GRIDSIZE = 196  # requires sqrt(GRIDSIZE) is an integer
# now create a grid object (see grid.py)
g = grid.Grid(GRIDMIN, GRIDMAX, GRIDSIZE, distort=1.0/model.ALPHA) 
# initialize an affine approximation object, initial data from U
U_vals = g.eval(model.U)  # evaluates U on each point in the grid
DU = scipy.zeros((2, GRIDSIZE))
DU[0,] = g.eval(model.DU0) # first partial
DU[1,] = g.eval(model.DU1) # second partial
# create an approximation instance that approximates U
cpwaf = cpwaf.CPWAF(GRIDSIZE, g.X, U_vals, DU)
# and an iterator object
iterate = iterator.Iterator(cpwaf, model)

def main():

    counter = 1
    while counter <= 15:
        print "\n\n\n" + str(counter) + "\n\n\n"
        iterate.update()
        counter += 1

    n = 1000
    print "Computing time series for iterate %d" % iterate.iterate_number
    xobs = scipy.zeros((2, n))  # stores state
    iobs = scipy.zeros((2, n))  # and corresponding investment
    pobs = scipy.zeros((2, n))  # and prices
    W = model.rshock(n)
    xobs[:,0] = (1., 1.)  # initial condition
    for t in range(n - 1):
        iobs[:,t] = iterate.policy(xobs[:,t])
        pobs[0:,t] = model.DU0(xobs[:,t] - iobs[:,t])
        pobs[1:,t] = model.DU1(xobs[:,t] - iobs[:,t])
        xobs[:,t+1] = model.ALPHA * iobs[:,t] + W[:,t]
    iobs[:,n-1] = iterate.policy(xobs[:,n-1])
    pobs[0:,n-1] = model.DU0(xobs[:,n-1] - iobs[:,n-1])
    pobs[1:,n-1] = model.DU1(xobs[:,n-1] - iobs[:,n-1])

    scipy.io.write_array('prices.txt', pobs)

