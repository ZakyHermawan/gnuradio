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

#include <gnuradio/blocks/exponentiate_const_cci.h>
// pydoc.h is automatically generated in the build directory
#include <exponentiate_const_cci_pydoc.h>

void bind_exponentiate_const_cci(py::module& m)
{

    using exponentiate_const_cci = ::gr::blocks::exponentiate_const_cci;


    py::class_<exponentiate_const_cci,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<exponentiate_const_cci>>(
        m, "exponentiate_const_cci", D(exponentiate_const_cci))

        .def(py::init(&exponentiate_const_cci::make),
             py::arg("exponent"),
             py::arg("vlen") = 1,
             D(exponentiate_const_cci, make))


        .def("set_exponent",
             &exponentiate_const_cci::set_exponent,
             py::arg("exponent"),
             D(exponentiate_const_cci, set_exponent))

        ;
}
