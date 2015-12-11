#ifndef RENDERER_H
#define RENDERER_H

#include <QApplication>
#include <QDesktopWidget>

#include <QWidget>
#include <QWebView>
#include <QWebFrame>
#include <QWebElement>

#include <QQueue>
#include <QPixmap>
#include <QDir>

#include "mathwidget.h"

class Renderer : public QObject
{
    Q_OBJECT
public:
    explicit Renderer(QWidget *parent = 0);

    qreal zoomFactor;

    void setZoomFactor(double factor);
    void render(MathWidget *target);

public slots:
    void onLoadComplete();
    void onRenderComplete();
    void toggleRendering(bool disable);

private:
    QWebView *webkit;
    qreal baseScaling;
    bool isRendering;
    bool canRender;
    int getScreenDPI();
    void initMathJax();
    void startRendering();
    QSize getSize();
    QQueue<MathWidget*> queue;
    QPixmap createPixmap();
    MathWidget *currentlyRendering;

signals:

};

#endif // RENDERER_H
