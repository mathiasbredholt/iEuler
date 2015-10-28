#include "mathrenderer.h"
#include <QFile>
#include <QDir>
#include <QWebFrame>
#include <QWebElement>
#include <QEvent>
#include <QNativeGestureEvent>
#include <QApplication>
#include <QDesktopWidget>

qreal MathRenderer::zoomFactor = 1;
qreal MathRenderer::baseScaling;
QWebView *MathRenderer::renderer;
bool MathRenderer::isReady = false;
bool MathRenderer::isRendering = false;
QQueue<MathRenderer*> MathRenderer::renderQueue;

QString readFile (const QString& filename)
{
    QFile file(filename);
    if (file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        QTextStream stream(&file);
        return stream.readAll();
    }
    return "";
}

MathRenderer::MathRenderer(QObject *parent) : QObject(parent)
{
    renderer->page()->mainFrame()->addToJavaScriptWindowObject("Renderer", this);
    label = new QLabel();
    label->setFixedHeight(96);
}

// Static

void MathRenderer::initRenderer()
{
    // Detect dpi
    QWidget* window = QApplication::desktop()->screen();
    const int horizontalDpi = window->logicalDpiX();
    baseScaling = horizontalDpi / 96.0;

    renderer = new QWebView();
    renderer->setZoomFactor(zoomFactor*baseScaling);

    QString html = readFile(":/webkit/test");
    QUrl baseUrl = QUrl::fromLocalFile(QDir::currentPath() + "/mathnotesgui/webkit/");
    renderer->setHtml(html, baseUrl);
}

void MathRenderer::render()
{
    isRendering = true;
    QWebFrame *frame = renderer->page()->mainFrame();
    MathRenderer *target = renderQueue.dequeue();
    renderer->page()->mainFrame()->addToJavaScriptWindowObject("Target", target);
    renderer->setZoomFactor(zoomFactor*baseScaling);
    frame->findFirstElement("#input").setInnerXml(target->latexString);
    frame->evaluateJavaScript("UpdateMath()");
}

// non-static

void MathRenderer::hasLoaded()
{
    isReady = true;
    if (!renderQueue.empty()) {
        render();
    }
}

void MathRenderer::hasRendered()
{

    if (!renderQueue.empty()) {
        render();
    } else {
        isRendering = false;

        QPixmap pixmap(label->size());
        renderer->render(&pixmap);
        label->setPixmap(pixmap);
        pixmap.save("output.png");
    }
}

void MathRenderer::toggleRendering(bool disable)
{
    isReady = !disable;
    if (!disable && !renderQueue.empty()){
        MathRenderer::render();
    }
}
