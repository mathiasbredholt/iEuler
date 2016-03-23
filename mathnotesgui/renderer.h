#ifndef RENDERER_H
#define RENDERER_H

#include <QApplication>
#include <QDesktopWidget>

#include <QWidget>
#include <QtWebEngineWidgets>
#include <QWebEngineView>
#include <QWebChannel>

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
    int windowWidth;

public slots:
    void toggleRendering(bool disable);
    void onRenderComplete(int outputWidth, int outputHeight);


private:
    qreal baseScaling;
    bool isRendering;
    bool canRender;
    int getScreenDPI();
    void startRendering();
    QSize getSize();
    QQueue<MathWidget*> queue;
    QPixmap createPixmap(int width, int height);
    MathWidget *currentlyRendering;
    QWebChannel *channel;
};

#endif // RENDERER_H
