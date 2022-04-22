import time
from matplotlib import pyplot
from fm_solver import feature_model, translator
from fm_solver.feature_model.restriction import Cardinality
from z3 import *
import networkx as nx

from marco import get_id, main

def hentze2021():
    # mobile_phone = feature_model.Feature(identifier=1, name="Mobile Phone")
    # calls = feature_model.Feature(identifier=2, name="Calls")
    # gps = feature_model.Feature(identifier=3, name="GPS")
    # screen = feature_model.Feature(identifier=4, name="Screen")
    # media = feature_model.Feature(identifier=5, name="Media")
    # basic = feature_model.Feature(identifier=6, name="Basic")
    # colour = feature_model.Feature(identifier=7, name="Colour")
    # high_resolution = feature_model.Feature(identifier=8, name="High Resolution")
    # camera = feature_model.Feature(identifier=9, name="Camera")
    # mp3 = feature_model.Feature(identifier=10, name="MP3")

    root = feature_model.Feature(identifier=0, name="root")
    f1 = feature_model.Feature(identifier=1, name="f1") #Carbody
    f2 = feature_model.Feature(identifier=2, name="f2") #Radio
    f3 = feature_model.Feature(identifier=3, name="f3") #Gearbox
    f4 = feature_model.Feature(identifier=4, name="f4") #Ports
    f5 = feature_model.Feature(identifier=5, name="f5") #Navigation
    f6 = feature_model.Feature(identifier=6, name="f6") #Bluetooth
    f7 = feature_model.Feature(identifier=7, name="f7", selection=feature_model.Selection.SELECTED) #Manual
    f8 = feature_model.Feature(identifier=8, name="f8") #Automatic
    f9 = feature_model.Feature(identifier=9, name="f9") #USB
    f10 = feature_model.Feature(identifier=10, name="f10") #CD
    f11 = feature_model.Feature(identifier=11, name="f11") #DigitalCards
    f12 = feature_model.Feature(identifier=12, name="f12") #GPSAntenna
    f13 = feature_model.Feature(identifier=13, name="f13") #Europe
    f14 = feature_model.Feature(identifier=14, name="f14") #USA

    model = feature_model.FeatureModel(
        features=[
            root, f1, f2, f3, f4, f5, f6, f7, f8, f9,
            f10, f11, f12, f13, f14
        ],
        restrictions=[
            feature_model.Root(source=root),
            feature_model.Mandatory(source=root, destination=f1),
            feature_model.Optional(source=root, destination=f2),
            feature_model.Mandatory(source=root, destination=f3),
            feature_model.Optional(source=f2, destination=f4),
            feature_model.Optional(source=f2, destination=f5),
            feature_model.Optional(source=f2, destination=f6),
            feature_model.Range(source=f3, destination=[f7,f8], cardinality=Cardinality(lower_bound=1, upper_bound=1)),
            feature_model.Range(source=f4, destination=[f9,f10], cardinality=Cardinality(lower_bound=1, upper_bound=2)),
            feature_model.Optional(source=f5, destination=f11),
            feature_model.Mandatory(source=f5, destination=f12),
            feature_model.Range(source=f11, destination=[f13,f14], cardinality=Cardinality(lower_bound=1, upper_bound=1)),
            feature_model.Requires(source=f5, destination=f9),
            feature_model.Requires(source=f1, destination=f8),
            feature_model.Requires(source=f11, destination=f7),
        ],
    )

    return model

