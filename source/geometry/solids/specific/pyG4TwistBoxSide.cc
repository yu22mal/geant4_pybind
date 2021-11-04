#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <G4TwistBoxSide.hh>
#include <G4AffineTransform.hh>
#include <G4VoxelLimits.hh>
#include <G4VPVParameterisation.hh>
#include <G4VPhysicalVolume.hh>
#include <G4VGraphicsScene.hh>
#include <G4Polyhedron.hh>
#include <G4VisExtent.hh>
#include <G4DisplacedSolid.hh>

#include "typecast.hh"
#include "opaques.hh"

namespace py = pybind11;

class PyG4TwistBoxSide : public G4TwistBoxSide, public py::trampoline_self_life_support {
public:
   using G4TwistBoxSide::G4TwistBoxSide;

   G4ThreeVector SurfacePoint(G4double arg0, G4double arg1, G4bool isGlobal) override
   {
      PYBIND11_OVERRIDE_PURE(G4ThreeVector, G4TwistBoxSide, SurfacePoint, arg0, arg1, isGlobal);
   }

   G4double GetBoundaryMin(G4double arg0) override
   {
      PYBIND11_OVERRIDE_PURE(G4double, G4TwistBoxSide, GetBoundaryMin, arg0);
   }

   G4double GetBoundaryMax(G4double arg0) override
   {
      PYBIND11_OVERRIDE_PURE(G4double, G4TwistBoxSide, GetBoundaryMax, arg0);
   }

   G4double GetSurfaceArea() override { PYBIND11_OVERRIDE_PURE(G4double, G4TwistBoxSide, GetSurfaceArea, ); }

   G4int GetAreaCode(const G4ThreeVector &xx, G4bool withtol) override
   {
      PYBIND11_OVERRIDE_PURE(G4int, G4TwistBoxSide, GetAreaCode, xx, withtol);
   }

   G4ThreeVector GetNormal(const G4ThreeVector &xx, G4bool isGlobal) override
   {
      PYBIND11_OVERRIDE(G4ThreeVector, G4TwistBoxSide, GetNormal, xx, isGlobal);
   }

   G4int DistanceToSurface(const G4ThreeVector &gp, const G4ThreeVector &gv, G4ThreeVector *gxx, G4double *distance,
                           G4int *areacode, G4bool *isvalid, G4VTwistSurface::EValidate validate) override
   {
      PYBIND11_OVERRIDE(G4int, G4TwistBoxSide, DistanceToSurface, gp, gv, gxx, distance, areacode, isvalid, validate);
   }

   G4int DistanceToSurface(const G4ThreeVector &gp, G4ThreeVector *gxx, G4double *distance, G4int *areacode) override
   {
      PYBIND11_OVERRIDE(G4int, G4TwistBoxSide, DistanceToSurface, gp, gxx, distance, areacode);
   }

   G4int AmIOnLeftSide(const G4ThreeVector &me, const G4ThreeVector &vec, G4bool withTol) override
   {
      PYBIND11_OVERRIDE(G4int, G4TwistBoxSide, AmIOnLeftSide, me, vec, withTol);
   }

   G4double DistanceToBoundary(G4int areacode, G4ThreeVector &xx, const G4ThreeVector &p) override
   {
      PYBIND11_OVERRIDE_IMPL(G4double, G4TwistBoxSide, "DistanceToBoundary", areacode, std::addressof(xx), p);
      return G4TwistBoxSide::DistanceToBoundary(areacode, xx, p);
   }

   G4double DistanceToIn(const G4ThreeVector &gp, const G4ThreeVector &gv, G4ThreeVector &gxxbest) override
   {
      PYBIND11_OVERRIDE_IMPL(G4double, G4TwistBoxSide, "DistanceToIn", gp, gv, std::addressof(gxxbest));
      return G4TwistBoxSide::DistanceToIn(gp, gv, gxxbest);
   }

   G4double DistanceToOut(const G4ThreeVector &gp, const G4ThreeVector &gv, G4ThreeVector &gxxbest) override
   {
      PYBIND11_OVERRIDE_IMPL(G4double, G4TwistBoxSide, "DistanceToOut", gp, gv, std::addressof(gxxbest));
      return G4TwistBoxSide::DistanceToOut(gp, gv, gxxbest);
   }

   G4double DistanceTo(const G4ThreeVector &gp, G4ThreeVector &gxx) override
   {
      PYBIND11_OVERRIDE_IMPL(G4double, G4TwistBoxSide, "DistanceTo", gp, std::addressof(gxx));
      return G4TwistBoxSide::DistanceTo(gp, gxx);
   }

   G4String GetName() const override { PYBIND11_OVERRIDE(G4String, G4TwistBoxSide, GetName, ); }

   void GetBoundaryParameters(const G4int &areacode, G4ThreeVector &d, G4ThreeVector &x0,
                              G4int &boundarytype) const override
   {
      PYBIND11_OVERRIDE(void, G4TwistBoxSide, GetBoundaryParameters, areacode, d, x0, boundarytype);
   }

   G4ThreeVector GetBoundaryAtPZ(G4int areacode, const G4ThreeVector &p) const override
   {
      PYBIND11_OVERRIDE(G4ThreeVector, G4TwistBoxSide, GetBoundaryAtPZ, areacode, p);
   }

   void SetBoundary(const G4int &axiscode, const G4ThreeVector &direction, const G4ThreeVector &x0,
                    const G4int &boundarytype) override
   {
      PYBIND11_OVERRIDE(void, G4TwistBoxSide, SetBoundary, axiscode, direction, x0, boundarytype);
   }
};

void export_G4TwistBoxSide(py::module &m)
{
   py::class_<G4TwistBoxSide, PyG4TwistBoxSide, G4VTwistSurface>(m, "G4TwistBoxSide")

      .def(py::init<const G4String &, G4double, G4double, G4double, G4double, G4double, G4double, G4double, G4double,
                    G4double, G4double, G4double, G4double>(),
           py::arg("name"), py::arg("PhiTwist"), py::arg("pDz"), py::arg("pTheta"), py::arg("pPhi"), py::arg("pDy1"),
           py::arg("pDx1"), py::arg("pDx2"), py::arg("pDy2"), py::arg("pDx3"), py::arg("pDx4"), py::arg("pAlph"),
           py::arg("AngleSide"))

      .def("__copy__", [](const PyG4TwistBoxSide &self) { return PyG4TwistBoxSide(self); })
      .def("__deepcopy__", [](const PyG4TwistBoxSide &self, py::dict) { return PyG4TwistBoxSide(self); })
      .def("GetNormal", &G4TwistBoxSide::GetNormal, py::arg("xx"), py::arg("isGlobal") = false)
      .def("DistanceToSurface",
           py::overload_cast<const G4ThreeVector &, const G4ThreeVector &, G4ThreeVector *, G4double *, G4int *,
                             G4bool *, G4VTwistSurface::EValidate>(&G4TwistBoxSide::DistanceToSurface),
           py::arg("gp"), py::arg("gv"), py::arg("gxx"), py::arg("distance"), py::arg("areacode"), py::arg("isvalid"),
           py::arg("validate") = G4VTwistSurface::kValidateWithTol)

      .def("DistanceToSurface",
           py::overload_cast<const G4ThreeVector &, G4ThreeVector *, G4double *, G4int *>(
              &G4TwistBoxSide::DistanceToSurface),
           py::arg("gp"), py::arg("gxx"), py::arg("distance"), py::arg("areacode"));
}
