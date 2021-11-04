#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <G4ErrorSurfaceTarget.hh>
#include <G4Step.hh>

#include "typecast.hh"
#include "opaques.hh"

namespace py = pybind11;

class PyG4ErrorSurfaceTarget : public G4ErrorSurfaceTarget, public py::trampoline_self_life_support {
public:
   using G4ErrorSurfaceTarget::G4ErrorSurfaceTarget;

   G4Plane3D GetTangentPlane(const G4ThreeVector &point) const override
   {
      PYBIND11_OVERRIDE_PURE(G4Plane3D, G4ErrorSurfaceTarget, GetTangentPlane, point);
   }

   void Dump(const G4String &msg) const override { PYBIND11_OVERRIDE_PURE(void, G4ErrorSurfaceTarget, Dump, msg); }

   G4double GetDistanceFromPoint(const G4ThreeVector &arg0, const G4ThreeVector &arg1) const override
   {
      PYBIND11_OVERRIDE_PURE(G4double, G4ErrorSurfaceTarget, GetDistanceFromPoint, arg0, arg1);
   }

   G4double GetDistanceFromPoint(const G4ThreeVector &arg0) const override
   {
      PYBIND11_OVERRIDE_PURE(G4double, G4ErrorSurfaceTarget, GetDistanceFromPoint, arg0);
   }

   G4bool TargetReached(const G4Step *arg0) override
   {
      PYBIND11_OVERRIDE(G4bool, G4ErrorSurfaceTarget, TargetReached, arg0);
   }
};

void export_G4ErrorSurfaceTarget(py::module &m)
{
   py::class_<G4ErrorSurfaceTarget, PyG4ErrorSurfaceTarget, G4ErrorTanPlaneTarget>(m, "G4ErrorSurfaceTarget")

      .def(py::init<>())
      .def("__copy__", [](const PyG4ErrorSurfaceTarget &self) { return PyG4ErrorSurfaceTarget(self); })
      .def("__deepcopy__", [](const PyG4ErrorSurfaceTarget &self, py::dict) { return PyG4ErrorSurfaceTarget(self); })
      .def("GetDistanceFromPoint",
           py::overload_cast<const G4ThreeVector &, const G4ThreeVector &>(&G4ErrorSurfaceTarget::GetDistanceFromPoint,
                                                                           py::const_),
           py::arg("point"), py::arg("direc"))

      .def("GetDistanceFromPoint",
           py::overload_cast<const G4ThreeVector &>(&G4ErrorSurfaceTarget::GetDistanceFromPoint, py::const_),
           py::arg("point"))

      .def("GetTangentPlane", &G4ErrorSurfaceTarget::GetTangentPlane, py::arg("point"))
      .def("Dump", &G4ErrorSurfaceTarget::Dump, py::arg("msg"));
}
