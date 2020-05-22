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
/* BINDTOOL_HEADER_FILE(agc3_cc.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(a3249a33ccef3b89642aa41df853772e)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/analog/agc3_cc.h>
// pydoc.h is automatically generated in the build directory
#include <agc3_cc_pydoc.h>

void bind_agc3_cc(py::module& m)
{

    using agc3_cc = ::gr::analog::agc3_cc;


    py::class_<agc3_cc,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<agc3_cc>>(m, "agc3_cc", D(agc3_cc))

        .def(py::init(&agc3_cc::make),
             py::arg("attack_rate") = 0.10000000000000001,
             py::arg("decay_rate") = 0.01,
             py::arg("reference") = 1.,
             py::arg("gain") = 1.,
             py::arg("iir_update_decim") = 1,
             D(agc3_cc, make))


        .def("attack_rate", &agc3_cc::attack_rate, D(agc3_cc, attack_rate))


        .def("decay_rate", &agc3_cc::decay_rate, D(agc3_cc, decay_rate))


        .def("reference", &agc3_cc::reference, D(agc3_cc, reference))


        .def("gain", &agc3_cc::gain, D(agc3_cc, gain))


        .def("max_gain", &agc3_cc::max_gain, D(agc3_cc, max_gain))


        .def("set_attack_rate",
             &agc3_cc::set_attack_rate,
             py::arg("rate"),
             D(agc3_cc, set_attack_rate))


        .def("set_decay_rate",
             &agc3_cc::set_decay_rate,
             py::arg("rate"),
             D(agc3_cc, set_decay_rate))


        .def("set_reference",
             &agc3_cc::set_reference,
             py::arg("reference"),
             D(agc3_cc, set_reference))


        .def("set_gain", &agc3_cc::set_gain, py::arg("gain"), D(agc3_cc, set_gain))


        .def("set_max_gain",
             &agc3_cc::set_max_gain,
             py::arg("max_gain"),
             D(agc3_cc, set_max_gain))

        ;
}