def create_model1():
    # mobile_phone = feature_model.Feature(identifier=1, name="Mobile Phone")
    # calls = feature_model.Feature(identifier=2, name="Calls")
    # gps = feature_model.Feature(identifier=3, name="GPS")
    # screen = feature_model.Feature(identifier=4, name="Screen")
    # media = feature_model.Feature(identifier=5, name="Media")
    # basic = feature_model.Feature(identifier=6, name="Basic")
    # colour = feature_model.Feature(identifier=7, name="Colour")
    # high_resolution = feature_model.Feature(identifier=8, name="High Resolution")
    # camera = feature_model.Feature(identifier=9, name="Camera")
    # mp3 = feature_model.Feature(identifier=10, name="MP3")

    root = feature_model.Feature(identifier=0, name="root")
    f1 = feature_model.Feature(identifier=1, name="f1")
    f2 = feature_model.Feature(identifier=2, name="f2")
    f3 = feature_model.Feature(identifier=3, name="f3")
    f4 = feature_model.Feature(identifier=4, name="f4")
    f5 = feature_model.Feature(identifier=5, name="f5")
    f6 = feature_model.Feature(identifier=6, name="f6")
    f7 = feature_model.Feature(identifier=7, name="f7")
    f8 = feature_model.Feature(identifier=8, name="f8")
    f9 = feature_model.Feature(identifier=9, name="f9")

    model = feature_model.FeatureModel(
        features=[
            root, f1, f2, f3, f4, f5, f6, f7, f8, f9
        ],
        restrictions=[
            feature_model.Root(source=root),
            feature_model.Mandatory(source=root, destination=f1),
            feature_model.Mandatory(source=f1, destination=f6),
            feature_model.Mandatory(source=f1, destination=f5),
            feature_model.Mandatory(source=f4, destination=f8),
            feature_model.Optional(source=f4, destination=f9),
            feature_model.Optional(source=f3, destination=f7),
            feature_model.Requires(source=f8, destination=f7),
            feature_model.Requires(source=f5, destination=f9),
            feature_model.Excludes(source=f3, destination=f8),
            feature_model.Excludes(source=f3, destination=f5),
            feature_model.Range(source=root, destination=[f2,f3,f4], cardinality=Cardinality(lower_bound=1, upper_bound=1))
        ],
    )

    return model

def create_model2():
    root = feature_model.Feature(identifier=0, name="root")
    f1 = feature_model.Feature(identifier=1, name="f1")
    f2 = feature_model.Feature(identifier=2, name="f2")
    f3 = feature_model.Feature(identifier=3, name="f3 - backdoor")
    f4 = feature_model.Feature(identifier=4, name="f4")
    f5 = feature_model.Feature(identifier=5, name="f5")
    f6 = feature_model.Feature(identifier=6, name="f6")
    f7 = feature_model.Feature(identifier=7, name="f7")
    f8 = feature_model.Feature(identifier=8, name="f8")
    f9 = feature_model.Feature(identifier=9, name="f9 -> back windshield")
    f10 = feature_model.Feature(identifier=10, name="f10")
    f11 = feature_model.Feature(identifier=11, name="f11")
    f12 = feature_model.Feature(identifier=12, name="f12")
    f13 = feature_model.Feature(identifier=13, name="f13")
    f14 = feature_model.Feature(identifier=14, name="f14 -> wiper")
    f15 = feature_model.Feature(identifier=15, name="f15")
    f16 = feature_model.Feature(identifier=16, name="f16 -> antifog")
    f17 = feature_model.Feature(identifier=17, name="f17")
    f18 = feature_model.Feature(identifier=18, name="f18 -> type 1")
    f19 = feature_model.Feature(identifier=19, name="f19 -> type 2")
    f20 = feature_model.Feature(identifier=20, name="f20 -> circuits")
    f21 = feature_model.Feature(identifier=21, name="f21")
    f22 = feature_model.Feature(identifier=22, name="f22")
    f23 = feature_model.Feature(identifier=23, name="f23")
    f24 = feature_model.Feature(identifier=24, name="f24")
    f25 = feature_model.Feature(identifier=25, name="f25")
    f26 = feature_model.Feature(identifier=26, name="f26")
    f27 = feature_model.Feature(identifier=27, name="f27")
    f28 = feature_model.Feature(identifier=28, name="f28")
    f29 = feature_model.Feature(identifier=29, name="f29")

    model = feature_model.FeatureModel(
        features=[
            root, f1, f2, f3, f4, f5, f6, f7, f8, f9,
            f10, f11, f12, f13, f14, f15, f16, f17, f18, f19,
            f20, f21, f22, f23, f24, f25, f26, f27, f28, f29,
        ],
        restrictions=[
            feature_model.Root(source=root), #C0
            feature_model.Mandatory(source=root, destination=f1), #C1
            feature_model.Optional(source=root, destination=f2), #C2
            feature_model.Mandatory(source=root, destination=f3), #C3 -> backdoor
            feature_model.Optional(source=f2,destination=f6), #C4
            feature_model.Optional(source=f2, destination=f5), #C5
            feature_model.Optional(source=f2, destination=f9), #C6 -> back windshield
            feature_model.Optional(source=f2, destination=f8), #C7
            feature_model.Range(source=f3, destination=[f4,f5], cardinality=Cardinality(lower_bound=1, upper_bound=2)), #C8
            feature_model.Optional(source=f9, destination=f15), #C9
            feature_model.Mandatory(source=f9, destination=f16), #C10 -> antifog
            feature_model.Mandatory(source=f9, destination=f20), #C11 -> circuits
            feature_model.Mandatory(source=f9, destination=f14), #C12 -> wiper
            feature_model.Range(source=f9, destination=[f10,f11,f12], cardinality=Cardinality(lower_bound=1, upper_bound=3)), #C13
            feature_model.Optional(source=f9, destination=f17), #C14
            feature_model.Range(source=f20, destination=[f18,f19], cardinality=Cardinality(lower_bound=1, upper_bound=1)), #C15 -> type 1 (18) and type 2 (19)
            feature_model.Mandatory(source=f10, destination=f13), #C16
            feature_model.Mandatory(source=f11, destination=f22), #C17
            feature_model.Optional(source=f11, destination=f21), #C18
            feature_model.Optional(source=f11, destination=f23), #C19
            feature_model.Optional(source=f22, destination=f29), #C20
            feature_model.Mandatory(source=f23, destination=f27), #C21
            feature_model.Mandatory(source=f23, destination=f24), #C22
            feature_model.Optional(source=f23, destination=f25), #C23
            feature_model.Mandatory(source=f23, destination=f28), #C24
            feature_model.Optional(source=f23, destination=f26), #C25
            feature_model.Requires(source=f3, destination=f9), #C26
            feature_model.Excludes(source=f7, destination=f29), #C27
            feature_model.Excludes(source=f19, destination=f29), #C28
            feature_model.Excludes(source=f10, destination=f22), #C29
            feature_model.Excludes(source=f8, destination=f26), #C30
            feature_model.Excludes(source=f24, destination=f25), #C31
            feature_model.Requires(source=f6, destination=f27), #C32
            feature_model.Requires(source=f16, destination=f18), #C33
            feature_model.Requires(source=f17, destination=f5), #C34
            feature_model.Requires(source=f10, destination=f20), #C35
            feature_model.Requires(source=f13, destination=f14), #C36
            feature_model.Requires(source=f18, destination=f23), #C37
            feature_model.Requires(source=f14, destination=f19), #C38
        ],
    )

    return model

