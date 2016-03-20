
#include "util.h"

int ptX(qreal points)
{
    return (int) (dpiX()/POINTS_PER_INCH * points);
}

int ptY(qreal points)
{
    return (int) (dpiY()/POINTS_PER_INCH * points);
}

int dpiX()
{
    return QApplication::screens().at(0)->logicalDotsPerInchX();
}

int dpiY()
{
    return QApplication::screens().at(0)->logicalDotsPerInchY();
}

int dpi()
{
    return QApplication::screens().at(0)->logicalDotsPerInch();
}
