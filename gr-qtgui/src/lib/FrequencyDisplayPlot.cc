#ifndef FREQUENCY_DISPLAY_PLOT_C
#define FREQUENCY_DISPLAY_PLOT_C

#include <FrequencyDisplayPlot.h>

#include <qwt_scale_draw.h>

class FreqPrecisionClass
{
public:
  FreqPrecisionClass(const int freqPrecision)
  {
    _frequencyPrecision = freqPrecision;
  }

  virtual ~FreqPrecisionClass()
  {
  }

  virtual unsigned int GetFrequencyPrecision() const
  {
    return _frequencyPrecision;
  }

  virtual void SetFrequencyPrecision(const unsigned int newPrecision)
  {
    _frequencyPrecision = newPrecision;
  }
protected:
  unsigned int _frequencyPrecision;

private:

};

class FreqDisplayScaleDraw: public QwtScaleDraw, public FreqPrecisionClass
{
public:
  FreqDisplayScaleDraw(const unsigned int precision)
    : QwtScaleDraw(), FreqPrecisionClass(precision)
  {
  }

  virtual ~FreqDisplayScaleDraw() 
  {
  }

  virtual QwtText label(double value) const
  {
    return QString("%1").arg(value, 0, 'f', GetFrequencyPrecision());
  }

protected:

private:

};

class FreqDisplayZoomer: public QwtPlotZoomer, public FreqPrecisionClass
{
public:
  FreqDisplayZoomer(QwtPlotCanvas* canvas, const unsigned int freqPrecision)
    : QwtPlotZoomer(canvas),FreqPrecisionClass(freqPrecision)
  {
    setTrackerMode(QwtPicker::AlwaysOn);
  }

  virtual ~FreqDisplayZoomer(){

  }
  
  virtual void updateTrackerText(){
    updateDisplay();
  }

protected:
  virtual QwtText trackerText( const QwtDoublePoint& p ) const 
  {
    QwtText t(QString("%1 %2, %3 dB").arg(p.x(), 0, 'f', GetFrequencyPrecision()).arg( (GetFrequencyPrecision() == 0) ? "Hz" : "kHz").arg(p.y(), 0, 'f', 2));

    return t;
  }
};

