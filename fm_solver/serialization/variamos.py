import pydantic
import typing
import uuid

from fm_solver import feature_model


class Property(pydantic.BaseModel, extra=pydantic.Extra.allow):
    id: uuid.UUID
    name: str
    value: typing.Any
    type: str


class Element(pydantic.BaseModel, extra=pydantic.Extra.allow):
    id: uuid.UUID
    name: str
    type: str
    properties: typing.List[Property]


class Relationship(pydantic.BaseModel, extra=pydantic.Extra.allow):
    id: uuid.UUID
    source_id: uuid.UUID = pydantic.Field(..., alias="sourceId")
    target_id: uuid.UUID = pydantic.Field(..., alias="targetId")
    properties: typing.List[Property]


class Model(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    elements: typing.List[Element]
    relationships: typing.List[Relationship]


ROOT_ELEMENT_TYPE_NAME = "RootFeature"
ABSTRACT_ELEMENT_TYPE_NAME = "AbstractFeature"
CONCRETE_ELEMENT_TYPE_NAME = "ConcreteFeature"
BUNDLE_ELEMENT_TYPE_NAME = "Bundle"

SELECTION_PROPERTY_NAME = "Selected"


def _get_property_by_name(
    properties: typing.List[dict], name: str, default: typing.Any = None
) -> typing.Any:
    return next(
        (
            getattr(property, name, default)
            for property in properties
            if property.name == name
        ),
        default,
    )


def from_variamos_model(
    variamos_model: typing.Dict[str, typing.Any]
) -> feature_model.FeatureModel:
    features, restrictions, id_mapping = [], [], {}

    for element_identifier, element in enumerate(variamos_model):
        if element.type == ROOT_ELEMENT_TYPE_NAME:
            feature = feature_model.Feature(
                identifier=element_identifier,
                name=element.name,
                selection=_get_property_by_name(
                    element.properties,
                    SELECTION_PROPERTY_NAME,
                    feature_model.Selection.UNDEFINED,
                ),
            )
            restriction = feature_model.Root(feature)
            features.append(feature)
            restrictions.append(restriction)

        elif (
            element.type == ABSTRACT_ELEMENT_TYPE_NAME
            or element.type == CONCRETE_ELEMENT_TYPE_NAME
        ):
            feature = feature_model.Feature(
                identifier=element_identifier,
                name=element.name,
                selection=_get_property_by_name(
                    element.properties,
                    SELECTION_PROPERTY_NAME,
                    feature_model.Selection.UNDEFINED,
                ),
            )
            features.append(feature)
