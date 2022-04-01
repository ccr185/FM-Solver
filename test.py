from fm_solver import feature_model, translator
from fm_solver.feature_model.restriction import Cardinality
from swiplserver import PrologMQI, PrologThread
import os

def create_model():
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
            feature_model.Range(source=root, destination=[f2,f3,f4], cardinality=Cardinality(1,1))
        ],
    )

    return model



if __name__ == '__main__':
    model = create_model()
    minizinc_problem = translator.MiniZincArithmeticTranslator(model).translate()
    with open('workfile.mzn', 'w') as f:
        f.write(minizinc_problem)
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            result = prolog_thread.query("['/home/kaiser185/workspace/variamos-minizinc-mus/main.pl']")
            path = os.path.abspath("./workfile.mzn")
            constraints = prolog_thread.query(f'read_and_collect_lines("{path}", Conss)')
            print(constraints)
            os.remove(path=path)

            
