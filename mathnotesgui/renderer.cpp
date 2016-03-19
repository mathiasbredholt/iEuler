#include "renderer.h"

#define WEBKIT_DPI 114.0
#define DEFAULT_ZOOM_FACTOR 1

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

Renderer::Renderer(QWidget *parent) : QObject(parent)
{
    webkit = new QWebEngineView();
    webkit->setPalette(parent->palette());

    // Setup zoom levels
    baseScaling = getScreenDPI() / WEBKIT_DPI;
    webkit->setZoomFactor(DEFAULT_ZOOM_FACTOR*baseScaling);

    isRendering = false;
//    hasLoaded = false;
    canRender = true;

    // Callback for complete load of MathJax
    initMathJax();

}

void Renderer::startRendering()
{
    if (queue.empty()) {

        qFatal("Renderer called without rendering job.");

    } else {
        QString js;
        MathWidget *target = queue.dequeue();
        currentlyRendering = target;

        js = QString("getElementById('input').innerHTML = str").replace("str", target->latexString);
        webkit->page()->runJavaScript(js);

        isRendering = true;

    }
}

QPixmap Renderer::createPixmap()
{
    QWebEnginePage *page = webkit->page();
    QString widthCSS = QString("0px");
    QString heightCSS = QString("0px");

    page->runJavaScript("getComputedStyle(getElementById('input')).style.getPropertyValue('width')",
                       [](const QVariant &v) {
//        widthCSS = v.toString();
    });
    page->runJavaScript("getComputedStyle(getElementById('input')).style.getPropertyValue('height')",
                       [](const QVariant &v) {
//        heightCSS = v.toString();
    });

    int w = widthCSS.left(widthCSS.indexOf("px")).toInt() - 34;
    int h = heightCSS.left(heightCSS.indexOf("px")).toInt() + 4;
    QPixmap pixmap(QSize(w, h));
    webkit->render(&pixmap, QPoint(0, -18));
    return pixmap;
}

void Renderer::setZoomFactor(double factor)
{
    webkit->setZoomFactor(factor*baseScaling);
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

void Renderer::initMathJax()
{
    QString html = readFile(":/webkit/test");
    QUrl baseUrl = QUrl::fromLocalFile(QDir::currentPath() + "/mathnotesgui/webkit/");
//    webkit->page()->mainFrame()->addToJavaScriptWindowObject("Renderer", this);
//    webkit->setHtml(html, baseUrl);
}

void Renderer::onLoadComplete()
{
    canRender = true;
    if (!queue.empty()) startRendering();
}

void Renderer::onRenderComplete()
{
    if (queue.empty() || queue.head() != currentlyRendering) {

        // Convert the rendered output to bitmap and assign it to target
        currentlyRendering->setPixmap(createPixmap());

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
