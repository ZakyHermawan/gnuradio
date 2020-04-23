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

#include <gnuradio/filter/mmse_interpolator_cc.h>
// pydoc.h is automatically generated in the build directory
#include <mmse_interpolator_cc_pydoc.h>

void bind_mmse_interpolator_cc(py::module& m)
{

    using mmse_interpolator_cc = ::gr::filter::mmse_interpolator_cc;


    py::class_<mmse_interpolator_cc,
               gr::block,
               gr::basic_block,
               std::shared_ptr<mmse_interpolator_cc>>(
        m, "mmse_interpolator_cc", D(mmse_interpolator_cc))

        .def(py::init(&mmse_interpolator_cc::make),
             py::arg("phase_shift"),
             py::arg("interp_ratio"),
             D(mmse_interpolator_cc, make))


        .def("mu", &mmse_interpolator_cc::mu, D(mmse_interpolator_cc, mu))


        .def("interp_ratio",
             &mmse_interpolator_cc::interp_ratio,
             D(mmse_interpolator_cc, interp_ratio))


        .def("set_mu",
             &mmse_interpolator_cc::set_mu,
             py::arg("mu"),
             D(mmse_interpolator_cc, set_mu))


        .def("set_interp_ratio",
             &mmse_interpolator_cc::set_interp_ratio,
             py::arg("interp_ratio"),
             D(mmse_interpolator_cc, set_interp_ratio))

        ;
}
