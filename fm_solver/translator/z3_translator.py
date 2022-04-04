from dataclasses import dataclass
import functools
import typing
from uuid import uuid4

from fm_solver import feature_model
from fm_solver.translator import translator

from z3 import *

import networkx as nx

class Z3Translator(translator.Translator):
    def translate(self):
        csp = []
        res_hashes = {}
        fm_graph = nx.DiGraph()

        model_features_keys = self.feature_model.features.keys()
        feats_dict = dict(zip(model_features_keys, BoolVector('f',len(model_features_keys))))

        for id, feature in self.feature_model.features.items():
            fm_graph.add_node(id, feature=feature)
        # for feature in self.feature_model.features.values():
        #     csp.append(self.translate_feature(feature))

        for restriction in self.feature_model.restrictions:
            z3_constraint = self.translate_restriction(restriction, feats_dict, fm_graph)
            csp.append(z3_constraint)
            res_hashes[Bool(str(z3_constraint)).hash()] = restriction
        
        return csp, res_hashes, fm_graph

    def translate_feature(self, feature: feature_model.Feature) -> str:
        if feature.selection == feature_model.Selection.SELECTED:
            return f"var 0..1: feature_{feature.identifier} = 1;"

        if feature.selection == feature_model.Selection.UNSELECTED:
            return f"var 0..1: feature{feature.identifier} = 0;"

        return f"var 0..1: feature_{feature.identifier};"

    @functools.singledispatchmethod
    def translate_restriction(self, restriction, feats_dict: dict, fm_graph: nx.DiGraph) -> BoolRef:
        raise NotImplementedError

    @translate_restriction.register
    def _(self, restriction: feature_model.Root, feats_dict: dict, _: nx.DiGraph) -> BoolRef:
        #No edge for the root for now
        return feats_dict[restriction.source.identifier] == True
        # return f"constraint (feature_{restriction.source.identifier} == 1);"

    @translate_restriction.register
    def _(self, restriction: feature_model.Mandatory, feats_dict: dict, fm_graph: nx.DiGraph) -> BoolRef:
        fm_graph.add_edge(restriction.source.identifier, restriction.destination[0].identifier, restriction=restriction)
        return feats_dict[restriction.source.identifier] == feats_dict[restriction.destination[0].identifier]
        # return (
        #     f"constraint (feature_{restriction.source.identifier} "
        #     + f"== feature_{restriction.destination[0].identifier});"
        # )

    @translate_restriction.register
    def _(self, restriction: feature_model.Optional, feats_dict: dict, fm_graph: nx.DiGraph) -> BoolRef:
        fm_graph.add_edge(restriction.source.identifier,restriction.destination[0].identifier,restriction=restriction)
        return Implies(
            feats_dict[restriction.destination[0].identifier],
            feats_dict[restriction.source.identifier])
        # return (
        #     f"constraint (feature_{restriction.destination[0].identifier} "
        #     + f"<= feature_{restriction.source.identifier});"
        # )

    @translate_restriction.register
    def _(self, restriction: feature_model.Requires, feats_dict: dict, fm_graph: nx.DiGraph) -> BoolRef:
        fm_graph.add_edge(restriction.source.identifier,restriction.destination[0].identifier,restriction=restriction)
        return Implies(
            feats_dict[restriction.source.identifier],
            feats_dict[restriction.destination[0].identifier]
        )
        # return (
        #     f"constraint (feature_{restriction.source.identifier} = 1) -> "
        #     + f"(feature_{restriction.destination[0].identifier} = 1);"
        # )

    @translate_restriction.register
    def _(self, restriction: feature_model.Excludes, feats_dict: dict, fm_graph: nx.DiGraph) -> BoolRef:
        fm_graph.add_edge(restriction.source.identifier,restriction.destination[0].identifier,restriction=restriction)
        return Not(And(
            feats_dict[restriction.source.identifier],
            feats_dict[restriction.destination[0].identifier]
        ))
        # return (
        #     f"constraint not (feature_{restriction.source.identifier} = 1 /\\ "
        #     + f"feature_{restriction.destination[0].identifier} = 1);"
        # )

    def build_cardinality_restriction(
        self,
        restriction: typing.Union[
            feature_model.And, feature_model.Or, feature_model.Xor, feature_model.Range
        ],
        feats_dict: dict, fm_graph: nx.DiGraph
    ) -> BoolRef:
        card_elems = [feats_dict[dest.identifier] for dest in restriction.destination]
        uuid = uuid4()
        fm_graph.add_node(uuid,bundle=True,restriction=restriction)
        fm_graph.add_edge(restriction.source.identifier,uuid,restriction=restriction)
        for dest in restriction.destination:
            fm_graph.add_edge(uuid,dest.identifier,restriction=restriction)
        return Implies(feats_dict[restriction.source.identifier],And(
            AtLeast(*card_elems, restriction.cardinality.lower_bound),
            AtMost(*card_elems, restriction.cardinality.upper_bound)
        ))
        # destination_sum = " + ".join(
        #     [
        #         f"feature_{restriction.identifier}"
        #         for restriction in restriction.destination
        #     ]
        # )

        # return (
        #     f"constraint (feature_{restriction.source.identifier} * {restriction.cardinality.lower_bound} <= {destination_sum}) /\\ "
        #     + f"({destination_sum} <= feature_{restriction.source.identifier} * {restriction.cardinality.upper_bound});"
        # )

    @translate_restriction.register
    def _(self, restriction: feature_model.And, feats_dict: dict, fm_graph: nx.DiGraph) -> BoolRef:
        return self.build_cardinality_restriction(restriction, feats_dict, fm_graph)

    @translate_restriction.register
    def _(self, restriction: feature_model.Or, feats_dict: dict, fm_graph: nx.DiGraph) -> BoolRef:
        return self.build_cardinality_restriction(restriction, feats_dict, fm_graph)

    @translate_restriction.register
    def _(self, restriction: feature_model.Xor, feats_dict: dict, fm_graph: nx.DiGraph) -> BoolRef:
        return self.build_cardinality_restriction(restriction, feats_dict, fm_graph)

    @translate_restriction.register
    def _(self, restriction: feature_model.Range, feats_dict: dict, fm_graph: nx.DiGraph) -> BoolRef:
        return self.build_cardinality_restriction(restriction, feats_dict, fm_graph)
