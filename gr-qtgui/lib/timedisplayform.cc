/* -*- c++ -*- */
/*
 * Copyright 2011 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#include <cmath>
#include <QColorDialog>
#include <QMessageBox>
#include <timedisplayform.h>

TimeDisplayForm::TimeDisplayForm(QWidget* parent)
  : QWidget(parent)
{
  _systemSpecifiedFlag = false;
  _intValidator = new QIntValidator(this);
  _intValidator->setBottom(0);
  _timeDomainDisplayPlot = new TimeDomainDisplayPlot(this);

  _numRealDataPoints = 1024;
  
  Reset();

  // Create a timer to update plots at the specified rate
  displayTimer = new QTimer(this);
  connect(displayTimer, SIGNAL(timeout()), this, SLOT(UpdateGuiTimer()));

  connect(_timeDomainDisplayPlot, SIGNAL(plotPointSelected(const QPointF)),
	  this, SLOT(onTimePlotPointSelected(const QPointF)));
}

TimeDisplayForm::~TimeDisplayForm()
{
  // Qt deletes children when parent is deleted

  // Don't worry about deleting Display Plots - they are deleted when parents are deleted
  delete _intValidator;

  displayTimer->stop();
  delete displayTimer;
}

void
TimeDisplayForm::newData( const TimeUpdateEvent* spectrumUpdateEvent)
{
  const gr_complex* timeDomainDataPoints = spectrumUpdateEvent->getTimeDomainPoints();
  const uint64_t numTimeDomainDataPoints = spectrumUpdateEvent->getNumTimeDomainDataPoints();
  const timespec generatedTimestamp = spectrumUpdateEvent->getDataTimestamp();

  // FIXME: make time domain display take complex inputs
  double *real = new double[numTimeDomainDataPoints];
  double *imag = new double[numTimeDomainDataPoints];
  for(uint64_t i = 0; i < numTimeDomainDataPoints; i++) {
    real[i] = timeDomainDataPoints[i].real();
    imag[i] = timeDomainDataPoints[i].imag();
  }
  
  _timeDomainDisplayPlot->PlotNewData(real, imag,
				      numTimeDomainDataPoints,
				      d_update_time);

  // Tell the system the GUI has been updated
  //if(_systemSpecifiedFlag){
  //  _system->SetLastGUIUpdateTime(generatedTimestamp);
  //  _system->DecrementPendingGUIUpdateEvents();
  //}

  delete [] real;
  delete [] imag;
}

void
TimeDisplayForm::resizeEvent( QResizeEvent *e )
{
  QSize s(0,0);
  //s.setWidth(TimeDomainDisplayFrame->width());
  //s.setHeight(TimeDomainDisplayFrame->height());
  emit _timeDomainDisplayPlot->resizeSlot(&s);
}

void
TimeDisplayForm::customEvent( QEvent * e)
{
  if(e->type() == 10005) {
    TimeUpdateEvent* timeUpdateEvent = (TimeUpdateEvent*)e;
    newData(timeUpdateEvent);
  }
  //else if(e->type() == 10008){
  //setWindowTitle(((SpectrumWindowCaptionEvent*)e)->getLabel());
  //}
  //else if(e->type() == 10009){
  //Reset();
  //if(_systemSpecifiedFlag){
  //  _system->ResetPendingGUIUpdateEvents();
  //}
  //}
}

void
TimeDisplayForm::UpdateGuiTimer()
{
  _timeDomainDisplayPlot->canvas()->update();
}

void
TimeDisplayForm::onTimePlotPointSelected(const QPointF p)
{
  emit plotPointSelected(p, 3);
}

void
TimeDisplayForm::SetFrequencyRange(const double newCenterFrequency,
				   const double newStartFrequency, 
				   const double newStopFrequency)
{
  double fdiff = std::max(fabs(newStartFrequency), fabs(newStopFrequency));

  if(fdiff > 0) {
    std::string strtime[4] = {"sec", "ms", "us", "ns"};
    double units10 = floor(log10(fdiff));
    double units3  = std::max(floor(units10 / 3.0), 0.0);
    double units = pow(10, (units10-fmod(units10, 3.0)));
    int iunit = static_cast<int>(units3);
    
    _startFrequency = newStartFrequency;
    _stopFrequency = newStopFrequency;

    _timeDomainDisplayPlot->SetSampleRate(_stopFrequency - _startFrequency,
					  units, strtime[iunit]);
  }
}

void
TimeDisplayForm::Reset()
{
}


void
TimeDisplayForm::closeEvent( QCloseEvent *e )
{
  //if(_systemSpecifiedFlag){
  //  _system->SetWindowOpenFlag(false);
  //}

  qApp->processEvents();

  QWidget::closeEvent(e);
}

void
TimeDisplayForm::SetTimeDomainAxis(double min, double max)
{
  _timeDomainDisplayPlot->set_yaxis(min, max);
}

void
TimeDisplayForm::SetUpdateTime(double t)
{
  d_update_time = t;
  // QTimer class takes millisecond input
  displayTimer->start(d_update_time*1000);
}

