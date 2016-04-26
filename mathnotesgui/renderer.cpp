#include "renderer.h"

#define webengine_DPI 96.0
#define DEFAULT_ZOOM_FACTOR 1

Renderer::Renderer(int windowWidth, int windowHeight, QWidget *parent) : QObject(parent)
{
    this->windowWidth = windowWidth;
    QString html = readFile(":/katex.html");

    QUrl baseUrl = QUrl::fromLocalFile(QDir::currentPath() + "/mathnotesgui/webkit/");
    webengine = new QWebEngineView();
    webengine->setWindowFlags(Qt::FramelessWindowHint | Qt::SubWindow);
    webengine->setFixedSize(windowWidth * 0.9, windowHeight * 0.5);
    webengine->show();

    connect(webengine, SIGNAL(loadFinished(bool)), this, SLOT(loadFinished(bool)));

    channel = new QWebChannel(webengine->page());
    channel->registerObject(QStringLiteral("jshelper"), this);
    webengine->page()->setWebChannel(channel);

    webengine->setHtml(html, baseUrl);

    isRendering = false;
    canRender = true;
    hasRenderedOnce = false;
}

void Renderer::close()
{
    // close
    webengine->close();
}

void Renderer::move(const QPoint p)
{
    webengine->move(p.x() + 10, p.y());
}

void Renderer::startRendering()
{
    if (queue.empty()) {

        qFatal("Renderer called without rendering job.");

    } else {
        QString js;
        MathWidget *target = queue.dequeue();
        currentlyRendering = target;

        webengine->page()->runJavaScript("try { doRender(String.raw`" + target->latexString + "`); } catch(err) { console.log(err) }");
        isRendering = true;
    }
}

QPixmap Renderer::createPixmap(int width, int height)
{
    QPixmap pixmap(QSize(width, height * 1.75));
    webengine->render(&pixmap, QPoint(0, 0));
    return pixmap;
}

void Renderer::setZoomFactor(int factor)
{
//    webengine->page()->runJavaScript("MathJax.Hub.Config({'SVG': { scale: " + factor + " } });");
    QString fontSize = QString::number((factor * 13) * dpi() / webengine_DPI / 100);
    webengine->page()->runJavaScript("try { changeFontSize('" + fontSize + "pt'); } catch(err) { console.log(err) }");
}

void Renderer::render(MathWidget *target)
{
    if (queue.empty() || queue.head() != target) queue.enqueue(target);
    if (!isRendering && !queue.empty()) startRendering();

//    if (!isRendering && canRender && !queue.empty()) startRendering();
//    webengine->page()->runJavaScript("doRender(String.raw`"+target->latexString+"`);");
    //    currentlyRendering = target;
}

void Renderer::restart()
{
    //webengine->reload();
}

int Renderer::getScreenDPI()
{
    return QApplication::desktop()->screen()->physicalDpiX();
}

void Renderer::onRenderComplete(int outputWidth, int outputHeight)
{
    if (!hasRenderedOnce) {
        webengine->page()->runJavaScript("try { doRender(String.raw`" + currentlyRendering->latexString + "\\;`); } catch(err) { console.log(err) }");
        hasRenderedOnce = true;
    } else {
        hasRenderedOnce = false;
    }

    if (queue.empty() || queue.head() != currentlyRendering) {
        // Convert the rendered output to bitmap and assign it to target
        currentlyRendering->setPixmap(createPixmap(windowWidth * 0.9, outputHeight));
        isRendering = false;
    }

//    if (!queue.empty() && canRender) {
    if (!queue.empty()) {
        startRendering();
    }
}

void Renderer::loadFinished(bool)
{
    setZoomFactor(100);
}

void Renderer::toggleRendering(bool disable)
{
    canRender = !disable;
    if (canRender && !queue.empty()) {
        startRendering();
    }
}
