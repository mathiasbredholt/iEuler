#ifndef UTIL_H
#define UTIL_H

#include <QApplication>
#include <QScreen>
#include <QDebug>
#include <QDesktopWidget>
#include <QFile>

#define POINTS_PER_INCH 1.0/72.0

int ptX(qreal points);

int ptY(qreal points);

int dpiX();

int dpiY();

int dpi();

QString readFile(const QString& filename);

#endif // UTIL_H
