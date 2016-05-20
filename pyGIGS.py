#PyGIGS contains functions for performing GIGS (Geospatial Integrity of Geoscience Software) test within PyOcean (Schlumberger Ocean/Petrel platform).
#Please see www.iogp.org/pubs/430-1.pdf and www.iogp.org/pubs/430-2.pdf for more info


from Slb.Ocean.Petrel import *
from Slb.Ocean.Petrel.DomainObject.Seismic import *
from Slb.Ocean.Core import *
from Slb.Ocean.Basics import *

from Slb.Ocean.Catalogs import *
from Slb.Ocean.Coordinates import *
from Slb.Ocean.CoordinateSystems import *
from Slb.Ocean.Data import *
from Slb.Ocean.Geometry import *
from Slb.Ocean.Units import *
from Slb.Ocean.Petrel.Basics import *
from Slb.Ocean.Petrel.Data import *
from Slb.Ocean.Petrel.DomainObject import *
from Slb.Ocean.Petrel.DomainObject.Seismic import *
from Slb.Ocean.Petrel.DomainObject.Shapes import *
from Slb.Ocean.Petrel.DomainObject.Well import *
from Slb.Ocean.Petrel.DomainObject.FaultModel import *
from Slb.Ocean.Petrel.IO import *
from Slb.Ocean.Petrel.Licensing import *
from Slb.Ocean.Petrel.PropertyModeling import *
from Slb.Ocean.Petrel.Seismic import *
from Slb.Ocean.Petrel.SeismicAttribute import *
from Slb.Ocean.Petrel.Simulation import *
from Slb.Ocean.Petrel.UI import *
from Slb.Ocean.Petrel.Uncertainty import *
from Slb.Ocean.Petrel.Workflow import *

from Slb.Ocean.Coordinates import PrePostUnitConversions


def DoTestPoints5100(projCRS,pt_set):
  
  coord_service = CoreSystem.GetService(ICoordinateService)
  catalog_service = CoreSystem.GetService(ICatalogService)
  unit_service = CoreSystem.GetService(IUnitService)

  print "51xx: Projection Test\n%s [%s] to %s [%s]" % (projCRS.ReferenceCoordSys,projCRS.ReferenceCoordSys.AuthorityCode,projCRS,projCRS.AuthorityCode)
  opB = coord_service.CreateOperationToReference(projCRS, PrePostUnitConversions.FromSI)[1]
  opA = coord_service.CreateOperationFromReference(projCRS, PrePostUnitConversions.ToSI)[1]
  
  pt_set_len = len(pt_set)
  meter_unit = unit_service.Catalogs[0].GetUnit('Meter')
  m_to_crsunit = PetrelUnitSystem.GetConverter( meter_unit,projCRS.NativeSurfaceUnit)
  crsunit_to_m = PetrelUnitSystem.GetConverter( projCRS.NativeSurfaceUnit,meter_unit)
      
  for i in range(0, pt_set_len):
    if pt_set[i][2] == 'A':
      result = opA.Convert( Point3( pt_set[i][1], pt_set[i][0],0) )[1]
      
     
      result = Point3( m_to_crsunit.Convert(result.X), m_to_crsunit.Convert(result.Y),0)
      
      print "A\t%s\t%s\t%s\t%s" % ( pt_set[i][0], pt_set[i][1], result.X, result.Y)
    else:
      result = opB.Convert( Point3( crsunit_to_m.Convert(pt_set[i][0]), crsunit_to_m.Convert(pt_set[i][1]),0) )[1]
      print "B\t%s\t%s\t%s\t%s" % ( result.Y, result.X, pt_set[i][0], pt_set[i][1])



