#ifndef PLOT_WATERFALL_H
#define PLOT_WATERFALL_H

#include <qglobal.h>
#include <waterfallGlobalData.h>
#include <qwt_plot_rasteritem.h>

#if QWT_VERSION >= 0x060000
#include <qwt_point_3d.h>  // doesn't seem necessary, but is...
#include <qwt_compat.h>
#endif

class QwtColorMap;

/*!
  \brief A plot item, which displays a waterfall spectrogram

  A waterfall displays threedimenional data, where the 3rd dimension
  ( the intensity ) is displayed using colors. The colors are calculated
  from the values using a color map.
  
  \sa QwtRasterData, QwtColorMap
*/

class PlotWaterfall: public QwtPlotRasterItem
{
public:
    explicit PlotWaterfall(WaterfallData* data,
			   const QString &title = QString::null);
    virtual ~PlotWaterfall();

    const WaterfallData* data()const;

    void setColorMap(const QwtColorMap &);
    const QwtColorMap &colorMap() const;

#if QWT_VERSION < 0x060000
    virtual QwtDoubleRect boundingRect() const;
#endif
    //virtual QSize rasterHint(const QwtDoubleRect &) const;

    virtual int rtti() const;

    virtual void draw(QPainter *p,
		      const QwtScaleMap &xMap,
		      const QwtScaleMap &yMap,
		      const QRectF &rect) const;

protected:
    QImage renderImage(const QwtScaleMap &xMap,
		       const QwtScaleMap &yMap, 
		       const QRectF &rect,
		       const QSize &size=QSize(0,0)) const;

private:
    class PrivateData;
    PrivateData *d_data;
};

#endif
