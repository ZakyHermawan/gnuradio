/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(simple_squelch_cc.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(783bde73814b6714237f8eeda6f0e6d8)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/analog/simple_squelch_cc.h>
// pydoc.h is automatically generated in the build directory
#include <simple_squelch_cc_pydoc.h>

void bind_simple_squelch_cc(py::module& m)
{

    using simple_squelch_cc = ::gr::analog::simple_squelch_cc;


    py::class_<simple_squelch_cc,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<simple_squelch_cc>>(
        m, "simple_squelch_cc", D(simple_squelch_cc))

        .def(py::init(&simple_squelch_cc::make),
             py::arg("threshold_db"),
             py::arg("alpha"),
             D(simple_squelch_cc, make))


        .def("unmuted", &simple_squelch_cc::unmuted, D(simple_squelch_cc, unmuted))


        .def("set_alpha",
             &simple_squelch_cc::set_alpha,
             py::arg("alpha"),
             D(simple_squelch_cc, set_alpha))


        .def("set_threshold",
             &simple_squelch_cc::set_threshold,
             py::arg("decibels"),
             D(simple_squelch_cc, set_threshold))


        .def("threshold", &simple_squelch_cc::threshold, D(simple_squelch_cc, threshold))


        .def("squelch_range",
             &simple_squelch_cc::squelch_range,
             D(simple_squelch_cc, squelch_range))

        ;
}