FrequencyDisplayPlot::FrequencyDisplayPlot(QWidget* parent)
  : QwtPlot(parent)
{
  _startFrequency = 0;
  _stopFrequency = 4000;
  
  timespec_reset(&_lastReplot);

  resize(parent->width(), parent->height());

  _displayIntervalTime = (1.0/10.0); // 1/10 of a second between updates

  _useCenterFrequencyFlag = false;

  _numPoints = 1024;
  _dataPoints = new double[_numPoints];
  _minFFTPoints = new double[_numPoints];
  _maxFFTPoints = new double[_numPoints];
  _xAxisPoints = new double[_numPoints];

  // Disable polygon clipping
  QwtPainter::setDeviceClipping(false);
  
  // We don't need the cache here
  canvas()->setPaintAttribute(QwtPlotCanvas::PaintCached, false);
  canvas()->setPaintAttribute(QwtPlotCanvas::PaintPacked, false);
  
  QPalette palette;
  palette.setColor(canvas()->backgroundRole(), QColor("white"));
  canvas()->setPalette(palette);  

  setAxisScaleDraw(QwtPlot::xBottom, new FreqDisplayScaleDraw(0));
  setAxisScale(QwtPlot::xBottom, _startFrequency, _stopFrequency);
  setAxisTitle(QwtPlot::xBottom, "Frequency (Hz)");

  _minYAxis = -120;
  _maxYAxis = 10;
  setAxisScaleEngine(QwtPlot::yLeft, new QwtLinearScaleEngine);
  setAxisScale(QwtPlot::yLeft, _minYAxis, _maxYAxis);
  setAxisTitle(QwtPlot::yLeft, "Power (dB)");

  // Automatically deleted when parent is deleted
  _fft_plot_curve = new QwtPlotCurve("Power Spectrum");
  _fft_plot_curve->attach(this);
  _fft_plot_curve->setPen(QPen(Qt::blue));
  _fft_plot_curve->setRawData(_xAxisPoints, _dataPoints, _numPoints);

  _min_fft_plot_curve = new QwtPlotCurve("Minimum Power");
  _min_fft_plot_curve->attach(this);
  _min_fft_plot_curve->setPen(QPen(Qt::magenta));
  _min_fft_plot_curve->setRawData(_xAxisPoints, _minFFTPoints, _numPoints);
  _min_fft_plot_curve->setVisible(false);

  _max_fft_plot_curve = new QwtPlotCurve("Maximum Power");
  _max_fft_plot_curve->attach(this);
  _max_fft_plot_curve->setPen(QPen(Qt::darkYellow));
  _max_fft_plot_curve->setRawData(_xAxisPoints, _maxFFTPoints, _numPoints);
  _max_fft_plot_curve->setVisible(false);

  _lower_intensity_marker = new QwtPlotMarker();
  _lower_intensity_marker->setLineStyle(QwtPlotMarker::HLine);
  _lower_intensity_marker->setLinePen(QPen(Qt::cyan));
  _lower_intensity_marker->attach(this);

  _upper_intensity_marker = new QwtPlotMarker();
  _upper_intensity_marker->setLineStyle(QwtPlotMarker::HLine);
  _upper_intensity_marker->setLinePen(QPen(Qt::green));
  _upper_intensity_marker->attach(this);

  memset(_dataPoints, 0x0, _numPoints*sizeof(double));
  memset(_xAxisPoints, 0x0, _numPoints*sizeof(double));

  for(int64_t number = 0; number < _numPoints; number++){
    _minFFTPoints[number] = 200.0;
    _maxFFTPoints[number] = -280.0;
  }

  _resetXAxisPoints();


  // set up peak marker
  QwtSymbol symbol;

  _markerPeakAmplitude = new QwtPlotMarker();
  _markerPeakAmplitude->setLinePen(QPen(Qt::yellow));
  symbol.setStyle(QwtSymbol::Diamond);
  symbol.setSize(8);
  symbol.setPen(QPen(Qt::yellow));
  symbol.setBrush(QBrush(Qt::yellow));
  _markerPeakAmplitude->setSymbol(symbol);
  _markerPeakAmplitude->attach(this);

  _markerNoiseFloorAmplitude = new QwtPlotMarker();
  _markerNoiseFloorAmplitude->setLineStyle(QwtPlotMarker::HLine);
  _markerNoiseFloorAmplitude->setLinePen(QPen(Qt::darkRed, 0, Qt::DotLine));
  _markerNoiseFloorAmplitude->attach(this);

  _peakFrequency = 0;
  _peakAmplitude = -HUGE_VAL;

  _noiseFloorAmplitude = -HUGE_VAL;

  replot();

  _zoomer = new FreqDisplayZoomer(canvas(), 0);
#if QT_VERSION < 0x040000
  _zoomer->setMousePattern(QwtEventPattern::MouseSelect2,
			  Qt::RightButton, Qt::ControlModifier);
#else
  _zoomer->setMousePattern(QwtEventPattern::MouseSelect2,
			  Qt::RightButton, Qt::ControlModifier);
#endif
  _zoomer->setMousePattern(QwtEventPattern::MouseSelect3,
			  Qt::RightButton);

  _panner = new QwtPlotPanner(canvas());
  _panner->setAxisEnabled(QwtPlot::yRight, false);
  _panner->setMouseButton(Qt::MidButton);

  // Avoid jumping when labels with more/less digits
  // appear/disappear when scrolling vertically

  const QFontMetrics fm(axisWidget(QwtPlot::yLeft)->font());
  QwtScaleDraw *sd = axisScaleDraw(QwtPlot::yLeft);
  sd->setMinimumExtent( fm.width("100.00") );

  const QColor c(Qt::darkRed);
  _zoomer->setRubberBandPen(c);
  _zoomer->setTrackerPen(c);
}

FrequencyDisplayPlot::~FrequencyDisplayPlot()
{
  delete[] _dataPoints;
  delete[] _maxFFTPoints;
  delete[] _minFFTPoints;
  delete[] _xAxisPoints;

  // _fft_plot_curves deleted when parent deleted
  // _zoomer and _panner deleted when parent deleted
}

void
FrequencyDisplayPlot::set_yaxis(double min, double max)
{
  // Get the new max/min values for the plot
  _minYAxis = min;
  _maxYAxis = max;

  // Set the axis max/min to the new values
  setAxisScale(QwtPlot::yLeft, _minYAxis, _maxYAxis);

  // Reset the base zoom level to the new axis scale set here
  _zoomer->setZoomBase();
}

void
FrequencyDisplayPlot::SetFrequencyRange(const double constStartFreq,
					const double constStopFreq,
					const double constCenterFreq,
					const bool useCenterFrequencyFlag,
					const double units, const std::string &strunits)
{
  double startFreq = constStartFreq / units;
  double stopFreq = constStopFreq / units;
  double centerFreq = constCenterFreq / units;

  _useCenterFrequencyFlag = useCenterFrequencyFlag;

  if(_useCenterFrequencyFlag){
    startFreq = (startFreq + centerFreq);
    stopFreq = (stopFreq + centerFreq);
  }

  _startFrequency = startFreq;
  _stopFrequency = stopFreq;
  _resetXAxisPoints();

  setAxisScale(QwtPlot::xBottom, _startFrequency, _stopFrequency);
  setAxisScaleDraw(QwtPlot::xBottom, new FreqDisplayScaleDraw(2));
  setAxisTitle(QwtPlot::xBottom, QString("Frequency (%1)").arg(strunits.c_str()));
  ((FreqDisplayZoomer*)_zoomer)->SetFrequencyPrecision(2);

  // Load up the new base zoom settings
  _zoomer->setZoomBase();
  
  // Zooms back to the base and clears any other zoom levels
  _zoomer->zoom(0);
}


