#ifndef RENDERER_H
#define RENDERER_H

#include <QApplication>
#include <QDesktopWidget>

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
    explicit Renderer(QObject *parent = 0);

    qreal zoomFactor;

    void setZoomFactor(int factor);
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
    QQueue<MathWidget*> queue;
    QPixmap createPixmap(QSize size);
    MathWidget *currentlyRendering;

signals:

};

#endif // RENDERER_H
