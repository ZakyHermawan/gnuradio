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
/* BINDTOOL_HEADER_FILE(additive_scrambler_bb.h)                                   */
/* BINDTOOL_HEADER_FILE_HASH(526b44ff08fc8ae301bc1e7a3508c540)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/digital/additive_scrambler_bb.h>
// pydoc.h is automatically generated in the build directory
#include <additive_scrambler_bb_pydoc.h>

void bind_additive_scrambler_bb(py::module& m)
{

    using additive_scrambler_bb = ::gr::digital::additive_scrambler_bb;


    py::class_<additive_scrambler_bb,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<additive_scrambler_bb>>(
        m, "additive_scrambler_bb", D(additive_scrambler_bb))

        .def(py::init(&additive_scrambler_bb::make),
             py::arg("mask"),
             py::arg("seed"),
             py::arg("len"),
             py::arg("count") = 0,
             py::arg("bits_per_byte") = 1,
             py::arg("reset_tag_key") = "",
             D(additive_scrambler_bb, make))


        .def("mask", &additive_scrambler_bb::mask, D(additive_scrambler_bb, mask))


        .def("seed", &additive_scrambler_bb::seed, D(additive_scrambler_bb, seed))


        .def("len", &additive_scrambler_bb::len, D(additive_scrambler_bb, len))


        .def("count", &additive_scrambler_bb::count, D(additive_scrambler_bb, count))


        .def("bits_per_byte",
             &additive_scrambler_bb::bits_per_byte,
             D(additive_scrambler_bb, bits_per_byte))

        ;
}