def DoTestPoints5200(srcCRS,targetCRS,transform,pt_set):
  
  coord_service = CoreSystem.GetService(ICoordinateService)
  catalog_service = CoreSystem.GetService(ICatalogService)
  unit_service = CoreSystem.GetService(IUnitService)

  print "52xx: Transform Test\n%s [%s] (%s) <-> %s [%s] (%s)" % (srcCRS,srcCRS.AuthorityCode,srcCRS.NativeSurfaceUnit,targetCRS,targetCRS.AuthorityCode,targetCRS.NativeSurfaceUnit)
  #transform = coord_service.GetCartographicTransform("EPSG:1764")[1]
  opB = coord_service.CreateOperation(targetCRS,srcCRS, [transform], PrePostUnitConversions.None)[1]
  opA = coord_service.CreateOperation(srcCRS,targetCRS,[transform], PrePostUnitConversions.None)[1]
  
  print opA
  print opB
  pt_set_len = len(pt_set)
  unit_catalog = unit_service.Catalogs[0]
  
  #meter_unit = unit_catalog.GetUnit('Meter')
  #m_to_srcCRSunit = unit_catalog.GetConverter( meter_unit,srcCRS.NativeSurfaceUnit)
  #m_to_targetCRSunit = unit_catalog.GetConverter( meter_unit,targetCRS.NativeSurfaceUnit)
  #targetCRSunit_to_m = unit_catalog.GetConverter( targetCRS.NativeSurfaceUnit,meter_unit)
  #srcCRSunit_to_m = unit_catalog.GetConverter( srcCRS.NativeSurfaceUnit,meter_unit)
      
  for i in range(0, pt_set_len):
    if pt_set[i][2] == 'A':
      result = opA.Convert( Point3( pt_set[i][1], pt_set[i][0],0) )[1]
      #result = Point3( pt_set[i][0], pt_set[i][1],0)
     
      #result = Point3( m_to_crsunit.Convert(result.X), m_to_crsunit.Convert(result.Y),0)
      
      print "A\t%s\t%s\t%s\t%s" % ( pt_set[i][0], pt_set[i][1], result.X, result.Y)
    else:
      
      result = opB.Convert( Point3( pt_set[i][1], pt_set[i][0],0) )[1]
      #result = opB.Convert( Point3( crsunit_to_m.Convert(pt_set[i][0]), crsunit_to_m.Convert(pt_set[i][1]),0) )[1]
      print "B\t%s\t%s\t%s\t%s" % ( result.Y, result.X, pt_set[i][1], pt_set[i][0])
      pass


def DoTestPoints5100ThousandIterations(projCRS,pt):
  coord_service = CoreSystem.GetService(ICoordinateService)
  catalog_service = CoreSystem.GetService(ICatalogService)
  unit_service = CoreSystem.GetService(IUnitService)
  print "51xx: 1000 Iteration Projection Test\n%s [%s] to %s [%s]" % (projCRS.ReferenceCoordSys,projCRS.ReferenceCoordSys.AuthorityCode,projCRS,projCRS.AuthorityCode)
  opB = coord_service.CreateOperationToReference(projCRS, PrePostUnitConversions.None)[1]
  opA = coord_service.CreateOperationFromReference(projCRS, PrePostUnitConversions.None)[1]
  
  
  meter_unit = unit_service.Catalogs[0].GetUnit('Meter')
  m_to_crsunit = PetrelUnitSystem.GetConverter( meter_unit,projCRS.NativeSurfaceUnit)
  crsunit_to_m = PetrelUnitSystem.GetConverter( projCRS.NativeSurfaceUnit,meter_unit)
  
  tmp_point =  Point3(pt[1],pt[0],0)
  
  #print tmp_point
  
  for i in range(0, 1000):
    tmp_point = opA.Convert( Point3( tmp_point.X, tmp_point.Y,0) )[1] # convert lat long to XY
    tmp_point = Point3( m_to_crsunit.Convert(tmp_point.X), m_to_crsunit.Convert(tmp_point.Y),0)
    tmp_point = opB.Convert( Point3( tmp_point.X, tmp_point.Y,0) )[1] # convert XY to lat long
  print tmp_point
