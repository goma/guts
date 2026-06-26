import exodus3 as exodus
import sys

assert(len(sys.argv) == 2)

efile = sys.argv[1]

e = exodus.exodus(efile)
x,y,z = e.get_coords()
conn, num_elem, num_nodes = e.get_elem_connectivity(1)
conn = list(map(lambda x: x-1, conn))

with open("xi.csv", "w") as f, open("eta.csv", "w") as g:
    print("x,y,z",file=f)
    print("x,y,z",file=g)
    for i in range(num_elem):
        #xi should be 0-1, 2-3
        #eta should be 1-2, 3-0
        nodes = [conn[i*num_nodes + j] for j in range(num_nodes)]
        print(nodes)
        xi1x = x[nodes[0]] + 0.5*(x[nodes[1]] - x[nodes[0]])
        xi1y = y[nodes[0]] + 0.5*(y[nodes[1]] - y[nodes[0]])
        xi2x = x[nodes[3]] + 0.5*(x[nodes[2]] - x[nodes[3]])
        xi2y = y[nodes[3]] + 0.5*(y[nodes[2]] - y[nodes[3]])
        eta1x = x[nodes[1]] + 0.5*(x[nodes[2]] - x[nodes[1]])
        eta1y = y[nodes[1]] + 0.5*(y[nodes[2]] - y[nodes[1]])
        eta2x = x[nodes[0]] + 0.5*(x[nodes[3]] - x[nodes[0]])
        eta2y = y[nodes[0]] + 0.5*(y[nodes[3]] - y[nodes[0]])
        print(xi1x,xi1y,0.0,file=f,sep=',')
        print(xi2x,xi2y,0.0,file=f,sep=',')
        print(eta1x,eta1y,0.0,file=g,sep=',')
        print(eta2x,eta2y,0.0,file=g,sep=',')
        


