import numpy as np
import matplotlib.pyplot as plt


def gaussienne(x,V,m):
    if x>26:
        return(0)
    if (x<=26):
        return(np.sqrt(1/(2*np.pi*V)) *(np.exp(-0.5*(x-m)**2/V)))

x=[k/100 for k in range(3000)]
y=[gaussienne(k/100,31.4,21.198) for k in range(3000)]
plt.clf()
plt.plot(x,y)
plt.show()
