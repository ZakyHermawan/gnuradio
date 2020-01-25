/* -*- c++ -*- */
/*
 * Copyright 2008,2013 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <gnuradio/thread/thread_body_wrapper.h>

#ifdef HAVE_SIGNAL_H
#include <signal.h>
#endif

#include <stdio.h>

namespace gr {
namespace thread {

#if defined(HAVE_PTHREAD_SIGMASK) && defined(HAVE_SIGNAL_H) && !defined(__MINGW32__)

void mask_signals()
{
    sigset_t new_set;
    int r;

    sigemptyset(&new_set);
    sigaddset(&new_set, SIGHUP); // block these...
    sigaddset(&new_set, SIGINT);
    sigaddset(&new_set, SIGPIPE);
    sigaddset(&new_set, SIGALRM);
    sigaddset(&new_set, SIGTERM);
    sigaddset(&new_set, SIGUSR1);
    sigaddset(&new_set, SIGCHLD);
#ifdef SIGPOLL
    sigaddset(&new_set, SIGPOLL);
#endif
#ifdef SIGPROF
    sigaddset(&new_set, SIGPROF);
#endif
#ifdef SIGSYS
    sigaddset(&new_set, SIGSYS);
#endif
#ifdef SIGTRAP
    sigaddset(&new_set, SIGTRAP);
#endif
#ifdef SIGURG
    sigaddset(&new_set, SIGURG);
#endif
#ifdef SIGVTALRM
    sigaddset(&new_set, SIGVTALRM);
#endif
#ifdef SIGXCPU
    sigaddset(&new_set, SIGXCPU);
#endif
#ifdef SIGXFSZ
    sigaddset(&new_set, SIGXFSZ);
#endif
    r = pthread_sigmask(SIG_BLOCK, &new_set, 0);
    if (r != 0)
        perror("pthread_sigmask");
}

#else

void mask_signals() {}

#endif

} /* namespace thread */
} /* namespace gr */
