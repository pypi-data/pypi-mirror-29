from osgeo import ogr
import os
import logging

logger = logging.getLogger(__name__)

from hyo.soundspeed.base.gdal_aux import GdalAux
from hyo.soundspeed.profile.dicts import Dicts


class ExportDb:
    """Class that exports sound speed db data"""

    def __init__(self, db):
        self.db = db

    @classmethod
    def export_folder(cls, output_folder):
        folder = os.path.join(output_folder, "export")
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    def _create_ogr_lyr_and_fields(self, ds):
        # create the only data layer
        lyr = ds.CreateLayer('ssp', None, ogr.wkbPoint)
        if lyr is None:
            logger.error("Layer creation failed")
            return

        field = ogr.FieldDefn('pk', ogr.OFTInteger)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        field = ogr.FieldDefn('datetime', ogr.OFTString)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        field = ogr.FieldDefn('sensor', ogr.OFTString)
        field.SetWidth(254)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        field = ogr.FieldDefn('probe', ogr.OFTString)
        field.SetWidth(254)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        field = ogr.FieldDefn('path', ogr.OFTString)
        field.SetWidth(254)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        field = ogr.FieldDefn('agency', ogr.OFTString)
        field.SetWidth(254)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        field = ogr.FieldDefn('survey', ogr.OFTString)
        field.SetWidth(254)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        field = ogr.FieldDefn('vessel', ogr.OFTString)
        field.SetWidth(254)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        field = ogr.FieldDefn('sn', ogr.OFTString)
        field.SetWidth(254)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        field = ogr.FieldDefn('proc_time', ogr.OFTString)
        field.SetWidth(254)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        field = ogr.FieldDefn('proc_info', ogr.OFTString)
        field.SetWidth(254)
        if lyr.CreateField(field) != 0:
            raise RuntimeError("Creating field failed.")

        return lyr

    def export_profiles_metadata(self, project_name, output_folder, ogr_format=GdalAux.ogr_formats['ESRI Shapefile']):

        GdalAux()
        output = os.path.join(self.export_folder(output_folder=output_folder), project_name)

        # create the data source
        try:
            ds = GdalAux.create_ogr_data_source(ogr_format=ogr_format, output_path=output)
            lyr = self._create_ogr_lyr_and_fields(ds)

        except RuntimeError as e:
            logger.error("%s" % e)
            return

        rows = self.db.list_profiles()
        if rows is None:
            raise RuntimeError("Unable to retrieve profiles. Empty database?")
        if len(rows) == 0:
            raise RuntimeError("Unable to retrieve profiles. Empty database?")

        for row in rows:

            ft = ogr.Feature(lyr.GetLayerDefn())
            ft.SetField('pk', int(row[0]))
            ft.SetField('datetime', row[1].isoformat())
            ft.SetField('sensor', Dicts.first_match(Dicts.sensor_types, row[3]))
            ft.SetField('probe', Dicts.first_match(Dicts.probe_types, row[4]))
            ft.SetField('path', row[5])
            if row[6]:
                ft.SetField('agency', row[6])
            if row[7]:
                ft.SetField('survey', row[7])
            if row[8]:
                ft.SetField('vessel', row[8])
            if row[9]:
                ft.SetField('sn', row[9])
            ft.SetField('proc_time', row[10].isoformat())
            ft.SetField('proc_info', row[11])

            pt = ogr.Geometry(ogr.wkbPoint)
            pt.SetPoint_2D(0, row[2].x, row[2].y)

            try:
                ft.SetGeometry(pt)

            except Exception as e:
                RuntimeError("%s > pt: %s, %s" % (e, row[2].x, row[2].y))

            if lyr.CreateFeature(ft) != 0:
                raise RuntimeError("Unable to create feature")
            ft.Destroy()

        ds = None
        return True
