#ifndef UTIL_H
#define UTIL_H

#include <QApplication>
#include <QScreen>
#include <QDebug>
#include <QDesktopWidget>

#define POINTS_PER_INCH 1.0/72.0

int ptX(qreal points);

int ptY(qreal points);

int dpiX();

int dpiY();

int dpi();

#endif // UTIL_H
