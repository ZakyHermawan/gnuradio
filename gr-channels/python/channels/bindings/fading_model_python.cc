/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/* This file is automatically generated using bindtool */

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/channels/fading_model.h>
// pydoc.h is automatically generated in the build directory
#include <fading_model_pydoc.h>

void bind_fading_model(py::module& m)
{

    using fading_model = ::gr::channels::fading_model;


    py::class_<fading_model,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<fading_model>>(m, "fading_model", D(fading_model))

        .def(py::init(&fading_model::make),
             py::arg("N"),
             py::arg("fDTs") = 0.00999999977F,
             py::arg("LOS") = true,
             py::arg("K") = 4,
             py::arg("seed") = 0,
             D(fading_model, make))


        .def("fDTs", &fading_model::fDTs, D(fading_model, fDTs))


        .def("K", &fading_model::K, D(fading_model, K))


        .def("step", &fading_model::step, D(fading_model, step))


        .def("set_fDTs",
             &fading_model::set_fDTs,
             py::arg("fDTs"),
             D(fading_model, set_fDTs))


        .def("set_K", &fading_model::set_K, py::arg("K"), D(fading_model, set_K))


        .def("set_step",
             &fading_model::set_step,
             py::arg("step"),
             D(fading_model, set_step))

        ;
}
