import matplotlib.pyplot as plt
import random
random.seed(1)
a=[]
s1k=[]
s2k=[]
s3k=[]
Lambda=0.35
Mu=1
for x in range(7000):
    a.append(random.expovariate(Lambda))
    s1k.append(random.expovariate(Mu))
    s2k.append(random.expovariate(Mu))
    s3k.append(random.expovariate(Mu))
plt.figure(1)
ax1=plt.subplot(221)
ax2=plt.subplot(222)
ax3=plt.subplot(223)
ax4=plt.subplot(224)
plt.sca(ax1)
plt.hist(a,50)
plt.title('arrival')
plt.sca(ax2)
plt.hist(s1k,50)
plt.title('s1k')
plt.sca(ax3)
plt.hist(s2k,50)
plt.title('s2k')
plt.sca(ax4)
plt.hist(s3k,50)
plt.title('s3k')
plt.savefig('verify_exp.png')
plt.show()