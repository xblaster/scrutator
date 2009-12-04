'''
Created on 1 Dec 2009

@author: wax
'''

def getComputername(identifier):
    return identifier.split("/")[0]


def getNickName():
    firstpart = ['abr', 'ahl', 'white', 'red', 'yellow','spark', 'dark', 'light','ebo','marb','silky','accr','spee','clas','gla','gill','pink','small','Big']
    lastpart = ['angel', 'epo','gold','arr', 'pow','pack', 'tooth','fly','gloo','lab','poll','fii','fit','flow','in','boot','doll','blow','claw']
    
    from random import Random
    rnd = Random()
    
    nickname = firstpart[rnd.randint(0, len(firstpart)-1)]
    nickname = nickname + lastpart[rnd.randint(0, len(lastpart)-1)]
    
    return nickname