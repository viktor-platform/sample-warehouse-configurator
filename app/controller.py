from viktor import ViktorController
from viktor.geometry import CartesianAxes, Group, Point
from viktor.views import (
    GeometryResult,
    GeometryView,
    MapResult,
    MapView,
)

from app.parametrization import Parametrization

from .model import BuildingExterior, Map, OfficeFrame, WarehouseSteelFrame


class Controller(ViktorController):
    label = "Warehouse configurator"
    parametrization = Parametrization

    @MapView("Map View", duration_guess=1)
    def get_map_view(self, params, **kwargs):
        """Initiates the process of rendering a Map of the terrain and location of the warehouse model."""
        map_plot = Map.from_params(params=params)

        features = []
        if map_plot.land_polygon:
            features.append(map_plot.get_land_polygon())
        if map_plot.building_corner:
            features.append(map_plot.get_office_polygon())
            features.append(map_plot.get_warehouse_polygon())

        return MapResult(features)

    @GeometryView("Building", duration_guess=1, x_axis_to_right=True)
    def visualize_exterior(self, params, **kwargs):
        """Initiates the process of rendering a 3D model of the exterior of the warehouse model."""
        exterior = BuildingExterior.from_params(params).visualize()
        land = Map.from_params(params=params).visualize()
        cartesian = CartesianAxes(Point(0, 0, 0), 10, 0.1)

        exterior = Group([exterior, land, cartesian])
        return GeometryResult(exterior)

    @GeometryView("Structure", duration_guess=10, x_axis_to_right=True)
    def visualize_structure(self, params, **kwargs):
        """Initiates the process of rendering the steel structure of the warehouse model."""
        if params.structure.advanced_settings.visual_settings.warehouse_visible:
            warehouse = WarehouseSteelFrame.from_params(params=params).visualise()
        else:
            warehouse = WarehouseSteelFrame.from_params(params).draw_floor()

        if params.structure.advanced_settings.visual_settings.office_visible:
            office = OfficeFrame.from_params(params=params).visualise()
        else:
            office = OfficeFrame.from_params(params=params).draw_floor()

        beams = Group([warehouse, office])
        return GeometryResult(beams)
