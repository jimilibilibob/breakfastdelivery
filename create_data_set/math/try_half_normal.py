import matplotlib.pyplot as plt
import math
import statistics
import random
import matplotlib.ticker

def n_try(n, mu):
    results = []
    for i in range(0,n):
        results.append(abs(random.gauss(0,mu)))
    return results

def main():
    averages, mus= [], []
    min_mu,max_mu = 20, 80
    repeat= 100000
    for i in range(min_mu,max_mu+1):
        print("%s/%s" % (i, max_mu) )
        averages.append(round(statistics.mean(n_try(repeat,i)),2))
        mus.append(i)
    print('Ready to plot')
    plt.plot(mus,averages)
    plt.gca().yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
    plt.gca().xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(3))
    plt.savefig('half_normal.png')
    print('Done')

if __name__ == "__main__":
    main()