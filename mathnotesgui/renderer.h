#ifndef RENDERER_H
#define RENDERER_H

#include <QApplication>
#include <QDesktopWidget>

#include <QWidget>
#include <QtWebEngineWidgets>
#include <QWebEngineView>

#include <QQueue>
#include <QPixmap>
#include <QDir>
#include <QDebug>

#include "mathwidget.h"
#include "util.h"

class Renderer : public QObject
{
    Q_OBJECT
public:
    explicit Renderer(QWidget *parent = 0);
    QWebEngineView *webengine;

    qreal zoomFactor;

    void setZoomFactor(int factor);
    void render(MathWidget *target);

public slots:
    void onLoadComplete();
    void onRenderComplete();
    void toggleRendering(bool disable);

private:
    qreal baseScaling;
    bool isRendering;
    bool canRender;
    int getScreenDPI();
    void startRendering();
    QSize getSize();
    QQueue<MathWidget*> queue;
    QPixmap createPixmap();
    MathWidget *currentlyRendering;

signals:

};

#endif // RENDERER_H
