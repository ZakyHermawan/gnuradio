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
/* BINDTOOL_HEADER_FILE(mmse_fir_interpolator_ff.h) */
/* BINDTOOL_HEADER_FILE_HASH(a5230c4b6ad2c4241956c24184a499c5)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/filter/mmse_fir_interpolator_ff.h>
// pydoc.h is automatically generated in the build directory
#include <mmse_fir_interpolator_ff_pydoc.h>

void bind_mmse_fir_interpolator_ff(py::module& m)
{

    using mmse_fir_interpolator_ff = ::gr::filter::mmse_fir_interpolator_ff;


    py::class_<mmse_fir_interpolator_ff, std::shared_ptr<mmse_fir_interpolator_ff>>(
        m, "mmse_fir_interpolator_ff", D(mmse_fir_interpolator_ff))

        .def(py::init<>(), D(mmse_fir_interpolator_ff, mmse_fir_interpolator_ff, 0))


        .def(
            "ntaps", &mmse_fir_interpolator_ff::ntaps, D(mmse_fir_interpolator_ff, ntaps))


        .def("nsteps",
             &mmse_fir_interpolator_ff::nsteps,
             D(mmse_fir_interpolator_ff, nsteps))


        .def("interpolate",
             &mmse_fir_interpolator_ff::interpolate,
             py::arg("input"),
             py::arg("mu"),
             D(mmse_fir_interpolator_ff, interpolate))

        ;


    py::module m_kernel = m.def_submodule("kernel");
}
