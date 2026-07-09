import random
def jet_de_des(face,nb):
    return sum(random.randint(1, face) for _ in range(nb))