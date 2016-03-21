#include "renderer.h"

#define webengine_DPI 96.0
#define DEFAULT_ZOOM_FACTOR 1

Renderer::Renderer(QWidget *parent) : QObject(parent)
{
    QString html = readFile(":/katex.html");
//    QString html = readFile(":/mathjax.html");

    QUrl baseUrl = QUrl::fromLocalFile(QDir::currentPath() + "/mathnotesgui/webkit/");
    webengine = new QWebEngineView();
    webengine->show();

    channel = new QWebChannel(webengine->page());
    channel->registerObject(QStringLiteral("jshelper"), this);
    webengine->page()->setWebChannel(channel);

    webengine->setHtml(html, baseUrl);

    // Setup zoom levels
//    setZoomFactor((int) dpi() / webengine_DPI * 100);
    isRendering = false;
//    hasLoaded = false;
    canRender = true;

}

void Renderer::startRendering()
{
    if (queue.empty()) {

        qFatal("Renderer called without rendering job.");

    } else {
        QString js;
        MathWidget *target = queue.dequeue();
        currentlyRendering = target;

        webengine->page()->runJavaScript("doRender(String.raw`"+target->latexString+"`);");
        isRendering = true;
    }
}

QPixmap Renderer::createPixmap(int width, int height)
{
    QPixmap pixmap(QSize(width, height*1.75));
    webengine->render(&pixmap, QPoint(0, 0));
    return pixmap;
}

void Renderer::setZoomFactor(int factor)
{
//    webengine->page()->runJavaScript("MathJax.Hub.Config({'SVG': { scale: " + factor + " } });");
}

void Renderer::render(MathWidget *target)
{
    if (queue.empty() || queue.head() != target) queue.enqueue(target);
    if (!isRendering && canRender && !queue.empty()) startRendering();
}

int Renderer::getScreenDPI()
{
    return QApplication::desktop()->screen()->physicalDpiX();
}

void Renderer::onRenderComplete(int outputWidth, int outputHeight)
{
    if (queue.empty() || queue.head() != currentlyRendering) {
        // Convert the rendered output to bitmap and assign it to target
        currentlyRendering->setPixmap(createPixmap(webengine->width(), outputHeight));
        isRendering = false;
    }

    if (!queue.empty() && canRender){
        startRendering();
    }

}

void Renderer::toggleRendering(bool disable)
{
    canRender = !disable;
    if (canRender && !queue.empty()){
        startRendering();
    }
}