double
FrequencyDisplayPlot::GetStartFrequency() const
{
  return _startFrequency;
}

double
FrequencyDisplayPlot::GetStopFrequency() const
{
  return _stopFrequency;
}

void
FrequencyDisplayPlot::replot()
{
  const timespec startTime = get_highres_clock();

  _markerNoiseFloorAmplitude->setYValue(_noiseFloorAmplitude);
  
  // Make sure to take into account the start frequency
  if(_useCenterFrequencyFlag){
    _markerPeakAmplitude->setXValue((_peakFrequency/1000.0) + _startFrequency);
  }
  else{
    _markerPeakAmplitude->setXValue(_peakFrequency + _startFrequency);
  }
  _markerPeakAmplitude->setYValue(_peakAmplitude);
  
  QwtPlot::replot();

  double differenceTime = (diff_timespec(get_highres_clock(), startTime));

  differenceTime *= 99.0;
  // Require at least a 10% duty cycle
  if(differenceTime > (1.0/10.0)){
    _displayIntervalTime = differenceTime;
  }
}

void
FrequencyDisplayPlot::PlotNewData(const double* dataPoints, const int64_t numDataPoints,
				  const double noiseFloorAmplitude, const double peakFrequency,
				  const double peakAmplitude)
{
  if(numDataPoints > 0){

    if(numDataPoints != _numPoints){
      _numPoints = numDataPoints;

      delete[] _dataPoints;
      delete[] _minFFTPoints;
      delete[] _maxFFTPoints;
      delete[] _xAxisPoints;
      _dataPoints = new double[_numPoints];
      _xAxisPoints = new double[_numPoints];
      _minFFTPoints = new double[_numPoints];
      _maxFFTPoints = new double[_numPoints];
      
      _fft_plot_curve->setRawData(_xAxisPoints, _dataPoints, _numPoints);
      _min_fft_plot_curve->setRawData(_xAxisPoints, _minFFTPoints, _numPoints);
      _max_fft_plot_curve->setRawData(_xAxisPoints, _maxFFTPoints, _numPoints);

      _resetXAxisPoints();
      ClearMaxData();
      ClearMinData();
    }
    memcpy(_dataPoints, dataPoints, numDataPoints*sizeof(double));
    for(int64_t point = 0; point < numDataPoints; point++){
      if(dataPoints[point] < _minFFTPoints[point]){
	_minFFTPoints[point] = dataPoints[point];
      }
      if(dataPoints[point] > _maxFFTPoints[point]){
	_maxFFTPoints[point] = dataPoints[point];
      }
    }

    _noiseFloorAmplitude = noiseFloorAmplitude;
    _peakFrequency = peakFrequency;
    _peakAmplitude = peakAmplitude;

  }

  // Allow at least a 50% duty cycle
  if(diff_timespec(get_highres_clock(), _lastReplot) > _displayIntervalTime){
    // Only replot the screen if it is visible
    if(isVisible()){
      replot();
    }
    _lastReplot = get_highres_clock();
  }
}

void
FrequencyDisplayPlot::ClearMaxData()
{
  for(int64_t number = 0; number < _numPoints; number++){
    _maxFFTPoints[number] = _maxYAxis;
  }
}

void
FrequencyDisplayPlot::ClearMinData()
{
  for(int64_t number = 0; number < _numPoints; number++){
    _minFFTPoints[number] = _minYAxis;
  }
}

void
FrequencyDisplayPlot::SetMaxFFTVisible(const bool visibleFlag)
{
  _max_fft_plot_curve->setVisible(visibleFlag);
}

void
FrequencyDisplayPlot::SetMinFFTVisible(const bool visibleFlag)
{
  _min_fft_plot_curve->setVisible(visibleFlag);
}

void
FrequencyDisplayPlot::_resetXAxisPoints()
{
  double fft_bin_size = (_stopFrequency-_startFrequency) / static_cast<double>(_numPoints);
  double freqValue = _startFrequency;
  for(int64_t loc = 0; loc < _numPoints; loc++){
    _xAxisPoints[loc] = freqValue;
    freqValue += fft_bin_size;
  }
}

void
FrequencyDisplayPlot::SetLowerIntensityLevel(const double lowerIntensityLevel)
{
  _lower_intensity_marker->setYValue( lowerIntensityLevel );
}

void
FrequencyDisplayPlot::SetUpperIntensityLevel(const double upperIntensityLevel)
{
  _upper_intensity_marker->setYValue( upperIntensityLevel );
}


#endif /* FREQUENCY_DISPLAY_PLOT_C */
