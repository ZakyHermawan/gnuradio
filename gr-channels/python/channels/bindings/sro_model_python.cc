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
/* BINDTOOL_HEADER_FILE(sro_model.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(b96a9b261c81e7c0ecc36ecbf7e54912)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/channels/sro_model.h>
// pydoc.h is automatically generated in the build directory
#include <sro_model_pydoc.h>

void bind_sro_model(py::module& m)
{

    using sro_model = ::gr::channels::sro_model;


    py::class_<sro_model, gr::block, gr::basic_block, std::shared_ptr<sro_model>>(
        m, "sro_model", D(sro_model))

        .def(py::init(&sro_model::make),
             py::arg("sample_rate_hz"),
             py::arg("std_dev_hz"),
             py::arg("max_dev_hz"),
             py::arg("noise_seed") = 0,
             D(sro_model, make))


        .def("set_std_dev",
             &sro_model::set_std_dev,
             py::arg("_dev"),
             D(sro_model, set_std_dev))


        .def("set_max_dev",
             &sro_model::set_max_dev,
             py::arg("_dev"),
             D(sro_model, set_max_dev))


        .def("set_samp_rate",
             &sro_model::set_samp_rate,
             py::arg("_rate"),
             D(sro_model, set_samp_rate))


        .def("std_dev", &sro_model::std_dev, D(sro_model, std_dev))


        .def("max_dev", &sro_model::max_dev, D(sro_model, max_dev))


        .def("samp_rate", &sro_model::samp_rate, D(sro_model, samp_rate))

        ;
}