def artifical_model():
    root = feature_model.Feature(identifier=0, name="root")
    f1 = feature_model.Feature(identifier=1, name="f1")
    f2 = feature_model.Feature(identifier=2, name="f2")
    f3 = feature_model.Feature(identifier=3, name="f3")
    f4 = feature_model.Feature(identifier=4, name="f4")
    f5 = feature_model.Feature(identifier=5, name="f5")
    f6 = feature_model.Feature(identifier=6, name="f6")

    model = feature_model.FeatureModel(
        features=[
            root, f1, f2, f3, f4, f5, f6
        ],
        restrictions=[
            feature_model.Root(source=root), #C0
            feature_model.Mandatory(source=root, destination=f1), #C1
            feature_model.Mandatory(source=root, destination=f2),
            feature_model.Mandatory(source=f1, destination=f3),
            feature_model.Mandatory(source=f1, destination=f4),
            feature_model.Mandatory(source=f2, destination=f5),
            feature_model.Mandatory(source=f2, destination=f6),
            feature_model.Excludes(source=f3, destination=f4),
            feature_model.Excludes(source=f5, destination=f6)
        ]
    )
    return model


if __name__ == '__main__':
    model = artifical_model()
    z3_constraints, res_hashes, fm_graph = translator.Z3Translator(model).translate()
    # print(z3_constraints)
    # s = Solver()
    # s.add(*z3_constraints)
    # print(s)
    # print(s.check())
    # print([c for c in z3_constraints])
    # print([Bool(str(c)).hash() for c in z3_constraints])
    # print([c.ctx.ref() for c in z3_constraints])
    # print("#############")
    start= time.time()
    mus_hashes = main(z3_constraints)
    end= time.time()
    print(end-start)
    mus_restrictions = []
    for mus_hash_list in mus_hashes:
        restrictions = []
        for constraint_hash in mus_hash_list:
            try:
                restrictions.append(res_hashes[constraint_hash])
            except KeyError:
                print("something went wrong")
                exit(1)
        mus_restrictions.append(restrictions)
    print("success")
    for reslist in mus_restrictions:
        print(reslist)
        print("\n")    
    #print(fm_graph.edges)
    print(len(mus_hashes))
    nx.draw_circular(fm_graph,with_labels=True)
    pyplot.show(block=True)